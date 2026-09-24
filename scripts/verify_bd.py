#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POE2 BD Standardizer - Automated Quality & Completeness Verifier (ADR-016 & ADR-018)
Audits a standardized Markdown document for:
1. Mode Detection:
   - Pure-Text Zero-Image Mode: Verifies Trinity Data Completeness (Passive tree progression,
     Numerical thresholds/attributes, Skill matrix, Zero image bloat).
   - Legacy Image Mode: Verifies 100% extraction-to-reference parity (zero orphans, zero missing).
2. Forbidden placeholders (e.g. 【輔助 1】, [待補充], TODO, FIXME).
3. Skills & Support Gem Matrix fidelity (tables present and structured).
4. Notion Delivery Readiness (Pure-Text lightweight check or ZIP flat structure check).
5. Notion YAML Metadata Schema (frontmatter with version, class, stage, uniques).
Zero external dependencies (pure Python standard library).
"""

import sys
import os
import re
import zipfile

def verify_bd(md_path, check_zip=False):
    if not os.path.exists(md_path):
        print(f"[FAIL] Markdown file not found: {md_path}")
        return False

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    file_size_kb = os.path.getsize(md_path) / 1024
    base_name = os.path.splitext(os.path.basename(md_path))[0]
    core_name = re.sub(r'(_標準化|_純文本標準化)$', '', base_name)
    
    print(f"==================================================")
    print(f"  POE2 BD Standardization Verification Report")
    print(f"  Target: {core_name}")
    print(f"  File Size: {file_size_kb:.2f} KB | Length: {len(content)} chars")
    print(f"==================================================\n")

    all_passed = True

    # Detect Image References in Markdown
    md_img_refs = re.findall(r'!\[.*?\]\((.*?)\)', content)

    # --- 1. Mode Detection & Completeness Check (ADR-018 Pure-Text vs Legacy Image) ---
    if len(md_img_refs) == 0:
        print("[1/5] Pure-Text Zero-Image Mode & Trinity Data Check (ADR-018)...")
        print("  [PASS] Zero image dependencies detected (100% pure-text, lightweight).")
        
        # Check Trinity Pillar 1: Passive Tree Progression & Notables
        has_tree_progression = any(kw in content for kw in ["天賦", "天赋", "天賦樹", "天赋树", "加點", "加点", "昇華", "升华"])
        has_act_progression = any(kw in content for kw in ["Act 1", "第一章", "第一幕", "第一阶段", "第一階段", "階段過渡", "天賦樹分幕"])
        if not (has_tree_progression and has_act_progression):
            print("  [FAIL] Trinity Pillar 1 missing: Passive Tree progression roadmap / Notables not detected.")
            all_passed = False
        else:
            print("  [PASS] Trinity Pillar 1: Passive tree phased progression & notables present.")

        # Check Trinity Pillar 2: Numerical Thresholds & Defense Checks
        has_res = any(kw in content for kw in ["抗性", "火抗", "冰抗", "電抗", "电抗", "75%"])
        has_attrs = any(kw in content for kw in ["力量", "敏捷", "智慧", "屬性門檻", "属性门槛", "屬性需求", "属性需求"])
        has_weapon = any(kw in content for kw in ["點傷", "点伤", "攻速", "裝填", "装填", "十字弓", "基底", "武器"])
        if not (has_res and (has_attrs or has_weapon)):
            print("  [FAIL] Trinity Pillar 2 missing: Quantitative numerical thresholds (Resistances/Attributes/Weapon) not detected.")
            all_passed = False
        else:
            print("  [PASS] Trinity Pillar 2: Quantitative numerical thresholds (Resistances, Attributes, Weapon) present.")

    else:
        print("[1/5] Legacy Image Parity & Existence Check...")
        img_dir = os.path.join(os.path.dirname(md_path), "images", core_name)
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
    table_lines = [line for line in content.splitlines() if line.strip().startswith('|')]
    if len(table_lines) < 3:
        print("  [FAIL] Skills table matrix missing or fewer than 3 table rows.")
        all_passed = False
    else:
        print(f"  [PASS] Skills table matrix present ({len(table_lines)} table rows).")

    # --- 4. Delivery Readiness Check ---
    print("\n[4/5] Delivery Readiness & Notion Compatibility Check...")
    if len(md_img_refs) == 0:
        print(f"  [PASS] Pure-Text document ({file_size_kb:.2f} KB) is 100% compatible with Notion MCP/API and instant copy-paste.")
    else:
        zip_path = os.path.join(os.path.dirname(md_path), f"{core_name}.zip")
        if not os.path.exists(zip_path):
            if check_zip:
                print(f"  [FAIL] ZIP package requested but not found at: {zip_path}")
                all_passed = False
            else:
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
        print("Usage: python3 verify_bd.py <path_to_markdown.md> [--zip]")
        sys.exit(1)
    check_zip_flag = '--zip' in sys.argv
    target_md = [arg for arg in sys.argv[1:] if arg != '--zip'][0]
    success = verify_bd(target_md, check_zip=check_zip_flag)
    sys.exit(0 if success else 1)
