import os
import shutil
import pandas as pd
from tqdm import tqdm
import cv2
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random
from pathlib import Path
import json
from PIL import Image

# CODE FOR MAPPING YOLO CLASS LABELS WHEN MERGING DIFFERENT DATASETS WITH DIFFERENT NUMBERS OF CLASSES AND YOLO LABEL FORMAT

def create_mapping(classes):
    """
    Create a mapping from class names to indices.
    
    Parameters:
    - classes: List of class names.
    
    Returns:
    - mapping: Dictionary with class names as keys and indices as values.
    """
    mapping = {}
    for idx, cls in enumerate(sorted(classes)):
        mapping[cls] = idx
    return mapping

def get_name_by_index(index, my_dict):
    """
    Get the class name by index from a mapping dictionary.
    
    Parameters:
    - index: The index to look up.
    - my_dict: The mapping dictionary.
    
    Returns:
    - The class name corresponding to the given index.
    """
    for name, idx in my_dict.items():
        if idx == int(index):
            return name
    return None

def update_labels(label_file, old_mapping, new_mapping):
    """
    Update YOLO labels in a file from old mapping to new mapping.
    
    Parameters:
    - label_file: The path to the YOLO label file.
    - old_mapping: The old class-to-index mapping.
    - new_mapping: The new class-to-index mapping.
    """
    with open(label_file, 'r') as f:
        lines = f.readlines()
    print(f'Updating labels in {label_file} ....')
    print('Old labels: ', lines)
    updated_lines = []
    for line in lines:
        if len(line.split()) == 5:
            class_id = line.split()[0]
            class_name = get_name_by_index(class_id, old_mapping)
            if class_name in new_mapping:
                updated_class_id = new_mapping[class_name]   
                updated_line = f"{updated_class_id} {' '.join(line.split()[1:])}"
                updated_lines.append(updated_line)
                print(f'Mapped the class {class_name} from old id of {class_id} to {updated_class_id}')
            else:
                print(f'Deleting the label for class {class_name} as it is not found in new mapping')
    with open(label_file, 'w') as f:
        for item in updated_lines:
            f.write(item + '\n')
    print('Updated labels: ', updated_lines)
    print('\n\n')

# Lists of class names from different datasets
dataset1 = ['airan-katyk', 'almond', 'apple', 'artichoke', 'arugula', 'asparagus', 'avocado', 'bacon', 'banana', 'beans', 'beet', 'bell pepper', 'black olives', 'blackberry', 'blueberry', 'boiled chicken', 'bread', 'broccoli', 'buckwheat', 'cabbage', 'cakes', 'carrot', 'cashew', 'casserole with meat and vegetables', 'cauliflower', 'celery', 'cereal based cooked food', 'cheese', 'chickpeas', 'chips', 'cooked eggplant', 'cooked food based on meat', 'cooked food meat with vegetables', 'cooked zucchini', 'cookies', 'corn', 'crepe', 'cucumber', 'cutlet', 'desserts', 'egg product', 'fish', 'fried chicken', 'fried eggs', 'fried fish', 'fried meat', 'fruits', 'granola', 'grapes', 'green beans', 'herbs', 'hummus', 'ice-cream', 'juice', 'kiwi', 'lavash', 'legumes', 'lemon', 'mandarin', 'mashed potato', 'meat product', 'melon', 'mixed berries', 'mixed nuts', 'mushrooms', 'onion', 'orange', 'pasta', 'pastry', 'peanut', 'pear', 'peas', 'pecan', 'pickled cabbage', 'pickled squash', 'pie', 'pineapple', 'pizza', 'plov', 'porridge', 'potatoes', 'pumpkin', 'radish', 'raspberry', 'rice', 'salad fresh', 'salad leaves', 'salad with fried meat veggie', 'salad with sauce', 'sandwich', 'sausages', 'seafood', 'snacks bread', 'souces', 'soup-plain', 'soy product', 'spinach', 'strawberry', 'suzbe', 'sweet potatoes', 'tomato', 'tomato souce', 'tushpara-wo-soup', 'vegetable based cooked food', 'waffles', 'walnut', 'watermelon', 'zucchini']
dataset2 = ['airan-katyk', 'almond', 'apple', 'arugula', 'asparagus', 'avocado', 'bacon', 'banana', 'beans', 'beet', 'bell pepper', 'black olives', 'blackberry', 'blueberry', 'boiled chicken', 'bread', 'broccoli', 'cabbage', 'carrot', 'cashew', 'casserole with meat and vegetables', 'cauliflower', 'celery', 'cereal based cooked food', 'cheese', 'chickpeas', 'chips', 'cooked eggplant', 'cooked food based on meat', 'cooked food meat with vegetables', 'cooked zucchini', 'cookies', 'corn', 'cucumber', 'cutlet', 'desserts', 'egg product', 'eggplant', 'fish', 'fried chicken', 'fried fish', 'fried meat', 'fruits', 'granola', 'grapes', 'green beans', 'herbs', 'hummus', 'ice-cream', 'irimshik', 'juice', 'kiwi', 'lavash', 'lemon', 'mandarin', 'mango', 'meat product', 'melon', 'mixed berries', 'mixed nuts', 'mushrooms', 'onion', 'orange', 'pasta', 'pastry', 'pear', 'peas', 'pecan', 'pickled cabbage', 'pickled squash', 'pie', 'pineapple', 'pizza', 'porridge', 'potatoes', 'radish', 'raspberry', 'rice', 'salad fresh', 'salad with fried meat veggie', 'salad with sauce', 'sausages', 'seafood', 'smetana', 'snacks', 'snacks bread', 'souces', 'soup-plain', 'soy product', 'spinach', 'strawberry', 'suzbe', 'sweet potatoes', 'tomato', 'tushpara-wo-soup', 'vegetable based cooked food', 'waffles', 'walnut', 'watermelon']
dataset3 = ['achichuk', 'airan-katyk', 'almond', 'apple', 'apricot', 'artichoke', 'arugula', 'asip', 'asparagus', 'avocado', 'bacon', 'baklava', 'banana', 'basil', 'bauyrsak', 'bean soup', 'beans', 'beef shashlyk', 'beef shashlyk-v', 'beer', 'beet', 'bell pepper', 'beshbarmak', 'beverages', 'black olives', 'blackberry', 'blueberry', 'boiled chicken', 'boiled eggs', 'boiled meat', 'borsch', 'bread', 'brizol', 'broccoli', 'buckwheat', 'butter', 'cabbage', 'cakes', 'carrot', 'cashew', 'casserole with meat and vegetables', 'cauliflower', 'caviar', 'celery', 'cereal based cooked food', 'chak-chak', 'cheburek', 'cheese', 'cheese souce', 'cherry', 'chestnuts', 'chicken shashlyk', 'chicken shashlyk-v', 'chickpeas', 'chili pepper', 'chips', 'chocolate', 'chocolate paste', 'cinnabons', 'coffee', 'condensed milk', 'cooked eggplant', 'cooked food based on meat', 'cooked food meat with vegetables', 'cooked tomatoes', 'cooked zucchini', 'cookies', 'corn', 'corn flakes', 'crepe', 'crepe w filling', 'croissant', 'croissant sandwich', 'cucumber', 'cutlet', 'dates', 'desserts', 'dill', 'doner-lavash', 'doner-nan', 'dragon fruit', 'dried fruits', 'egg product', 'eggplant', 'figs', 'fish', 'french fries', 'fried cheese', 'fried chicken', 'fried eggs', 'fried fish', 'fried meat', 'fruits', 'garlic', 'granola', 'grapefruit', 'grapes', 'green beans', 'green olives', 'hachapuri', 'hamburger', 'hazelnut', 'herbs', 'hinkali', 'honey', 'hot dog', 'hummus', 'hvorost', 'ice-cream', 'irimshik', 'jam', 'juice', 'karta', 'kattama-nan', 'kazy-karta', 'ketchup', 'kiwi', 'kurt', 'kuyrdak', 'kymyz-kymyran', 'lagman-fried', 'lagman-w-soup', 'lavash', 'legumes', 'lemon', 'lime', 'mandarin', 'mango', 'manty', 'mashed potato', 'mayonnaise', 'meat based soup', 'meat product', 'melon', 'milk', 'minced meat shashlyk', 'mint', 'mixed berries', 'mixed nuts', 'muffin', 'mushrooms', 'naryn', 'nauryz-kozhe', 'noodles soup', 'nuggets', 'oil', 'okra', 'okroshka', 'olivie', 'onion', 'onion rings', 'orama', 'orange', 'pancakes', 'parsley', 'pasta', 'pastry', 'peach', 'peanut', 'pear', 'peas', 'pecan', 'persimmon', 'pickled cabbage', 'pickled cucumber', 'pickled ginger', 'pickled squash', 'pie', 'pineapple', 'pistachio', 'pizza', 'plov', 'plum', 'pomegranate', 'porridge', 'potatoes', 'pumpkin', 'pumpkin seeds', 'quince', 'radish', 'raspberry', 'redcurrant', 'ribs', 'rice', 'rosemary', 'salad fresh', 'salad leaves', 'salad with fried meat veggie', 'salad with sauce', 'samsa', 'sandwich', 'sausages', 'scallion', 'seafood', 'seafood soup', 'sheep-head', 'shelpek', 'shorpa', 'shorpa chicken', 'smetana', 'smoked fish', 'snacks', 'snacks bread', 'soda', 'souces', 'soup-plain', 'soy souce', 'spinach', 'spirits', 'strawberry', 'sugar', 'sushi', 'sushi fish', 'sushi nori', 'sushki', 'suzbe', 'sweets', 'syrniki', 'taba-nan', 'talkan-zhent', 'tartar', 'tea', 'tomato', 'tomato souce', 'tomato-cucumber-salad', 'tushpara-fried', 'tushpara-w-soup', 'tushpara-wo-soup', 'vareniki', 'vegetable based cooked food', 'vegetable soup', 'waffles', 'walnut', 'wasabi', 'water', 'watermelon', 'wine', 'wings', 'zucchini']

# Combine and create sets of class names for different datasets
combined_classes = set(folder1 + folder2)
all_classes = set(dataset1 + dataset2 + dataset3)

with open('./new_dataset_classes.txt', 'w') as f:
    for cls in sorted(all_classes):
       f.write(cls + '\n')

# Ensure the class count is correct
assert len(google_classes) == 113
assert len(all_classes) == 241

# Create mappings from class names to indices
old_mapping = create_mapping(dataset1)
new_mapping = create_mapping(all_classes)

# Update labels in the given directory
labelfolder = '../datasets/Nutrition5k/train/labels'
for labelfile in tqdm(sorted(os.listdir(labelfolder))):
    labelfilepath = os.path.join(labelfolder, labelfile)
    update_labels(labelfilepath, old_mapping, new_mapping)
