import cv2
import pathlib
import shutil
import random
import pickle

TARGET_DIR = pathlib.Path("unclassified")
WHITE_DIR = pathlib.Path("training-data/white")
BLACK_DIR = pathlib.Path("training-data/black")
BLANK_DIR = pathlib.Path("training-data/blank")
DISCARD_DIR = pathlib.Path("discard")
SET_PATH = TARGET_DIR.joinpath("already_classified.p")

# Lets try to grab some data from the directory
# Specifically we want to grab a set we created using pickle
# This will store the all of the filenames we have already classified
already_classified = set()
try:
    already_classified = pickle.load(open(SET_PATH, "rb"))
    print(
        f"Loaded already classified set with {len(already_classified)} pictures"
    )
except FileNotFoundError:
    print("Was unable to grab the file from target directory")
    pass
# So we want to go ahead and iterate through all of the files
# We want to show them to the user
# The user will choose if the file contains a spikeball
# Then we will move the file into the appropriate directory

paths = list(TARGET_DIR.glob("square*"))
print(f"{len(paths)} Files Found")

# Lets go ahead and randomize them so we don't get any bias
paths_shuffled = paths.copy()
random.shuffle(paths_shuffled)

for p in paths_shuffled:
    if p not in already_classified:
        # Lets grab the image
        img = cv2.imread(str(p))
        # Lets show it to the user
        cv2.imshow("Image To Classify", cv2.resize(img, (200, 200)))
        # Lets ask the user if this is a spikeball
        # If the user presses the space bar we will move the file
        # Otherwise we will move it to the non-spikeball directory
        key = cv2.waitKey(0)
        if key == ord("q"):
            exit(1)
        print(key)
        if key == ord('w'):
            print(f"Copying {p} to White Directory")
            shutil.copyfile(str(p), str(WHITE_DIR.joinpath(p.name)))
        elif key == ord('b'):
            print(f"Copying {p} to Black Directory")
            shutil.copyfile(str(p), str(BLACK_DIR.joinpath(p.name)))
        elif key == ord('d'):
            print(f"Copying {p} to Discard Directory")
            shutil.copyfile(str(p), str(DISCARD_DIR.joinpath(p.name)))
        else:
            print(f"Copying {p} to Blank Directory")
            shutil.move(str(p), str(BLANK_DIR.joinpath(p.name)))
        # Lets add this to the set of already classified files
        already_classified.add(p.name)
        # Lets save the set of already classified files
        pickle.dump(already_classified, open(SET_PATH, "wb"))