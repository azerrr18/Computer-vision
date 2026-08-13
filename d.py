from ultralytics import YOLO    



model = YOLO("yolov8n.pt")
results = model("yarpaq_dolmasi.jpg")
results[0].show()
print(results[0].boxes.cls)
print(model.names)



