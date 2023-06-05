# Jurassic Campus

## Mission

Have you ever looked at a chicken and wondered - what if this delicious animal was 100 times larger and featherless? Unfortunately, those big chickens we know as dinosaurs were wiped out eons before humans came to be. Deprived of the opportunity to play hide-and-seek with our dino pets, we decided to imagine a world where, between the perfect cover of city skyscrapers, we can play i-spy with our favorite dinosaurs. 

## Setup

The non-technical setup instructions include printing the specific ArUco tags and downloading the dinosaur videos. Both are detailed and linked below.

- The required ArUco tags can be found [here](https://docs.google.com/document/d/1eA6-tnGdpKxbonCRuyIRx6itX3ZplzBn_FTm_ptHkCE/edit). Print the first page to test with a single piece of paper. Print the rest to test in an open environment.

- The recommended dinosaur videos can be found [here](https://drive.google.com/drive/u/1/folders/1s04W4yC9aMDRX1DZCRmgnEE9NPL-GhlU). Download and place them in the `dinos/` directory in this repository after cloning it.

The technical setup instructions only require the installation of a few libraries. They assume you have [Python](https://www.python.org/downloads/) and [pip](https://pypi.org/project/pip/) downloaded and configured on your system. Please note that these commands may look different depending on your machine.

```shell
pip install opencv-python
pip install numpy
pip install numba
```

## Codebase

This repository has four Python files that all separate a layer of abstraction.

- `jurassic_campus.py` picks a random video from the `dinos/` folder to show on the webcam feed

- `augment_video.py` starts the webcam and input file video streams to get frames to augment

- `augment_frame.py` augments the input frame onto the webcam frame where tags are detected

- `transparent_overlay.py` overlays the input frame onto the webcam frame with a transparent background

Run `python jurassic_campus.py` to run the entire system. 