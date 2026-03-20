import safequant

# Load your quantized model
report = safequant.audit("Qwen/Qwen2-0.5B-4bit")

# Generate the AEGIS-4 Security Report
report.export_pdf("security_audit_v1.pdf")
print(f"Safety Score: {report.score}%")