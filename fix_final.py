import re

# Read the file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove 6" from the h3 tag
content = content.replace('<h3>6"</h3>', '<h3></h3>')

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed 6 inch reference successfully!")
