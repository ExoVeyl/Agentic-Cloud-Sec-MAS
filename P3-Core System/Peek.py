#3rd Script
#Gives a peek on the .json file

import json
import random

def inspect_brain():
    with open("P2 - Implementation/brain_knowledge_dump.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"--- TOTAL ENTRIES: {len(data)} ---\n")
    
    # We want to see one sample from each source to verify the logic
    sources = ["NVD", "PROWLER", "MITRE", "CWE"]
    found = {s: False for s in sources}
    
    for entry in data:
        for s in sources:
            if f"[SRC:{s}]" in entry and not found[s]:
                print(f"=== {s} SAMPLE ===")
                print(f"{entry}\n")
                found[s] = True
        
        if all(found.values()):
            break

if __name__ == "__main__":
    inspect_brain()