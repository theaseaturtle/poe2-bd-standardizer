#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POE2 BD Standardizer - Unified Pipeline CLI Runner
Single entrypoint to manage the full BD standardization lifecycle:
1. ingest: Auto-detects .docx or .pdf, extracts images and interleaved flow (document_flow.txt).
2. verify: Audits Markdown document, images, and frontmatter.
3. pack: Builds flat ZIP package for Notion/Obsidian and verifies completeness.
4. batch-verify: Audits all standardized BD markdowns in target directory.
Zero external dependencies (pure Python standard library).
"""

import sys
import os
import re
import argparse
import subprocess

def get_script_path(script_name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)

def cmd_ingest(input_path, custom_name=None, output_dir="output"):
    if not os.path.exists(input_path):
        print(f"[Error] Input file not found: {input_path}")
        sys.exit(1)

    ext = os.path.splitext(input_path)[1].lower()
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    target_name = custom_name or base_name
    img_dir = os.path.join(output_dir, "images", target_name)
    os.makedirs(img_dir, exist_ok=True)

    print(f"=== [Standardize Ingest] Processing: {input_path} ===")
    print(f"Target Asset Folder: {img_dir}")

    if ext == '.docx':
        script = get_script_path("read_docx.py")
        res = subprocess.run([sys.executable, script, input_path, img_dir])
    elif ext == '.pdf':
        script = get_script_path("extract_pdf_pages.py")
        res = subprocess.run([sys.executable, script, input_path, img_dir])
    else:
        print(f"[Error] Unsupported file format: {ext} (supported: .docx, .pdf)")
        sys.exit(1)

    if res.returncode != 0:
        print("[Error] Ingestion failed.")
        sys.exit(res.returncode)

    flow_path = os.path.join(img_dir, "document_flow.txt")
    print(f"\n[Success] Ingestion complete!")
    print(f"-> Assets: {img_dir}")
    print(f"-> Interleaved Flow: {flow_path}")
    print(f"-> Next: Inspect '{flow_path}', write standardized Markdown to '{output_dir}/{target_name}_標準化.md', then verify with `standardize.py verify <md>`.\n")

def cmd_verify(md_path):
    script = get_script_path("verify_bd.py")
    res = subprocess.run([sys.executable, script, md_path])
    sys.exit(res.returncode)

def cmd_pack(md_path, zip_output=None):
    print(f"=== [Standardize Pack] Packaging & Verifying: {md_path} ===")
    pack_script = get_script_path("pack_notion_zip.py")
    args = [sys.executable, pack_script, md_path]
    if zip_output:
        args.append(zip_output)
    pack_res = subprocess.run(args)
    if pack_res.returncode != 0:
        print("[Error] Packaging failed.")
        sys.exit(pack_res.returncode)

    print("\nRunning Automated Quality Gate...")
    verify_script = get_script_path("verify_bd.py")
    verify_res = subprocess.run([sys.executable, verify_script, md_path])
    sys.exit(verify_res.returncode)

def cmd_batch_verify(output_dir="output"):
    if not os.path.exists(output_dir):
        print(f"[Error] Directory not found: {output_dir}")
        sys.exit(1)

    md_files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('_標準化.md')]
    if not md_files:
        print(f"No standardized Markdown files found in {output_dir}/.")
        sys.exit(0)

    print(f"=== [Batch Verify] Checking {len(md_files)} BD document(s) in {output_dir} ===\n")
    failed = []
    verify_script = get_script_path("verify_bd.py")
    for f in sorted(md_files):
        res = subprocess.run([sys.executable, verify_script, f])
        if res.returncode != 0:
            failed.append(f)

    if failed:
        print(f"\n❌ Batch Verification Failed for {len(failed)} file(s):")
        for f in failed:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print(f"\n🎉 All {len(md_files)} BD documents passed verification perfectly!")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="POE2 BD Standardizer Unified Pipeline Runner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Ingest
    p_ingest = subparsers.add_parser("ingest", help="Ingest .docx or .pdf into interleaved flow & image assets")
    p_ingest.add_argument("input_path", help="Path to input .docx or .pdf file")
    p_ingest.add_argument("--name", dest="custom_name", help="Target standardized name for image folder")
    p_ingest.add_argument("-o", "--output-dir", default="output", help="Directory where images and Markdown will be saved (default: output)")

    # Verify
    p_verify = subparsers.add_parser("verify", help="Run automated quality gate on standardized markdown")
    p_verify.add_argument("md_path", help="Path to [BD名稱]_標準化.md")

    # Pack
    p_pack = subparsers.add_parser("pack", help="Build flat ZIP package for Notion/Obsidian and verify")
    p_pack.add_argument("md_path", help="Path to [BD名稱]_標準化.md")
    p_pack.add_argument("-o", "--output", dest="zip_output", help="Custom output path for the zip file")

    # Batch Verify
    p_batch = subparsers.add_parser("batch-verify", help="Verify all standardized BD markdowns in target directory")
    p_batch.add_argument("-d", "--dir", default="output", help="Directory to scan for standardized markdowns (default: output)")

    args = parser.parse_args()

    if args.command == "ingest":
        cmd_ingest(args.input_path, args.custom_name, args.output_dir)
    elif args.command == "verify":
        cmd_verify(args.md_path)
    elif args.command == "pack":
        cmd_pack(args.md_path, args.zip_output)
    elif args.command == "batch-verify":
        cmd_batch_verify(args.dir)

if __name__ == '__main__':
    main()
