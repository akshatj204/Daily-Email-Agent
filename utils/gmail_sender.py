"""
Gmail Sender
Sends emails via Gmail API with OAuth authentication.
"""

import os
import base64
import logging
from typing import Optional, List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient import discovery
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False
    logger.warning("Gmail API libraries not installed. Install with: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    print(f"GMAIL_AVAILABLE = {GMAIL_AVAILABLE}")


class GmailSender:
    """Send emails via Gmail API"""
    
    # Gmail API scopes
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    
    def __init__(self, credentials_file: str = "credentials.json", token_file: str = "token.json"):
        """
        Initialize Gmail sender.
        
        Args:
            credentials_file: Path to Google OAuth credentials JSON
            token_file: Path to store OAuth token
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.user_email = None
        
        if GMAIL_AVAILABLE:
            try:
                self._initialize_service()
            except Exception as e:
                import traceback
                traceback.print_exc()
                logger.exception("Gmail service not initialized")
    
    def _initialize_service(self):
        """Initialize Gmail API service with OAuth"""
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
        
        # If no valid credentials, create new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_file}\n"
                        "To set up Gmail:\n"
                        "1. Create OAuth credentials in Google Cloud Console\n"
                        "2. Download as JSON and save as 'credentials.json'\n"
                        "3. Run this script again"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save token for next run
            with open(self.token_file, 'w') as f:
                f.write(creds.to_json())
        
        # Build service
        self.service = discovery.build('gmail', 'v1', credentials=creds)
        
        # Get user email
        profile = self.service.users().getProfile(userId='me').execute()
        self.user_email = profile.get('emailAddress')
        
        logger.info(f"Gmail service initialized for: {self.user_email}")
    
    def send_email(
        self,
        to: str,
        subject: str,
        html_body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        reply_to: Optional[str] = None
    ) -> bool:
        """
        Send email via Gmail API.
        
        Args:
            to: Recipient email address
            subject: Email subject
            html_body: Email body in HTML format
            cc: List of CC recipients
            bcc: List of BCC recipients
            reply_to: Reply-to email address
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.service:
            logger.error("Gmail service not initialized")
            return False
        
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['subject'] = subject
            message['from'] = self.user_email
            message['to'] = to
            
            if cc:
                message['cc'] = ', '.join(cc)
            
            if reply_to:
                message['reply-to'] = reply_to
            
            # Attach HTML content
            html_part = MIMEText(html_body, 'html')
            message.attach(html_part)
            
            # Prepare message for sending
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            send_message = {
                'raw': raw_message,
                'threadId': None
            }
            
            if bcc:
                send_message['bcc'] = ', '.join(bcc)
            
            # Send message
            result = self.service.users().messages().send(
                userId='me',
                body=send_message
            ).execute()
            
            message_id = result.get('id')
            logger.info(f"Email sent successfully to {to} (Message ID: {message_id})")
            
            return True
        
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_morning_email(
        self,
        to: str,
        html_body: str,
        cc: Optional[List[str]] = None,
        day_of_week: Optional[str] = None
    ) -> bool:
        """
        Send morning email with standard formatting.
        
        Args:
            to: Recipient email address
            html_body: Email body in HTML format
            cc: List of CC recipients
            day_of_week: Day of week for subject (e.g., "Monday")
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not day_of_week:
            day_of_week = datetime.now().strftime("%A")
        
        date_str = datetime.now().strftime("%B %d, %Y")
        subject = f"📧 Morning Update - {day_of_week}, {date_str}"
        
        return self.send_email(
            to=to,
            subject=subject,
            html_body=html_body,
            cc=cc,
            reply_to="noreply@morningagent.local"
        )
    
    def test_connection(self) -> bool:
        """Test Gmail connection"""
        if not self.service:
            logger.error("Gmail service not available")
            return False
        
        try:
            profile = self.service.users().getProfile(userId='me').execute()
            email = profile.get('emailAddress')
            logger.info(f"✓ Gmail connection test successful: {email}")
            return True
        except Exception as e:
            logger.error(f"✗ Gmail connection test failed: {str(e)}")
            return False


class MockGmailSender:
    """Mock Gmail sender for testing (doesn't actually send emails)"""
    
    def __init__(self, *args, **kwargs):
        self.user_email = "test@example.com"
        logger.info("Mock Gmail sender initialized")
    
    def send_email(self, to: str, subject: str, html_body: str, **kwargs) -> bool:
        """Mock send - just logs the email"""
        logger.info(f"[MOCK] Email would be sent to: {to}")
        logger.info(f"[MOCK] Subject: {subject}")
        logger.info(f"[MOCK] Body size: {len(html_body)} bytes")
        return True
    
    def send_morning_email(self, to: str, html_body: str, **kwargs) -> bool:
        """Mock morning email send"""
        return self.send_email(
            to=to,
            subject="[MOCK] Morning Update",
            html_body=html_body
        )
    
    def test_connection(self) -> bool:
        """Mock test connection"""
        logger.info("✓ Mock Gmail connection test successful")
        return True


def get_gmail_sender(use_mock: bool = False) -> object:
    """
    Get Gmail sender (real or mock).
    
    Args:
        use_mock: If True, use mock sender for testing
    
    Returns:
        GmailSender or MockGmailSender instance
    """
    if use_mock or not GMAIL_AVAILABLE:
        return MockGmailSender()
    
    try:
        return GmailSender()
    except Exception as e:
        logger.warning(f"Failed to initialize real Gmail sender: {str(e)}")
        logger.info("Falling back to mock sender")
        return MockGmailSender()


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test with mock sender
    print("\nTesting Mock Gmail Sender:")
    print("="*70)
    
    sender = get_gmail_sender(use_mock=True)
    
    # Test connection
    sender.test_connection()
    
    # Send sample email
    sample_html = """
    <html>
        <body>
            <h1>Hello!</h1>
            <p>This is a test email from the Morning Email Agent.</p>
        </body>
    </html>
    """
    
    success = sender.send_morning_email(
        to="your-email@gmail.com",
        html_body=sample_html,
        day_of_week="Monday"
    )
    
    print(f"Send result: {success}")
    
    print("\n" + "="*70)
    print("To use the real Gmail sender:")
    print("1. Set up Google Cloud credentials")
    print("2. Download OAuth credentials JSON")
    print("3. Save as 'credentials.json'")
    print("4. Run: sender = GmailSender()")
    print("="*70)
