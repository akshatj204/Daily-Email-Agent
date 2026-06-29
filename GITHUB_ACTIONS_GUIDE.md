# GitHub Actions Setup Guide

## What is This?

Instead of running a scheduler 24/7, **GitHub Actions runs your script automatically every day at 6 AM IST**.

Benefits:
- ✅ **Not running 24/7** (only executes at 6 AM)
- ✅ **Free** (GitHub includes it)
- ✅ **In your git repo** (config file, not cron job)
- ✅ **Works everywhere** (no computer needed)
- ✅ **Secure** (credentials stored safely)
- ✅ **Logging** (see execution logs on GitHub)

---

## ⚡ Quick Setup (5 minutes)

### **Step 1: Push to GitHub**

```bash
cd /Users/akshatjain/morning-email-agent

git init
git add .
git commit -m "Morning email agent - ready for production"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/morning-email-agent.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### **Step 2: Enable GitHub Actions**

1. Go to: `https://github.com/YOUR_USERNAME/morning-email-agent`
2. Click **Actions** tab
3. Click **"I understand my workflows, go ahead and enable them"**

### **Step 3: Verify Workflow is Setup**

1. Go to **Actions** tab
2. You should see **"Morning Email Agent"** workflow
3. It's scheduled to run daily at **6 AM IST**

That's it! 🎉

---

## 🔧 **Optional: Send Emails (If You Want Them Sent)**

### **Option A: Manual (Simpler)**

The workflow currently just **generates emails** and stores them in `data/emails/`.

You can still manually check them:
```bash
# After workflow runs, check the artifacts:
# Go to GitHub Actions → Click the run → Download "morning-emails" artifact
```

### **Option B: Auto-Send via Gmail (More Complex)**

If you want emails **automatically sent to your inbox**:

#### **Step 1: Add Gmail Credentials as Secret**

1. Download your `credentials.json` from Google Cloud
2. Open it and copy the entire content
3. Go to GitHub repo → **Settings** → **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Name: `GMAIL_CREDENTIALS_JSON`
6. Value: Paste your entire credentials.json content
7. Click **Add secret**

#### **Step 2: Update Workflow**

Edit `.github/workflows/morning-email.yml`:

```yaml
- name: Run Morning Email Agent with Gmail
  run: |
    echo "${{ secrets.GMAIL_CREDENTIALS_JSON }}" > credentials.json
    python main.py
```

#### **Step 3: Update main.py**

Modify the end of `main.py` to send emails:

```python
if __name__ == "__main__":
    from utils.gmail_sender import GmailSender
    
    agent = MorningEmailAgent()
    result = agent.run()
    
    # Send email if generated
    if result["html"]:
        sender = GmailSender()
        sender.send_morning_email(
            to="your-email@gmail.com",  # CHANGE THIS!
            html_body=result["html"],
            day_of_week=agent.day_of_week
        )
        print("✅ Email sent!")
```

Then commit and push:
```bash
git add .
git commit -m "Add automatic email sending"
git push
```

---

## 📊 **How It Works**

```
Every day at 6 AM IST:
    ↓
GitHub Actions wakes up
    ↓
Checks out your code
    ↓
Installs dependencies
    ↓
Runs: python main.py
    ↓
Generates email
    ↓
Optionally sends via Gmail
    ↓
Saves logs & artifacts
    ↓
GitHub Action completes (no continuous running!)
```

---

## ✅ **Verify It's Working**

### **Check Workflow Runs**

1. Go to: `https://github.com/YOUR_USERNAME/morning-email-agent/actions`
2. Click **Morning Email Agent**
3. You'll see all past runs with:
   - ✅ Successful runs (green)
   - ❌ Failed runs (red)
   - ⏱️ Execution time
   - 📊 Logs

### **View Logs**

Click a run → See detailed logs of what happened

### **Download Generated Emails**

Click a run → **Artifacts** section → Download `morning-emails.zip`

---

## ⏰ **Time Settings**

The workflow currently runs at **6 AM IST**.

To change the time, edit `.github/workflows/morning-email.yml`:

```yaml
on:
  schedule:
    # Format: 'minute hour day month day-of-week'
    # Times in UTC (not IST!)
    
    # Examples:
    - cron: '30 0 * * *'      # 6:00 AM IST (0:30 UTC)
    - cron: '0 7 * * *'        # 12:30 PM IST (7:00 UTC)
    - cron: '30 14 * * *'      # 8:00 PM IST (14:30 UTC)
```

Then push the change:
```bash
git add .github/workflows/morning-email.yml
git commit -m "Update workflow time"
git push
```

---

## 🔐 **Security Notes**

✅ **Credentials are safe:**
- Stored as GitHub secret (encrypted)
- Not visible in logs
- Only used during workflow run
- Can be rotated anytime

✅ **Best practices:**
- Never commit `credentials.json` to git
- Keep it in `.gitignore` (already there)
- Use GitHub secrets for sensitive data
- Rotate credentials periodically

---

## 🐛 **Troubleshooting**

### **"Workflow not running at scheduled time"**
- GitHub Actions uses UTC, not your timezone
- 6 AM IST = 0:30 UTC
- Check cron expression in workflow file

### **"Workflow failed with error"**
- Click the failed run
- Check logs for the error
- Most common: Missing dependencies
- Fix: Update requirements.txt and push

### **"Can't send email from GitHub Actions"**
- Credentials need to be added as GitHub secret
- Follow "Auto-Send via Gmail" section above
- Make sure credentials.json is valid

### **"Email not being sent"**
- Check main.py is modified to send emails
- Verify credentials.json is correct
- Try running locally first to test

---

## 📋 **Complete Setup Checklist**

- [ ] Pushed code to GitHub
- [ ] GitHub Actions enabled
- [ ] Workflow file exists: `.github/workflows/morning-email.yml`
- [ ] Can see "Morning Email Agent" in Actions tab
- [ ] Time is set correctly (6 AM IST = 0:30 UTC)
- [ ] (Optional) Gmail credentials added as secret
- [ ] (Optional) main.py modified to send emails
- [ ] (Optional) Verified first email sent successfully

---

## 🎯 **What You Get**

✅ **Automated daily emails** at 6 AM IST
✅ **No computer needed** (runs on GitHub's servers)
✅ **Free** (included with GitHub)
✅ **Logs and history** (all runs visible on GitHub)
✅ **Scalable** (can add multiple workflows)
✅ **Version controlled** (everything in git)

---

## 🚀 **You're Done!**

That's it! GitHub Actions will now run your morning email agent every day at 6 AM IST, completely automatically.

No cron jobs, no running process, no computer needed. Just push to GitHub and it works! 🎉

---

## 📚 **Learn More**

- GitHub Actions docs: https://docs.github.com/en/actions
- Cron syntax: https://crontab.guru/
- Secrets management: https://docs.github.com/en/actions/security-guides/encrypted-secrets

---

**Ready to set it up? Just push your code to GitHub and enable Actions!** 👍
