"""
Kijiji Dual Room Rental Automation Script
=========================================

This script automates the process of posting room rental ads on Kijiji.ca
It implements a dual-ad strategy, posting 2 unique ads targeting different audiences:
- Ad 1: Targets working professionals ($500/month)
- Ad 2: Targets students ($450/month)

Features:
- Automatic login to Kijiji
- Deletion of existing ads to avoid duplicates
- Posting of 2 optimized ads with unique content
- Silent image upload (no visual file picker)
- Screenshot logging for debugging
- Ready for daily automation via cron/scheduler

Author: Built with ❤️ using Playwright and Python
Repository: https://github.com/BlockchainHB/KijijiBot
"""

# Import required libraries
import asyncio          # For asynchronous operations (waiting, delays)
import json            # For reading configuration files
import os              # For file system operations (creating directories)
from datetime import datetime    # For timestamps in screenshots and logs
from playwright.async_api import async_playwright  # Web automation library

class KijijiDualPosting:
    """
    Main automation class for Kijiji dual room rental posting.
    
    This class handles:
    1. Configuration loading from JSON file
    2. Browser automation using Playwright
    3. Kijiji login and navigation
    4. Ad deletion and posting workflow
    5. Image upload management
    6. Error handling and screenshot logging
    """
    
    def __init__(self, config_file='test_input.json'):
        """
        Initialize the automation with configuration settings.
        
        Args:
            config_file (str): Path to JSON config file containing login credentials
        
        The config file should contain:
        - username: Kijiji email address
        - password: Kijiji password  
        - headless: Boolean (True for background mode, False to see browser)
        """
        # Load configuration from JSON file
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Extract login credentials from config
        self.username = self.config.get('username')
        self.password = self.config.get('password')
        self.headless = self.config.get('headless', False)  # Default to visible browser
        
        # =================================================================
        # AD CONFIGURATION - CUSTOMIZE THESE FOR YOUR ROOM
        # =================================================================
        
        # Ad 1: Professional-focused listing targeting working professionals
        # This ad uses higher price point and professional language
        self.ad1 = {
            'title': 'Furnished Basement Room Scarborough',  # 54 chars (under 100 limit)
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
            'price': '500',  # Higher price for professional market
            'tags': ['furnished', 'basement', 'scarborough', 'inclusive', 'utilities'],  # SEO keywords
            'location': '138 Chillery Avenue',
            'phone': '647-607-4050'
        }
        
        # Ad 2: Student-focused listing targeting college/university students  
        # This ad uses lower price point and student-friendly language
        self.ad2 = {
            'title': 'Shared Student Room Rental Near TTC',  # 55 chars (under 100 limit)
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
            'price': '450',  # Lower price for student market
            'tags': ['student', 'furnished', 'ttc', 'scarborough', 'college'],  # Student-focused keywords
            'location': '138 Chillery Avenue',
            'phone': '647-607-4050'
        }
        
        # =================================================================
        # IMAGE CONFIGURATION - SEPARATE PHOTOS FOR EACH AD
        # =================================================================
        
        # IMPORTANT: Each ad uses different photos to avoid Kijiji's duplicate content detection
        # Take the same room from different angles or with different staging for each ad
        
        # Images for Ad 1 (Professional focus) - stored in images/ad1/ folder
        self.ad1_images = [
            "images/ad1/room_main.png",      # Main room view - professional staging
            "images/ad1/bed_area.png",       # Bed area - clean, professional setup  
            "images/ad1/workspace.png",      # Desk/work area - work-from-home focused
            "images/ad1/kitchen.png",        # Kitchen access - angle 1
            "images/ad1/bathroom.png",       # Bathroom - angle 1, clean/modern
            "images/ad1/exterior.png"        # House/building exterior - angle 1
        ]
        
        # Images for Ad 2 (Student focus) - stored in images/ad2/ folder
        self.ad2_images = [
            "images/ad2/room_study.png",     # Same room - student/study staging
            "images/ad2/bed_desk.png",       # Bed + desk combo view for students
            "images/ad2/living_space.png",   # Common area - casual, student-friendly
            "images/ad2/kitchen_shared.png", # Kitchen access - angle 2, shared focus
            "images/ad2/bathroom_clean.png", # Bathroom - angle 2, student-appropriate
            "images/ad2/building.png"        # Building exterior - angle 2
        ]
        
        # =================================================================
        # DIRECTORY SETUP - CREATE REQUIRED FOLDERS
        # =================================================================
        
        # Create necessary directories if they don't exist
        # exist_ok=True prevents errors if directories already exist
        os.makedirs('screenshots', exist_ok=True)    # For automation progress screenshots
        os.makedirs('images/ad1', exist_ok=True)     # For professional ad photos  
        os.makedirs('images/ad2', exist_ok=True)     # For student ad photos
        
    async def login(self, page):
        """
        Handle Kijiji login process.
        
        This method:
        1. Navigates to Kijiji login page
        2. Fills in username and password from config
        3. Submits login form
        4. Waits for successful redirect
        5. Takes screenshot for verification
        
        Args:
            page: Playwright page object for browser interaction
            
        Raises:
            Exception: If login fails or times out
        """
        print("🔐 Logging in to Kijiji...")
        
        # Kijiji's OAuth login URL - this ensures we get redirected to main site after login
        login_url = "https://id.kijiji.ca/login?service=https%3A%2F%2Fid.kijiji.ca%2Foauth2.0%2FcallbackAuthorize%3Fclient_id%3Dkijiji_horizontal_web_gpmPihV3%26redirect_uri%3Dhttps%253A%252F%252Fwww.kijiji.ca%252Fapi%252Fauth%252Fcallback%252Fcis%26response_type%3Dcode%26client_name%3DCasOAuthClient&locale=en&scope=openid+email+profile"
        
        # Navigate to login page and wait for network to be idle (page fully loaded)
        await page.goto(login_url, wait_until='networkidle')
        await asyncio.sleep(2)  # Additional wait for any dynamic content
        
        # Step 1: Enter email address
        # Using get_by_role for more reliable element selection than CSS selectors
        await page.get_by_role("textbox", name="Email Address").click()
        await page.get_by_role("textbox", name="Email Address").fill(self.username)
        
        # Step 2: Tab to password field (mimics human behavior)
        await page.get_by_role("textbox", name="Email Address").press("Tab")
        await page.get_by_role("link", name="Forgot Password?").press("Tab")
        
        # Step 3: Enter password and submit
        await page.get_by_role("textbox", name="Password").fill(self.password)
        await page.get_by_role("button", name="Sign in").click()
        
        # Step 4: Wait for successful login redirect to main Kijiji site
        # The ** pattern matches any path under kijiji.ca
        await page.wait_for_url('https://www.kijiji.ca/**', timeout=30000)
        await asyncio.sleep(3)  # Allow page to fully load after redirect
        
        print("   ✅ Login successful!")
        # Take screenshot for verification/debugging - timestamp prevents filename conflicts
        await page.screenshot(path=f'screenshots/01-login-{datetime.now().strftime("%H%M%S")}.png')
        
    async def delete_existing_ads(self, page):
        """
        Delete all existing ads from the user's account.
        
        This is crucial to avoid duplicate content issues on Kijiji.
        The method:
        1. Navigates to "My Ads" section
        2. Scans for all existing listings
        3. Deletes each ad individually
        4. Confirms deletion and closes modals
        
        Args:
            page: Playwright page object for browser interaction
            
        Note: 
            - Prevents infinite loops by collecting all IDs first, then deleting
            - Uses try/catch for each deletion to continue if one fails
            - Takes screenshot for debugging
        """
        print("🗑️  Deleting existing ads...")
        
        # =================================================================
        # STEP 1: NAVIGATE TO "MY ADS" SECTION
        # =================================================================
        
        # Click "My Account" dropdown in header
        await page.get_by_role("button", name="My Account").click()
        await asyncio.sleep(1)  # Wait for dropdown to appear
        
        # Click "My Ads" link in dropdown menu
        await page.get_by_role("link", name="My Ads").click()
        await asyncio.sleep(3)  # Wait for ads page to load completely
        
        # Take screenshot of current ads before deletion
        await page.screenshot(path=f'screenshots/02-my-ads-{datetime.now().strftime("%H%M%S")}.png')
        
        # =================================================================
        # STEP 2: SCAN FOR EXISTING ADS
        # =================================================================
        
        print("   Scanning for existing ads...")
        
        try:
            # Find all ad elements using data-testid attribute
            # Kijiji uses test IDs like "listing-id-1234567890" for each ad
            listing_elements = await page.query_selector_all('[data-testid^="listing-id-"]')
            listing_ids = []
            
            # Extract the actual test-id values from each element
            for element in listing_elements:
                test_id = await element.get_attribute('data-testid')
                if test_id and test_id.startswith('listing-id-'):
                    listing_ids.append(test_id)
            
            print(f"   Found {len(listing_ids)} ads to delete: {listing_ids}")
            
            # =================================================================
            # STEP 3: DELETE EACH AD INDIVIDUALLY  
            # =================================================================
            
            # IMPORTANT: We collect all IDs first, then delete each one
            # This prevents infinite loops that could occur if we tried to
            # find and delete ads in the same loop (DOM changes during deletion)
            
            deleted_count = 0
            for listing_id in listing_ids:
                try:
                    print(f"   Deleting ad: {listing_id}")
                    
                    # Find and click the delete button for this specific listing
                    # Each ad has its own delete button with adDeleteButton test-id
                    delete_button = page.get_by_test_id(listing_id).get_by_test_id("adDeleteButton")
                    await delete_button.click()
                    await asyncio.sleep(1)  # Wait for delete confirmation modal
                    
                    # Kijiji requires a reason for deletion - we select "Prefer not to say"
                    await page.get_by_role("button", name="Prefer not to say").click()
                    await asyncio.sleep(1)
                    
                    # Confirm the deletion
                    await page.get_by_role("button", name="Delete My Ad").click()
                    await asyncio.sleep(2)  # Wait for deletion to process
                    
                    # Close the confirmation modal that appears after deletion
                    await page.get_by_test_id("ModalCloseButton").click()
                    await asyncio.sleep(2)  # Wait for modal to close and page to update
                    
                    deleted_count += 1
                    print(f"   ✅ Ad {deleted_count} deleted: {listing_id}")
                    
                except Exception as e:
                    # If one ad fails to delete, log the error but continue with others
                    print(f"   ⚠️ Failed to delete {listing_id}: {e}")
                    continue
                    
            print(f"   ✅ Total ads deleted: {deleted_count}")
            
        except Exception as e:
            # Handle case where no ads exist or scanning fails
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