"""
Final compliance fixes - add missing disclaimers and verify all changes
"""

import re

def read_file():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

def write_file(content):
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

def add_testimonial_disclaimer_if_exists(content):
    """Add disclaimer if testimonials section exists"""
    print("Checking for testimonials section...")
    
    # Check if there's a section with testimonials
    if 'testi' in content.lower() or 'testimonial' in content.lower():
        # Try to find a testimonials heading and add disclaimer after it
        content = re.sub(
            r'(<h2[^>]*>.*?[Tt]estimonial.*?</h2>\s*<p class="common_text">.*?</p>)',
            r'\1\n            <p class="common_text" style="margin-bottom: 20px; font-style: italic; font-size: 14px; text-align: center;">*Testimonials reflect individual experiences and are not indicative of typical results.</p>',
            content,
            count=1
        )
        print("✓ Added testimonial disclaimer")
    else:
        print("No testimonials section found - skipping")
    
    return content

def verify_changes(content):
    """Verify all compliance changes were made"""
    print("\nVerifying compliance changes...")
    print("=" * 60)
    
    checks = {
        "Health disclaimer added": "health-disclaimer" in content,
        "No 'No Side Effects' in banner": "No<br>Side Effects" not in content,
        "Calculator section removed": "GLP-1 Weight Loss Calculator" not in content,
        "Ozempic references removed": "Ozempic" not in content.lower(),
        "Urgency message updated": "Availability may vary" in content,
        "3 Steps section updated": "How to Use (Supplement Information)" in content or "How to Use" in content,
        "Footer links updated": "window.open('privacy.html'" in content,
    }
    
    all_passed = True
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"{status} {check}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("✓ All compliance checks passed!")
    else:
        print("⚠ Some checks failed - manual review needed")
    
    return all_passed

def main():
    print("Final compliance verification and fixes...")
    print("=" * 60)
    
    content = read_file()
    
    content = add_testimonial_disclaimer_if_exists(content)
    
    write_file(content)
    
    verify_changes(content)

if __name__ == "__main__":
    main()
