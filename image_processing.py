import cv2
import os
import numpy as np

input_folder = "cleaned_batch/SAFE"
output_folder = "processed/SAFE" 

os.makedirs(output_folder, exist_ok=True)

for img_name in os.listdir(input_folder):

    img_path = os.path.join(input_folder, img_name)
    img = cv2.imread(img_path)

    if img is None:
        continue

    # Resize
    img = cv2.resize(img, (224, 224))

    # Mild brightness
    img = cv2.convertScaleAbs(img, alpha=1.02, beta=2)

    # light sharpening
    kernel = np.array([[0,-1,0],
                       [-1,5,-1],
                       [0,-1,0]])
    img = cv2.filter2D(img, -1, kernel)

    # Save OUTSIDE folder
    save_path = os.path.join(output_folder, img_name)
    cv2.imwrite(save_path, img)

    print(f"{img_name} processed")