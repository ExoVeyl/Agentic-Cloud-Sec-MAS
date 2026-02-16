import chromadb
import json
import re
from chromadb.utils import embedding_functions
from tqdm import tqdm

# 1. Setup Brain Memory
client = chromadb.PersistentClient(path="./brain_memory")
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
nvd_coll = client.get_or_create_collection(name="nvd_cves", embedding_function=ef)

# 2. Load your local JSON
file_path = "brain_knowledge_dump.json"
print(f"Loading {file_path}...")

with open(file_path, 'r', encoding='utf-8') as f:
    raw_data = json.load(f)


# 3. The Custom Parser Function
def parse_brain_string(entry):
    # This regex extracts the pieces inside the [ ] brackets and the INFO text
    src = re.search(r"\[SRC:(.*?)\]", entry)
    entry_id = re.search(r"\[ID:(.*?)\]", entry)
    info = re.search(r"INFO: (.*?) \|", entry)

    return {
        "document": info.group(1) if info else entry,
        "id": entry_id.group(1) if entry_id else f"gen_{hash(entry)}",
        "metadata": {
            "source": src.group(1) if src else "Unknown",
            "full_text": entry  # Keep the whole string for Llama to read later
        }
    }


# 4. Batch Loading (Processing 100 at a time to prevent RAM crash)
batch_size = 100
print(f"Starting ingestion of {len(raw_data)} records...")

for i in tqdm(range(0, len(raw_data), batch_size)):
    batch = raw_data[i:i + batch_size]

    docs, ids, metas = [], [], []

    for item in batch:
        parsed = parse_brain_string(item)
        docs.append(parsed["document"])
        ids.append(parsed["id"])
        metas.append(parsed["metadata"])

    nvd_coll.add(documents=docs, ids=ids, metadatas=metas)

print(f"Done! Brain now holds {nvd_coll.count()} high-precision security records.")