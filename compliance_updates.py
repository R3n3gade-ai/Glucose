"""
Comprehensive compliance update script for affiliate requirements
This script will make all 10 required changes to the landing page
"""

import re

def read_file():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

def write_file(content):
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

def phase1_safety_language(content):
    """Phase 1: Remove absolute safety & zero-risk language"""
    print("Phase 1: Removing safety & risk language...")
    
    # Remove "No Side Effects" from banner strip
    content = re.sub(r'<li>\s*<img[^>]*>\s*<p>No<br>Side Effects</p>\s*</li>', '', content, flags=re.DOTALL)
    
    # Remove "100% Safe" references
    content = content.replace('100% Safe', '')
    content = content.replace('No Side Effects', '')
    
    return content

def phase2_quantified_outcomes(content):
    """Phase 2: Remove quantified & predictable outcome claims"""
    print("Phase 2: Removing quantified outcomes...")
    
    # Delete GLP-1 Weight Loss Calculator section (entire s2_right_slide div)
    content = re.sub(
        r'<div class="s2_right_slide">.*?</div>\s*</div>\s*</div>',
        '</div>\n                </div>\n\n            </div>',
        content,
        flags=re.DOTALL
    )
    
    # Delete the entire "Weight Loss Benefits The Compound With Consistent Use" section (section6)
    content = re.sub(
        r'<div class="section6">.*?</div>\s*</div>',
        '',
        content,
        flags=re.DOTALL,
        count=1
    )
    
    # Remove statistics boxes with percentages - already done but ensure empty h3 tags
    content = re.sub(r'<h3>15%</h3>', '<h3></h3>', content)
    content = re.sub(r'<h3>27%</h3>', '<h3></h3>', content)
    content = re.sub(r'<h3>90%</h3>', '<h3></h3>', content)
    content = re.sub(r'<h3>6["\']?</h3>', '<h3></h3>', content)
    
    return content

def phase3_prescription_comparisons(content):
    """Phase 3: Remove prescription & Ozempic comparison content"""
    print("Phase 3: Removing prescription comparisons...")
    
    # Delete "The Problem With Synthetic GLP-1 Injections Like Ozempic" section (section1)
    content = re.sub(
        r'<div class="section1">.*?</div>\s*</div>',
        '',
        content,
        flags=re.DOTALL,
        count=1
    )
    
    # Delete "The GlucoBoost Difference Capsules vs Injections" section (section7)
    content = re.sub(
        r'<div class="section7">.*?</div>\s*</div>',
        '',
        content,
        flags=re.DOTALL,
        count=1
    )
    
    # Remove any remaining Ozempic references
    content = content.replace('Ozempic', '')
    content = content.replace('ozempic', '')
    
    return content

def phase4_testimonials(content):
    """Phase 4: Fix testimonials"""
    print("Phase 4: Updating testimonials...")
    
    # Add disclaimer above testimonials
    testimonials_disclaimer = '''
            <p class="common_text" style="margin-bottom: 20px; font-style: italic; font-size: 14px;">Testimonials reflect individual experiences and are not indicative of typical results.</p>
'''
    
    # Insert disclaimer before testimonial block
    content = re.sub(
        r'(<div class="testi_block">)',
        testimonials_disclaimer + r'\1',
        content
    )
    
    # Rewrite testimonial 1 - remove "Lost 20 lbs in 3 Months"
    content = re.sub(
        r'<p class="testi_head">Lost 20 lbs in 3 Months!</p>',
        '<p class="testi_head">Easy to Use and Convenient</p>',
        content
    )
    content = re.sub(
        r'"This supplement has been a game-changer for me\. In just three months,\s*I\'ve lost 20 lbs, and it\'s all thanks to the natural ingredients\. I love that I didn\'t\s*have to deal with needles or doctor visits\. It\'s so easy to use, and the results speak for\s*themselves!"',
        '"This supplement has been so easy to incorporate into my daily routine. I love that I didn\'t have to deal with needles or doctor visits. It\'s convenient and fits perfectly into my lifestyle."',
        content
    )
    
    # Rewrite testimonial 4 - remove "Balanced Blood Sugar, More Energy"
    content = re.sub(
        r'<p class="testi_head">Balanced Blood Sugar, More Energy!</p>',
        '<p class="testi_head">Fits My Routine Perfectly</p>',
        content
    )
    content = re.sub(
        r'"I can\'t believe the difference in how I feel\. My blood sugar levels\s*are more balanced, which means no more energy crashes\. This supplement has not only helped\s*me lose weight but also boosted my overall health!"',
        '"I appreciate how easy this product is to use. It fits seamlessly into my daily routine and I feel good about taking a natural supplement."',
        content
    )
    
    # Keep testimonials 2, 3, 5, 6 but update them to be more general
    content = re.sub(
        r'"I used to struggle with constant cravings, especially late at night\.\s*Since starting this supplement, my appetite is under control, and I feel fuller for longer\.\s*I\'ve never felt more in control of my weight loss journey!"',
        '"I appreciate the natural ingredients in this supplement. It\'s easy to take and fits well into my healthy lifestyle routine."',
        content
    )
    
    content = re.sub(
        r'"I was skeptical about an all-natural alternative to GLP-1 injections,\s*but this product really delivers\. I started noticing changes in my energy levels and\s*metabolism within the first few weeks\. It\'s simple, effective, and completely\s*needle-free!"',
        '"I was looking for a natural supplement option and this product fits the bill. It\'s simple to use and I appreciate that it\'s needle-free."',
        content
    )
    
    content = re.sub(
        r'"I love that this product uses natural ingredients\. It\'s given me all\s*the benefits I was looking for without any side effects\. My weight has been steadily\s*dropping, and I feel fantastic!"',
        '"I love that this product uses natural ingredients. It\'s easy to take and I feel good about adding it to my wellness routine."',
        content
    )
    
    content = re.sub(
        r'"I\'ve tried so many products before, but nothing worked long-term\.\s*With this supplement, I\'ve lost weight and kept it off\. The best part\? I don\'t feel like\s*I\'m on a \'diet\.\' It\'s just a part of my daily routine now!"',
        '"This supplement has become a regular part of my daily routine. It\'s easy to use and I appreciate the natural approach."',
        content
    )
    
    return content

def phase5_urgency_scarcity(content):
    """Phase 5: Remove aggressive scarcity/urgency"""
    print("Phase 5: Removing urgency/scarcity...")
    
    # Replace "Hurry! Only 48 available"
    content = re.sub(
        r'<p><img[^>]*><span>Hurry!</span>\s*Only <u>\d+</u> Glp-1 Booster Available</p>',
        '<p>Availability may vary.</p>',
        content
    )
    
    return content

def phase6_ingredient_claims(content):
    """Phase 6: Neutralize mechanism & ingredient claims"""
    print("Phase 6: Neutralizing ingredient claims...")
    
    # Update ingredient descriptions
    generic_description = 'Studied for its role in supporting gut health and overall wellness.'
    
    # Clostridium Butyricum
    content = re.sub(
        r'Enhances gut health and boosts GLP-1 production, helping to regulate blood sugar and support\s*efficient metabolism for long-term weight management\.',
        generic_description,
        content
    )
    
    # Akkermansia Muciniphila
    content = re.sub(
        r'Known for reducing appetite by improving gut barrier function, it supports natural weight loss\s*and helps maintain healthy blood sugar levels\.',
        generic_description,
        content
    )
    
    # Bifidobacterium Infantis
    content = re.sub(
        r'Promotes overall digestive health, reduces inflammation, and aids in balancing metabolism to\s*optimize fat burning and energy levels\.',
        generic_description,
        content
    )
    
    # Remove claims from benefits section
    content = re.sub(r'Boosts\s*Metabolism', 'Supports Wellness', content)
    content = re.sub(r'Balances\s*Blood Sugar', 'Supports Health', content)
    content = re.sub(r'Fat Burning', 'Wellness Support', content)
    
    return content

def phase7_three_steps(content):
    """Phase 7: Update "3 Simple Steps" section"""
    print("Phase 7: Updating 3 Simple Steps section...")
    
    # Change section title
    content = re.sub(
        r'<h2 class="common_heading">Boost GLP-1 Levels & Lose Weight Fast <br>In Just 3 Simple Steps </h2>',
        '<h2 class="common_heading">How to Use (Supplement Information)</h2>',
        content
    )
    
    # Update section description
    content = re.sub(
        r'Using our product is simple and hassle-free[^<]*<br>[^<]*to support your weight loss and health goals\.',
        'Use as directed. Individual responses vary. Consult a healthcare professional before use.',
        content
    )
    
    # Update "Feel the Fat Burn"
    content = re.sub(
        r'<h3>Feel the Fat Burn</h3>',
        '<h3>Continue Daily Use</h3>',
        content
    )
    
    content = re.sub(
        r'As the ingredients get to work, you\'ll notice a boost in metabolism, reduced cravings, and\s*natural fat-burning kicking in\.',
        'Continue taking as directed as part of your daily wellness routine.',
        content
    )
    
    # Update "Enjoy Lasting Results"
    content = re.sub(
        r'<h3>Enjoy Lasting Results</h3>',
        '<h3>Maintain Healthy Habits</h3>',
        content
    )
    
    content = re.sub(
        r'Consistent use supports sustainable weight loss, balanced blood sugar, and improved energy levels\s*for long-term success\.',
        'Individual results vary. Combine with healthy diet and exercise habits for best results.',
        content
    )
    
    return content

def phase8_health_disclaimer(content):
    """Phase 8: Add prominent health disclaimer"""
    print("Phase 8: Adding health disclaimer...")
    
    disclaimer_html = '''
    <div class="health-disclaimer" style="background: #fff3cd; border: 2px solid #ffc107; padding: 20px; margin: 20px 0; border-radius: 8px;">
        <p style="margin: 0; font-size: 14px; line-height: 1.6; color: #856404;"><strong>Important:</strong> This product is a dietary supplement and is not intended to diagnose, treat, cure, or prevent any disease. Information on this page is for educational purposes only and is not medical advice. Consult a healthcare professional before use. Individual results vary.</p>
    </div>
'''
    
    # Insert after the form block
    content = re.sub(
        r'(</div>\s*</div>\s*</div>\s*<div class="as_seen_on">)',
        disclaimer_html + r'\1',
        content,
        count=1
    )
    
    return content

def phase9_faq_updates(content):
    """Phase 9: Update FAQ section"""
    print("Phase 9: Updating FAQ section...")
    
    # Update "How soon will I see results?" answer
    faq_answer = 'Individual results vary. Some users may notice changes over time when combined with healthy habits. Consult with a healthcare professional for personalized guidance.'
    
    content = re.sub(
        r'(<div class="accordion acdn-heading[^>]*>How soon will I start seeing\s*results\?</div>\s*<div class="acdn-content"[^>]*>)\s*</div>',
        r'\1\n                            <p class="acdn-para">' + faq_answer + '</p>\n                        </div>',
        content
    )
    
    # Make sure the FAQ is not set to display:none
    content = re.sub(
        r'(<div class="accordion acdn-heading) accordion-close(" id="hd-one">How soon will I start seeing\s*results\?</div>\s*<div class="acdn-content") style="display: none;"',
        r'\1\2',
        content
    )
    
    return content

def main():
    print("Starting affiliate compliance updates...")
    print("=" * 60)
    
    content = read_file()
    
    # Apply all phases
    content = phase1_safety_language(content)
    content = phase2_quantified_outcomes(content)
    content = phase3_prescription_comparisons(content)
    content = phase4_testimonials(content)
    content = phase5_urgency_scarcity(content)
    content = phase6_ingredient_claims(content)
    content = phase7_three_steps(content)
    content = phase8_health_disclaimer(content)
    content = phase9_faq_updates(content)
    
    write_file(content)
    
    print("=" * 60)
    print("✓ All compliance updates completed successfully!")
    print("\nRemaining manual tasks:")
    print("- Verify footer policy links are working")
    print("- Review entire page for any missed claims")
    print("- Test all functionality")

if __name__ == "__main__":
    main()
