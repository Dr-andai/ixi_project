import os
import json
import numpy as np
import pandas as pd

emb_dir = "../embeddings/embeddings_output"
rows = []

for file in os.listdir(emb_dir):
    if file.endswith(".npy"):
        participant_id, scan_type = file.replace(".npy", "").split("_")
        emb = np.load(os.path.join(emb_dir, file))
        rows.append({
            "participant_id": participant_id,
            "scan_type": scan_type,
            "embedding": json.dumps(emb.tolist())
        })

df = pd.DataFrame(rows)

embeddings_path = "../data/emeddings_data/embeddings_data.csv"
df.to_csv(embeddings_path, index=False)
