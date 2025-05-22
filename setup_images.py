"""
Image Setup Helper for Kijiji Room Rental Automation
Helps organize your room photos and content optimization
"""

import os
import shutil
from pathlib import Path

def setup_images_directory():
    """Create images directory and provide guidance"""
    
    print("📸 Kijiji Room Rental - Image Setup Helper")
    print("=" * 50)
    
    # Create separate directories for each ad
    ad1_dir = Path("images/ad1")
    ad2_dir = Path("images/ad2")
    ad1_dir.mkdir(parents=True, exist_ok=True)
    ad2_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"✅ Created 'images/ad1' and 'images/ad2' directories")
    
    # Expected image files for each ad
    ad1_images = [
        ("room_main.jpg", "📸 Professional-focused room staging"),
        ("bed_area.jpg", "🛏️ Clean, professional bedroom setup"),
        ("workspace.jpg", "💼 Work-from-home workspace"),
        ("kitchen.jpg", "🍳 Kitchen - angle 1"),
        ("bathroom.jpg", "🚿 Bathroom - angle 1"),
        ("exterior.jpg", "🏠 House exterior - angle 1")
    ]
    
    ad2_images = [
        ("room_study.jpg", "📚 Student-focused room with study area"),
        ("bed_desk.jpg", "🎓 Bed and desk combination"),
        ("living_space.jpg", "👥 Student-friendly common area"),
        ("kitchen_shared.jpg", "🍳 Kitchen - angle 2"),
        ("bathroom_clean.jpg", "🚿 Bathroom - angle 2"),
        ("building.jpg", "🏢 Building exterior - angle 2")
    ]
    
    print("\n📋 Photo Checklist - SEPARATE PHOTOS FOR EACH AD:")
    print("=" * 70)
    
    print("\n🏢 AD 1 PHOTOS (Professional Audience) - images/ad1/:")
    print("-" * 50)
    for filename, description in ad1_images:
        filepath = ad1_dir / filename
        status = "✅ Found" if filepath.exists() else "❌ Missing"
        print(f"{status} | {filename:<20} | {description}")
    
    print("\n🎓 AD 2 PHOTOS (Student Audience) - images/ad2/:")
    print("-" * 50)
    for filename, description in ad2_images:
        filepath = ad2_dir / filename
        status = "✅ Found" if filepath.exists() else "❌ Missing"
        print(f"{status} | {filename:<20} | {description}")
    
    print("\n💡 Photo Strategy Tips:")
    print("• Use DIFFERENT angles/staging for each ad")
    print("• Ad 1: Professional, clean, work-focused")
    print("• Ad 2: Student-friendly, study-focused") 
    print("• Same space, different presentation")
    print("• Avoid duplicate photos (Kijiji may flag as spam)")
    
    print("\n📷 Photo Quality Tips:")
    print("• Use good lighting (natural light is best)")
    print("• Clean and organize spaces before photographing") 
    print("• Take horizontal (landscape) photos when possible")
    print("• Keep file sizes under 10MB each")
    print("• Use .jpg format for best compatibility")
    
    # Check current status
    ad1_count = sum(1 for filename, _ in ad1_images 
                    if (ad1_dir / filename).exists())
    ad2_count = sum(1 for filename, _ in ad2_images 
                    if (ad2_dir / filename).exists())
    total_expected = len(ad1_images) + len(ad2_images)
    total_existing = ad1_count + ad2_count
    
    print(f"\n📊 Current Status:")
    print(f"   Ad 1: {ad1_count}/{len(ad1_images)} photos ready")
    print(f"   Ad 2: {ad2_count}/{len(ad2_images)} photos ready") 
    print(f"   Total: {total_existing}/{total_expected} photos ready")
    
    if total_existing == 0:
        print("\n🚀 Next Steps:")
        print("1. Take photos of your room and common areas")
        print("2. Stage them differently for each ad:")
        print("   • Ad 1: Professional, work-focused")
        print("   • Ad 2: Student-friendly, study-focused")
        print("3. Save with exact filenames shown above")
        print("4. Run the automation script")
    elif total_existing < total_expected:
        print(f"\n⚠️ Missing {total_expected - total_existing} photos")
        print("Add the missing photos for best results!")
    else:
        print("\n🎉 All photos ready! Your ads will look great!")
    
    return total_existing

def show_content_tips():
    """Show tips for optimizing ad content"""
    
    print("\n" + "=" * 50)
    print("📝 Content Optimization Tips")
    print("=" * 50)
    
    print("""
🎯 TITLE OPTIMIZATION:
• Include key search terms: "furnished", "all-inclusive", location
• Mention price in title for transparency
• Use descriptive words: "student-friendly", "professional"

📝 DESCRIPTION BEST PRACTICES:
• Use bullet points and emojis for readability
• Highlight what's included (utilities, WiFi, etc.)
• Mention location benefits (transit, shopping)
• Include contact information clearly
• Add urgency: "Available immediately"

🏷️ EFFECTIVE TAGS:
• Use terms people search for
• Include neighborhood name
• Add lifestyle terms (student, professional)
• Mention key features (furnished, wifi, transit)

💰 PRICING STRATEGY:
• Research similar listings in your area
• Consider all-inclusive vs. separate utilities
• Offer student discounts if applicable
• Be transparent about additional costs

📞 CONTACT INFO:
• Use a working phone number
• Respond quickly to inquiries
• Be professional in communications
""")

def main():
    """Main setup function"""
    
    # Setup images
    existing_photos = setup_images_directory()
    
    # Show content tips
    show_content_tips()
    
    print("\n🤖 Ready to Run Automation:")
    print("• Test once: python kijiji_dual_posting.py")
    print("• Daily schedule: python daily_scheduler.py schedule 09:00")
    
    print(f"\n✨ Your automation is ready with {existing_photos}/6 photos!")

if __name__ == "__main__":
    main() 