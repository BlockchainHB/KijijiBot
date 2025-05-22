"""
Kijiji Dual Room Rental Automation Script
Posts 2 unique room rental ads based on recorded workflow
"""

import asyncio
import json
import os
from datetime import datetime
from playwright.async_api import async_playwright

class KijijiDualPosting:
    def __init__(self, config_file='test_input.json'):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.username = self.config.get('username')
        self.password = self.config.get('password')
        self.headless = self.config.get('headless', False)
        
        # Two optimized room ads - Kijiji character limits & search optimization
        self.ad1 = {
            'title': 'Furnished Basement Room Scarborough',  # 54 chars
            'description': '''FURNISHED BASEMENT ROOM - SCARBOROUGH

WHAT'S INCLUDED:
✓ Private furnished bedroom
✓ ALL utilities included (hydro, heat, water)
✓ High-speed internet/WiFi
✓ Shared kitchen and laundry
✓ Parking available
✓ Clean, quiet home

LOCATION BENEFITS:
✓ Scarborough near TTC routes
✓ Close to grocery stores and shopping
✓ Safe residential neighborhood
✓ Easy access to downtown Toronto

IDEAL FOR:
✓ Working professionals
✓ Graduate students  
✓ Responsible tenants

RENT: $500/month ALL-INCLUSIVE
No hidden fees or extra charges

Available immediately
References required
Non-smoking home

Contact: 647-607-4050
Call or text anytime''',
            'price': '500',
            'tags': ['furnished', 'basement', 'scarborough', 'inclusive', 'utilities'],
            'location': '138 Chillery Avenue',
            'phone': '647-607-4050'
        }
        
        self.ad2 = {
            'title': 'Shared Student Room Rental Near TTC',  # 55 chars
            'description': '''STUDENT-FRIENDLY ROOM RENTAL - SCARBOROUGH

PERFECT FOR STUDENTS:
✓ Private furnished bedroom
✓ Quiet study environment
✓ Fast WiFi for online classes
✓ Shared kitchen access
✓ All utilities included
✓ Laundry facilities

EXCELLENT LOCATION:
✓ Walking distance to TTC bus stops
✓ Easy commute to UTSC, Centennial College
✓ Near grocery stores and restaurants
✓ Safe family neighborhood
✓ Free street parking

WHAT'S INCLUDED:
✓ Hydro, heat, water, internet
✓ Kitchen privileges
✓ Laundry access
✓ 24/7 building access

SPECIAL STUDENT RATE: $450/month
All utilities included - no extra costs

Available now for September
References and student ID required
Non-smoking environment

Text/Call: 647-607-4050''',
            'price': '450', 
            'tags': ['student', 'furnished', 'ttc', 'scarborough', 'college'],
            'location': '138 Chillery Avenue',
            'phone': '647-607-4050'
        }
        
        # Separate image sets for each ad to avoid duplicate content
        # Each ad gets its own photos for uniqueness
        self.ad1_images = [
            "images/ad1/room_main.png",      # Professional-focused staging
            "images/ad1/bed_area.png",       # Clean, professional setup
            "images/ad1/workspace.png",      # Work-from-home setup
            "images/ad1/kitchen.png",        # Kitchen angle 1
            "images/ad1/bathroom.png",       # Bathroom angle 1
            "images/ad1/exterior.png"        # House exterior angle 1
        ]
        
        self.ad2_images = [
            "images/ad2/room_study.png",     # Student-focused staging
            "images/ad2/bed_desk.png",       # Study area emphasized
            "images/ad2/living_space.png",   # Student-friendly common area
            "images/ad2/kitchen_shared.png", # Kitchen angle 2
            "images/ad2/bathroom_clean.png", # Bathroom angle 2
            "images/ad2/building.png"        # Building exterior angle 2
        ]
        
        # Create directories
        os.makedirs('screenshots', exist_ok=True)
        os.makedirs('images/ad1', exist_ok=True)
        os.makedirs('images/ad2', exist_ok=True)
        
    async def login(self, page):
        """Login to Kijiji - based on recording"""
        print("🔐 Logging in to Kijiji...")
        
        login_url = "https://id.kijiji.ca/login?service=https%3A%2F%2Fid.kijiji.ca%2Foauth2.0%2FcallbackAuthorize%3Fclient_id%3Dkijiji_horizontal_web_gpmPihV3%26redirect_uri%3Dhttps%253A%252F%252Fwww.kijiji.ca%252Fapi%252Fauth%252Fcallback%252Fcis%26response_type%3Dcode%26client_name%3DCasOAuthClient&locale=en&scope=openid+email+profile"
        
        await page.goto(login_url, wait_until='networkidle')
        await asyncio.sleep(2)
        
        # Login process from recording
        await page.get_by_role("textbox", name="Email Address").click()
        await page.get_by_role("textbox", name="Email Address").fill(self.username)
        await page.get_by_role("textbox", name="Email Address").press("Tab")
        await page.get_by_role("link", name="Forgot Password?").press("Tab")
        await page.get_by_role("textbox", name="Password").fill(self.password)
        await page.get_by_role("button", name="Sign in").click()
        
        # Wait for redirect
        await page.wait_for_url('https://www.kijiji.ca/**', timeout=30000)
        await asyncio.sleep(3)
        
        print("   ✅ Login successful!")
        await page.screenshot(path=f'screenshots/01-login-{datetime.now().strftime("%H%M%S")}.png')
        
    async def delete_existing_ads(self, page):
        """Delete all existing ads - based on recording"""
        print("🗑️  Deleting existing ads...")
        
        # Navigate to My Ads
        await page.get_by_role("button", name="My Account").click()
        await asyncio.sleep(1)
        await page.get_by_role("link", name="My Ads").click()
        await asyncio.sleep(3)
        
        await page.screenshot(path=f'screenshots/02-my-ads-{datetime.now().strftime("%H%M%S")}.png')
        
        # First, collect all unique listing IDs
        print("   Scanning for existing ads...")
        
        try:
            # Find all elements with test-id that starts with "listing-id-"
            listing_elements = await page.query_selector_all('[data-testid^="listing-id-"]')
            listing_ids = []
            
            for element in listing_elements:
                test_id = await element.get_attribute('data-testid')
                if test_id and test_id.startswith('listing-id-'):
                    listing_ids.append(test_id)
            
            print(f"   Found {len(listing_ids)} ads to delete: {listing_ids}")
            
            # Now delete each specific listing ID
            deleted_count = 0
            for listing_id in listing_ids:
                try:
                    print(f"   Deleting ad: {listing_id}")
                    
                    # Click the specific delete button for this listing
                    delete_button = page.get_by_test_id(listing_id).get_by_test_id("adDeleteButton")
                    await delete_button.click()
                    await asyncio.sleep(1)
                    
                    # Select reason and confirm (from recording)
                    await page.get_by_role("button", name="Prefer not to say").click()
                    await asyncio.sleep(1)
                    await page.get_by_role("button", name="Delete My Ad").click()
                    await asyncio.sleep(2)
                    
                    # Close modal (from recording)
                    await page.get_by_test_id("ModalCloseButton").click()
                    await asyncio.sleep(2)
                    
                    deleted_count += 1
                    print(f"   ✅ Ad {deleted_count} deleted: {listing_id}")
                    
                except Exception as e:
                    print(f"   ⚠️ Failed to delete {listing_id}: {e}")
                    continue
                    
            print(f"   ✅ Total ads deleted: {deleted_count}")
            
        except Exception as e:
            print(f"   ⚠️ Error scanning for ads: {e}")
            print("   No ads found or already deleted")
        
    async def post_ad(self, page, ad_data, ad_number):
        """Post a single ad - based on recording"""
        print(f"📝 Posting Ad #{ad_number}: {ad_data['title']}")
        
        # Start posting
        await page.get_by_test_id("header-link-post-ad").click()
        await asyncio.sleep(2)
        
        # Close drawer if it appears (from recording)
        try:
            await page.get_by_test_id("drawer-close-button").click(timeout=3000)
            await asyncio.sleep(1)
        except:
            pass
            
        # STEP 1: Enter title FIRST (this is the key from your recording!)
        await page.get_by_role("textbox", name="Ad title").click()
        await page.get_by_role("textbox", name="Ad title").fill(ad_data['title'])
        await asyncio.sleep(1)
        
        # STEP 2: Click Next (now enabled because title is filled)
        await page.get_by_role("button", name="Next").click()
        await asyncio.sleep(2)
        
        # STEP 3: Select category
        await page.get_by_role("button", name="Room Rentals & Roommates Real").click()
        await asyncio.sleep(2)
        
        # STEP 4: Fill form details (with correct images for this ad)
        image_set = self.ad1_images if ad_number == 1 else self.ad2_images
        await self.fill_ad_form(page, ad_data, image_set)
        
        # STEP 5: Submit
        await page.get_by_test_id("package-0-bottom-select").click()
        await asyncio.sleep(2)
        await page.get_by_test_id("checkout-post-btn").click()
        await asyncio.sleep(5)
        
        print(f"   ✅ Ad #{ad_number} posted successfully!")
        await page.screenshot(path=f'screenshots/03-ad{ad_number}-posted-{datetime.now().strftime("%H%M%S")}.png')
        
    async def fill_ad_form(self, page, ad_data, image_files):
        """Fill the ad form with details"""
        print("   📋 Filling form details...")
        
        # Set furnished to Yes (from recording)
        await page.get_by_role("listitem").filter(has_text="Furnished: (optional) Yes No").locator("label").nth(2).click()
        await asyncio.sleep(1)
        
        # Set additional room option (from recording)
        await page.locator("li:nth-child(6) > .radio-button-container > .form-section > label:nth-child(2) > .radio-button-rd").click()
        await asyncio.sleep(1)
        
        # Fill description
        await page.get_by_role("textbox", name="Description:").click()
        await page.get_by_role("textbox", name="Description:").fill(ad_data['description'])
        await asyncio.sleep(1)
        
        # Add tags
        for tag in ad_data['tags'][:5]:  # Max 5 tags
            await page.get_by_role("textbox", name="Tags: (optional)").click()
            await page.get_by_role("textbox", name="Tags: (optional)").fill(tag)
            await page.get_by_role("button", name="Add").click()
            await asyncio.sleep(0.5)
        
        # Upload images for this specific ad
        try:
            existing_images = [img for img in image_files if os.path.exists(img)]
            if existing_images:
                print(f"   📸 Uploading {len(existing_images)} unique images for this ad...")
                
                # Direct upload without clicking - find the hidden file input
                file_input = page.locator('input[type="file"]')
                await file_input.set_input_files(existing_images)
                await asyncio.sleep(5)  # More time for upload
                
                print(f"   ✅ Successfully uploaded {len(existing_images)} images")
            else:
                ad_folder = image_files[0].split('/')[1] if image_files else "ad1"
                print(f"   ⚠️ No images found for this ad!")
                print(f"   💡 Add photos to 'images/{ad_folder}/' folder")
                print(f"   Expected files: {', '.join([f.split('/')[-1] for f in image_files])}")
        except Exception as e:
            print(f"   ⚠️ Image upload failed: {e}")
            print(f"   💡 Tip: Make sure image files exist and are under 10MB each")
        
        # Set location (from recording)
        await page.locator("#location").click()
        await page.locator("#location").fill("138 Chillery A")
        await asyncio.sleep(1)
        await page.get_by_role("option", name="138 Chillery Avenue,").click()
        await page.locator("#FESLocationModuleWrapper span").first.click()
        await asyncio.sleep(1)
        
        # Set price
        await page.locator("#PriceAmount").click()
        await page.locator("#PriceAmount").fill(ad_data['price'])
        await asyncio.sleep(1)
        
        # Set phone
        await page.get_by_role("textbox", name="e.g. 123 456").click()
        await page.get_by_role("textbox", name="e.g. 123 456").fill(ad_data['phone'])
        await asyncio.sleep(1)
        
        print("   ✅ Form completed")
        
    async def run_automation(self):
        """Run the complete dual posting automation"""
        print("🤖 Starting Kijiji Dual Room Posting Automation")
        print("=" * 55)
        print(f"Username: {self.username}")
        print(f"Ad 1: {self.ad1['title']} - ${self.ad1['price']}")
        print(f"Ad 2: {self.ad2['title']} - ${self.ad2['price']}")
        print(f"Headless: {self.headless}")
        print()
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=self.headless,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = await context.new_page()
            
            try:
                # Step 1: Login
                await self.login(page)
                
                # Step 2: Delete existing ads
                await self.delete_existing_ads(page)
                
                # Step 3: Post first ad
                await self.post_ad(page, self.ad1, 1)
                
                # Step 4: Post second ad  
                await self.post_ad(page, self.ad2, 2)
                
                print("\n🎉 Dual Posting Automation Completed Successfully!")
                print("✅ All old ads deleted")
                print("✅ Ad 1 posted: Shared Basement Room - $500")
                print("✅ Ad 2 posted: Student Rental - $450")
                
                await page.screenshot(path=f'screenshots/04-final-success-{datetime.now().strftime("%H%M%S")}.png')
                
            except Exception as e:
                print(f"\n❌ Error during automation: {e}")
                await page.screenshot(path=f'screenshots/error-{datetime.now().strftime("%H%M%S")}.png')
                raise
                
            finally:
                if not self.headless:
                    print("\n⏱️ Keeping browser open for 5 seconds...")
                    await asyncio.sleep(5)
                
                await context.close()
                await browser.close()

async def main():
    automation = KijijiDualPosting()
    await automation.run_automation()

if __name__ == "__main__":
    asyncio.run(main()) 