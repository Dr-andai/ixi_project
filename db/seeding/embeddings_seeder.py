import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pandas as pd
import numpy as np
import json
from sqlalchemy.orm import Session
from db.utilis.config import SessionLocal, engine
from db.utilis.models import Base, MRIEmbedding, ParticipantMetadata
from db.utilis.logger import setup_logging

logger = setup_logging()

embeddings_data = "../../data/emeddings_data/embeddings_data.csv"

embeddings_df = pd.read_csv(embeddings_data)
# Reduce 28160-dim embedding to 512-dim by averaging across slices
embeddings_df["embedding"] = embeddings_df["embedding"].apply(
    lambda x: np.mean(np.array(json.loads(x)).reshape(-1, 512), axis=0).tolist()
)

# --- Insert into DB ---
with Session(engine) as session:
    for _, row in embeddings_df.iterrows():
        participant_id = row["participant_id"]

        # Check if participant exists in participant_metadata
        exists = session.query(ParticipantMetadata).filter_by(participant_id=participant_id).first()
        if not exists:
            logger.warning(f"⚠️ Skipping embedding for unknown participant_id: {participant_id}")
            continue

        try:
            emb = MRIEmbedding(
                participant_id=participant_id,
                scan_type=row["scan_type"],
                embedding=row["embedding"]
            )
            session.add(emb)
        except Exception as e:
            logger.error(f"❌ Error processing {participant_id} - {row['scan_type']}: {e}")

    try:
        session.commit()
        logger.info("✅ All valid embeddings committed successfully.")
    except Exception as e:
        session.rollback()
        logger.error("❌ Commit failed: %s", e)