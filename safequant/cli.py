import argparse
import json
import os
import sys
from .core import SafeQuant
from .audit import Aegis4Auditor
from .reporter import AuditReporter
from .guard import SafetyGuard

def main():
    parser = argparse.ArgumentParser(description="SafeQuant-SLM Enterprise Framework")
    parser.add_argument("--model", type=str, required=True, help="HuggingFace Model ID")
    parser.add_argument("--bits", type=int, default=4, help="Quantization (bits)")
    parser.add_argument("--custom-attacks", type=str, help="Path for JSON with the new threat vectors")
    args = parser.parse_args()

    # 1. Initialization and Quantization
    sq = SafeQuant(args.model, args.bits)
    model, tokenizer = sq.quantize()

    # 2. Audit Configuration
    auditor = Aegis4Auditor(model, tokenizer, args.model)
    
    # Custom Attack Vectors Logic
    if args.custom_attacks:
        if os.path.exists(args.custom_attacks):
            with open(args.custom_attacks, 'r') as f:
                custom_vectors = json.load(f)
            # Update auditor attacks
            auditor.attacks.update(custom_vectors)
            print(f"[*] {len(custom_vectors)} custom vectors loaded.")
        else:
            print(f"[!] Warning: File {args.custom_attacks} not found. Using default vectors.")

    # 3. Execute Full Diagnostic
    diagnostic = auditor.execute_full_diagnostic()

    # 4. Terminal UI (Visual Interface)
    score = diagnostic['security_audit']['global_score']
    
    print("\n" + "═"*70)
    print(f"    SAFEQUANT ENTERPRISE REPORT | {diagnostic['model_metadata']['timestamp']}")
    print("═"*70)

    # --- Metrics Section ---
    print(f" [RESOURCE] Memory Footprint:  {diagnostic['resource_metrics']['vram_allocated_mib']} MiB")
    print(f" [PERFORMANCE] Latency:        {diagnostic['performance_metrics']['latency_sec']}s")
    print(f" [PERFORMANCE] Throughput:     {diagnostic['performance_metrics']['throughput_tps']} tok/s")
    print(f" [SECURITY] AEGIS-4 Score:     {score}%")
    print("-" * 70)

    # --- Detailed Audit Table ---
    print(f"{'CATEGORY':<25} | {'STATUS':<12} | {'LEAK PREVIEW'}")
    print("-" * 70)
    
    for test in diagnostic['security_audit']['audit_details']:
        status = "✅ PASSED" if test['passed'] else "❌ VULNERABLE"
        print(f"{test['category']:<25} | {status:<12} | {test['leak_preview']}")
    
    print("═"*70)

    # --- Final Guard Alert ---
    SafetyGuard.display_alert(score)

    # 5. Data Persistence (JSON and PDF)
    try:
        reporter = AuditReporter(diagnostic)
        json_path = reporter.save_json()
        pdf_path = reporter.save_pdf()
                
        print(f"\n[🚀] AUDIT ARTIFACTS GENERATED:")
        print(f"      Location: ./reports/")
        print(f"      PDF:  {os.path.basename(pdf_path)}")
        print(f"      JSON: {os.path.basename(json_path)}")
    except Exception as e:
        print(f"\n[🚨] ERROR GENERATING REPORTS: {e}")

if __name__ == "__main__":
    main()