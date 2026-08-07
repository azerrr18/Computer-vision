---
license: cc-by-nc-4.0
task_categories:
- object-detection
tags:
- food dataset
- object recognition
size_categories:
- 10K<n<100K
---

# Global Gastronomic Culinary Dataset

In this work, we propose the food object detection dataset named the Global Gastronomic Culinary Dataset (GGCD). This is a follow-up to our previous work Central Asian Food Scenes Dataset (CAFSD)[1]. The dataset is the extension of our CAFSD dataset with the Nutrition5k dataset[2]. 
The original Nutrition5k contains images taken from an overhead angle for approximately 3,500 dishes and four different side-angle videos for approximately 1,500 dishes. We extracted different frames from the side-angle videos and combined them with the overhead images.
We annotated the Nutrition5k dataset with bounding boxes resulting in 12,839 images across 113 classes. 

The original CAFSD dataset contains 21,306 images spanning 239 classes. The final combined GFSD dataset contains 34,145 images across 241 food classes. Some visual examples of a few classes are shown for the annotated Nutrition5k and CAFSD datasets in the figure below. 
![Alt text](figures/paper_front.png)
*The images on the left illustrate the samples from the CAFSD dataset and on the right-hand side from the Nutrition5k dataset.*

The table below shows the number of images per split and instances across three datasets.
<table style="font-size:20px">
  <tr>
    <th>Dataset</th>
    <th>Number of Instances</th>
    <th>Train</th>
    <th>Valid</th>
    <th>Test</th>
  </tr>
  <tr>
    <td>CAFSD</td>
    <td>69,865</td>
    <td>17,046</td>
    <td>2,084</td>
    <td>2,176</td>
  </tr>
  <tr>
    <td>Nutrition5k</td>
    <td>23,445</td>
    <td>10,257</td>
    <td>1,272</td>
    <td>1,310</td>
  </tr>
  <tr>
    <td>GGCD</td>
    <td>102,017</td>
    <td>27,303</td>
    <td>3,356</td>
    <td>3,486</td>
  </tr>
</table>


The statistics of classes grouped into 18 coarse categories are shown in Figure below.
![Alt text](figures/side_by_side_categories.png)


## Project Files

The project directory contains the following files and directories:

- `coco_to_yolo.py`: Script to convert annotations from COCO format to YOLO format.
- `map_labels_yolo.py`: Script to map and update the label files for the YOLO dataset, when merging multiple datasets with YOLO label format.
- `split_data.py`: Script to split the dataset into training, validation, and test sets.
- `train_rtdetr.py`: Script used to train the RT-DETR (Real-Time Detection Transformer) model.
- `train_yolo.py`: Script used to train the YOLO (You Only Look Once) model.


# Download Datasets and Pre-trained Models

All dataset files and different models pre-trained on different datasets are available for download.

### Datasets
- **Global Gastronomic Culinary Dataset (GGCD)**: [Download GFSD.zip](https://issai.nu.edu.kz/wp-content/themes/issai-new/data/models/GFSD/GFSD.zip)
- **Annotated Nutrition5k Dataset**: [Download Nutrition5k.zip](https://issai.nu.edu.kz/wp-content/themes/issai-new/data/models/Nutrition5k/Nutrition5k.zip)

### Pre-trained Models
- **YOLOv8n model trained on Nutrition5k**: https://issai.nu.edu.kz/wp-content/themes/issai-new/data/models/Nutrition5k/yolov8n.pt
- **YOLOv8s model trained on GFSD**: https://issai.nu.edu.kz/wp-content/themes/issai-new/data/models/GFSD/yolov8s.pt
- **RT-DETR-x model trained on CAFSD**: https://issai.nu.edu.kz/wp-content/themes/issai-new/data/models/CAFSD/rtdetr-x.pt

### Download Instructions
You can download different versions of the YOLOv8 model (n, s, m, l, x) and RT-DETR-x model for each dataset by modifying this link accordingly: `https://issai.nu.edu.kz/wp-content/themes/issai-new/data/models/<DATASET>/<MODEL>`

Below are the placeholders for the model names and dataset names:
- Replace `<MODEL>` with: `yolov8n.pt`, `yolov8s.pt`, `yolov8m.pt`, `yolov8l.pt`, `yolov8x.pt`, `rtdetr-x.pt`
- Replace `<DATASET>` with: `CAFSD`, `GFSD`, `Nutrition5k`

#### Example Links
- **YOLOv8x model trained on Nutrition5k**: https://issai.nu.edu.kz/wp-content/themes/issai-new/data/models/Nutrition5k/yolov8x.pt



## Test Set Results

| Model Size   | CAFSD (mAP50) | CAFSD (mAP50-95)  | Nutrition5k (mAP50)| Nutrition5k (mAP50-95)| GFSD (mAP50)| GFSD (mAP50-95)|
|-------------------------|-------------------|--------------|---------------|--------------|---------------|------------------------|
| YOLOv8n                 | 0.57              | 0.487        | 0.775         | 0.673        | 0.615                 | 0.529         |
| YOLOv8s                 | 0.612             | 0.529        | 0.781         | 0.688        | 0.668                 | 0.584         |
| YOLOv8m                 | 0.652             | 0.576        | 0.787         | 0.711        | 0.698                 | 0.621         |
| YOLOv8l                 | 0.659             | 0.586        | **0.802**         | **0.724**        | 0.712                 | 0.635         |
| YOLOv8xl                | 0.677             | 0.601        | 0.797         | 0.717        | **0.714**                 | **0.641**         |
| RT-DETR-x               | **0.685**             |   **0.613**      |   0.768       |  0.688       |  0.711              |  0.637      |



## References
[1] Karabay, A., Varol, H. A., & Chan, M. Y. (2025). Improved food image recognition by leveraging deep learning and data-driven methods with an application to Central Asian food scene. Scientific Reports. (In press).
[2] Thames, Q., Karpur, A., Norris, W., Xia, F., Panait, L., Weyand, T., & Sim, J. (2021). Nutrition5k: Towards automatic nutritional understanding of generic food. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition* (pp. 8903–8911).





