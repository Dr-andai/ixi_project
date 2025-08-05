import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Directories
input_base = "data/ixi_dataset"
output_base = "data/ixi_png_dataset"
rotation_angle = 90

# List of patients
patient_ids = [d for d in os.listdir(input_base) if os.path.isdir(os.path.join(input_base, d))]

for patient_id in tqdm(patient_ids, desc="Processing patients"):
    patient_dir = os.path.join(input_base, patient_id)

    for modality in ['t1', 't2']:
        modality_dir = os.path.join(patient_dir, modality)
        if not os.path.exists(modality_dir):
            continue

        for file in os.listdir(modality_dir):
            if not file.endswith(('.nii', '.nii.gz')):
                continue

            nii_path = os.path.join(modality_dir, file)

            try:
                img = nib.load(nii_path)
                img_data = img.get_fdata()
            except Exception as e:
                print(f"[{patient_id}] Failed to load {modality}/{file}: {e}")
                continue

            output_dir = os.path.join(output_base, patient_id, modality)
            os.makedirs(output_dir, exist_ok=True)

            # Progress bar for slices
            for i in tqdm(range(img_data.shape[2]), desc=f"{patient_id}-{modality}", leave=False):
                slice_data = img_data[:, :, i] 
                #slice_data = np.rot90(img_data[:, :, i], k=rotation_angle // 90)
                img_name = f"{os.path.splitext(file)[0]}_z{str(i).zfill(3)}.png"
                output_path = os.path.join(output_dir, img_name)
                plt.imsave(output_path, slice_data, cmap='gray')

