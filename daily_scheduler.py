"""
Daily Scheduler for Kijiji Room Rental Automation
Runs the dual posting automation every 24 hours
"""

import asyncio
import schedule
import time
import sys
from datetime import datetime, timedelta
from kijiji_dual_posting import KijijiDualPosting

class DailyScheduler:
    def __init__(self):
        self.automation = KijijiDualPosting()
        self.next_run = None
        
    async def run_daily_automation(self):
        """Run the daily automation job"""
        print(f"\n{'='*60}")
        print(f"🕐 DAILY AUTOMATION STARTED - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        try:
            await self.automation.run_automation()
            print(f"\n✅ Daily automation completed successfully!")
            
            # Calculate next run time
            self.next_run = datetime.now() + timedelta(hours=24)
            print(f"⏰ Next run scheduled for: {self.next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"\n❌ Daily automation failed: {e}")
            print("Will retry tomorrow at the same time")
            
        print(f"{'='*60}\n")
        
    def job_wrapper(self):
        """Wrapper to run async function in sync context"""
        asyncio.run(self.run_daily_automation())
        
    def start_scheduler(self, run_time="09:00"):
        """Start the daily scheduler"""
        print(f"🤖 Kijiji Daily Automation Scheduler")
        print(f"{'='*50}")
        print(f"📅 Schedule: Every day at {run_time}")
        print(f"🏠 Posting: 2 room rental ads")
        print(f"📧 Account: {self.automation.username}")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Calculate next run
        now = datetime.now()
        next_run = datetime.strptime(f"{now.date()} {run_time}", "%Y-%m-%d %H:%M")
        if next_run <= now:
            next_run += timedelta(days=1)
        self.next_run = next_run
        
        print(f"🚀 Next run: {self.next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")
        
        # Schedule the job
        schedule.every().day.at(run_time).do(self.job_wrapper)
        
        # Keep the scheduler running
        try:
            while True:
                schedule.run_pending()
                
                # Show countdown every minute
                now = datetime.now()
                if self.next_run:
                    time_until = self.next_run - now
                    if time_until.total_seconds() > 0:
                        hours = int(time_until.total_seconds() // 3600)
                        minutes = int((time_until.total_seconds() % 3600) // 60)
                        print(f"⏳ Time until next run: {hours}h {minutes}m", end='\r')
                
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            print(f"\n\n🛑 Scheduler stopped by user")
            print(f"📊 Last successful run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
    def run_once_now(self):
        """Run the automation once immediately (for testing)"""
        print("🧪 Running automation once for testing...")
        asyncio.run(self.run_daily_automation())

def main():
    scheduler = DailyScheduler()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "test":
            # Run once for testing
            scheduler.run_once_now()
            
        elif command == "schedule":
            # Start daily scheduling
            run_time = sys.argv[2] if len(sys.argv) > 2 else "09:00"
            scheduler.start_scheduler(run_time)
            
        else:
            print("Usage:")
            print("  python daily_scheduler.py test              - Run once now")
            print("  python daily_scheduler.py schedule [HH:MM]  - Start daily scheduler")
            print("  Example: python daily_scheduler.py schedule 09:00")
    else:
        print("🤖 Kijiji Daily Automation Scheduler")
        print("Usage:")
        print("  python daily_scheduler.py test              - Run once now")
        print("  python daily_scheduler.py schedule [HH:MM]  - Start daily scheduler")
        print("  Example: python daily_scheduler.py schedule 09:00")

if __name__ == "__main__":
    main() 