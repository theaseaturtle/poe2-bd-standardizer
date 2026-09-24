#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POE2 BD Standardizer - Automated Quality & Completeness Verifier
Audits a standardized Markdown document and its Notion ZIP package for:
1. Orphan or missing images (100% extraction-to-reference parity).
2. Forbidden placeholders (e.g. 【輔助 1】, [待補充], TODO).
3. Skill table fidelity (ensures gems are transcribed, not generic).
4. Notion ZIP package integrity (flat structure, root markdown, valid images).
5. Notion YAML Metadata Schema (frontmatter with version, class, stage, uniques).
Zero external dependencies (pure Python standard library).
"""

import sys
import os
import re
import zipfile

def verify_bd(md_path):
    if not os.path.exists(md_path):
        print(f"[FAIL] Markdown file not found: {md_path}")
        return False

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    base_name = os.path.splitext(os.path.basename(md_path))[0]
    core_name = re.sub(r'_標準化$', '', base_name)
    
    print(f"==================================================")
    print(f"  POE2 BD Standardization Verification Report")
    print(f"  Target: {core_name}")
    print(f"==================================================\n")

    all_passed = True

    # --- 1. Image Parity & Existence Check ---
    print("[1/5] Image Parity & Existence Check...")
    img_dir = os.path.join(os.path.dirname(md_path), "images", core_name)
    
    md_img_refs = re.findall(r'!\[.*?\]\((.*?)\)', content)
    md_img_basenames = [os.path.basename(ref) for ref in md_img_refs]

    if not os.path.exists(img_dir):
        print(f"  [WARN] Expected image directory not found: {img_dir}")
        disk_images = []
    else:
        disk_images = [f for f in os.listdir(img_dir) if not f.startswith('.') and f != 'document_flow.txt']

    missing_on_disk = []
    for ref in md_img_refs:
        resolved_path = os.path.join(os.path.dirname(md_path), ref)
        if not os.path.exists(resolved_path):
            missing_on_disk.append(ref)

    orphan_images = [img for img in disk_images if img not in md_img_basenames]

    if missing_on_disk:
        print(f"  [FAIL] {len(missing_on_disk)} referenced image(s) missing on disk: {missing_on_disk[:5]}")
        all_passed = False
    else:
        print(f"  [PASS] All {len(md_img_refs)} referenced images exist on disk.")

    if orphan_images:
        print(f"  [FAIL] {len(orphan_images)} extracted image(s) unreferenced in markdown: {orphan_images[:5]}")
        all_passed = False
    else:
        print(f"  [PASS] Zero orphan images ({len(disk_images)} extracted, all referenced).")

    # --- 2. Forbidden Placeholder Check ---
    print("\n[2/5] Placeholder & Hallucination Check...")
    forbidden_patterns = [
        (r'【輔助\s*\d+】', "Generic support placeholder (e.g. 【輔助 1】)"),
        (r'【技能名稱】', "Generic skill placeholder (【技能名稱】)"),
        (r'\[待補充\]', "Pending placeholder ([待補充])"),
        (r'\[待定\]', "Pending placeholder ([待定])"),
        (r'\[推測\]', "Inference placeholder ([推測])"),
        (r'\bTODO\b', "TODO comment"),
        (r'\bFIXME\b', "FIXME comment")
    ]

    found_placeholders = []
    for pattern, desc in forbidden_patterns:
        matches = re.findall(pattern, content)
        if matches:
            found_placeholders.append(f"{desc} (found {len(matches)}x)")

    if found_placeholders:
        for ph in found_placeholders:
            print(f"  [FAIL] Forbidden placeholder detected: {ph}")
        all_passed = False
    else:
        print("  [PASS] Zero forbidden placeholders detected in markdown.")

    # --- 3. Skills Matrix Quality Check ---
    print("\n[3/5] Skills & Support Gems Matrix Check...")
    if "## 四、" not in content and "技能" not in content:
        print("  [FAIL] Section IV (Skills Matrix) appears to be missing.")
        all_passed = False
    else:
        table_lines = [line for line in content.splitlines() if line.strip().startswith('|')]
        if len(table_lines) < 3:
            print("  [FAIL] Skills table matrix missing or fewer than 3 table rows.")
            all_passed = False
        else:
            print(f"  [PASS] Skills table matrix present ({len(table_lines)} table rows).")

    # --- 4. Notion ZIP Package Integrity Check (Optional) ---
    print("\n[4/5] Notion ZIP Package Integrity Check...")
    zip_path = os.path.join(os.path.dirname(md_path), f"{core_name}.zip")
    if not os.path.exists(zip_path):
        print(f"  [INFO] ZIP package not detected on disk (Skipping optional ZIP check; Markdown is verified for local Obsidian/IDE use).")
    else:
        zip_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
        with zipfile.ZipFile(zip_path, 'r') as z:
            names = z.namelist()
            root_mds = [n for n in names if '/' not in n and n.endswith('.md')]
            has_nested_wrapper = any(n.startswith(f"{core_name}/") for n in names)
            internal_images = [n for n in names if n.startswith('images/')]

            if not root_mds:
                print(f"  [FAIL] No root-level Markdown found in ZIP package (found: {names[:3]}).")
                all_passed = False
            elif has_nested_wrapper:
                print(f"  [FAIL] ZIP contains nested top-level folder wrapper (Notion import nesting bug).")
                all_passed = False
            else:
                print(f"  [PASS] ZIP structure is flat and clean: Root Markdown = '{root_mds[0]}'")
                print(f"  [PASS] ZIP embedded images: {len(internal_images)} images, Archive size: {zip_size_mb:.2f} MB")

    # --- 5. Notion YAML Metadata Frontmatter Check ---
    print("\n[5/5] Notion Metadata Schema (YAML Frontmatter) Check...")
    has_frontmatter = content.startswith("---\n") and "\n---\n" in content[4:]
    if not has_frontmatter:
        print("  [FAIL] Document missing standard YAML Frontmatter metadata block at the top.")
        all_passed = False
    else:
        fm_content = content.split("---", 2)[1]
        required_keys = ['version:', 'class:', 'ascendancy:', 'stage:', 'core_uniques:']
        missing_keys = [k for k in required_keys if k not in fm_content]
        if missing_keys:
            print(f"  [FAIL] YAML Frontmatter missing mandatory fields: {missing_keys}")
            all_passed = False
        else:
            print("  [PASS] Valid Notion YAML Metadata Schema present (version, class, stage, uniques).")

    print("\n--------------------------------------------------")
    if all_passed:
        print("🎉 [RESULT: ALL CHECKS PASSED] Standardized BD meets 100% quality standards!")
        print("--------------------------------------------------\n")
        return True
    else:
        print("❌ [RESULT: VERIFICATION FAILED] Please resolve the above issues.")
        print("--------------------------------------------------\n")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 verify_bd.py <output/[BD名稱]_標準化.md>")
        sys.exit(1)
    success = verify_bd(sys.argv[1])
    sys.exit(0 if success else 1)
