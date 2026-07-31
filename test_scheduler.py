import os
import sys

sys.path.insert(0, '.')

from scheduler import EmailScheduler


def test_scheduler_accepts_recipient_override(monkeypatch):
    monkeypatch.delenv('RECIPIENT_EMAIL', raising=False)
    monkeypatch.delenv('GMAIL_USER', raising=False)

    scheduler = EmailScheduler(send_email=False, use_mock_gmail=True, recipient_email='test@example.com')

    assert scheduler.recipient_email == 'test@example.com'


def test_scheduler_uses_env_recipient_when_available(monkeypatch):
    monkeypatch.setenv('RECIPIENT_EMAIL', 'env-recipient@example.com')
    monkeypatch.delenv('GMAIL_USER', raising=False)

    scheduler = EmailScheduler(send_email=False, use_mock_gmail=True)

    assert scheduler.recipient_email == 'env-recipient@example.com'
