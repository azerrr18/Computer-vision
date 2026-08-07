from ultralytics import YOLO

model = YOLO('yolov8s.pt')

results = model.train(data='data.yaml', epochs=150, augment=True, patience=30)


results = model.export()