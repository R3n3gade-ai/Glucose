import re

# Read the file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the supplement description paragraph - remove the extra text
content = re.sub(
    r'levels to help you <br>not just lose weight fast but also keep it off[^<]+all without prescriptions or\s+needles\.',
    'levels to help you lose weight and keep it off.',
    content
)

# Remove 6" from waist - fix the h3 tag
content = re.sub(r'<h3>6"</h3>', '<h3></h3>', content)

# Also remove "Size" from "In Waist Size"
content = re.sub(r'In Waist Size', 'In Waist', content)

# Write the file back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Additional fixes applied successfully!")
