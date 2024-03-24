import shlex
import json
from pathlib import Path
from typing import Any, Dict, Iterable
import logging
try:
    import torch as _
except ImportError:
    pass
import os
import configargparse
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

import tensorflow as tf
import numpy as np
import imageio
import run_nerf
from run_nerf import get_rays, render, get_rays_np
from load_llff import load_llff_data, spherify_poses, poses_avg
from load_deepvoxels import load_dv_data
from load_blender import load_blender_data
from train import config_parser, create_nerf, img2mse, mse2psnr
from argparse import ArgumentParser

from nerfbaselines.types import Dataset, CurrentProgress, RenderOutput, MethodInfo, ModelInfo, ProgressCallback
from nerfbaselines import Cameras, CameraModel
from nerfbaselines import Method
from nerfbaselines.types import Optional
from nerfbaselines.utils import padded_stack, convert_image_dtype
from nerfbaselines.pose_utils import pad_poses, apply_transform, unpad_poses, invert_transform


tf.compat.v1.enable_eager_execution()


def load_dataset(args, dataset: Dataset, transform_args=None):
    poses = dataset.cameras.poses.copy()
    imgs = np.stack(dataset.images, 0)
    imgs = convert_image_dtype(imgs, np.float32)

    # Convert from OpenCV to OpenGL coordinate system
    poses[..., 1:3] *= -1
    poses = poses.astype(np.float32)
    if args.dataset_type == "blender":
        W, H = dataset.cameras.image_sizes[0]
        focal = dataset.cameras.intrinsics[0, 0]
        assert (
            np.all(dataset.cameras.image_sizes[..., 0] == W) and
            np.all(dataset.cameras.image_sizes[..., 1] == H) and
            np.all(dataset.cameras.intrinsics[..., 0] == focal) and
            np.all(dataset.cameras.intrinsics[..., 1] == focal)
        ), "All images must have the same width, height, and focal lenghts"
        cx, cy = W / 2, H / 2
        assert (
            np.all(dataset.cameras.intrinsics[..., 2] == cx) and
            np.all(dataset.cameras.intrinsics[..., 3] == cy)
        ), "All images must have the same principal point in the center of the image"

        near = 2.
        far = 6.

        if args.white_bkgd:
            imgs = imgs[..., :3]*imgs[..., -1:] + (1.-imgs[..., -1:])
        else:
            imgs = imgs[..., :3]
        transform_args = {
            "transform": np.eye(4, dtype=np.float32),
            "hwfnearfar": (H, W, focal, near, far)
        }
        return imgs, poses[:, :3, :4], transform_args

    # Load data
    elif args.dataset_type == 'llff':
        if transform_args is None:
            recenter=True
            spherify=args.spherify

            bds = dataset.cameras.nears_fars
            print('Loaded', bds.min(), bds.max())
            
            # Rescale if bd_factor is provided
            near_original = dataset.cameras.nears_fars.min()
            bd_factor=.75  # 0.75 is the default parameter
            sc = 1 / (near_original * bd_factor)
            poses[:,:3,3] *= sc
            bds *= sc

            transform = np.eye(4, dtype=np.float32)
            
            if recenter:
                transform = np.linalg.inv(pad_poses(poses_avg(poses)))
                poses = apply_transform(transform, poses)
                
            if spherify:
                poses, render_poses, bds = spherify_poses(poses, bds)
            else:
                # Find a reasonable "focus depth" for this dataset
                close_depth, inf_depth = bds.min()*.9, bds.max()*5.
                dt = .75
                mean_dz = 1./(((1.-dt)/close_depth + dt/inf_depth))
                focal = mean_dz

            if args.no_ndc:
                near = np.min(bds) * .9
                far = np.max(bds) * 1.
            else:
                near = 0.
                far = 1.
        else:
            transform = transform_args["transform"]
            H, W, focal, near, far, sc = transform_args["hwfnearfarscale"]
            poses[:,:3,3] *= sc
            poses = apply_transform(transform, poses)
            if spherify:
                poses, _, _ = spherify_poses(poses, 1)
        transform_args = {
            "transform": transform,
            "hwfnearfarscale": (H, W, focal, near, far, sc)
        }
        print('Data:')
        print(poses.shape, imgs.shape)
        print('Loaded llff', imgs.shape,
            render_poses.shape, (H, W, focal))
        print('DEFINING BOUNDS')
        print('NEAR FAR', near, far)
        return imgs, poses[:, :3, :4], transform_args
    else:
        raise RuntimeError('Unsupported dataset type', args.dataset_type)


class NeRF(Method):
    _method_name: str = "nerf"

    def __init__(self, *,
                 checkpoint: Optional[Path] = None, 
                 train_dataset: Optional[Dataset] = None,
                 config_overrides: Optional[dict] = None):
        self.checkpoint = checkpoint
        self.args = None
        self.metadata = {}
        self._arg_list = ()
        if checkpoint is not None:
            with open(os.path.join(checkpoint, "metadata.json"), "r") as f:
                self.metadata = json.load(f)
                self.metadata["transform_args"]["transform"] = np.array(self.metadata["transform_args"]["transform"], dtype=np.float32)
            self._arg_list = shlex.split(self.metadata["args"])
        self.step = 0

        self._load_config()
        self._setup(train_dataset, config_overrides=config_overrides)

    def _load_config(self):
        parser: ArgumentParser = config_parser()
        self.args = parser.parse_args(self._arg_list)

    @classmethod
    def get_method_info(cls) -> MethodInfo:
        assert cls._method_name is not None, "Method was not properly registered"
        return MethodInfo(
            name=cls._method_name,
            required_features=frozenset(("color",)),
            supported_camera_models=frozenset(CameraModel.__members__.values()),
        )

    def get_info(self) -> ModelInfo:
        N_iters = 1000000
        return ModelInfo(
            name=self._method_name,
            num_iterations=N_iters,
            supported_camera_models=frozenset(CameraModel.__members__.values()),
            loaded_step=self.metadata.get("step"),
            batch_size=self.args.batch_size,
            eval_batch_size=self.args.batch_size,
            hparams=vars(self.args) if self.args else {},
        )

    def save(self, path: Path):
        with open(str(path) + "/args.txt", "w") as f:
            f.write(shlex.join(self._arg_list))
        # TODO: ...
        # self.tensorf.save(str(path / "tensorf.th"))
        self.metadata["args"] = shlex.join(self._arg_list)
        self.metadata["step"] = self.step
        metadata = self.metadata.copy()
        metadata["transform_args"]["transform"] = metadata["transform_args"]["transform"].tolist()
        with (path / "metadata.json").open("w") as f:
            json.dump(metadata, f)

    def _setup(self, train_dataset: Dataset, *, config_overrides: Optional[Dict[str, Any]] = None):
        if train_dataset is None:
            config_overrides = (config_overrides or {}).copy()

            self.metadata["dataset_metadata"] = {
                "type": train_dataset.metadata.get("type"),
                "name": train_dataset.metadata.get("name"),
            }

            # Load dataset-specific config
            dataset_name = train_dataset.metadata.get("name")
            # TODO: ...
            config_name = "your_own_data.txt"
            if dataset_name == "blender":
                config_name = "lego.txt"
            elif dataset_name == "llff":
                config_name = "flower.txt"
            config_file = Path(run_nerf.__file__).absolute().parent.joinpath("paper_configs", config_name)
            logging.info(f"Loading config from {config_file}")
            with config_file.open("r", encoding="utf8") as f:
                config_overrides.update(configargparse.DefaultConfigFileParser().parse(f))

            for k, v in config_overrides.items():
                if isinstance(v, list):
                    for vs in v:
                        self._arg_list += (f"--{k}", str(vs))
                elif isinstance(v, str) and v.startswith("[") and v.endswith("]"):
                    for vs in v[1:-1].split(","):
                        self._arg_list += (f"--{k}", str(vs))
                else:
                    self._arg_list += (f"--{k}", str(v))
            logging.info("Using arguments: " + shlex.join(self._arg_list))
        self._load_config()

        if self.args.random_seed is not None:
            print('Fixing random seed', self.args.random_seed)
            np.random.seed(self.args.random_seed)
            tf.compat.v1.set_random_seed(self.args.random_seed)

        # Load data
        images, poses, bds, render_poses, i_test, (H, W, focal, near, far) = load_dataset(self.args, train_dataset)

        # Cast intrinsics to right types
        H, W = int(H), int(W)
        self.focal = focal

        # Create nerf model
        render_kwargs_train, render_kwargs_test, start, grad_vars, models = create_nerf(
            self.args)

        bds_dict = {
            'near': tf.cast(near, tf.float32),
            'far': tf.cast(far, tf.float32),
        }
        render_kwargs_train.update(bds_dict)
        render_kwargs_test.update(bds_dict)
        self.render_kwargs_train = render_kwargs_train
        self.render_kwargs_test = render_kwargs_test

        # Short circuit if only rendering out from trained model
        if train_dataset is None:
            return

        # Create optimizer
        lrate = self.args.lrate
        if self.args.lrate_decay > 0:
            lrate = tf.keras.optimizers.schedules.ExponentialDecay(
                lrate,
                decay_steps=self.args.lrate_decay * 1000, 
                decay_rate=0.1)
        self.optimizer = tf.keras.optimizers.Adam(lrate)
        models['optimizer'] = self.optimizer

        global_step = tf.compat.v1.train.get_or_create_global_step()
        global_step.assign(start)

        # Prepare raybatch tensor if batching random rays
        use_batching = not self.args.no_batching
        self.images = images
        self.poses = poses
        self.rays_rgb = None
        self.i_batch = None
        if use_batching:
            # For random ray batching.
            #
            # Constructs an array 'rays_rgb' of shape [N*H*W, 3, 3] where axis=1 is
            # interpreted as,
            #   axis=0: ray origin in world space
            #   axis=1: ray direction in world space
            #   axis=2: observed RGB color of pixel
            logging.debug('get rays')
            # get_rays_np() returns rays_origin=[H, W, 3], rays_direction=[H, W, 3]
            # for each pixel in the image. This stack() adds a new dimension.
            rays = [get_rays_np(H, W, focal, p) for p in poses[:, :3, :4]]
            rays = np.stack(rays, axis=0)  # [N, ro+rd, H, W, 3]
            logging.debug('done, concats')
            # [N, ro+rd+rgb, H, W, 3]
            rays_rgb = np.concatenate([rays, images[:, None, ...]], 1)
            # [N, H, W, ro+rd+rgb, 3]
            rays_rgb = np.transpose(rays_rgb, [0, 2, 3, 1, 4])
            rays_rgb = np.stack(rays_rgb, axis=0)  # train images only
            # [(N-1)*H*W, ro+rd+rgb, 3]
            rays_rgb = np.reshape(rays_rgb, [-1, 3, 3])
            rays_rgb = rays_rgb.astype(np.float32)
            logging.debug('shuffle rays')
            np.random.shuffle(rays_rgb)
            logging.debug('done')

            self.i_batch = 0
            self.rays_rgb = rays_rgb
        logging.debug('Begin')


    def train_iteration(self, step: int):
        self.global_step.assign(step)
        # Sample random ray batch

        use_batching = not self.args.no_batching
        N_rand = self.args.N_rand
        if use_batching:
            # Random over all images
            batch = self.rays_rgb[self.i_batch:self.i_batch+N_rand]  # [B, 2+1, 3*?]
            batch = tf.transpose(batch, [1, 0, 2])

            # batch_rays[i, n, xyz] = ray origin or direction, example_id, 3D position
            # target_s[n, rgb] = example_id, observed color.
            batch_rays, target_s = batch[:2], batch[2]

            self.i_batch += N_rand
            if self.i_batch >= self.rays_rgb.shape[0]:
                np.random.shuffle(self.rays_rgb)
                self.i_batch = 0

        else:
            # Random from one image
            img_i = np.random.choice(list(range(len(self.poses))))
            target = self.images[img_i]
            H, W, _ = target.shape
            pose = self.poses[img_i, :3, :4]

            if N_rand is not None:
                rays_o, rays_d = get_rays(H, W, self.focal, pose)
                if step < self.args.precrop_iters:
                    dH = int(H//2 * self.args.precrop_frac)
                    dW = int(W//2 * self.args.precrop_frac)
                    coords = tf.stack(tf.meshgrid(
                        tf.range(H//2 - dH, H//2 + dH), 
                        tf.range(W//2 - dW, W//2 + dW), 
                        indexing='ij'), -1)
                    if step < 10:
                        print('precrop', dH, dW, coords[0,0], coords[-1,-1])
                else:
                    coords = tf.stack(tf.meshgrid(
                        tf.range(H), tf.range(W), indexing='ij'), -1)
                coords = tf.reshape(coords, [-1, 2])
                select_inds = np.random.choice(
                    coords.shape[0], size=[N_rand], replace=False)
                select_inds = tf.gather_nd(coords, select_inds[:, tf.newaxis])
                rays_o = tf.gather_nd(rays_o, select_inds)
                rays_d = tf.gather_nd(rays_d, select_inds)
                batch_rays = tf.stack([rays_o, rays_d], 0)
                target_s = tf.gather_nd(target, select_inds)

        #####  Core optimization loop  #####

        with tf.GradientTape() as tape:

            # Make predictions for color, disparity, accumulated opacity.
            rgb, disp, acc, extras = render(
                H, W, self.focal, chunk=self.args.chunk, rays=batch_rays,
                verbose=step < 10, retraw=True, **self.render_kwargs_train)

            # Compute MSE loss between predicted and true RGB.
            img_loss = img2mse(rgb, target_s)
            # trans = extras['raw'][..., -1]
            loss = img_loss
            psnr = mse2psnr(img_loss)

            # Add MSE loss for coarse-grained model
            if 'rgb0' in extras:
                img_loss0 = img2mse(extras['rgb0'], target_s)
                loss += img_loss0
                psnr0 = mse2psnr(img_loss0)

        gradients = tape.gradient(loss, self.grad_vars)
        self.optimizer.apply_gradients(zip(gradients, self.grad_vars))
        self.step = step + 1
        return {
            "loss": loss.numpy().item(),
            "psnr": psnr.numpy().item(),
            "mse": img_loss.numpy().item(),
            "psnr0": psnr0.numpy().item(),
            "mse0": img_loss0.numpy().item(),
        }

    def render(self, cameras: Cameras, progress_callback: Optional[ProgressCallback] = None) -> Iterable[RenderOutput]:
        assert self.metadata.get("dataset_metadata") is not None, "Missing dataset_metadata"
        assert self.metadata.get("dataset_transform") is not None, "Missing dataset_transform"
        poses, imgs = load_dataset(self.args,
            Dataset(
                cameras=cameras,
                file_paths=[f"{i:06d}.png" for i in range(len(cameras))],
                metadata=self.metadata["dataset_metadata"],
            ),
            transform_args=self.metadata["dataset_transform"]
        )
        idx = 0
        if progress_callback is not None:
            progress_callback(CurrentProgress(idx, len(test_dataset), idx, len(test_dataset)))
        for idx, samples in enumerate(test_dataset.all_rays):
            W, H = cameras.image_sizes[idx]
            rays = samples.view(-1, samples.shape[-1])

            rgb_map, _, depth_map, _, _ = self.renderer(rays, self.tensorf, chunk=4096, N_samples=-1, ndc_ray=self.args.ndc_ray, white_bg=self.white_bg, device=self.device)

            rgb_map = rgb_map.clamp(0.0, 1.0)
            rgb_map, depth_map = rgb_map.reshape(H, W, 3).cpu(), depth_map.reshape(H, W).cpu()
            if progress_callback is not None:
                progress_callback(CurrentProgress(idx + 1, len(test_dataset), idx + 1, len(test_dataset)))

            W, H = cameras.image_sizes[idx]
            focal, *_ = cameras.intrinsics[idx]
            pose = cameras.poses[idx, :3, :4]
            rgb, disp, acc, extras = render(
                H, W, focal, chunk=self.args.chunk, c2w=pose, **self.render_kwargs_test)

            # Save out the validation image for Tensorboard-free monitoring
            testimgdir = os.path.join(basedir, expname, 'tboard_val_imgs')
            if i==0:
                os.makedirs(testimgdir, exist_ok=True)
            imageio.imwrite(os.path.join(testimgdir, '{:06d}.png'.format(i)), to8b(rgb))

            with tf.contrib.summary.record_summaries_every_n_global_steps(args.i_img):

                tf.contrib.summary.image('rgb', to8b(rgb)[tf.newaxis])
                tf.contrib.summary.image(
                    'disp', disp[tf.newaxis, ..., tf.newaxis])
                tf.contrib.summary.image(
                    'acc', acc[tf.newaxis, ..., tf.newaxis])

                tf.contrib.summary.scalar('psnr_holdout', psnr)
                tf.contrib.summary.image('rgb_holdout', target[tf.newaxis])

            if args.N_importance > 0:

                with tf.contrib.summary.record_summaries_every_n_global_steps(args.i_img):
                    tf.contrib.summary.image(
                        'rgb0', to8b(extras['rgb0'])[tf.newaxis])
                    tf.contrib.summary.image(
                        'disp0', extras['disp0'][tf.newaxis, ..., tf.newaxis])
                    tf.contrib.summary.image(
                        'z_std', extras['z_std'][tf.newaxis, ..., tf.newaxis])










            yield {
                "color": rgb_map.detach().numpy(),
                "depth": depth_map.detach().numpy(),
            }
