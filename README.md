# cse455-final-project

## Mission

Have you ever looked at a chicken and wondered - what if this delicious animal was 100 times larger and featherless? Unfortunately, those big chickens we know as dinosaurs were wiped out eons before humans came to be. Deprived of the opportunity to play hide-and-seek with our dino pets, we decided to imagine a world where, between the perfect cover of city skyscrapers, we can play i-spy with our favorite dinosaurs. 

## Execution

This repository has three Python files that all separate a layer of abstraction.

- `jurassic_park.py`: picks a random video from the `dinos/` folder to show on the webcam feed

- `augment_video.py`: starts the webcam and input file video streams to get frames to augment

- `augment_frame.py`: augments the input frame onto the webcam frame where tags are detected

- `transparent_overlay`: overlays the input frame onto the webcam frame with a transparent background

Run `python jurassic_park.py` to run the entire system. 