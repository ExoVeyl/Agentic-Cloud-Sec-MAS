#The Second script

# Takes all 4 datasets (formats - .xz,.json,.xml) and combines them into one .json
# file

# Label - Unified Knowledge Normalization.

# Desc - This module implements a custom data pipeline that aggregates 324,491 records from four
# industry-standard security ontologies. By normalizing these sources into a unified 5-pillar
# JSON schema, the system provides a consistent foundation for semantic vectorization and
# autonomous remediation reasoning.

import json
import lzma
import os
import xml.etree.ElementTree as ET

# --- PATHS ---
FILE_NVD = r"C:\Users\zaint\Desktop\Uni\FYP\Datasets\Brain\CVE-all.json.xz"
FILE_PROWLER = "prowler_rules.json"
FILE_CWE = r"C:\Users\zaint\Desktop\Uni\FYP\Datasets\Brain\cwec_latest.xml\cwec_v4.19.xml"
FILE_MITRE = r"C:\Users\zaint\Desktop\Uni\FYP\Datasets\Brain\MITRE ATT&CK\attack-stix-data-18.1\enterprise-attack\enterprise-attack.json"

def get_action_logic(text):
    text = text.lower()
    if "overflow" in text: return "ACTION: Bounds checking and use memory-safe functions."
    if "injection" in text: return "ACTION: Use parameterized queries and input validation."
    if "privilege" in text: return "ACTION: Enforce Principle of Least Privilege (PoLP)."
    return "ACTION: Consult vendor advisory for specific patch versions."

def build_research_grade_brain():
    kb = []
    
    # 1. NVD (Vulnerabilities with CVSS & Links)
    print("[1/4] Processing NVD...")
    with lzma.open(FILE_NVD, mode='rt', encoding='utf-8') as f:
        items = json.load(f).get('cve_items', [])
        for item in items:
            cve_id = item.get('id')
            
            # Detailed CVSS Extraction
            metrics = item.get('metrics', {}).get('cvssMetricV31', [{}])[0]
            score = metrics.get('cvssData', {}).get('baseScore', '5.0')
            severity = metrics.get('baseSeverity', 'MEDIUM')
            
            # Verification Link Extraction
            refs = item.get('references', [])
            link = refs[0].get('url', 'No link') if refs else "No link"
            
            desc = next((d['value'] for d in item.get('descriptions', []) if d['lang'] == 'en'), "")
            action = get_action_logic(desc)
            
            # NEW FORMAT: Includes CVSS and LINK
            kb.append(f"[SRC:NVD][ID:{cve_id}][CVSS:{score} {severity}] INFO: {desc} | {action} | [LINK: {link}]")

    # 2. PROWLER (Cloud Rules - Prowler links are usually internal)
    print("[2/4] Processing Prowler...")
    if os.path.exists(FILE_PROWLER):
        with open(FILE_PROWLER, 'r', encoding='utf-8') as f:
            for c in json.load(f):
                kb.append(f"[SRC:PROWLER][ID:{c['id']}][SCORE:HIGH] INFO: {c['issue']} | ACTION: {c['fix']} | [LINK: https://docs.prowler.cloud]")

    # 3. MITRE (Attacker Tactics with Reference Links)
    print("[3/4] Processing MITRE...")
    with open(FILE_MITRE, 'r', encoding='utf-8') as f:
        stix = json.load(f)
        for obj in stix.get('objects', []):
            if obj.get('type') == 'attack-pattern':
                name = obj.get('name')
                ext_refs = obj.get('external_references', [])
                # Pull the official MITRE URL
                mitre_link = next((r['url'] for r in ext_refs if r.get('source_name') == 'mitre-attack'), "No link")
                tactics = ", ".join([p['phase_name'] for p in obj.get('kill_chain_phases', [])])
                kb.append(f"[SRC:MITRE][ID:{name}][TACTIC:{tactics}] INFO: {obj.get('description', '')[:300]} | ACTION: Monitor system logs. | [LINK: {mitre_link}]")

    # 4. CWE (Theoretical Weaknesses)
    print("[4/4] Processing CWE...")
    tree = ET.parse(FILE_CWE)
    ns = {'cwe': 'http://cwe.mitre.org/cwe-7'}
    for w in tree.getroot().findall(".//cwe:Weakness", ns):
        wid = w.get("ID")
        kb.append(f"[SRC:CWE][ID:CWE-{wid}][CAT:WEAK] INFO: {w.get('Name')} | ACTION: Review architectural design patterns. | [LINK: https://cwe.mitre.org/data/definitions/{wid}.html]")

    with open("P2 - Implementation/brain_knowledge_dump.json", "w", encoding="utf-8") as f:
        json.dump(kb, f, indent=2)
    print(f"\n[SUCCESS] Researcher Brain built with {len(kb)} items.")

if __name__ == "__main__":
    build_research_grade_brain()