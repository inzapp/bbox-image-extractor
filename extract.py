import os
import cv2

from glob import glob

save_path = 'classes'


if not (os.path.exists(save_path) and os.path.isdir(save_path)):
    os.makedirs(save_path, exist_ok=True)

for path in glob('*.jpg'):
    label_path = f'{path[:-4]}.txt'
    if not (os.path.exists(label_path) and os.path.isfile(label_path)):
        print(f'label not exist : {label_path}')
        continue

    img = cv2.imread(path, cv2.IMREAD_COLOR)
    raw_height, raw_width = img.shape[0], img.shape[1]
    with open(label_path, 'rt') as f:
        lines = f.readlines()

    inc = 0
    for line in lines:
        class_index, cx, cy, w, h = list(map(float, line.split(' ')))
        class_index = int(class_index)

        x1 = cx - w / 2.0
        y1 = cy - h / 2.0
        x2 = cx + w / 2.0
        y2 = cy + h / 2.0

        x1 = int(x1 * raw_width)
        x2 = int(x2 * raw_width)
        y1 = int(y1 * raw_height)
        y2 = int(y2 * raw_height)

        sub = img[y1:y2, x1:x2]
        class_path = f'{save_path}/{class_index}'
        if not (os.path.exists(class_path) and os.path.isdir(class_path)):
            os.makedirs(class_path, exist_ok=True)

        cv2.imwrite(f'{class_path}/{path[:-4]}_{inc}.jpg', sub)
        inc += 1

