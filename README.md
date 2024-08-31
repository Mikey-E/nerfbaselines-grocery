---- BEGIN fork preamble ----

This is a fork for benchmarking the grocery dataset.
The original readme text at the time of the fork is after the fork preamble.

Tables of models setup (reproducibility). Results are (theirs, ours). Some of our results are averaged from multiple runs.

Geo1

| model                   | conda setup? | docker setup? | dataset | PSNR | SSIM | LPIPS (VGG) | Notes |
|----------|----------|----------|----------|----------|----------|----------|----------|
| instant-ngp             |      ✅      |      ✅       | kitchen | 29.02, 29.03 | 0.844, 0.853 | 0.255, 0.234 | conda: numpy 1.25 |
| nerfstudio (nerfacto)   |      ❌      |      ✅       | bicycle | 23.58, 19.00 | 0.567, 0.550 | 0.456, 0.670 | conda: backend forces bad numpy, can't find how to make it stop |
| gaussian-opacity-fields |      ❌      |      ❌       | | | | | numpy error |
| gaussian-splatting      |      ❌      |      ❌       | | | | | numpy error |
| mip-splatting           |      ✅      |      ❌       | lego | 35.45, 35.46 | 0.982, 0.982 | 0.021, 0.021 | |
| mipnerf360              |      ❌      |      ❌       | | | | | numpy error |
| zipnerf                 |      ❌      |      ❌       | | | | | conda: ptxas error (11.8), docker: numpy error |
| nerf                    |      ❌      |      ❌       | | | | | numpy error |
| tetra-nerf              |      ❌      |      ✅       | lego | 33.93, 34.03 | 0.972, 0.972 | 0.036, 0.035 |  uses nerfstudio environment |
| kplanes                 |      ✅      |      ❌       | lego | 35.73, 35.63 | 0.981, 0.981 | 0.047, 0.048 | docker: numpy error |
| tensorf                 |      ✅      |      ❌       | lego | 36.49, 36.50 | 0.983, 0.983 | 0.022, 0.022 | docker: numpy error |
| nerfw                   |      ❌      |      ❌       | | | | | numpy error |

Medicine Bow

| model                   | conda setup? | docker setup? | dataset | PSNR | SSIM | LPIPS (VGG) | Notes |
|----------|----------|----------|----------|----------|----------|----------|----------|
| instant-ngp             |      ✅     |      ❌       | kitchen | 29.02, 29.15 | 0.844, 0.847 | 0.255, 0.253 | numpy version bypassed by activ and deactiv the ingp env |
| nerfstudio (nerfacto)   |      ✅     |      ❌       | lego | 31.37, 30.54 | 0.967, 0.963 | 0.069, 0.066 | |
| gaussian-opacity-fields |      ✅     |      ❌       | | | | | |
| gaussian-splatting      |      ✅     |      ❌       | | | | | |
| mip-splatting           |      ✅     |      ❌       | | | | | |
| mipnerf360              |      ❌     |      ❌       | | | | | XLA runtime error |
| zipnerf                 |      ❌     |      ❌       | | | | | XLA runtime error |
| nerf                    |      ?      |      ❌       | | | | | trains but will take 17 hours per run |
| tetra-nerf              |      ❌     |      ❌       | | | | | uses nerfstudio env which is gone now, no module named torch |
| kplanes                 |      ✅     |      ❌       | lego | 35.73, 35.64 | 0.981, 0.981 | 0.047, 0.051 | |
| tensorf                 |      ✅     |      ❌       | lego | 36.49, 36.52 | 0.983, 0.983 | 0.022, 0.022 | |
| nerfw                   |      ❌     |      ❌       | | | | | TypeError: __init__() got an unexpected keyword argument 'devices' |

Important:
- utils/convert.py requires colmap on the system. Our recommended way is to simply run:
`conda install -c conda-forge colmap` and consider that you may need a cuda toolkit first for this.
Highly consider making a separate conda environment to run convert.py. Before running convert.py,
the dataset about to be converted must have its images folder named as "input". utils contains a script for doing this
and it should be run first if the input image folder is not already named as such.
Not all the new images may write to the created image folder.
In our case we (afterward) have renamed input to images so they are all there and are all the original size.

Recommended:
- Create a soft-link called "datasets", at the highest directory level,
to point to wherever you will keep the nerfbaselines datasets.
- Create a results directory for keeping info about training runs.
- With that being done, you'll be able to stay organized with training run commands in similar form to:
nerfbaselines train --method instant-ngp --data datasets/mipnerf360/kitchen --output results/ingp_kitchen
- Set env variable NERFBASELINES_PREFIX to wherever you want new environments to be made.

Environment variables to set (with example values that you may change as needed)
- export NERFBASELINES_PREFIX=/project/3dllms/melgin/conda/envs/
- export NERFBASELINES_HOME_DIR=/project/3dllms/melgin/nerfbaselines-grocery/
- export GROCERY_DATA_CONVERTED_DIR=/project/3dllms/DATASETS/CONVERTED/UNGROUPED/
- export GROCERY_DATA_CONVERTED_GROUPED_DIR=/project/3dllms/DATASETS/CONVERTED/GROUPED/
- export GROCERY_DATA_NORMAL_DIR=/project/3dllms/DATASETS/PROCESSED/
- export GROCERY_DATA_NORMAL_GROUPED_DIR=/project/3dllms/DATASETS/GROUPED/
- export GROCERY_RESULTS_DIR=${NERFBASELINES_HOME_DIR}results/
- export GROCERY_LOGS_DIR=${NERFBASELINES_HOME_DIR}logs/
- export GROCERY_CSVS_DIR=${NERFBASELINES_HOME_DIR}csv/csv_results/

---- END fork preamble ----

<img width=112 height=112 align="left" src="assets/logo.png" />
<h1>
    <div>NerfBaselines</div>

[![PyPI - Version](https://img.shields.io/pypi/v/nerfbaselines)](https://pypi.org/project/nerfbaselines/)
[![GitHub License](https://img.shields.io/badge/license-MIT-%2397ca00)](https://github.com/jkulhanek/nerfbaselines/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/nerfbaselines)](https://pepy.tech/project/nerfbaselines)
</h1>

NerfBaselines is a framework for **evaluating and comparing existing NeRF and 3DGS methods**. Currently, most official implementations use different dataset loaders, evaluation protocols, and metrics, which renders benchmarking difficult. Therefore, this project aims to provide a **unified interface** for running and evaluating methods on different datasets in a consistent way using the same metrics. But instead of reimplementing the methods, **we use the official implementations** and wrap them so that they can be run easily using the same interface.

Please visit the <a href="https://jkulhanek.com/nerfbaselines">project page to see the results</a> of implemented methods on dataset benchmarks.<br/>

### [Project Page + Results](https://jkulhanek.com/nerfbaselines)  &nbsp;|&nbsp; [Paper](https://arxiv.org/pdf/2406.17345.pdf)

## Getting started
Start by installing the `nerfbaselines` pip package on your host system.
```bash
pip install nerfbaselines
```
Now you can use the `nerfbaselines` cli to interact with NerfBaselines.

The next step is to choose the backend which will be used to install different methods. At the moment there are the following backends implemented:
- **docker**: Offers good isolation, requires `docker` (with [NVIDIA container toolkit](https://github.com/NVIDIA/nvidia-container-toolkit)) to be installed and the user to have access to it (being in the docker user group).
- **apptainer**: Similar level of isolation as `docker`, but does not require the user to have privileged access.
- **conda** (default): Does not require docker/apptainer to be installed, but does not offer the same level of isolation and some methods require additional
dependencies to be installed. Also, some methods are not implemented for this backend because they rely on dependencies not found on `conda`.
- **python**: Will run everything directly in the current environment. Everything needs to be installed in the environment for this backend to work.

The backend can be set as the `--backend <backend>` argument or using the `NERFBASELINES_BACKEND` environment variable.

## Downloading data
For some datasets, e.g. Mip-NeRF 360, NerfStudio, Blender, or Tanks and Temples, the datasets can be downloaded automatically. 
You can specify the argument `--data external://dataset/scene` during training
or download the dataset beforehand by running `nerfbaselines download-dataset dataset/scene`.
Examples:
```bash
# Downloads the garden scene to the cache folder.
nerfbaselines download-dataset mipnerf360/garden

# Downloads all nerfstudio scenes to the cache folder.
nerfbaselines download-dataset nerfstudio

# Downloads kithen scene to folder kitchen
nerfbaselines download-dataset mipnerf360/kitchen -o kitchen
```

## Training
To start the training, use the `nerfbaselines train --method <method> --data <data>` command. Use `--help` argument to learn about all implemented methods and supported features.

## Rendering
The `nerfbaselines render --checkpoint <checkpoint>` command can be used to render images from a trained checkpoint. Again, use `--help` to learn about the arguments.

In order to render a camera trajectory (e.g., created using the interactive viewer), use the following command command:
```bash
nerfbaselines render-trajectory --checkpoint <checkpoint> --trajectory <trajectory> --output <output.mp4>
```

## Interactive viewer
Given a trained checkpoint, the interactive viewer can be launched as follows:
```bash
nerfbaselines viewer --checkpoint <checkpoin> --data <dataset>
```
Even though the argument `--data <dataset>` is optional, it is recommended, as the camera poses
are used to perform gravity alignment and rescaling for a better viewing experience.
It also enables visualizing the input camera frustums.

## Results
In this section, we present results of implemented methods on standard benchmark datasets. For detailed results, visit the project page:
[https://jkulhanek.com/nerfbaselines](https://jkulhanek.com/nerfbaselines)

### Mip-NeRF 360
Mip-NeRF 360 is a collection of four indoor and five outdoor object-centric scenes. The camera trajectory is an orbit around the object with fixed elevation and radius. The test set takes each n-th frame of the trajectory as test views.
Detailed results are available on the project page: [https://jkulhanek.com/nerfbaselines/mipnerf360](https://jkulhanek.com/nerfbaselines/mipnerf360)

| Method                                                                                   |       PSNR |      SSIM | LPIPS (VGG) |        Time |   GPU mem. |
|:-----------------------------------------------------------------------------------------|-----------:|----------:|------------:|------------:|-----------:|
| [Zip-NeRF](https://jkulhanek.com/nerfbaselines/m-zipnerf)                                | **28.553** | **0.829** |   **0.218** |  5h 30m 20s |    26.8 GB |
| [Mip-NeRF 360](https://jkulhanek.com/nerfbaselines/m-mipnerf360)                         |   *27.681* |     0.792 |       0.272 | 30h 14m 36s |    33.6 GB |
| [Mip-Splatting](https://jkulhanek.com/nerfbaselines/m-mip-splatting)                     |     27.492 |     0.815 |       0.258 |     25m 37s |    11.0 GB |
| [Gaussian Splatting](https://jkulhanek.com/nerfbaselines/m-gaussian-splatting)           |     27.434 |     0.814 |       0.257 |     23m 25s |    11.1 GB |
| [Gaussian Opacity Fields](https://jkulhanek.com/nerfbaselines/m-gaussian-opacity-fields) |     27.421 |   *0.826* |     *0.234* |   1h 3m 54s |    28.4 GB |
| [NerfStudio](https://jkulhanek.com/nerfbaselines/m-nerfacto)                             |     26.388 |     0.731 |       0.343 |   *19m 30s* | **5.9 GB** |
| [Instant NGP](https://jkulhanek.com/nerfbaselines/m-instant-ngp)                         |     25.507 |     0.684 |       0.398 |  **3m 54s** |   *7.8 GB* |


### Blender
Blender (nerf-synthetic) is a synthetic dataset used to benchmark NeRF methods. It consists of 8 scenes of an object placed on a white background. Cameras are placed on a semi-sphere around the object.
Detailed results are available on the project page: [https://jkulhanek.com/nerfbaselines/blender](https://jkulhanek.com/nerfbaselines/blender)

| Method                                                                                   |       PSNR |      SSIM | LPIPS (VGG) |        Time |   GPU mem. |
|:-----------------------------------------------------------------------------------------|-----------:|----------:|------------:|------------:|-----------:|
| [Zip-NeRF](https://jkulhanek.com/nerfbaselines/m-zipnerf)                                | **33.670** | **0.973** |   **0.036** |  5h 21m 57s |    26.2 GB |
| [Gaussian Opacity Fields](https://jkulhanek.com/nerfbaselines/m-gaussian-opacity-fields) |   *33.451* |   *0.969* |       0.038 |     18m 26s |     3.1 GB |
| [Mip-Splatting](https://jkulhanek.com/nerfbaselines/m-mip-splatting)                     |     33.330 |     0.969 |       0.039 |      6m 49s |   *2.7 GB* |
| [Gaussian Splatting](https://jkulhanek.com/nerfbaselines/m-gaussian-splatting)           |     33.308 |     0.969 |     *0.037* |     *6m 6s* |     3.1 GB |
| [TensoRF](https://jkulhanek.com/nerfbaselines/m-tensorf)                                 |     33.172 |     0.963 |       0.051 |     10m 47s |    16.4 GB |
| [K-Planes](https://jkulhanek.com/nerfbaselines/m-kplanes)                                |     32.265 |     0.961 |       0.062 |     23m 58s |     4.6 GB |
| [Instant NGP](https://jkulhanek.com/nerfbaselines/m-instant-ngp)                         |     32.198 |     0.959 |       0.055 |  **2m 23s** | **2.6 GB** |
| [Tetra-NeRF](https://jkulhanek.com/nerfbaselines/m-tetra-nerf)                           |     31.951 |     0.957 |       0.056 |  6h 53m 20s |    29.6 GB |
| [Mip-NeRF 360](https://jkulhanek.com/nerfbaselines/m-mipnerf360)                         |     30.345 |     0.951 |       0.060 |  3h 29m 39s |   114.8 GB |
| [NerfStudio](https://jkulhanek.com/nerfbaselines/m-nerfacto)                             |     29.191 |     0.941 |       0.095 |      9m 38s |     3.6 GB |
| [NeRF](https://jkulhanek.com/nerfbaselines/m-nerf)                                       |     28.723 |     0.936 |       0.092 | 23h 26m 30s |    10.2 GB |


### Tanks and Temples
Tanks and Temples is a benchmark for image-based 3D reconstruction. The benchmark sequences were acquired outside the lab, in realistic conditions. Ground-truth data was captured using an industrial laser scanner. The benchmark includes both outdoor scenes and indoor environments. The dataset is split into three subsets: training, intermediate, and advanced.
Detailed results are available on the project page: [https://jkulhanek.com/nerfbaselines/tanksandtemples](https://jkulhanek.com/nerfbaselines/tanksandtemples)

| Method                                                                                   |       PSNR |      SSIM |     LPIPS |       Time |   GPU mem. |
|:-----------------------------------------------------------------------------------------|-----------:|----------:|----------:|-----------:|-----------:|
| [Zip-NeRF](https://jkulhanek.com/nerfbaselines/m-zipnerf)                                | **24.628** | **0.840** | **0.131** |  5h 44m 9s |    26.6 GB |
| [Mip-Splatting](https://jkulhanek.com/nerfbaselines/m-mip-splatting)                     |   *23.930* |   *0.833* |     0.166 |    15m 56s |     7.3 GB |
| [Gaussian Splatting](https://jkulhanek.com/nerfbaselines/m-gaussian-splatting)           |     23.827 |     0.831 |   *0.165* |  *13m 48s* |     6.9 GB |
| [Gaussian Opacity Fields](https://jkulhanek.com/nerfbaselines/m-gaussian-opacity-fields) |     22.395 |     0.825 |     0.172 |          - |          - |
| [NerfStudio](https://jkulhanek.com/nerfbaselines/m-nerfacto)                             |     22.043 |     0.743 |     0.270 |    19m 27s | **3.7 GB** |
| [Instant NGP](https://jkulhanek.com/nerfbaselines/m-instant-ngp)                         |     21.623 |     0.712 |     0.340 | **4m 27s** |   *4.1 GB* |


### Reproducing results
| Method                  | Mip-NeRF 360  | Blender    | NerfStudio | Tanks and Temples | LLFF    | Photo Tourism | SeaThru-NeRF |
|:-----------------------:|:-------------:|:----------:|:----------:|:-----------------:|:-------:|:-------------:|:------------:|
| NerfStudio              | 🥇 gold       | 🥇 gold    | ❔         | 🥇 gold           | ❌      | ❔            | ❔           |
| Instant-NGP             | 🥇 gold       | 🥇 gold    | 🥇 gold    | 🥇 gold           | ❌      | ❔            | ❔           |
| Gaussian Splatting      | 🥇 gold       | 🥇 gold    | ❌         | 🥇 gold           | ❌      | ❔            | 🥇 gold      | 
| Mip-Splatting           | 🥇 gold       | 🥇 gold    | ❌         | 🥇 gold           | ❌      | ❔            | 🥇 gold      |
| Gaussian Opacity Fields | 🥇 gold       | 🥇 gold    | ❌         | 🥇 gold           | ❌      | ❔            | ❔           |
| Tetra-NeRF              | 🥈 silver     | 🥈 silver  | ❔         | ❔                | ❌      | ❔            | ❔           |
| Mip-NeRF 360            | 🥇 gold       | 🥇 gold    | ❔         | ❔                | ❌      | ❔            | ❔           |
| Zip-NeRF                | 🥇 gold       | 🥇 gold    | 🥇 gold    | 🥇 gold           | ❌      | ❔            | ❔           |
| CamP                    | ❔            | ❔         | ❔         | ❔                | ❌      | ❔            | ❔           |
| TensoRF                 | ❌            | 🥇 gold    | ❔         | ❔                | 🥇 gold | ❔            | ❔           |
| NeRF                    | ❔            | 🥇 gold    | ❔         | ❔                | ❔      | ❔            | ❔           |
| K-Planes                | ❔            | 🥇 gold    | ❔         | ❔                | ❔      | 🥈 silver     | ❔           |
| Nerf-W (reimpl.)        | ❔            |  ❔        | ❔         | ❔                | ❔      | 🥇 gold       | ❔           |
| SeaThru-NeRF            | ❔            |  ❔        | ❔         | ❔                | ❔      | ❔            | 🥇 gold      |

## Contributing
Contributions are very much welcome. Please open a PR with a dataset/method/feature that you want to contribute. The goal of this project is to slowly expand by implementing more and more methods.

## Citation
If you use this project in your research, please cite the following paper:
```bibtex
@article{kulhanek2024nerfbaselines,
  title={NerfBaselines: Consistent and Reproducible Evaluation of Novel View Synthesis Methods},
  author={Jonas Kulhanek and Torsten Sattler},
  year={2024},
  journal={arXiv},
}
```

## License
This project is licensed under the [MIT license](https://raw.githubusercontent.com/jkulhanek/nerfbaselines/main/LICENSE)
Each implemented method is licensed under the license provided by the authors of the method.
For the currently implemented methods, the following licenses apply:
- CamP: [Apache 2.0](https://raw.githubusercontent.com/jonbarron/camp_zipnerf/main/LICENSE)
- Gaussian Opacity Fields: [custom, research only](https://raw.githubusercontent.com/autonomousvision/gaussian-opacity-fields/main/LICENSE.md)
- Gaussian Splatting: [custom, research only](https://raw.githubusercontent.com/graphdeco-inria/gaussian-splatting/main/LICENSE.md)
- Instant NGP: [custom, research only](https://raw.githubusercontent.com/NVlabs/instant-ngp/master/LICENSE.txt)
- K-Planes: [BSD 3](https://raw.githubusercontent.com/sarafridov/K-Planes/main/LICENSE)
- Mip-NeRF 360: [Apache 2.0](https://raw.githubusercontent.com/google-research/multinerf/main/LICENSE)
- Mip-Splatting: [custom, research only](https://raw.githubusercontent.com/autonomousvision/mip-splatting/main/LICENSE.md)
- NeRF-W (reimplementation): [MIT](https://raw.githubusercontent.com/kwea123/nerf_pl/master/LICENSE)
- NeRF: [MIT](https://github.com/bmild/nerf/blob/master/LICENSE)
- SeaThru-NeRF: [Apache 2.0](https://raw.githubusercontent.com/deborahLevy130/seathru_NeRF/master/LICENSE)
- TensoRF: [MIT](https://github.com/apchenstu/TensoRF/blob/main/LICENSE)
- Tetra-NeRF: [MIT](https://raw.githubusercontent.com/jkulhanek/tetra-nerf/master/LICENSE)
- Zip-NeRF: [Apache 2.0](https://raw.githubusercontent.com/jonbarron/camp_zipnerf/main/LICENSE)


## Acknowledgements
A big thanks to the authors of all implemented methods for the great work they have done.
We would also like to thank the authors of [NerfStudio](https://github.com/nerfstudio-project/nerfstudio), 
especially Brent Yi, for [viser](https://github.com/nerfstudio-project/viser) - a great framework powering the viewer.
This work was supported by the Czech Science Foundation (GAČR) EXPRO (grant no. 23-07973X), the Grant Agency of the Czech Technical University in Prague (grant no. SGS24/095/OHK3/2T/13), and by the Ministry of Education, Youth and Sports of the Czech
Republic through the e-INFRA CZ (ID:90254).
