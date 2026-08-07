import os
import shutil
from pathlib import Path
import random

# CODE FOR SPLITTING THE DATASET INTO TRAIN/TEST/VAL

def split_data(source_images_folder, source_labels_folder, destination_folder, train_ratio=0.8):
    """
    Split the dataset into training, validation, and testing sets.
    
    Parameters:
    - source_images_folder: Path to the source folder containing images.
    - source_labels_folder: Path to the source folder containing labels.
    - destination_folder: Path to the destination folder for the split datasets.
    - train_ratio: Ratio of training data. Default is 0.8.
    """
    # Read image files from the source directory
    image_files = os.listdir(source_images_folder)
    
    # Shuffle and split image files into training, testing, and validation sets
    random.seed(100)
    random.shuffle(image_files)
    split_1 = int(train_ratio * len(image_files))
    split_2 = int((train_ratio + (1 - train_ratio) / 2) * len(image_files))
    train_images = image_files[:split_1]
    test_images = image_files[split_1:split_2]
    val_images = image_files[split_2:]
    
    # Create destination directories
    destination_folder.mkdir(parents=True, exist_ok=True)
    splits = [train_images, val_images, test_images]
    for i in range(3):
        if i == 0:
            split_folder = 'train'
        elif i == 1:
            split_folder = 'val'
        else:
            split_folder = 'test'
        for image in splits[i]:
            image_path = os.path.join(source_images_folder, image) 
            destination_image_path = destination_folder / split_folder / "images" / image
            destination_image_path.parent.mkdir(parents=True, exist_ok=True)
            label_file = image.rsplit(".", 1)[0] + '.txt'
            label_path = os.path.join(source_labels_folder, label_file)
            destination_label_path = destination_folder / split_folder / "labels" / label_file
            destination_label_path.parent.mkdir(parents=True, exist_ok=True)
            # Copying files to respective splits
            shutil.copy2(label_path, destination_label_path)
            shutil.copy2(image_path, destination_image_path)
            print("Image copied to ", destination_image_path)
    
    # Print the number of images in each split
    print(f"Number of train images: {len(train_images)}\n", 
          f"Number of validation images: {len(val_images)}\n",
          f"Number of test images: {len(test_images)}\n")

# Define source and destination folders
source_images_folder = Path('../datasets/Nutrition5k/train/images')
source_labels_folder = Path('../datasets/Nutrition5k/train/labels')
destination_folder = Path('../datasets/new')

# Split the dataset
split_data(source_images_folder, source_labels_folder, destination_folder, train_ratio=0.8)
