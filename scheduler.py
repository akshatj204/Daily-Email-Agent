"""
Scheduler Utility
Runs the morning email agent on a schedule (6 AM daily).
This replaces the need for cron jobs - everything is in code!
"""

import schedule
import time
import logging
from datetime import datetime
from main import MorningEmailAgent
from utils.gmail_sender import get_gmail_sender

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class EmailScheduler:
    """Schedule the morning email to run daily at a specific time"""
    
    def __init__(self, send_email: bool = True, use_mock_gmail: bool = False):
        """
        Initialize scheduler.
        
        Args:
            send_email: Whether to actually send emails (True) or just generate (False)
            use_mock_gmail: Use mock Gmail for testing (True) or real Gmail (False)
        """
        self.send_email = send_email
        self.use_mock_gmail = use_mock_gmail
        self.recipient_email = "your-email@gmail.com"  # CHANGE THIS!
        
        logger.info(f"Scheduler initialized")
        logger.info(f"  Send Email: {self.send_email}")
        logger.info(f"  Mock Gmail: {self.use_mock_gmail}")
    
    def set_recipient_email(self, email: str) -> None:
        """Set the email address to send to"""
        self.recipient_email = email
        logger.info(f"Recipient email set to: {email}")
    
    def morning_email_job(self) -> None:
        """Job to run every morning at 6 AM"""
        logger.info("\n" + "="*70)
        logger.info("MORNING EMAIL JOB - SCHEDULED RUN")
        logger.info("="*70 + "\n")
        
        try:
            # Step 1: Generate email
            logger.info("Step 1: Generating email...")
            agent = MorningEmailAgent()
            result = agent.run()
            
            # Step 2: Send email if enabled
            if self.send_email and result["status"] in ["success", "partial"]:
                logger.info("\nStep 2: Sending email...")
                
                try:
                    sender = get_gmail_sender(use_mock=self.use_mock_gmail)
                    
                    success = sender.send_morning_email(
                        to=self.recipient_email,
                        html_body=result.get("html", "<p>No email generated</p>"),
                        day_of_week=agent.day_of_week
                    )
                    
                    if success:
                        logger.info(f"✅ Email sent to {self.recipient_email}")
                    else:
                        logger.error(f"❌ Failed to send email to {self.recipient_email}")
                
                except Exception as e:
                    logger.error(f"Error sending email: {str(e)}")
            else:
                logger.info("Step 2: Email sending disabled or no email generated")
            
            logger.info("\n" + "="*70)
            logger.info("JOB COMPLETE")
            logger.info("="*70 + "\n")
        
        except Exception as e:
            logger.error(f"FATAL ERROR in scheduled job: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def schedule_daily_at(self, hour: int = 6, minute: int = 0) -> schedule.Job:
        """
        Schedule job to run daily at specified time.
        
        Args:
            hour: Hour (0-23) - default 6 (6 AM)
            minute: Minute (0-59) - default 0
        
        Returns:
            schedule.Job object
        """
        time_str = f"{hour:02d}:{minute:02d}"
        
        job = schedule.every().day.at(time_str).do(self.morning_email_job)
        
        logger.info(f"✅ Scheduled email for daily at {time_str}")
        return job
    
    def start(self) -> None:
        """
        Start the scheduler (runs indefinitely).
        Blocks the program - use in dedicated process or container.
        """
        logger.info("\n" + "="*70)
        logger.info("SCHEDULER STARTED")
        logger.info("="*70)
        logger.info(f"Next run: {self._get_next_run_time()}")
        logger.info("Press Ctrl+C to stop")
        logger.info("="*70 + "\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("\n✋ Scheduler stopped by user")
    
    def _get_next_run_time(self) -> str:
        """Get the next scheduled run time"""
        if schedule.jobs:
            return str(schedule.jobs[0].next_run)
        return "No jobs scheduled"
    
    def run_once_now(self) -> None:
        """Run the job immediately (useful for testing)"""
        logger.info("Running job immediately (not waiting for schedule)...")
        self.morning_email_job()


def run_scheduler_in_background():
    """
    Run scheduler in a background thread (non-blocking).
    Use this if you want the program to do other things too.
    """
    import threading
    
    scheduler = EmailScheduler(send_email=True, use_mock_gmail=False)
    scheduler.set_recipient_email("your-email@gmail.com")  # CHANGE THIS!
    scheduler.schedule_daily_at(hour=6, minute=0)
    
    # Start scheduler in background thread
    thread = threading.Thread(target=scheduler.start, daemon=True)
    thread.start()
    
    logger.info("Scheduler running in background thread")
    return scheduler, thread


# Example usage
if __name__ == "__main__":
    print("\n" + "="*70)
    print("  MORNING EMAIL AGENT - SCHEDULER")
    print("="*70 + "\n")
    
    # Create scheduler
    scheduler = EmailScheduler(
        send_email=True,           # Set to False to just generate emails
        use_mock_gmail=False       # Set to True to test without sending
    )
    
    # Set your email (IMPORTANT!)
    scheduler.set_recipient_email("your-email@gmail.com")  # CHANGE THIS!
    
    # Schedule for 6 AM daily
    scheduler.schedule_daily_at(hour=6, minute=0)
    
    print("Options:")
    print("1. Run once now (for testing): scheduler.run_once_now()")
    print("2. Start scheduler: scheduler.start()")
    print()
    print("Example: python scheduler.py")
    print()
    
    # Uncomment ONE of these to run:
    
    # Option A: Test run (generates email but doesn't send)
    # scheduler.use_mock_gmail = True
    # scheduler.run_once_now()
    
    # Option B: Start scheduler (runs at 6 AM daily)
    scheduler.start()
