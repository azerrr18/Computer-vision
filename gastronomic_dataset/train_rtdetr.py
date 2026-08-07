from ultralytics import RTDETR

model = RTDETR('rtdetr-x.pt') 

results = model.train(data='data.yaml', epochs=150, augment=True, patience=30, freeze=6)

results = model.export() 