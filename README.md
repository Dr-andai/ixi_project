# 🧠 MRI Participant Similarity Search

This is a FastAPI-powered web application that allows users to search for similar MRI participants based on metadata embeddings. It leverages a PostgreSQL database with pgvector to store and compare metadata embeddings efficiently.

## 🚀 Features

- Search for similar participants using a `participant_id`.
- Display top similar participants in a clean web interface.
- Example participant IDs provided for quick access.
- MRI similarity calculated using vector embeddings stored in PostgreSQL.
- User interface powered by HTMX and FastAPI templates.
- Static image display served from local PNG MRI dataset (`ixi_png_dataset`).

# To run
pip install -r requirements.txt

Make sure your PostgreSQL database is running and the environment variables are configured correctly.

   ```bash
   uvicorn main:app --reload