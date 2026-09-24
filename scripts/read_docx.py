#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POE2 BD Standardizer - Word (.docx) Importer with Interleaved Flow
Extracts text paragraphs, tables, hyperlinks, and embedded images from an input .docx file.
Crucially, it preserves the exact interleaved reading order of images and text, outputting
`[IMG: imageX.ext]` tokens inline so that context, skill setups, and tooltips are never lost.
Zero dependencies (pure Python standard library).
"""

import sys
import os
import zipfile
import xml.etree.ElementTree as ET

def extract_docx(docx_path, output_dir=None):
    if not os.path.exists(docx_path):
        print(f"Error: File not found: {docx_path}")
        sys.exit(1)

    if output_dir is None:
        base_name = os.path.splitext(os.path.basename(docx_path))[0]
        output_dir = os.path.join("output", "images", base_name)

    os.makedirs(output_dir, exist_ok=True)

    extracted_images = []
    text_lines = []

    with zipfile.ZipFile(docx_path, 'r') as z:
        # 1. Extract embedded images from word/media/
        for name in z.namelist():
            if name.startswith('word/media/') and not name.endswith('/'):
                base_name = os.path.basename(name)
                if not base_name:
                    continue
                ext = os.path.splitext(base_name)[1].lower()
                if ext in ('.wmf', '.emf'):
                    print(f"[Warning] 檢測到微軟專用向量格式圖片: {base_name}，網頁或 Notion 可能無法直接渲染，建議確認源文檔。")
                out_img_path = os.path.join(output_dir, base_name)
                with open(out_img_path, 'wb') as img_out:
                    img_out.write(z.read(name))
                extracted_images.append(out_img_path)

        # 2. Extract relationships (for hyperlinks and image rIds)
        rels = {}
        if 'word/_rels/document.xml.rels' in z.namelist():
            try:
                rels_tree = ET.fromstring(z.read('word/_rels/document.xml.rels'))
                for rel in rels_tree:
                    r_id = rel.attrib.get('Id')
                    target = rel.attrib.get('Target')
                    if r_id and target:
                        rels[r_id] = target
            except Exception:
                pass

        # 3. Extract text, hyperlinks, and image positions from word/document.xml
        xml_data = z.read('word/document.xml')
        root = ET.fromstring(xml_data)

        ns = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
            'v': 'urn:schemas-microsoft-com:vml'
        }

        body = root.find('.//w:body', ns)
        if body is None:
            body = root

        def process_p(p):
            p_parts = []
            for child in p:
                tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if tag == 'hyperlink':
                    r_id = child.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
                    target_url = rels.get(r_id, '')
                    link_text = "".join(child.itertext()).strip()
                    if link_text and target_url and target_url.startswith(('http://', 'https://')):
                        p_parts.append(f" [{link_text}]({target_url}) ")
                    elif link_text:
                        p_parts.append(link_text)
                else:
                    for elem in child.iter():
                        etag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                        if etag == 't' and elem.text:
                            p_parts.append(elem.text)
                        elif etag == 'blip':
                            embed = elem.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                            if embed and embed in rels:
                                img_filename = os.path.basename(rels[embed])
                                p_parts.append(f" [IMG: {img_filename}] ")
                        elif etag == 'imagedata':
                            rid = elem.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
                            if rid and rid in rels:
                                img_filename = os.path.basename(rels[rid])
                                p_parts.append(f" [IMG: {img_filename}] ")
            line = "".join(p_parts).strip()
            if line:
                text_lines.append(line)

        for child in body:
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if tag == 'p':
                process_p(child)
            elif tag == 'tbl':
                # Traverse cells in table
                for tc in child.iterfind('.//w:tc', ns):
                    for p in tc.iterfind('.//w:p', ns):
                        process_p(p)

    full_text = "\n".join(text_lines)
    
    # Save the interleaved text flow for easy agent inspection
    flow_file = os.path.join(output_dir, "document_flow.txt")
    with open(flow_file, 'w', encoding='utf-8') as f:
        f.write(full_text)

    return full_text, extracted_images, flow_file

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 read_docx.py <input.docx> [output_img_dir]")
        sys.exit(1)
    doc_path = sys.argv[1]
    base_name = os.path.splitext(os.path.basename(doc_path))[0]
    img_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join("output", "images", base_name)
    text, imgs, flow_path = extract_docx(doc_path, img_dir)
    print(f"--- Extracted {len(imgs)} image(s) to '{img_dir}' ---")
    print(f"--- Interleaved document flow saved to '{flow_path}' ---")
    print("\n[Preview First 30 Lines]:\n")
    preview_lines = text.splitlines()[:30]
    print("\n".join(preview_lines))
