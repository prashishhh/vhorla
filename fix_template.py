#!/usr/bin/env python3
import re

# Read the file
with open('templates/home/contactus.html', 'r') as f:
    content = f.read()

# Fix split template variables by removing newlines within {{ }}
# Pattern: {{ followed by content split across lines, ending with }}
content = re.sub(r'\{\{\s*\n\s*', '{{ ', content)
content = re.sub(r'\s*\n\s*\}\}', ' }}', content)

# Write back
with open('templates/home/contactus.html', 'w') as f:
    f.write(content)

print("Fixed template variables")
