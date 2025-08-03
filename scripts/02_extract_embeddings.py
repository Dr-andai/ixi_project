"""
1. load resnet model
- remove the last layer, classifier

2. transform
- resize
- to tensor
- normalize

3. load grayscale PNG as RGB
- convert img to RGB

4. get embedding from one image
- create image embedding

5. loop over png folder
6. save 
7. run script file

"""

from torchvision import models, transforms
import torch.nn as nn
import torch
from PIL import Image
import os
import numpy as np
from tqdm import tqdm

# 1. Load ResNet
resnet = models.resnet18(pretrained=True)
embedding_model = nn.Sequential(*list(resnet.children())[:-1])
embedding_model.eval()

# 2. Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# 3. Load grayscale PNG as RGB
def load_grayscale_as_rgb(path):
    img = Image.open(path).convert("L")
    img = img.convert("RGB")
    return img

# 4. Get embedding from one image
def get_image_embedding(image_path):
    img = load_grayscale_as_rgb(image_path)
    img_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        embedding = embedding_model(img_tensor)
    return embedding.squeeze().numpy()

# 5. Loop over PNG folder
def embed_folder(folder_path):
    results = []
    for file in tqdm(sorted(os.listdir(folder_path))):
        if file.endswith(".png"):
            path = os.path.join(folder_path, file)
            emb = get_image_embedding(path)
            results.append((file, emb))
    return results

# 6. save
def save_embeddings(embeddings, save_path):
    # Unpack: embeddings = [(filename, emb), ...]
    filenames, vectors = zip(*embeddings)
    np.save(save_path, np.array(vectors))  # Save only the vectors

# 7. Main script
if __name__ == "__main__":
    base_folder = "data/ixi_png_dataset"
    output_base = "embeddings/embeddings_output"
    modalities = ["t1", "t2"]

    for patient_id in tqdm(sorted(os.listdir(base_folder)), desc="Patients"):
        patient_folder = os.path.join(base_folder, patient_id)
        
        if not os.path.isdir(patient_folder):
            continue

        for modality in modalities:
            modality_path = os.path.join(patient_folder, modality)
            if not os.path.exists(modality_path):
                continue
            
            embeddings = embed_folder(modality_path)
            
            # Save path
            save_path = os.path.join(output_base, f"{patient_id}_{modality}.npy")
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            save_embeddings(embeddings, save_path)