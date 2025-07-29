# scripts/database_builder.py
import os
import pandas as pd
import numpy as np
import chromadb
from chromadb.utils.embedding_functions import NumPyEmbeddingFunction

# Load your metadata CSV
metadata_path = "data/metadata.csv"
embedding_dir = "embeddings/"
collection_name = "brain_mri_embeddings"

# Load metadata
df = pd.read_csv(metadata_path)

# Connect to ChromaDB
client = chromadb.Client()
if collection_name in [c.name for c in client.list_collections()]:
    client.delete_collection(collection_name)
collection = client.create_collection(collection_name, embedding_function=NumPyEmbeddingFunction())

# Load embeddings and register with ChromaDB
for row in df.itertuples():
    patient_id = row.PatientID  # adjust column name if different
    scan_type = "t1"  # or infer from filename or CSV

    emb_path = os.path.join(embedding_dir, f"{patient_id}_{scan_type}.npy")
    if os.path.exists(emb_path):
        emb = np.load(emb_path)
        metadata = {
            "age": row.Age,
            "sex": row.Sex,
            "site": row.Site
        }
        collection.add(
            embeddings=[emb.tolist()],
            metadatas=[metadata],
            ids=[f"{patient_id}_{scan_type}"]
        )
        print(f"Added {patient_id}_{scan_type} to DB.")
    else:
        print(f"Missing embedding for {patient_id}_{scan_type}")

print("✅ ChromaDB built successfully.")
