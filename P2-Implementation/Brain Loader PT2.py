import chromadb
import json
import re
from chromadb.utils import embedding_functions
from tqdm import tqdm

# 1. Setup Brain Memory
client = chromadb.PersistentClient(path="./brain_memory")
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
nvd_coll = client.get_or_create_collection(name="nvd_cves", embedding_function=ef)

# 2. Load the JSON
file_path = "brain_knowledge_dump.json"
with open(file_path, 'r', encoding='utf-8') as f:
    raw_data = json.load(f)


def parse_brain_string(entry):
    src = re.search(r"\[SRC:(.*?)\]", entry)
    entry_id = re.search(r"\[ID:(.*?)\]", entry)
    info = re.search(r"INFO: (.*?) \|", entry)

    # We add a unique suffix to the ID to ensure duplicates don't crash us
    base_id = entry_id.group(1) if entry_id else "gen_id"
    # Adding a hash of the content makes even same-named IDs unique if content differs
    unique_id = f"{base_id}_{hash(entry) % 10 ** 8}"

    return {
        "document": info.group(1) if info else entry,
        "id": unique_id,
        "metadata": {"source": src.group(1) if src else "Unknown"}
    }


# 3. Resume with 'upsert' instead of 'add'
# 'upsert' means "Update if exists, insert if new" - this prevents the crash!
batch_size = 100
print(f"Resuming ingestion. Current count in DB: {nvd_coll.count()}")

for i in tqdm(range(0, len(raw_data), batch_size)):
    batch = raw_data[i:i + batch_size]
    docs, ids, metas = [], [], []

    for item in batch:
        parsed = parse_brain_string(item)
        docs.append(parsed["document"])
        ids.append(parsed["id"])
        metas.append(parsed["metadata"])

    # We use UPSERT here to avoid DuplicateIDError
    nvd_coll.upsert(documents=docs, ids=ids, metadatas=metas)

print(f"Final Count: {nvd_coll.count()}")