# Python
output_lines = []
output_lines.append("Building project...")
output_lines.append("Compiling src/main.at")
output_lines.append("Done: 2 files compiled")

print(f"Captured {len(output_lines)} lines:")
for line in output_lines:
    print(f"  {line}")
