# RadTA: RADiomics Trend Analysis for CT scans

blabla CHATgpt

todo:
- apply RadTA on public datasets
- write eval: ploting
- requirements.txt fix
- write documentation

### Usage



### Install

 *Requirement:* `python3.9`

How to install `python3.9`:
```sh
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
# braucht man das????
apt-get -y update; DEBIAN_FRONTEND=noninteractive apt-get -y install \
    curl ffmpeg libsm6 libxext6 libpangocairo-1.0-0 dcmtk xvfb libjemalloc2 && rm -rf /var/lib/apt/lists/*

python3.9 -m pip install -r requirements.txt
python3.9 -m pip install pyradiomics # add to requirements
python3.9 -m pip install torch  # add to requirements
python3.9 -m pip install external_BOA/.
```
