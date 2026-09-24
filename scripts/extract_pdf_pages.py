#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POE2 BD Standardizer - Native macOS Dual-Track PDF Extractor
Extracts both high-resolution Retina page images AND the underlying text stream from an input PDF.
Preserves interleaved document flow with `[IMG: page_X.png]` markers into `document_flow.txt`.
Uses native macOS CoreGraphics and PDFKit (compiled Swift helper / 0 external dependencies).
"""

import sys
import os
import subprocess

def extract_pdf_dual_track(pdf_path, output_dir=None):
    if not os.path.exists(pdf_path):
        print(f"Error: PDF not found: {pdf_path}")
        sys.exit(1)

    if output_dir is None:
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_dir = os.path.join("output", "images", base_name)

    os.makedirs(output_dir, exist_ok=True)

    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    binary_path = os.path.join(scripts_dir, "extract_pdf")
    swift_src = os.path.join(scripts_dir, "extract_pdf.swift")

    if not os.path.exists(binary_path):
        print("[Info] Compiling native Swift PDF extractor helper...")
        res = subprocess.run(["swiftc", "-O", "-o", binary_path, swift_src], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[Error] Failed to compile Swift PDF extractor: {res.stderr}")
            sys.exit(1)

    cmd = [binary_path, pdf_path, output_dir]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[Error] Native PDF extraction failed:\n{res.stderr}")
        sys.exit(1)

    print(res.stdout.strip())
    flow_file = os.path.join(output_dir, "document_flow.txt")
    return output_dir, flow_file

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 extract_pdf_pages.py <input.pdf> [output_img_dir]")
        sys.exit(1)
    pdf = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    extract_pdf_dual_track(pdf, out)
