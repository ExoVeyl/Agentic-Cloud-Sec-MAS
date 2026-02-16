# The first script (Expanded)
# Checks each dataset (NVD, CWE, MITRE, Prowler) to verify path accuracy,
# file permissions, and structural integrity before compilation.

import lzma
import json
import os

# --- PATHS ---
FILE_NVD = r"C:\Users\zaint\Desktop\Uni\FYP\Datasets\Brain\CVE-all.json.xz"
FILE_CWE = r"C:\Users\zaint\Desktop\Uni\FYP\Datasets\Brain\cwec_latest.xml\cwec_v4.19.xml"
FILE_MITRE = r"C:\Users\zaint\Desktop\Uni\FYP\Datasets\Brain\MITRE ATT&CK\attack-stix-data-18.1\enterprise-attack\enterprise-attack.json"
FILE_PROWLER = "prowler_rules.json"

print("--- DEBUGGING DATASETS ---")

# 1. TEST NVD KEYS (Compressed JSON)
try:
    with lzma.open(FILE_NVD, mode='rt', encoding='utf-8') as f:
        sample = f.read(1000)
        print(f"[NVD Sample Head]:\n{sample[:300]}...")
        f.seek(0)
        data = json.loads(f.read(5000) + '}') # Structural check
        print(f"[NVD Top Level Keys Found]: {list(data.keys())}")
except Exception as e:
    print(f"[!] NVD Debug Error: {e}")

# 2. TEST CWE ACCESS (XML)
if not os.path.exists(FILE_CWE):
    print(f"\n[!] CWE ERROR: File not found. Verify your XML path.")
else:
    try:
        with open(FILE_CWE, 'r', encoding='utf-8') as f:
            head = f.read(200)
            print(f"\n[CWE Sample Head]:\n{head}...")
    except Exception as e:
        print(f"\n[!] CWE Permission Error: {e}")

# 3. TEST MITRE ATT&CK (Standard JSON)
if not os.path.exists(FILE_MITRE):
    print(f"\n[!] MITRE ERROR: STIX data file not found at {FILE_MITRE}")
else:
    try:
        with open(FILE_MITRE, 'r', encoding='utf-8') as f:
            # MITRE files are large; we check the start to confirm it is valid JSON
            sample = f.read(1000)
            print(f"\n[MITRE Sample Head]:\n{sample[:300]}...")
            f.seek(0)
            data = json.load(f) # Confirming full file can be parsed
            print(f"[MITRE Top Level Keys Found]: {list(data.keys())}")
            # Specifically look for 'objects' key used in All.py
            if 'objects' in data:
                print(f"-> SUCCESS: Found {len(data['objects'])} STIX objects.")
    except Exception as e:
        print(f"\n[!] MITRE Debug Error: {e}")

# 4. TEST PROWLER (Standard JSON)
if not os.path.exists(FILE_PROWLER):
    print(f"\n[!] PROWLER ERROR: Local rules file '{FILE_PROWLER}' not found.")
else:
    try:
        with open(FILE_PROWLER, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"\n[PROWLER Status]: Loaded {len(data)} cloud checks.")
            # Check for key fields expected by the Librarian
            sample_check = data[0]
            if 'id' in sample_check and 'issue' in sample_check:
                print(f"=== PROWLER SAMPLE ===\nID: {sample_check['id']} | ISSUE: {sample_check['issue']}\n")
    except Exception as e:
        print(f"\n[!] PROWLER Debug Error: {e}")

print("--- DEBUG COMPLETE ---")
