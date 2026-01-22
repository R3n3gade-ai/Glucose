import re

# Read the HTML file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and remove the timeline section
# Pattern to match the entire timeline section from first s6_row to the closing divs
pattern = r'    <div class="s6_row">.*?Week 4 - 8.*?</div>\s*</div>\s*</div>\s*</div>'

# Use DOTALL flag to match across newlines
content = re.sub(pattern, '', content, flags=re.DOTALL)

# Write back to the file
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Timeline section removed successfully!")
