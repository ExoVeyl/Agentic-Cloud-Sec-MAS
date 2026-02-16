import chromadb
from chromadb.utils import embedding_functions

# 1. Initialize the Local Database
# This creates a folder named 'brain_memory' inside your directory
client = chromadb.PersistentClient(path="./brain_memory")

# 2. Define the Embedding Model (The "Translator")
# We use a lightweight HuggingFace model that runs locally on your laptop
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# 3. Create Collections for each Dataset
# We separate them so the Brain can specifically look for a "CVE" or a "Mitre Technique"
mitre_coll = client.get_or_create_collection(name="mitre_attack", embedding_function=ef)
nvd_coll = client.get_or_create_collection(name="nvd_cves", embedding_function=ef)

# 4. Sample Data for Testing
mitre_data = [
    "T1562.001: Impair Defenses: Disable or Modify Tools. Adversaries may modify security tools to avoid detection.",
    "T1078: Valid Accounts. Adversaries may obtain and abuse credentials of existing accounts to gain access."
]

nvd_data = [
    "CVE-2021-44228: Log4Shell vulnerability in Apache Log4j2 allowing remote code execution.",
    "CVE-2023-32342: Buffer overflow in specific cloud network drivers."
]

# 5. Adding to the Database
print("Storing MITRE techniques...")
mitre_coll.add(
    documents=mitre_data,
    ids=["mitre_1", "mitre_2"],
    metadatas=[{"type": "technique"}, {"type": "technique"}]
)

print("Storing NVD records...")
nvd_coll.add(
    documents=nvd_data,
    ids=["cve_1", "cve_2"],
    metadatas=[{"severity": "Critical"}, {"severity": "High"}]
)

print(f"Done! Memory initialized. Current count: {mitre_coll.count()} MITRE items.")