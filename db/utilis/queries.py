import os
from sqlalchemy import text
from sqlalchemy.orm import Session

def get_top_similar_metadata(session: Session, participant_id: str, top_k: int = 5):
    sql = text("""
        SELECT 
            pm.participant_id,
            pm.age,
            pm.sex,
            pm.height,
            pm.weight,
            MIN(me2.embedding <#> me1.embedding) AS distance
        FROM mri_embeddings me1
        JOIN mri_embeddings me2 ON me1.id != me2.id
        JOIN participant_metadata pm ON me2.participant_id = pm.participant_id
        WHERE me1.participant_id = :pid
        GROUP BY pm.participant_id, pm.age, pm.sex, pm.height, pm.weight
        ORDER BY distance ASC
        LIMIT :k
    """)
    rows = session.execute(sql, {"pid": participant_id, "k": top_k}).fetchall()

    results = []
    for row in rows:
        pid = row.participant_id
        image_folder = f"data/ixi_png_dataset/{pid}/t1"
        image_filename = None

        if os.path.exists(image_folder):
            png_files = sorted([
                f for f in os.listdir(image_folder)
                if f.endswith(".png") and "_image.nii_z" in f
            ])
            if png_files:
                mid_index = len(png_files) // 2
                image_filename = png_files[mid_index]

        image_path = (
            f"/static/{pid}/t1/{image_filename}"
            if image_filename else "/static/placeholder.png"
        )

        results.append({
            "participant_id": row.participant_id,
            "age": row.age,
            "sex": row.sex,
            "height": row.height,
            "weight": row.weight,
            "distance": row.distance,
            "image_path": image_path,
        })

    return results
