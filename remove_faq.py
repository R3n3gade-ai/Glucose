"""
Remove FAQ section and fix image issue
"""

import re

def read_file():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

def write_file(content):
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

def remove_faq_section(content):
    """Remove the entire section9 FAQ section"""
    print("Removing FAQ section...")
    
    # Remove section9 entirely - from opening div to closing div before footer
    content = re.sub(
        r'<div class="section9">.*?</div>\s*</div>\s*<div class="footer">',
        '<div class="footer">',
        content,
        flags=re.DOTALL
    )
    
    print("✓ FAQ section removed")
    return content

def main():
    print("Removing FAQ section...")
    print("=" * 60)
    
    content = read_file()
    content = remove_faq_section(content)
    write_file(content)
    
    print("=" * 60)
    print("✓ FAQ section deleted successfully!")

if __name__ == "__main__":
    main()
