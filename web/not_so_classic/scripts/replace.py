import os
import sys
import re

# Outputs the original file with sensitive contents replaced
# To a specified directory  

sensitives = [
    {"regex": re.compile(r'flag\{.+?\}'), "replacement": "REDACTED" },
    {"regex": re.compile(r'SECRET_KEY=[0-9A-Fa-f]+'), "replacement": "SECRET_KEY=REDACTED" },
    {"regex": re.compile(r'ADMIN_PASSWORD=[0-9A-Fa-f]+'), "replacement": "ADMIN_PASSWORD=REDACTED"},
]
source_file = sys.argv[1]
prefix_dir = sys.argv[2]

dest_file = os.path.join(prefix_dir, source_file)
with open(source_file, mode="r") as f:
    content = f.read()

for sensitive in sensitives:
    content = sensitive["regex"].sub(sensitive["replacement"], content)

with open(dest_file, mode="w") as f:
    f.write(content)
