from pathlib import Path
import requests
from ultralytics import YOLO

url = "https://issai.nu.edu.kz/wp-content/themes/issai-new/data/models/GFSD/yolov8s.pt"

response = requests.get(url)

with open("yolov8s.pt","wb") as f:
    f.write(response.content)

print("File donwloaded succesfully")

model = YOLO("yolov8s.pt")
results = model("yarpaq_dolmasi.jpg")
results[0].show()
print(results[0].boxes.cls)