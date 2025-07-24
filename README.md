# Amul Product Scraper

An automated scraper that monitors Amul products for availability and sends notifications when products are in stock.

## 🚀 Quick Start

1. **Setup environment:**
   ```powershell
   .\setup.ps1
   ```

2. **Configure your credentials:**
   ```powershell
   notepad .env
   ```

3. **Test the setup:**
   ```powershell
   python test_env.py
   ```

4. **Deploy with Task Scheduler:**
   ```powershell
   .\setup_scheduler.ps1
   ```

## 🔧 Features

- 🛒 **Automatic cart addition** when products are in stock
- 📱 **Telegram notifications** with product alerts
- 📞 **Optional WhatsApp notifications**
- 🔒 **Secure credential management** via environment variables
- ⏰ **Automated scheduling** every 10 minutes
- 📝 **Comprehensive logging** for monitoring
- 🔄 **Multiple deployment options**

## 📋 Requirements

- Python 3.7+
- Chrome browser
- Telegram bot (for notifications)
- Windows (for Task Scheduler deployment)

## 🛠️ Installation

### Automatic Setup
```powershell
# Clone or download the project
cd "c:\MyPythonML\AmulScraper"

# Run setup script
.\setup.ps1
```

### Manual Setup
```powershell
# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env

# Edit .env with your credentials
notepad .env
```

## ⚙️ Configuration

### Environment Variables (.env file)

```bash
# Required - Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Optional - WhatsApp Configuration
WHATSAPP_NUMBER=+919876543210
ENABLE_WHATSAPP=false

# Optional - Location
PINCODE=462003
```

### Getting Telegram Credentials

1. **Create a Telegram Bot:**
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot` command
   - Follow instructions and copy the bot token

2. **Get your Chat ID:**
   - Send a message to your bot
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find your chat ID in the JSON response

## 🚀 Deployment Options

### Option 1: Windows Task Scheduler (Recommended for Windows)
```powershell
.\setup_scheduler.ps1
```
- ✅ Runs automatically every 10 minutes
- ✅ Survives system restarts
- ✅ Runs in background (headless)
- ✅ Automatic logging

### Option 2: Kubernetes (Recommended for Production)
```powershell
# Setup Kubernetes environment
.\setup-k8s.ps1

# Deploy to Kubernetes
.\deploy-k8s.ps1

# Or deploy with Helm
.\deploy-helm.ps1
```
- ✅ **Production-ready** with auto-scaling
- ✅ **High availability** and fault tolerance
- ✅ **Resource management** and monitoring
- ✅ **Cloud-native** deployment
- 📖 [Detailed Kubernetes Guide](KUBERNETES_GUIDE.md)

### Option 3: Docker (Cross-platform)
```powershell
docker-compose up -d
```
- ✅ Isolated environment
- ✅ Easy to reproduce
- ✅ Cross-platform compatibility

### Option 4: Continuous Service
```powershell
python scraper_service.py
```
- ✅ Runs continuously
- ✅ Graceful shutdown with Ctrl+C
- ⚠️  Requires terminal to stay open

### Option 5: Single Run (for testing)
```powershell
python amulscraper_scheduled.py
```

## 📊 Monitoring

### Logs
- **File:** `scraper_log.txt`
- **Content:** Execution details, errors, product status
- **Rotation:** Automatically appended

### Notifications
- **Telegram:** Instant notifications with cart links
- **WhatsApp:** Optional notifications (if enabled)

### Task Scheduler
- Open Task Scheduler (`taskschd.msc`)
- Find "AmulScraper" task
- View execution history and status

## 🔍 Testing

```powershell
# Test environment setup
python test_env.py

# Test single scraper run
python amulscraper_scheduled.py

# Test notifications (if configured)
python -c "from amulscraper_scheduled import notify_telegram; notify_telegram('Test Product')"
```

## 📁 File Structure

```
AmulScraper/
├── 📄 Core Scripts
│   ├── amulscraper.py              # Original continuous script
│   ├── amulscraper_scheduled.py    # Single-run version for scheduling
│   ├── scraper_service.py          # Service wrapper with health checks
│   └── test_env.py                 # Environment testing
├── 🏗️ Setup & Deployment
│   ├── setup.ps1                   # Automated setup script
│   ├── setup_scheduler.ps1         # Task Scheduler setup
│   ├── setup-k8s.ps1              # Kubernetes environment setup
│   └── run_scraper_scheduled.bat   # Batch file for Task Scheduler
├── ☸️ Kubernetes Deployment
│   ├── deploy-k8s.ps1              # Kubernetes deployment script
│   ├── deploy-helm.ps1             # Helm deployment script
│   ├── k8s-manage.ps1              # Kubernetes management utilities
│   ├── k8s/                        # Raw Kubernetes manifests
│   │   ├── namespace.yaml
│   │   ├── secret.yaml
│   │   ├── configmap.yaml
│   │   ├── deployment.yaml
│   │   ├── cronjob.yaml
│   │   ├── service.yaml
│   │   └── networkpolicy.yaml
│   └── helm/amul-scraper/          # Helm chart
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
├── 🐳 Docker Configuration
│   ├── Dockerfile                  # Multi-stage Docker build
│   ├── docker-compose.yml          # Docker Compose setup
│   └── .dockerignore              # Docker ignore rules
├── 🔒 Configuration
│   ├── .env                        # Your secrets (DO NOT COMMIT)
│   ├── .env.example               # Environment template
│   ├── requirements.txt           # Python dependencies
│   └── .gitignore                 # Git ignore rules
└── 📚 Documentation
    ├── README.md                   # This file
    ├── DEPLOYMENT_GUIDE.md         # Detailed deployment guide
    └── KUBERNETES_GUIDE.md         # Comprehensive Kubernetes guide
```

## 🛡️ Security

- ✅ **Secrets in environment variables** (not in code)
- ✅ **`.env` file excluded** from version control
- ✅ **Credential validation** at startup
- ✅ **Optional features** can be disabled

## 🐛 Troubleshooting

### Common Issues

1. **"TELEGRAM_BOT_TOKEN is required"**
   - Edit `.env` file with your actual bot token
   - Run `python test_env.py` to verify

2. **Chrome driver issues**
   - Script auto-downloads ChromeDriver
   - Ensure Chrome browser is installed

3. **Task Scheduler not running**
   - Check Task Scheduler (`taskschd.msc`)
   - Verify task exists and is enabled
   - Check execution history for errors

4. **No notifications received**
   - Verify Telegram bot token and chat ID
   - Test with: `python test_env.py`
   - Check `scraper_log.txt` for errors

### Debug Commands

```powershell
# Check environment
python test_env.py

# Test single run with verbose output
python amulscraper_scheduled.py

# Check logs
Get-Content scraper_log.txt -Tail 20

# Check Task Scheduler status
Get-ScheduledTask -TaskName "AmulScraper"
```

## 📞 Support

If you encounter issues:

1. Check the logs: `scraper_log.txt`
2. Run environment test: `python test_env.py`
3. Verify credentials in `.env` file
4. Check Task Scheduler for task status

## 📝 License

This project is for educational purposes. Please respect Amul's terms of service and rate limits.

## 🔄 Updates

To update the scraper:
1. Backup your `.env` file
2. Download/pull new version
3. Restore your `.env` file
4. Run `.\setup.ps1` if new dependencies are added
