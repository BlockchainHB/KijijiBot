# 🏗️ KijijiBot Project Architecture

**Technical documentation for the Kijiji room rental automation system**

---

## 📊 System Overview

KijijiBot is a web automation tool built with Python and Playwright that automatically manages Kijiji room rental listings. The system implements a sophisticated dual-ad strategy to maximize visibility and target different market segments.

### Core Architecture Components

```
┌─────────────────────────────────────────────────────────────┐
│                    KijijiBot System                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │Configuration│  │ Web Browser │  │Image Manager│       │
│  │   Manager   │  │ Automation  │  │             │       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
│         │                 │                 │             │
│         └─────────────────┼─────────────────┘             │
│                           │                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │  Scheduler  │  │    Kijiji   │  │  Logging &  │       │
│  │  Manager    │  │ API Handler │  │Screenshots  │       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Dual Ad Strategy Architecture

### Strategic Market Segmentation

The system posts two distinct ads targeting different demographics:

```
┌─────────────────┐              ┌─────────────────┐
│   Professional  │              │    Student      │
│      Ad (#1)    │              │     Ad (#2)     │
├─────────────────┤              ├─────────────────┤
│ Price: $500     │              │ Price: $450     │
│ Target: Workers │              │ Target: Students│
│ Focus: Quality  │              │ Focus: Budget   │
│ Images: 6 Pro   │              │ Images: 6 Casual│
└─────────────────┘              └─────────────────┘
         │                                │
         └────────────┬───────────────────┘
                      │
              ┌───────▼────────┐
              │  Same Physical │
              │      Room      │
              │ (Different     │
              │  Marketing)    │
              └────────────────┘
```

### Content Differentiation Strategy

| Aspect | Professional Ad | Student Ad |
|--------|----------------|------------|
| **Price Point** | $500/month | $450/month |
| **Language Tone** | Professional, formal | Casual, student-friendly |
| **Key Features** | Work-from-home setup, quiet environment | Study space, near campus |
| **Target Keywords** | "professional", "furnished", "utilities" | "student", "TTC", "college" |
| **Photo Style** | Clean, organized, business-like | Comfortable, lived-in, academic |

---

## 🔧 Technical Implementation

### Core Technologies

- **Python 3.11+**: Main programming language
- **Playwright**: Web browser automation framework
- **Asyncio**: Asynchronous programming for non-blocking operations
- **JSON**: Configuration and data serialization
- **Chromium**: Headless browser engine

### File Structure Deep Dive

```
KijijiBot/
├── Core Application Files
│   ├── kijiji_dual_posting.py      # Main automation engine (400+ lines)
│   ├── daily_scheduler.py          # Cron job automation wrapper
│   └── setup_images.py             # Image organization helper
│
├── Configuration & Documentation
│   ├── config.example.json         # Template configuration
│   ├── test_input.json            # User credentials (gitignored)
│   ├── requirements.txt           # Python dependencies
│   ├── README.md                  # User documentation  
│   ├── SETUP_GUIDE.md            # Beginner-friendly setup
│   └── PROJECT_ARCHITECTURE.md    # This technical document
│
├── Media Assets
│   ├── images/
│   │   ├── ad1/                   # Professional-focused photos
│   │   │   ├── room_main.png      # Primary room view
│   │   │   ├── bed_area.png       # Sleeping area
│   │   │   ├── workspace.png      # Work/study space
│   │   │   ├── kitchen.png        # Kitchen access
│   │   │   ├── bathroom.png       # Bathroom facilities
│   │   │   └── exterior.png       # Building exterior
│   │   └── ad2/                   # Student-focused photos  
│   │       ├── room_study.png     # Study-focused room view
│   │       ├── bed_desk.png       # Bed + desk combination
│   │       ├── living_space.png   # Common areas
│   │       ├── kitchen_shared.png # Shared kitchen view
│   │       ├── bathroom_clean.png # Student-appropriate bathroom
│   │       └── building.png       # Building exterior (different angle)
│   └── screenshots/               # Automation progress logs
│       ├── 01-login-HHMMSS.png    # Login verification
│       ├── 02-my-ads-HHMMSS.png   # Current ads before deletion
│       ├── 03-ad1-posted-HHMMSS.png # First ad completion
│       ├── 03-ad2-posted-HHMMSS.png # Second ad completion
│       └── 04-final-success-HHMMSS.png # Overall success
│
└── Version Control
    ├── .gitignore                 # Security exclusions
    └── .git/                      # Git repository data
```

---

## 🔐 Security Architecture

### Credential Management

```python
# Configuration Loading Pattern
{
    "username": "user@email.com",    # Kijiji account email
    "password": "secure_password",   # Account password  
    "headless": false,              # Browser visibility toggle
    "location": "Address, City",    # Rental location
    "phone": "XXX-XXX-XXXX"        # Contact number
}
```

### Security Measures

1. **Gitignore Protection**: Sensitive files automatically excluded from version control
2. **Local Storage Only**: Credentials never transmitted except to Kijiji
3. **Environment Isolation**: Virtual environment prevents system conflicts
4. **Access Logging**: Screenshot evidence of all automation actions
5. **Error Handling**: Graceful failure without exposing sensitive data

---

## 🌐 Web Automation Architecture

### Playwright Framework Integration

```python
# Browser Initialization Pattern
async with async_playwright() as p:
    browser = await p.chromium.launch(
        headless=self.headless,                              # Visibility control
        args=['--disable-blink-features=AutomationControlled'] # Anti-detection
    )
    
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},            # Standard resolution
        user_agent='Mozilla/5.0 ...'                        # Human-like UA
    )
```

### Selector Strategy

The automation uses multiple selector strategies for robustness:

| Strategy | Example | Purpose |
|----------|---------|---------|
| **Role-based** | `get_by_role("textbox", name="Email")` | Natural language selectors |
| **Test ID** | `get_by_test_id("header-link-post-ad")` | Stable automation targets |
| **CSS Selector** | `locator("#PriceAmount")` | Direct element targeting |
| **Text-based** | `get_by_text("Room Rentals")` | Content-based selection |

### Anti-Detection Measures

1. **Human-like Timing**: Random delays between actions
2. **Natural Navigation**: Tab key usage, proper click sequences  
3. **Browser Fingerprinting**: Standard user agent and viewport
4. **Error Recovery**: Graceful handling of failed operations

---

## 📸 Image Management System

### File Organization Strategy

```
images/
├── ad1/ (Professional Focus)
│   ├── Strategic naming for professional market
│   ├── Clean, organized photo composition
│   └── Work-from-home friendly staging
└── ad2/ (Student Focus)
    ├── Student-oriented naming convention
    ├── Casual, comfortable photo composition  
    └── Study-focused staging emphasis
```

### Upload Architecture

```python
# Direct Upload Pattern (No Visual File Picker)
async def upload_images(self, page, image_files):
    """
    Direct file upload without triggering visual file picker
    """
    # Find hidden file input element
    file_input = page.locator('input[type="file"]')
    
    # Upload directly to hidden input
    await file_input.set_input_files(existing_images)
    
    # Wait for upload completion
    await asyncio.sleep(5)
```

### Image Optimization Requirements

- **Format**: PNG or JPG only
- **Size Limit**: 10MB per file maximum
- **Quantity**: Exactly 6 photos per ad (12 total)
- **Uniqueness**: Different angles/staging per ad set
- **Quality**: High resolution for professional appearance

---

## 🔄 Automation Workflow Engine

### Main Execution Flow

```python
async def run_automation(self):
    """
    Main automation orchestrator
    """
    # Phase 1: Browser Initialization
    └── Launch browser with anti-detection settings
    └── Create isolated browser context
    └── Initialize page object
    
    # Phase 2: Authentication  
    └── Navigate to Kijiji login
    └── Input credentials from config
    └── Verify successful authentication
    
    # Phase 3: Cleanup (Deletion)
    └── Navigate to "My Ads" section
    └── Scan for existing listings
    └── Delete all found ads individually
    
    # Phase 4: Content Creation (Posting)
    └── Post Professional Ad (#1)
        ├── Fill form with professional content
        ├── Upload ad1 image set
        └── Submit and verify
    └── Post Student Ad (#2)  
        ├── Fill form with student content
        ├── Upload ad2 image set
        └── Submit and verify
        
    # Phase 5: Verification & Cleanup
    └── Take final success screenshots
    └── Log completion status
    └── Close browser and cleanup
```

### Error Handling Strategy

```python
# Multi-level Error Recovery
try:
    # Primary operation
    await main_automation_task()
except SpecificKijijiError as e:
    # Handle known Kijiji issues
    await handle_kijiji_specific_error(e)
except PlaywrightTimeoutError as e:
    # Handle browser timeout issues
    await handle_timeout_gracefully(e)
except Exception as e:
    # General error handling with screenshots
    await capture_error_state(e)
    raise
finally:
    # Always cleanup resources
    await ensure_browser_cleanup()
```

---

## ⏰ Scheduling Architecture

### Cron Integration (Unix/macOS)

```bash
# Daily automation at 9 AM
0 9 * * * cd /path/to/KijijiBot && source venv/bin/activate && python kijiji_dual_posting.py
```

### Windows Task Scheduler Integration

```python
# daily_scheduler.py - Windows automation wrapper
import schedule
import subprocess
import os

def run_kijiji_automation():
    """Execute automation in proper environment"""
    os.chdir('/path/to/KijijiBot')
    subprocess.run(['python', 'kijiji_dual_posting.py'])

# Schedule daily execution
schedule.every().day.at("09:00").do(run_kijiji_automation)
```

### Scheduling Considerations

- **Optimal Timing**: 9 AM posts catch morning searches
- **Frequency**: Daily posting for maximum visibility
- **Error Recovery**: Automated retry logic for failed runs
- **Logging**: Comprehensive logs for monitoring automation health

---

## 📊 Monitoring & Logging System

### Screenshot Documentation

The system automatically captures screenshots at key stages:

1. **01-login-HHMMSS.png**: Login verification
2. **02-my-ads-HHMMSS.png**: Pre-deletion state
3. **03-ad1-posted-HHMMSS.png**: First ad success  
4. **03-ad2-posted-HHMMSS.png**: Second ad success
5. **04-final-success-HHMMSS.png**: Complete workflow success
6. **error-HHMMSS.png**: Any error states

### Console Logging Pattern

```
🤖 Starting Kijiji Dual Room Posting Automation
=======================================================
Username: user@email.com
Ad 1: Furnished Basement Room Scarborough - $500
Ad 2: Shared Student Room Rental Near TTC - $450
Headless: False

🔐 Logging in to Kijiji...
   ✅ Login successful!

🗑️  Deleting existing ads...
   Scanning for existing ads...
   Found 2 ads to delete: ['listing-id-1234', 'listing-id-5678']
   ✅ Ad 1 deleted: listing-id-1234
   ✅ Ad 2 deleted: listing-id-5678
   ✅ Total ads deleted: 2

📝 Posting Ad #1: Furnished Basement Room Scarborough
   📋 Filling form details...
   📸 Uploading 6 unique images for this ad...
   ✅ Successfully uploaded 6 images
   ✅ Form completed
   ✅ Ad #1 posted successfully!

📝 Posting Ad #2: Shared Student Room Rental Near TTC
   📋 Filling form details...
   📸 Uploading 6 unique images for this ad...
   ✅ Successfully uploaded 6 images
   ✅ Form completed
   ✅ Ad #2 posted successfully!

🎉 Dual Posting Automation Completed Successfully!
✅ All old ads deleted
✅ Ad 1 posted: Shared Basement Room - $500
✅ Ad 2 posted: Student Rental - $450
```

---

## 🔍 Performance Optimization

### Speed Optimizations

1. **Asynchronous Operations**: Non-blocking I/O for better performance
2. **Selective Waiting**: Strategic sleep timing to minimize delays
3. **Direct Element Access**: Efficient selector strategies
4. **Resource Management**: Proper browser cleanup and memory management

### Reliability Optimizations

1. **Element Waiting**: Robust wait conditions for dynamic content
2. **Retry Logic**: Automatic retry for transient failures
3. **Error Isolation**: Compartmentalized error handling
4. **Graceful Degradation**: Continue operation despite minor failures

### Resource Management

```python
# Proper Resource Cleanup Pattern
async def run_automation(self):
    browser = None
    try:
        browser = await p.chromium.launch(...)
        # ... automation logic ...
    except Exception as e:
        # Error handling
        await capture_error_state(e)
        raise
    finally:
        # Always cleanup, even on errors
        if browser:
            await browser.close()
```

---

## 🚀 Deployment Architecture

### Environment Requirements

```python
# requirements.txt - Dependency Management
playwright==1.40.0      # Web automation framework
asyncio                  # Asynchronous programming (built-in)
json                     # Configuration handling (built-in)
os                       # File system operations (built-in)
datetime                 # Timestamp generation (built-in)
```

### Virtual Environment Isolation

```bash
# Environment Setup Pattern
python3 -m venv venv                    # Create isolated environment
source venv/bin/activate                # Activate environment (Unix)
venv\Scripts\activate                   # Activate environment (Windows)
pip install -r requirements.txt        # Install dependencies
playwright install chromium            # Install browser engine
```

### Cross-Platform Compatibility

| Platform | Command Syntax | Path Separators | Special Considerations |
|----------|---------------|-----------------|----------------------|
| **macOS** | `source venv/bin/activate` | `/` | Homebrew for Python |
| **Linux** | `source venv/bin/activate` | `/` | Package manager variants |
| **Windows** | `venv\Scripts\activate` | `\` | PATH configuration critical |

---

## 🛠️ Development Architecture

### Code Organization Principles

1. **Single Responsibility**: Each method handles one specific task
2. **Async/Await Pattern**: Consistent asynchronous programming
3. **Error Handling**: Comprehensive try/catch blocks
4. **Documentation**: Extensive inline comments and docstrings
5. **Modularity**: Separate concerns into distinct methods

### Extension Points

The architecture supports easy customization:

```python
# Ad Content Customization
self.ad1 = {
    'title': 'Your Custom Title',           # ← Easily customizable
    'description': 'Your Description',      # ← Rich text supported
    'price': '500',                        # ← Dynamic pricing
    'tags': ['your', 'keywords'],         # ← SEO optimization
    'phone': 'XXX-XXX-XXXX'              # ← Contact information
}

# Image Set Customization  
self.ad1_images = [
    "images/ad1/your_photo1.png",         # ← Custom photo sets
    "images/ad1/your_photo2.png",         # ← Different per ad
    # ... up to 6 photos per ad
]
```

### Testing Strategy

```python
# Manual Testing Pattern
if __name__ == "__main__":
    # Direct execution for development testing
    automation = KijijiDualPosting()
    await automation.run_automation()

# Production Pattern  
# Scheduled execution via cron/task scheduler
```

---

## 📈 Scalability Considerations

### Horizontal Scaling

- **Multiple Properties**: Each property can have its own bot instance
- **Staggered Timing**: Different properties post at different times
- **Separate Credentials**: Each bot uses its own Kijiji account

### Vertical Scaling

- **Resource Optimization**: Minimal memory and CPU footprint
- **Browser Reuse**: Single browser instance for multiple operations
- **Image Compression**: Optimize image sizes for faster uploads

### Monitoring at Scale

```python
# Logging Architecture for Multiple Bots
logs/
├── property1/
│   ├── 2024-01-15-success.log
│   └── 2024-01-15-screenshots/
├── property2/
│   ├── 2024-01-15-success.log  
│   └── 2024-01-15-screenshots/
└── summary/
    └── daily-report-2024-01-15.log
```

---

## 🔐 Security Deep Dive

### Credential Security

```python
# Secure Configuration Pattern
{
    "username": "encrypted_or_env_var",      # Never in version control
    "password": "encrypted_or_env_var",      # Secured at rest
    "headless": true,                       # Production hiding
    "location": "public_address_only",       # No personal details
    "phone": "business_number_only"         # Professional contact only
}
```

### Browser Security

1. **Incognito Mode**: No persistent cookies or data
2. **Custom User Agent**: Appears as regular browser traffic
3. **Anti-Fingerprinting**: Standard viewport and settings
4. **Session Isolation**: Each run is independent

### Network Security

- **HTTPS Only**: All Kijiji communication encrypted
- **No Data Storage**: No persistent local data beyond config
- **Minimal Footprint**: Only necessary network requests
- **Rate Limiting**: Human-like posting frequency

---

## 🎯 SEO & Content Strategy Architecture

### Keyword Optimization

```python
# Strategic Keyword Distribution
ad1_keywords = [
    'furnished',        # High-value rental feature
    'basement',         # Specific room type
    'scarborough',      # Location targeting  
    'inclusive',        # Price positioning
    'utilities'         # Cost benefit
]

ad2_keywords = [
    'student',          # Demographic targeting
    'furnished',        # Shared high-value keyword
    'ttc',             # Transit accessibility
    'scarborough',      # Location consistency
    'college'          # Education proximity
]
```

### Content Differentiation Matrix

| Element | Professional Ad Strategy | Student Ad Strategy |
|---------|-------------------------|-------------------|
| **Price** | Premium positioning ($500) | Budget-conscious ($450) |
| **Language** | Formal, business-oriented | Casual, relatable |
| **Features** | Work-from-home, quiet | Study space, transit |
| **Benefits** | Quality, convenience | Affordability, location |
| **Call-to-Action** | Professional contact | Text-friendly approach |

---

## 📊 Analytics & Optimization

### Performance Metrics

```python
# Trackable Success Metrics
success_indicators = {
    'ads_posted': 2,                    # Daily posting count
    'old_ads_deleted': 'variable',      # Cleanup efficiency  
    'images_uploaded': 12,              # Content richness
    'automation_time': '< 5 minutes',   # Execution efficiency
    'error_rate': '< 5%',              # Reliability metric
    'uptime': '> 95%'                  # Availability metric
}
```

### Optimization Opportunities

1. **Content A/B Testing**: Rotate descriptions monthly
2. **Price Optimization**: Market-responsive pricing
3. **Timing Analysis**: Optimal posting times
4. **Keyword Performance**: Tag effectiveness tracking
5. **Image Performance**: Photo engagement analysis

---

## 🔄 Maintenance Architecture

### Regular Maintenance Tasks

```python
# Monthly Maintenance Checklist
maintenance_tasks = [
    'Update ad descriptions for seasonality',
    'Refresh photo sets with new angles',
    'Verify Kijiji selector stability',
    'Check automation error rates',
    'Update market pricing analysis',
    'Review screenshot logs for issues',
    'Test manual backup procedures'
]
```

### Troubleshooting Framework

```python
# Diagnostic Priority Matrix
if login_fails:
    check_credentials() → check_2fa() → check_account_status()
elif images_fail:
    verify_file_paths() → check_file_sizes() → test_upload_manually()
elif posts_fail:
    check_kijiji_limits() → verify_content_policy() → test_single_post()
elif automation_hangs:
    check_selectors() → verify_network() → update_browser()
```

---

## 🌟 Future Architecture Considerations

### Planned Enhancements

1. **Multi-Platform Support**: Facebook Marketplace, Craigslist integration
2. **AI Content Generation**: Dynamic description optimization
3. **Market Analysis**: Automatic price adjustment based on competition
4. **Performance Dashboard**: Web-based monitoring interface
5. **Mobile App**: Remote monitoring and control

### Architectural Expansion

```
Current Architecture:
KijijiBot → Single Platform → Dual Ads → Static Content

Future Architecture:
RentalBot → Multi-Platform → Dynamic Ads → AI-Generated Content
    ├── Kijiji Module
    ├── Facebook Module  
    ├── Craigslist Module
    └── Analytics Module
```

---

## 📚 Technical Resources

### Core Dependencies Documentation

- **Playwright**: https://playwright.dev/python/
- **Python Asyncio**: https://docs.python.org/3/library/asyncio.html
- **JSON Handling**: https://docs.python.org/3/library/json.html

### Kijiji-Specific Resources

- **Terms of Service**: https://www.kijiji.ca/t-terms-of-use.html
- **Posting Guidelines**: https://help.kijiji.ca/helpdesk/posting/
- **API Limitations**: https://developers.kijiji.ca/

### Automation Best Practices

- **Web Automation Ethics**: Respect rate limits and ToS
- **Anti-Detection**: Human-like behavior patterns
- **Error Handling**: Graceful failure and recovery
- **Security**: Credential protection and data privacy

---

**This architecture document provides a comprehensive technical overview of the KijijiBot system. For implementation details, refer to the heavily commented source code in `kijiji_dual_posting.py`.** 