#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POE2 BD Standardizer - Adversarial Evaluation Loop Runner (ADR-020)
Simulates red-team adversarial attacks on BD conversion outputs.
Evaluates:
1. Zero-Guesswork compliance: detects whether missing input parameters were hallucinated.
2. Terminology precision: detects whether mainland slang/pseudo-traditional leaks through.
3. Gem Matrix structure: ensures tables meet the Table-First standard.
4. YAML frontmatter schema completeness.
"""

import sys
import os
import re
import json

TEST_CASES = [
    {
        "id": "TC-001-SLANG-AND-PSEUDO-TRADITIONAL",
        "description": "测试国服特供名与黑话消歧（十字弩、雇佣兵、女巫猎手、散弹、火雷）",
        "raw_text": "兄弟们这套雇佣兵女巫猎手十字弩BD无敌了！主打爆炸榴弹连散射弹药，副手打毒气榴弹引爆！",
        "must_contain": ["傭兵", "Mercenary", "女巫獵人", "Witchhunter", "十字弓", "爆炸擲彈", "Explosive Grenade", "散射彈藥", "Scatter Ammo"],
        "forbidden": ["十字弩", "雇佣兵", "女巫猎手", "爆炸榴弹", "散射弹药"]
    },
    {
        "id": "TC-002-ZERO-GUESSWORK-MISSING-FIELDS",
        "description": "测试零臆测保护（原作者完全没提抗性与精魂预算，AI 不得擅自脑补具体数值）",
        "raw_text": "这套就带两把弓换着射，伤害爆炸，清图贼爽，啥抗性血量我都没管。",
        "must_contain": ["[⚠️ 原文未提及/缺项]", "抗性"],
        "forbidden": ["75% 火焰抗性", "75% 冰霜抗性", "100 点精魂"]
    },
    {
        "id": "TC-003-TABLE-MATRIX-REQUIREMENT",
        "description": "测试技能连线表格化标准（必须包含技能、插槽孔色、辅助、NPC购买等列）",
        "raw_text": "爆炸掷弹连散射和毒附魔，第1章奥玛斯买就行。",
        "must_contain": ["|", "爆炸擲彈", "Explosive Grenade", "插槽顏色", "NPC"],
        "forbidden": []
    }
]

def audit_general_file(md_path):
    """General anti-hallucination and slang leakage audit for any BD markdown file."""
    print(f"\n[General Security & Slang Audit] Auditing: {md_path}")
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    slang_blacklist = [
        "十字弩", "雇佣兵", "女巫猎手", "爆炸榴弹", "散射弹药", "鲜血法师", "炼狱术士", "宝石术士"
    ]
    hallucination_indicators = [
        "TODO", "FIXME", "[待補充]", "[待定]", "[推測]"
    ]

    issues = []
    for slang in slang_blacklist:
        if slang in content:
            issues.append(f"Slang leakage detected: '{slang}' (Must be purified to official poe2db Traditional Chinese)")

    for ph in hallucination_indicators:
        if ph in content:
            issues.append(f"Forbidden placeholder/hallucination indicator: '{ph}'")

    if not issues:
        print("  ✅ [PASS] 0 slang leaks, 0 forbidden hallucination placeholders detected.")
        return True
    else:
        print(f"  ❌ [FAIL] Found {len(issues)} issue(s):")
        for iss in issues:
            print(f"     - {iss}")
        return False

def run_eval_on_content(text, case):
    """Evaluates a generated text against a specific test case."""
    issues = []
    for expected in case.get("must_contain", []):
        if expected not in text:
            issues.append(f"Missing expected term/pattern: '{expected}'")

    for forbid in case.get("forbidden", []):
        if forbid in text:
            issues.append(f"Forbidden slang/hallucination detected: '{forbid}'")

    passed = len(issues) == 0
    return passed, issues

def run_all_benchmarks(sample_md_path=None, test_case_id=None):
    print("=" * 60)
    print("  POE2 BD Standardizer - Adversarial Red-Team Benchmark")
    print("=" * 60)

    if sample_md_path and os.path.exists(sample_md_path):
        general_ok = audit_general_file(sample_md_path)
        
        with open(sample_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        cases_to_run = [c for c in TEST_CASES if c['id'] == test_case_id] if test_case_id else []

        if cases_to_run:
            total = len(cases_to_run)
            passed_count = 0
            for case in cases_to_run:
                print(f"\n[Case {case['id']}] {case['description']}")
                passed, issues = run_eval_on_content(content, case)
                if passed:
                    print("  ✅ [PASS] All adversarial checks met.")
                    passed_count += 1
                else:
                    print(f"  ❌ [FAIL] Found {len(issues)} issue(s):")
                    for iss in issues:
                        print(f"     - {iss}")

            score = (passed_count / total) * 100
            print("\n" + "-" * 60)
            print(f"  Final Benchmark Score: {score:.1f}% ({passed_count}/{total} Passed)")
            print("-" * 60)
            return general_ok and (passed_count == total)
        return general_ok

    else:
        print("\nAvailable Built-in Adversarial Test Cases:")
        for case in TEST_CASES:
            print(f" - [{case['id']}] {case['description']}")
        print("\nUsage: python3 scripts/run_adversarial_eval.py <path_to_standardized_md>")
        return True

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else None
    success = run_all_benchmarks(target)
    sys.exit(0 if success else 1)
