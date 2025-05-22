# 🚀 KijijiBot Setup Guide - For Beginners

**A step-by-step guide to set up automated Kijiji room rental posting, written for complete beginners.**

---

## 📋 What You'll Need

Before we start, make sure you have:
- ✅ A Mac or Windows computer
- ✅ A Kijiji account (create one at kijiji.ca if you don't have one)
- ✅ 12 photos of your room (6 different photos for each ad)
- ✅ About 30 minutes of setup time

---

## 🎯 What This Bot Does

This automation will:
1. **Login** to your Kijiji account
2. **Delete** any old room rental ads you have
3. **Post** 2 new ads with different prices targeting different people:
   - **Ad 1**: $500 for working professionals
   - **Ad 2**: $450 for students
4. **Upload** 6 different photos to each ad
5. **Run automatically** every day to keep your ads fresh

---

## 📱 Step 1: Download the Project

### Option A: Download ZIP (Easiest)
1. Go to: https://github.com/BlockchainHB/KijijiBot
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Extract the ZIP file to your Desktop
5. Rename the folder to just **"KijijiBot"**

### Option B: Use Git (If you know how)
```bash
git clone https://github.com/BlockchainHB/KijijiBot.git
cd KijijiBot
```

---

## 💻 Step 2: Install Python

### For Mac Users:
1. Open **Terminal** (press Cmd+Space, type "terminal", press Enter)
2. Type this command and press Enter:
   ```bash
   brew install python3
   ```
   If you get an error, first install Homebrew by copying this entire line:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

### For Windows Users:
1. Go to: https://www.python.org/downloads/
2. Download **Python 3.11** or newer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click **"Install Now"**

### Test Python Installation:
Open Terminal (Mac) or Command Prompt (Windows) and type:
```bash
python3 --version
```
You should see something like "Python 3.11.5"

---

## 📁 Step 3: Navigate to Your Project

1. Open Terminal (Mac) or Command Prompt (Windows)
2. Navigate to where you downloaded KijijiBot:

**Mac:**
```bash
cd Desktop/KijijiBot
```

**Windows:**
```bash
cd Desktop\KijijiBot
```

---

## 🏗️ Step 4: Set Up the Environment

Copy and paste these commands one by one:

### Create Virtual Environment:
```bash
python3 -m venv venv
```

### Activate Virtual Environment:

**Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` at the beginning of your command line now.

### Install Required Packages:
```bash
pip install -r requirements.txt
```

### Install Browser:
```bash
playwright install chromium
```

---

## 🔐 Step 5: Add Your Kijiji Login Information

1. In the KijijiBot folder, find the file called **`config.example.json`**
2. **Copy** this file
3. **Rename** the copy to **`test_input.json`**
4. Open **`test_input.json`** with any text editor (Notepad, TextEdit, etc.)
5. Replace the placeholder information:

```json
{
    "username": "youremail@gmail.com",
    "password": "YourKijijiPassword123",
    "headless": false,
    "location": "Your Street Address, Your City",
    "phone": "647-XXX-XXXX"
}
```

**Example:**
```json
{
    "username": "john.doe@gmail.com",
    "password": "MySecretPassword123",
    "headless": false,
    "location": "123 Main Street, Toronto",
    "phone": "647-555-1234"
}
```

**Important Security Notes:**
- ⚠️ **Never share this file with anyone**
- ⚠️ **This file contains your password**
- ✅ The file is automatically ignored by Git for safety

---

## 📸 Step 6: Add Your Room Photos

You need **12 total photos** (6 for each ad):

### Create Photo Folders:
The folders should already exist, but if not:
1. Go to the **`images`** folder in KijijiBot
2. Make sure you have these folders:
   - **`images/ad1/`** (for professional ad)
   - **`images/ad2/`** (for student ad)

### Add Photos for Ad 1 (Professional Ad):
Put these 6 photos in **`images/ad1/`**:
- **`room_main.png`** - Main room view (clean, professional-looking)
- **`bed_area.png`** - Bed area (neat, well-made bed)
- **`workspace.png`** - Desk/work area (good lighting, organized)
- **`kitchen.png`** - Kitchen access (clean, modern)
- **`bathroom.png`** - Bathroom (clean, well-lit)
- **`exterior.png`** - House exterior (nice neighborhood view)

### Add Photos for Ad 2 (Student Ad):
Put these 6 photos in **`images/ad2/`**:
- **`room_study.png`** - Room as study space (desk prominent)
- **`bed_desk.png`** - Bed and desk combo view
- **`living_space.png`** - Common living area (comfortable, casual)
- **`kitchen_shared.png`** - Shared kitchen (student-friendly)
- **`bathroom_clean.png`** - Clean bathroom (different angle than ad1)
- **`building.png`** - Building exterior (different angle than ad1)

### Photo Tips:
- ✅ Take photos in **good lighting** (daytime, windows open)
- ✅ **Clean up** the room before taking photos
- ✅ Use **different angles** for each ad to avoid duplicate detection
- ✅ **PNG or JPG format** only
- ✅ Keep files **under 10MB** each
- ✅ Use **descriptive file names** exactly as listed above

---

## ✏️ Step 7: Customize Your Ad Content

1. Open **`kijiji_dual_posting.py`** in a text editor
2. Find the sections that start with `self.ad1 = {` and `self.ad2 = {`
3. Update these fields to match your room:

### Ad 1 (Professional Focus):
```python
'title': 'Your Professional Room Title Here',  # Keep under 100 characters
'description': '''YOUR ROOM DESCRIPTION HERE
- What's included
- Location benefits  
- Ideal for professionals''',
'price': '500',  # Your price for professionals
'phone': '647-XXX-XXXX'  # Your phone number
```

### Ad 2 (Student Focus):
```python
'title': 'Your Student Room Title Here',  # Keep under 100 characters  
'description': '''YOUR STUDENT-FRIENDLY DESCRIPTION HERE
- Student amenities
- Near campus/transit
- Student-friendly price''',
'price': '450',  # Your student price
'phone': '647-XXX-XXXX'  # Your phone number
```

### Content Writing Tips:
- ✅ **Keep titles under 100 characters**
- ✅ **Keep descriptions under 4000 characters**
- ✅ **Use bullet points** for easy reading
- ✅ **Mention specific benefits** for each audience
- ✅ **Include location advantages**
- ✅ **Be honest** about what's included

---

## 🧪 Step 8: Test Run (Very Important!)

Before automating, always test manually:

### Make Sure Environment is Active:
You should see `(venv)` in your terminal. If not:

**Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Run Test:
```bash
python kijiji_dual_posting.py
```

### What Should Happen:
1. **Browser opens** (you'll see it working)
2. **Logs into Kijiji** with your credentials
3. **Deletes old ads** (if any exist)
4. **Posts first ad** with ad1 photos
5. **Posts second ad** with ad2 photos
6. **Shows success message**

### If Something Goes Wrong:
- ❌ **Login fails**: Check your username/password in `test_input.json`
- ❌ **Images don't upload**: Check file names and formats
- ❌ **Ads don't post**: Check your Kijiji account status
- ❌ **Browser crashes**: Try restarting and running again

---

## 🔄 Step 9: Set Up Daily Automation

### Option A: Mac/Linux (Using Cron)

1. Open terminal and type:
   ```bash
   crontab -e
   ```

2. Add this line (replace `/path/to/KijijiBot` with your actual path):
   ```bash
   0 9 * * * cd /Users/yourusername/Desktop/KijijiBot && source venv/bin/activate && python kijiji_dual_posting.py
   ```

3. Save and exit (press Ctrl+X, then Y, then Enter)

### Option B: Windows (Using Task Scheduler)

1. Open **Task Scheduler** (search in Start menu)
2. Click **"Create Basic Task"**
3. Name: **"Kijiji Daily Posting"**
4. Trigger: **"Daily"**
5. Time: **"9:00 AM"** (or whenever you want)
6. Action: **"Start a program"**
7. Program: **`python`**
8. Arguments: **`kijiji_dual_posting.py`**
9. Start in: **`C:\Users\YourName\Desktop\KijijiBot`**

### Option C: Manual Daily Run
Just run this command every day:
```bash
cd Desktop/KijijiBot
source venv/bin/activate  # Mac only
python kijiji_dual_posting.py
```

---

## 📊 Step 10: Monitor Your Automation

### Check Screenshots:
- Look in the **`screenshots/`** folder
- New screenshots are saved each time it runs
- Use these to see what happened if something goes wrong

### Check Your Kijiji Account:
- Login to kijiji.ca manually
- Go to **"My Ads"**
- You should see your 2 fresh ads

### Success Indicators:
- ✅ **2 new ads** posted every day
- ✅ **Old ads deleted** before new ones post
- ✅ **Different photos** on each ad
- ✅ **No error messages** in terminal

---

## 🛠️ Troubleshooting Common Issues

### "Permission Denied" Errors:
```bash
chmod +x venv/bin/activate  # Mac only
```

### "Module Not Found" Errors:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### "Browser Not Found" Errors:
```bash
playwright install chromium
```

### Kijiji Login Issues:
- ✅ Check username/password in `test_input.json`
- ✅ Try logging in manually first at kijiji.ca
- ✅ Disable 2-factor authentication temporarily
- ✅ Make sure account is in good standing

### Photo Upload Issues:
- ✅ Check file names match exactly (case-sensitive)
- ✅ Ensure files are PNG or JPG format
- ✅ Check file sizes are under 10MB
- ✅ Make sure photos are in correct folders

### Ads Not Posting:
- ✅ Check if you have too many existing ads
- ✅ Verify ad content follows Kijiji guidelines
- ✅ Ensure prices are reasonable for your area
- ✅ Check that your account isn't restricted

---

## 🔒 Security & Safety Tips

### Protect Your Information:
- 🔐 **Never share** your `test_input.json` file
- 🔐 **Use a strong password** for your Kijiji account
- 🔐 **Monitor your account** regularly for unauthorized activity
- 🔐 **Keep the bot updated** by checking GitHub periodically

### Legal Compliance:
- ✅ **Follow Kijiji's Terms of Service**
- ✅ **Post only legitimate rental ads**
- ✅ **Don't spam** or post misleading information
- ✅ **Respect rate limits** (don't run more than once per day)

### Best Practices:
- 📅 **Run daily** for best results (fresh ads get more views)
- 📸 **Update photos** monthly to keep content fresh
- 💰 **Adjust prices** based on market conditions
- 📝 **Update descriptions** seasonally
- 🎯 **Monitor performance** and adjust strategy

---

## 🆘 Getting Help

### Self-Help Resources:
1. **Check screenshots** in the `screenshots/` folder
2. **Read error messages** carefully in terminal
3. **Try running again** (sometimes it's just a temporary issue)
4. **Check your internet connection**

### Community Support:
1. **GitHub Issues**: https://github.com/BlockchainHB/KijijiBot/issues
2. **Search existing issues** before creating new ones
3. **Include screenshots** and error messages when asking for help
4. **Mention your operating system** (Mac/Windows)

### When Creating an Issue:
- 📝 **Describe what you were trying to do**
- 📝 **Include the exact error message**
- 📝 **Attach a screenshot** of the problem
- 📝 **Mention your OS** (Mac/Windows/Linux)
- 📝 **Include Python version** (`python3 --version`)

---

## 🎉 You're All Set!

Congratulations! Your KijijiBot is now ready to automatically post room rental ads daily. 

### Quick Daily Checklist:
- ✅ Bot runs automatically (if scheduled) or manually daily
- ✅ Check screenshots for any issues
- ✅ Monitor your Kijiji "My Ads" section
- ✅ Respond to inquiries promptly
- ✅ Update content monthly for best results

### Success Metrics to Track:
- 📈 **Views per ad** (check in Kijiji dashboard)
- 📧 **Inquiries received** 
- 🏠 **Successful rentals**
- ⭐ **Ad positioning** in search results

**Happy Renting! 🏠✨**

---

*Need help? Create an issue on GitHub or ask a tech-savvy friend to help with the initial setup.* 