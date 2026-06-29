# Scheduler Guide

## What is This?

Instead of using **cron jobs** (which can't be committed to git), this `scheduler.py` runs the email agent on a schedule **entirely in Python**.

This way:
- ✅ No cron job setup needed
- ✅ Everything is in code (can be committed to git)
- ✅ Works on Mac, Linux, and Windows
- ✅ Easy to customize and test

---

## How to Use

### **Option 1: Run Scheduler (Always Running)**

The simplest way - scheduler runs continuously and checks every minute:

```bash
# Install updated requirements
pip install -r requirements_SCHEDULER.txt

# Edit scheduler.py and change your email:
# Line 158: scheduler.set_recipient_email("your-email@gmail.com")

# Run it
python scheduler.py
```

**This will:**
- ✅ Start at any time you run it
- ✅ Run email job daily at 6:00 AM
- ✅ Continue forever (until you stop it with Ctrl+C)
- ✅ Log everything to console

**To keep it running 24/7:**
- Run in a **screen/tmux session** (Mac/Linux)
- Run in **background** (Windows)
- Or use a **cloud service** (next section)

---

### **Option 2: Background Thread**

Run scheduler in background while doing other things:

```python
from scheduler import run_scheduler_in_background

# Start scheduler in background
scheduler, thread = run_scheduler_in_background()

# Now you can do other things
print("Scheduler running in background...")
print("Program can continue here...")

# Keep program alive
while True:
    time.sleep(1)
```

---

### **Option 3: Test Mode (Before Going Live)**

Test that everything works without sending real emails:

```bash
# Edit scheduler.py, uncomment lines 157-159:
scheduler.use_mock_gmail = True
scheduler.run_once_now()

# This will:
# 1. Generate the email
# 2. Pretend to send it (mock mode)
# 3. Show you what would happen
# 4. Exit
```

---

## 🚀 **For Production: Run in Cloud**

### **Option A: Google Cloud Function + Cloud Scheduler (Recommended)**

```python
# functions.py (deploy to Google Cloud)
from scheduler import EmailScheduler

def morning_email(request):
    scheduler = EmailScheduler(send_email=True, use_mock_gmail=False)
    scheduler.set_recipient_email("your-email@gmail.com")
    scheduler.run_once_now()
    return {"status": "success"}
```

Then set up Cloud Scheduler to call this function daily at 6 AM.

### **Option B: Docker Container**

```dockerfile
FROM python:3.11

WORKDIR /app
COPY . .

RUN pip install -r requirements_SCHEDULER.txt

# Run scheduler when container starts
CMD ["python", "scheduler.py"]
```

Run container with:
```bash
docker build -t morning-email-agent .
docker run -d morning-email-agent
```

### **Option C: Keep Laptop Running**

If you keep your computer on 24/7:

```bash
# Mac: Use launchd
# Create file: ~/Library/LaunchAgents/com.morning-email.plist
# Configure to run scheduler.py at startup

# Linux: Use systemd
# Create service file in /etc/systemd/system/
# Enable and start service

# Windows: Task Scheduler
# Create task to run: python C:\path\to\scheduler.py
# Run at startup
```

---

## 📝 **Step-by-Step Setup**

### **Step 1: Update Requirements**
```bash
pip install schedule
# or
pip install -r requirements_SCHEDULER.txt
```

### **Step 2: Edit scheduler.py**
Find line ~158 and change:
```python
scheduler.set_recipient_email("your-email@gmail.com")  # ← YOUR EMAIL
```

### **Step 3: Test Mode**
```bash
# Uncomment test section in scheduler.py (lines 157-159)
python scheduler.py
```

Should generate email and log output.

### **Step 4: Production Mode**
```bash
# Comment out test section
python scheduler.py
```

Will run forever, checking every minute, executing at 6 AM daily.

### **Step 5 (Optional): Deploy to Cloud**
Follow cloud deployment instructions above.

---

## 🔧 **Customization**

### **Change Email Time**
```python
# Default is 6 AM. To change:
scheduler.schedule_daily_at(hour=7, minute=30)  # 7:30 AM
```

### **Send to Multiple People**
```python
# Modify scheduler.py to:
for email in ["person1@gmail.com", "person2@gmail.com"]:
    scheduler.set_recipient_email(email)
    scheduler.morning_email_job()
```

### **Disable Email Sending (Generate Only)**
```python
scheduler = EmailScheduler(send_email=False)
scheduler.run_once_now()
```

### **Use Mock Gmail (Testing)**
```python
scheduler = EmailScheduler(send_email=True, use_mock_gmail=True)
scheduler.run_once_now()
# Pretends to send but doesn't actually
```

---

## 📊 **Logs**

All output goes to:
- Console (when running manually)
- `data/logs/agent_*.log` (when running via main.py)

Check logs:
```bash
cat data/logs/agent_*.log
```

---

## ✅ **Checklist**

- [ ] `schedule` installed: `pip install schedule`
- [ ] Email address changed in `scheduler.py`
- [ ] Test run successful: `python scheduler.py` (run for 1 min, then Ctrl+C)
- [ ] Confirmed email generated in `data/emails/`
- [ ] Ready for production

---

## 🎯 **Which Option Should I Use?**

| Scenario | Option |
|----------|--------|
| **Testing on Mac/Linux** | Option 1: Run scheduler locally |
| **Want background process** | Option 2: Background thread |
| **Keep running 24/7** | Cloud Function + Cloud Scheduler |
| **Don't want to keep laptop on** | Docker on VPS or Cloud |

---

## 🐛 **Troubleshooting**

### **"schedule module not found"**
```bash
pip install schedule
```

### **"Email not sending"**
```
1. Make sure credentials.json exists
2. Check email is correct in scheduler.py
3. Try mock mode first: use_mock_gmail=True
```

### **"Job not running at 6 AM"**
```
1. Check computer is on at 6 AM
2. Check scheduler still running (not crashed)
3. Verify with: schedule.jobs
```

---

## 📚 **Next Steps**

1. **Test locally** with: `python scheduler.py`
2. **Verify it works** for a few days
3. **Deploy to cloud** when ready (no computer needed!)

---

**Ready to use the scheduler?** Just run `python scheduler.py` and it's done! 🚀
