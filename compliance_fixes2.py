"""
Additional compliance fixes:
1. Add health disclaimer
2. Add testimonial disclaimer
3. Fix footer policy links
4. Additional cleanup
"""

import re

def read_file():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

def write_file(content):
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

def add_health_disclaimer(content):
    """Add health disclaimer after form section"""
    print("Adding health disclaimer...")
    
    disclaimer_html = '''
    <div class="health-disclaimer" style="background: #fff3cd; border: 2px solid #ffc107; padding: 20px; margin: 20px auto; max-width: 1200px; border-radius: 8px;">
        <p style="margin: 0; font-size: 14px; line-height: 1.6; color: #856404;"><strong>Important:</strong> This product is a dietary supplement and is not intended to diagnose, treat, cure, or prevent any disease. Information on this page is for educational purposes only and is not medical advice. Consult a healthcare professional before use. Individual results vary.</p>
    </div>
'''
    
    # Insert before "as_seen_on" section
    content = re.sub(
        r'(\s*<div class="as_seen_on">)',
        disclaimer_html + r'\1',
        content,
        count=1
    )
    
    return content

def add_testimonial_disclaimer(content):
    """Add disclaimer above testimonials"""
    print("Adding testimonial disclaimer...")
    
    disclaimer = '''
            <p class="common_text" style="margin-bottom: 20px; font-style: italic; font-size: 14px; text-align: center;">*Testimonials reflect individual experiences and are not indicative of typical results.</p>

'''
    
    # Find section8 and add disclaimer after the intro text
    content = re.sub(
        r'(<div class="section8">.*?<p class="common_text">.*?</p>)',
        r'\1' + disclaimer,
        content,
        flags=re.DOTALL,
        count=1
    )
    
    return content

def fix_footer_links(content):
    """Update footer policy links to point to actual files"""
    print("Fixing footer policy links...")
    
    # Update the footer links to use proper paths
    content = re.sub(
        r"openNewWindow\('disclosures/privacy\.php','modal'\)",
        "window.open('privacy.html', '_blank')",
        content
    )
    
    content = re.sub(
        r"openNewWindow\('disclosures/terms\.php','modal'\)",
        "window.open('terms.html', '_blank')",
        content
    )
    
    content = re.sub(
        r"openNewWindow\('disclosures/wireless\.php','modal'\)",
        "window.open('wireless.html', '_blank')",
        content
    )
    
    return content

def additional_cleanup(content):
    """Additional compliance cleanup"""
    print("Additional cleanup...")
    
    # Remove any remaining "Balances Blood Sugar" claims
    content = re.sub(r'Balances Blood Sugar Levels', 'Supports Wellness', content)
    content = re.sub(r'Supercharges Metabolism', 'Supports Wellness', content)
    
    # Update banner testimonial to be more compliant
    content = re.sub(
        r'This natural GLP-1 formula has transformed the way I look & feel! No\s*injections, no waiting, no drama - just results!',
        'This natural supplement is easy to use and fits perfectly into my daily routine!',
        content
    )
    
    return content

def main():
    print("Applying additional compliance fixes...")
    print("=" * 60)
    
    content = read_file()
    
    content = add_health_disclaimer(content)
    content = add_testimonial_disclaimer(content)
    content = fix_footer_links(content)
    content = additional_cleanup(content)
    
    write_file(content)
    
    print("=" * 60)
    print("✓ Additional fixes completed!")

if __name__ == "__main__":
    main()
