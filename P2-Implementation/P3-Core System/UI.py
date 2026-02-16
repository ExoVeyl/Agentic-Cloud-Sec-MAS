import chromadb
import ollama
import re
import datetime
from chromadb.utils import embedding_functions

# 1. Setup the Brain Connection
client = chromadb.PersistentClient(path="./brain_memory")
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
nvd_coll = client.get_collection(name="nvd_cves", embedding_function=ef)

# 2. Setup Log File (Named with today's date)
log_filename = f"Agent_Audit_Log_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"

print("\n" + "=" * 50)
print("🛡️  AGENTIC CLOUD SECURITY BRAIN ACTIVE")
print(f"🧠 Knowledge Base: {nvd_coll.count()} Records")
print(f"📝 Logging to: {log_filename}")
print("=" * 50)

while True:
    user_query = input("\n[QUESTION]: ")

    if user_query.lower() in ['exit', 'quit', 'stop']:
        print("Finalizing logs and shutting down. Goodbye!")
        break

    if not user_query.strip():
        continue

    # 3. Smart Retrieval (ID Lookup + Semantic Search)
    print("Searching the knowledge map...")
    cve_match = re.search(r'CVE-\d{4}-\d+', user_query.upper())

    retrieved_info = ""
    distance = 0.0

    if cve_match:
        specific_id = cve_match.group()
        id_results = nvd_coll.get(ids=[specific_id])
        if id_results['documents']:
            retrieved_info = id_results['documents'][-1]
            distance = 0.05
            print(f"Direct ID Match Found for {specific_id}!")

    if not retrieved_info:
        results = nvd_coll.query(query_texts=[user_query], n_results=5)
        retrieved_info = "\n---\n".join(results['documents'][0])
        distance = results['distances'][0][0]

    # 4. AI Reasoning Phase
    print(f"Analyzing match (Distance: {distance:.4f})...")
    response = ollama.chat(model='llama3.2:3b-instruct-q8_0', messages=[
        {'role': 'system',
         'content': 'You are a Cloud Security Analyst. Use the provided database record to answer professionally.'},
        {'role': 'user', 'content': f"DATABASE RECORD: {retrieved_info}\n\nUSER QUERY: {user_query}"},
    ])

    ai_answer = response['message']['content']

    # 5. WRITE TO LOG FILE
    with open(log_filename, "a", encoding="utf-8") as log:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log.write(f"\n[{timestamp}] USER: {user_query}\n")
        log.write(f"[{timestamp}] DATA QUALITY (Distance): {distance:.4f}\n")
        log.write(f"[{timestamp}] AGENT RESPONSE:\n{ai_answer}\n")
        log.write("=" * 60 + "\n")

    # 6. Display to Screen
    print("\n" + "-" * 30)
    print(f"🤖 AGENT ANALYSIS:")
    print(ai_answer)
    print("-" * 30)