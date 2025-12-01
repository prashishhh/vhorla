#!/usr/bin/env python3

# Read the file
with open('templates/home/contactus.html', 'r') as f:
    lines = f.readlines()

# Process line by line, joining split template variables
result = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Check if line has an opening {{ without closing }}
    if '{{' in line and '}}' not in line:
        # Keep appending next lines until we find }}
        combined = line.rstrip()
        i += 1
        while i < len(lines) and '}}' not in lines[i]:
            combined += ' ' + lines[i].strip()
            i += 1
        if i < len(lines):
            combined += ' ' + lines[i].strip()
            i += 1
        result.append(combined + '\n')
    else:
        result.append(line)
        i += 1

# Write back
with open('templates/home/contactus.html', 'w') as f:
    f.writelines(result)

print("Fixed all split template variables")
