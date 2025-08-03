from sqlalchemy import text
from sqlalchemy.orm import Session

def get_top_similar_metadata(session: Session, participant_id: str, top_k: int = 5):
    sql = text("""
        SELECT pm.*
        FROM mri_embeddings me1
        JOIN mri_embeddings me2 ON me1.id != me2.id
        JOIN participant_metadata pm ON me2.participant_id = pm.participant_id
        WHERE me1.participant_id = :pid
        ORDER BY me1.embedding <#> me2.embedding ASC
        LIMIT :k
    """)
    return session.execute(sql, {"pid": participant_id, "k": top_k}).fetchall()
