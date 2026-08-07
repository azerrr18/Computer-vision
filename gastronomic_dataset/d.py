
from ultralytics import YOLO    



model = YOLO("yolov8n.pt")
results = model("banana.jpg")
results[0].show()
print(results[0].boxes.cls)
print(model.names)

