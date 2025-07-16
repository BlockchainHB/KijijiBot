# GitHub Actions Deployment Guide

## Setup Instructions

### 1. Add Repository Secrets
In your GitHub repository, go to Settings → Secrets and variables → Actions, then add:

- `KIJIJI_USERNAME`: hasaamb@gmail.com
- `KIJIJI_PASSWORD`: BagChaser415!

### 2. Add Your Images
Create these folders and add your room photos:
```
images/ad1/
├── room_main.png
├── bed_area.png
├── workspace.png
├── kitchen.png
├── bathroom.png
└── exterior.png

images/ad2/
├── room_study.png
├── bed_desk.png
├── living_space.png
├── kitchen_shared.png
├── bathroom_clean.png
└── building.png
```

### 3. Push to GitHub
```bash
git add .
git commit -m "Add GitHub Actions automation"
git push origin main
```

### 4. Test the Workflow
- Go to Actions tab in your GitHub repo
- Click "Kijiji Dual Posting Automation"
- Click "Run workflow" to test manually

## Schedule
- Runs daily at 9 AM EST (2 PM UTC)
- Can be triggered manually from Actions tab
- Screenshots saved as artifacts for 7 days

## Important Notes
- Script runs in headless mode (no browser window)
- Credentials stored securely in GitHub Secrets
- Images must be under 10MB each
- Workflow will fail if images are missing (but that's OK)