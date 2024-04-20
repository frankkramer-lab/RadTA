# RadTA: RADiomics Trend Analysis for CT scans

RadTA (RADiomics Trend Analysis) is a powerful but intuitive AI-driven tool for clinical data scientists for creating time-series based radiomics trend analyses between pre- and post-condition CT volumes.
The framework automtically segments various body parts as well as tissues by incorperating the TotalSegmentator framework, and computes fat/muscle/etc body compositions as well as determines more than 100 radiomic features based on these segmentation masks by incorperating the BOA framework. Finally, the radiomic features between paired-volumes are statistically compared and trends identified. These results are visualized and summarized in the output directory.

## Usage

easy to use with the main runner, requiring only the pre- and post-condition NIfTI volumes as input.

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

For the submodules TotalSegmentator and BOA `python3.9` is required.

```sh
# Installation in unix/ubuntu
apt-get update
apt-get install software-properties-common
add-apt-repository ppa:deadsnakes/ppa
# Install py39 from deadsnakes repository
apt-get install python3.9
# Install pip from standard ubuntu packages
apt-get install python3-pip
```

Install BOA & RadTA:

```sh
# Get the RadTA software from GitHub
git clone --submodules https://TODO
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
