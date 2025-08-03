import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pandas as pd
import numpy as np

from sqlalchemy.orm import Session
from db.utilis.config import SessionLocal, engine
from db.utilis.models import Base, ParticipantMetadata
from db.utilis.logger import setup_logging

logger = setup_logging()

participant_metadata = "../../data/metadata/participant_metadata.csv"

participant_metadata_df = pd.read_csv(participant_metadata)


# --- Insert into DB ---
with Session(engine) as session:
    for _, row in participant_metadata_df.iterrows():
        try:
            participant_metadata = ParticipantMetadata(
                participant_id=row["participant_id"],
                age =row["age"],
                sex =row["sex"],
                height =row["height"],
                weight =row["weight"],
                site_name=row["site_name"]
            )
            session.add(participant_metadata)
        except Exception as e:
            logger.error(f"Error processing {row['participant_id']}: {e}")

    try:
        session.commit()
        logger.info("✅ All Participants committed successfully.")
    except Exception as e:
        session.rollback()
        logger.error("❌ Commit failed: %s", e)