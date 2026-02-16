#5th Script - takes the json file, uses a model to
# convert it into 384-dimensional math vectors,
# saved as brain_vectors.index (The FAISS index) and brain_metadata.json (Text map)

#Brain can be queried now via Semantic Test

import json
import time
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import os

# --- SETTINGS ---
INPUT_FILE = "P2 - Implementation/brain_knowledge_dump.json"
MODEL_NAME = "all-MiniLM-L6-v2" # Optimized for technical/security text
INDEX_FILE = "brain_vectors.index"
MAP_FILE = "brain_metadata.json"

def build_vector_db():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found!")
        return

    print("--- STEP 2: VECTOR EMBEDDING PHASE ---")
    
    # 1. Load the data
    print(f"[1/4] Loading {INPUT_FILE}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        kb_data = json.load(f)

    # 2. Load the Embedding Model
    print(f"[2/4] Initializing AI Model ({MODEL_NAME})...")
    # This model turns text into 384-dimensional math vectors
    model = SentenceTransformer(MODEL_NAME)

    # 3. Generate Embeddings
    print(f"[3/4] Encoding {len(kb_data)} items. This uses heavy CPU/RAM...")
    start_time = time.time()
    
    # Batch size 128 is efficient for your 16GB/32GB RAM laptop
    embeddings = model.encode(kb_data, batch_size=128, show_progress_bar=True)

    # 4. Create FAISS Index
    print("[4/4] Creating FAISS Index and saving files...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    
    # Save the index (The Math)
    faiss.write_index(index, INDEX_FILE)
    
    # Save the metadata (The Text)
    with open(MAP_FILE, "w", encoding="utf-8") as f:
        json.dump(kb_data, f)

    elapsed = (time.time() - start_time) / 60
    print(f"\n[SUCCESS] Vector Database built in {elapsed:.2f} minutes.")
    print(f"Files created: {INDEX_FILE} (Vectors), {MAP_FILE} (Text)")

if __name__ == "__main__":
    build_vector_db()