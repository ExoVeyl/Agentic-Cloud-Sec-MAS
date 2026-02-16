# Phase 1: Data Cleaning & Pre-Flight

## 🎯 Objective
This module serves as the initial "Sanity Check" for the raw security datasets. It prevents the pipeline from processing corrupted or improperly formatted JSON/CSV files, ensuring the integrity of the downstream AI reasoning.

## 📄 Key Scripts
- `Debug.py`: 
  - Validates file paths for NVD, MITRE, CWE, and Prowler datasets.
  - Checks structural integrity (e.g., verifying JSON keys exist and fields are not null).
  - Prevents "Garbage-In, Garbage-Out" by failing the build if mandatory pillars are missing.

## 🛠️ Logic Flow
1. Path Verification: Confirms that local data directories are accessible.
2. Schema Validation: Scans a 10% sample of the raw data to ensure the structure matches expectations.
3. Pre-flight Log: Generates a success/fail report for the system architect.

## 📤 Output
- Verified Raw Data pointers for Phase 2.
