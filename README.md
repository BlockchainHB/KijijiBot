# KijijiBot - Automated Room Rental Posting

🤖 An intelligent Playwright-based automation tool for posting room rental ads on Kijiji. Automatically deletes old listings and posts fresh, optimized ads daily.

## 🌟 Features

- **Dual Ad Strategy**: Posts 2 unique ads targeting different audiences (professionals & students)
- **Smart Content**: SEO-optimized titles and descriptions with character limit compliance
- **Image Management**: Separate photo sets for each ad to avoid duplicate content detection
- **Automated Deletion**: Removes old listings before posting new ones
- **Direct Upload**: Silent image upload without visual file picker popups
- **Scheduler Ready**: Perfect for daily automation with cron jobs
- **Screenshot Logging**: Captures automation progress for debugging

## 🎯 Ad Strategy

### Ad 1: Professional Focus
- **Target**: Working professionals
- **Price**: $500/month
- **Title**: "Furnished Basement Room Scarborough"
- **Focus**: Professional amenities, work-from-home setup

### Ad 2: Student Focus  
- **Target**: College/university students
- **Price**: $450/month
- **Title**: "Shared Student Room Rental Near TTC"
- **Focus**: Student-friendly features, transit access

## 📁 Project Structure

```
KijijiBot/
├── kijiji_dual_posting.py    # Main automation script
├── daily_scheduler.py        # Cron job scheduler
├── setup_images.py          # Image organization helper
├── requirements.txt         # Python dependencies
├── config.example.json      # Configuration template
├── images/
│   ├── ad1/                 # Professional-focused photos
│   │   ├── room_main.png
│   │   ├── workspace.png
│   │   └── ...
│   └── ad2/                 # Student-focused photos
│       ├── room_study.png
│       ├── bed_desk.png
│       └── ...
└── screenshots/             # Automation progress logs
```

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/BlockchainHB/KijijiBot.git
cd KijijiBot
```

### 2. Setup Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

### 3. Configure Credentials
```bash
cp config.example.json test_input.json
```

Edit `test_input.json` with your Kijiji credentials:
```json
{
    "username": "your-email@domain.com",
    "password": "your-password",
    "headless": false
}
```

### 4. Add Photos
```bash
python setup_images.py
```
Follow the prompts to organize your room photos into `images/ad1/` and `images/ad2/` folders.

### 5. Run Automation
```bash
python kijiji_dual_posting.py
```

## 📸 Image Requirements

- **Format**: PNG or JPG
- **Size**: Under 10MB each
- **Quantity**: 6 photos per ad (12 total)
- **Organization**: Separate folders for each ad to avoid duplicate detection

### Required Photos:
- Room main view
- Bed/sleeping area  
- Workspace/study area
- Kitchen access
- Bathroom
- Exterior/building

## ⚙️ Configuration Options

### Main Script Settings
```python
# In kijiji_dual_posting.py
self.headless = False  # Set to True for background running
```

### Ad Customization
Edit the `ad1` and `ad2` dictionaries in `kijiji_dual_posting.py`:
- Title (max 100 characters)
- Description (max 4000 characters)  
- Price
- Tags (max 5 tags)
- Contact information

## 🕐 Daily Automation

### Using Cron (macOS/Linux)
```bash
# Run daily at 9 AM
crontab -e

# Add this line:
0 9 * * * cd /path/to/KijijiBot && source venv/bin/activate && python kijiji_dual_posting.py
```

### Using Task Scheduler (Windows)
Use the included `daily_scheduler.py` for Windows task scheduling.

## 📊 Workflow Process

1. **Login** → Authenticate with Kijiji
2. **Scan** → Find existing room rental ads  
3. **Delete** → Remove old listings (prevents duplicates)
4. **Post Ad 1** → Professional-focused listing
5. **Post Ad 2** → Student-focused listing
6. **Screenshots** → Save progress for monitoring

## 🔧 Troubleshooting

### Common Issues

**Images not uploading:**
- Check file paths in `images/ad1/` and `images/ad2/`
- Ensure files are PNG format
- Verify file sizes under 10MB

**Login failures:**
- Update credentials in `test_input.json`
- Check for Kijiji login page changes
- Disable 2FA temporarily

**Element not found errors:**
- Kijiji may have updated their UI
- Check browser console for selector changes
- Update selectors in the script

### Debug Mode
```bash
# Run with browser visible for debugging
python kijiji_dual_posting.py
```

## 🛡️ Security Best Practices

- Keep `test_input.json` out of version control
- Use environment variables for production
- Enable 2FA on your Kijiji account (disable during automation)
- Monitor automation logs regularly

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## ⚠️ Disclaimer

This tool is for educational purposes. Users are responsible for:
- Complying with Kijiji's Terms of Service
- Following local rental advertising regulations  
- Ensuring posted content is accurate and legal
- Respecting rate limits and platform policies

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

- Create an issue for bug reports
- Check existing issues before posting
- Provide screenshots and error logs
- Include system information (OS, Python version)

---

**Built with ❤️ using Playwright and Python**