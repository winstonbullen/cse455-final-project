import random
from augment_video import run_augment_video

DINO_DIR = './dinos/'
NUM_DINOS = 1

def pick_random_dino():
    dino_index = random.randint(1, NUM_DINOS)
    dino_path = DINO_DIR + 'dino_' + str(dino_index) + '.mp4'
    return dino_path

def run():
    dino = pick_random_dino()
    run_augment_video(dino)

def main():
    run()

if __name__ == "__main__":
    main()