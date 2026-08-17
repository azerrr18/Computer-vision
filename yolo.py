from pathlib import Path
import requests
from ultralytics import YOLO


model = YOLO("yolov8s.pt")


def detect_photo(image_path:str) -> list[str]:
    results = model(image_path)
    class_ids = results[0].boxes.cls
    detected = [model.names[int (c)] for c in class_ids]
    return list(set(detected))

if __name__ =="__main__":
    results = model("yarpaq_dolmasi.jpg")
    results[0].show()
    print(results[0].boxes.cls)
