import os, shutil, random

SOURCE = "plantvillage dataset/color"
TRAIN  = "Dataset/train"
VALID  = "Dataset/valid"
SPLIT  = 0.2

random.seed(42)

for cls in os.listdir(SOURCE):
    cls_path = f"{SOURCE}/{cls}"
    if not os.path.isdir(cls_path):
        continue
    imgs = os.listdir(cls_path)
    random.shuffle(imgs)
    split_idx = int(len(imgs) * SPLIT)
    for phase, subset in [("valid", imgs[:split_idx]), ("train", imgs[split_idx:])]:
        os.makedirs(f"Dataset/{phase}/{cls}", exist_ok=True)
        for img in subset:
            shutil.copy(f"{cls_path}/{img}", f"Dataset/{phase}/{cls}/{img}")
    print(f"Done: {cls}")

print("Split complete!")