import re

# Read the file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the supplement description paragraph
content = re.sub(
    r'levels to help you <br>not just lose weight fast but also keep it off â€" all without prescriptions or\s+needles\.',
    'levels to help you lose weight and keep it off.',
    content
)

# Remove statistics percentages and claims
# Remove 15% from body weight
content = re.sub(r'<h3>15%</h3>\s+<p>Reduction', '<h3></h3>\n                                <p>Reduction', content)

# Remove 27% and fix "Cravings & Appletite" to "Appetite"
content = re.sub(r'<h3>27%</h3>\s+<p>Decrease In<br>Cravings &amp; Appletite', '<h3></h3>\n                                <p>Decrease In<br>Appetite', content)

# Remove 6" waist size
content = re.sub(r'<h3>6â€</h3>\s+<p>Reduction<br>In Waist Size', '<h3></h3>\n                                <p>Reduction<br>In Waist', content)

# Remove 90% savings vs Ozempic entirely
content = re.sub(r'<li>\s+<h3>90%</h3>\s+<p>Savings<br>Versus Ozempic</p>\s+</li>', '', content)

# Fix encoding issues - replace â€" with -
content = content.replace('â€"', '-')
content = content.replace('â€™', "'")
content = content.replace('â€˜', "'")
content = content.replace('â€œ', '"')
content = content.replace('â€', '"')

# Write the file back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Landing page updated successfully!")
