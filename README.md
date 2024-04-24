# RadTA: RADiomics Trend Analysis for CT scans

RadTA (RADiomics Trend Analysis) is a powerful yet intuitive AI-driven tool designed for clinical data scientists to perform time-series-based radiomics trend analyses between pre- and post-condition CT volumes. 

The framework automatically segments various body parts and tissues by incorporating the TotalSegmentator and BOA framework. It then computes fat/muscle/body compositions and determines over 100 radiomic features based on these segmentation masks by incorporating the BOA framework. Finally, it statistically compares the radiomic features between paired volumes, identifies trends, and visualizes and summarizes the results in the output directory.

## Usage

RadTA is easy to use with the main runner, requiring only the pre- and post-condition NIfTI volumes as input.

```sh
python3.9 radta/main.py -va volume-pre.nii.gz -vb volume-post.nii.gz -o results/
```

The command line interface documentation and its manual page can be viewed with the `--help` argument.

```sh
python3.9 radta/main.py --help

usage: main.py [-h] -va VOL_PRE -vb VOL_POST [-o PATH_OUTPUT]

CLI for RadTA: Radiomics Trend Analysis for CT scans

optional arguments:
  -h, --help            show this help message and exit
  -va VOL_PRE, --vol_pre VOL_PRE
                        Path to pre volume(s) file or directory with multiple volumes
  -vb VOL_POST, --vol_post VOL_POST
                        Path to post volume(s) file or directory with multiple volumes
  -o PATH_OUTPUT, --output PATH_OUTPUT
                        Path to evaluation output directory
```

## Install

For the submodules TotalSegmentator and BOA, `python3.9` is required.

Install Python3.9:

```sh
# Installation in unix/ubuntu
apt-get update
apt-get install software-properties-common
add-apt-repository ppa:deadsnakes/ppa
apt-get -y update; DEBIAN_FRONTEND=noninteractive apt-get -y install \
    curl ffmpeg libsm6 libxext6 libpangocairo-1.0-0 dcmtk xvfb libjemalloc2 && rm -rf /var/lib/apt/lists/*
# Install py39 from deadsnakes repository
apt-get install python3.9
# Install pip from standard ubuntu packages
apt-get install python3-pip
```

Install BOA & RadTA:

```sh
# Get the RadTA software from GitHub
git clone --recurse-submodules https://TODO
cd radta/
# Install all dependencies via pip
python3.9 -m pip install -r requirements.txt
python3.9 -m pip install external_BOA/.
```

## How to cite / More information

RadTA is currently unpublished. But coming soon!

```
Coming soon.
```

Thank you for citing our work.

**Additional References**

If you use this tool, please also thank and cite the following excellent works:

[BOA](https://journals.lww.com/investigativeradiology/abstract/9900/boa__a_ct_based_body_and_organ_analysis_for.176.aspx):
```
Haubold, J., Baldini, G., Parmar, V., Schaarschmidt, B. M., Koitka, S., Kroll, L., van Landeghem, N., Umutlu, L., Forsting, M., Nensa, F., & Hosch, R. (2023). BOA: A CT-Based Body and Organ Analysis for Radiologists at the Point of Care. Investigative radiology, 10.1097/RLI.0000000000001040. Advance online publication. https://doi.org/10.1097/RLI.0000000000001040
```

[TotalSegmentator](https://pubs.rsna.org/doi/10.1148/ryai.230024):
```
Wasserthal J, Breit H-C, Meyer MT, et al. TotalSegmentator: Robust Segmentation of 104 Anatomic Structures in CT Images. Radiol. Artif. Intell. 2023:e230024. Available at: https://pubs.rsna.org/doi/10.1148/ryai.230024.
```
[nnU-Net](https://www.nature.com/articles/s41592-020-01008-z):

```
Isensee F, Jaeger PF, Kohl SAA, et al. nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation. Nat. Methods. 2021;18(2):203–211. Available at: https://www.nature.com/articles/s41592-020-01008-z.
```

### Authors

Dr. Dominik Müller\
IT-Infrastructure for Translational Medical Research\
University of Augsburg\
Bavaria, Germany

Dr. Hannes Ulrich\
Medical Informatics Department - Kiel\
University Hospital Schleswig-Holstein\
Schleswig-Holstein, Germany

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3.\
See the LICENSE.md file for license rights and limitations.
