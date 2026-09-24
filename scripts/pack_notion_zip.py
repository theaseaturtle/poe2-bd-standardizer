#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POE2 BD Standardizer - Clean Notion & Markdown Packager (ADR-011 & ADR-014)
Bundles a standardized Markdown file and its local image assets into a 
clean, self-contained .zip archive ready for 1-click import into Notion, Obsidian, etc.
Naming: [版本]_[職業]_[機制]_[BD名稱].zip (Zero '_Notion導入包' suffix).
Pure Python standard library (zero external dependencies).
"""

import sys
import os
import re
import zipfile

def pack_notion_zip(md_path, zip_output_path=None):
    if not os.path.exists(md_path):
        print(f"Error: Markdown file not found: {md_path}")
        sys.exit(1)

    md_dir = os.path.dirname(os.path.abspath(md_path))
    raw_base_name = os.path.splitext(os.path.basename(md_path))[0]

    # Clean title by stripping trailing '_標準化' or '_Notion導入包'
    clean_title = re.sub(r'(_標準化|_Notion導入包)+$', '', raw_base_name)

    if zip_output_path is None:
        zip_output_path = os.path.join(md_dir, f"{clean_title}.zip")

    # Read markdown to detect all local referenced images
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find image paths: ![alt](path)
    img_matches = re.findall(r'!\[.*?\]\((.*?)\)', content)
    referenced_images = set()

    for path in img_matches:
        if path.startswith(('http://', 'https://')):
            continue
        # Strip anchors or query strings if any
        clean_path = path.split('#')[0].split('?')[0]
        full_path = os.path.normpath(os.path.join(md_dir, clean_path))
        if os.path.exists(full_path):
            referenced_images.add((full_path, clean_path))
        else:
            print(f"[Warning] Image not found on disk: {clean_path} -> {full_path}")

    # Create zip archive
    with zipfile.ZipFile(zip_output_path, 'w', zipfile.ZIP_DEFLATED) as z:
        # 1. Add markdown file with clean title at root of zip
        arc_md_name = f"{clean_title}.md"
        z.write(md_path, arc_md_name)

        # 2. Add all referenced images maintaining their relative folder paths
        for full_p, rel_p in sorted(referenced_images, key=lambda x: x[1]):
            z.write(full_p, rel_p)

    print(f"Successfully packaged Clean Notion import bundle:")
    print(f"  Archive: {zip_output_path}")
    print(f"  Root Document: {arc_md_name}")
    print(f"  Embedded Images: {len(referenced_images)} files")
    return zip_output_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 pack_notion_zip.py <path/to/BD_標準化.md> [output_zip_path]")
        sys.exit(1)
    target_md = sys.argv[1]
    custom_zip = sys.argv[2] if len(sys.argv) > 2 else None
    pack_notion_zip(target_md, custom_zip)
