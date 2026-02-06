# Free Hosting Deployment Guide for Auto-Rename Bot

This guide covers deploying the Auto-Rename Bot on various **free hosting platforms**.

## 📋 Prerequisites

Before deploying, make sure you have:

1. **Telegram Bot Token** - Get from [@BotFather](https://t.me/BotFather)
2. **API ID & Hash** - Get from [my.telegram.org](https://my.telegram.org)
3. **MongoDB Database** - Get free from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
4. **Your Telegram User ID** - Get from [@userinfobot](https://t.me/userinfobot)
5. **Log Channel ID** - Create a channel and add your bot as admin

---

## 🚀 Deployment Options

### Option 1: Railway.app (Recommended)

Railway offers 500 hours/month free tier with automatic deployments.

#### Steps:
1. Fork this repository to your GitHub account
2. Go to [railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your forked repository
5. Add environment variables:
   ```
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   DB_URL=your_mongodb_url
   OWNER_ID=your_telegram_user_id
   LOG_CHANNEL=your_log_channel_id
   SUPPORT_CHAT=your_support_chat_id
   WEBHOOK=True
   PORT=8980
   ```
6. Deploy! Railway will auto-detect the configuration from `railway.json`

**Note**: Railway provides a public URL automatically which keeps your bot alive.

---

### Option 2: Render.com

Render offers free web services with 750 hours/month.

#### Steps:
1. Fork this repository
2. Go to [render.com](https://render.com)
3. Click "New" → "Web Service"
4. Connect your GitHub and select the repository
5. Configure:
   - **Name**: auto-rename-bot
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
6. Add environment variables (same as Railway)
7. Click "Create Web Service"

**Note**: The bot configuration is already set in `render.yaml`.

---

### Option 3: Koyeb

Koyeb offers free tier with 2 free services.

#### Steps:
1. Fork this repository
2. Go to [koyeb.com](https://www.koyeb.com)
3. Click "Create App" → "Docker"
4. Connect your GitHub repository
5. Select the Dockerfile build method
6. Add environment variables
7. Deploy

**Note**: Configuration is in `koyeb.yaml`.

---

### Option 4: Heroku (Legacy Support)

Although Heroku removed free tier, existing users can still use it.

#### Steps:
1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login: `heroku login`
3. Create app: `heroku create your-bot-name`
4. Set environment variables:
   ```bash
   heroku config:set API_ID=your_api_id
   heroku config:set API_HASH=your_api_hash
   heroku config:set BOT_TOKEN=your_bot_token
   heroku config:set DB_URL=your_mongodb_url
   heroku config:set OWNER_ID=your_user_id
   heroku config:set LOG_CHANNEL=your_channel_id
   heroku config:set SUPPORT_CHAT=your_chat_id
   ```
5. Deploy: `git push heroku main`

**Note**: Heroku configuration is in `Procfile`, `app.json`, and `heroku.yml`.

---

## 🐳 Docker Deployment (Self-Hosted)

If you have a VPS or local machine:

### Using Docker Compose (Recommended)
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Auto-Rename.git
cd Auto-Rename

# Create .env file with your variables
cat > .env << EOF
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
DB_URL=your_mongodb_url
OWNER_ID=your_user_id
LOG_CHANNEL=your_channel_id
SUPPORT_CHAT=your_chat_id
EOF

# Start the bot
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Using Docker Only
```bash
# Build image
docker build -t auto-rename-bot .

# Run container
docker run -d \
  --name auto-rename-bot \
  --restart unless-stopped \
  -p 8980:8980 \
  -e API_ID=your_api_id \
  -e API_HASH=your_api_hash \
  -e BOT_TOKEN=your_bot_token \
  -e DB_URL=your_mongodb_url \
  -e OWNER_ID=your_user_id \
  -e LOG_CHANNEL=your_channel_id \
  -e SUPPORT_CHAT=your_chat_id \
  auto-rename-bot
```

---

## 📊 Monitoring & Health Checks

The bot includes built-in health check endpoints:

- `GET /` - Basic bot status
- `GET /health` - Detailed health check (for monitoring services)
- `GET /ping` - Simple ping response

These endpoints are used by hosting platforms to ensure your bot stays alive.

---

## 🔧 Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `API_ID` | ✅ Yes | Telegram API ID | `12345678` |
| `API_HASH` | ✅ Yes | Telegram API Hash | `abcdef1234567890` |
| `BOT_TOKEN` | ✅ Yes | Bot token from BotFather | `123456:ABC-DEF1234` |
| `DB_URL` | ✅ Yes | MongoDB connection string | `mongodb+srv://...` |
| `OWNER_ID` | ✅ Yes | Your Telegram user ID | `123456789` |
| `LOG_CHANNEL` | ✅ Yes | Log channel ID | `-1001234567890` |
| `SUPPORT_CHAT` | ⚠️ Optional | Support chat ID | `-1001234567890` |
| `DB_NAME` | ⚠️ Optional | Database name | `RexBots` (default) |
| `PORT` | ⚠️ Optional | Web server port | `8980` (default) |
| `WEBHOOK` | ⚠️ Optional | Enable webhook | `True` (default) |
| `START_PIC` | ⚠️ Optional | Start command picture URL | URL |
| `LEADERBOARD_PIC` | ⚠️ Optional | Leaderboard picture URL | URL |
| `FSUB_PIC` | ⚠️ Optional | Force subscribe picture URL | URL |
| `BOT_USERNAME` | ⚠️ Optional | Bot username | `@YourBot` |
| `DUMP_CHANNEL` | ⚠️ Optional | Dump channel ID | `-1001234567890` |

---

## 🆓 MongoDB Atlas Setup (Free)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free account
3. Create a new cluster (M0 Free tier)
4. Create a database user
5. Whitelist all IPs (0.0.0.0/0) for cloud hosting
6. Get connection string: `mongodb+srv://username:password@cluster.mongodb.net/`
7. Use this as `DB_URL` in your environment variables

---

## 🔍 Troubleshooting

### Bot not starting
- Check if all required environment variables are set
- Verify MongoDB connection string is correct
- Check logs for specific error messages

### Bot stops after a while
- Ensure WEBHOOK is set to `True` for cloud hosting
- Check if health check endpoint (`/health`) is accessible
- Verify hosting platform hasn't suspended your service

### Files not processing
- Check if ffmpeg is installed (included in Docker image)
- Verify bot has enough memory (at least 512MB)
- Check disk space on hosting platform

---

## 💡 Tips for Free Hosting

1. **Use MongoDB Atlas Free Tier**: 512MB storage is sufficient for most use cases
2. **Enable Webhooks**: Keeps the bot responsive without constant polling
3. **Monitor Usage**: Free tiers have limitations, monitor your usage regularly
4. **Use Health Checks**: Ensures your bot stays alive
5. **Optimize Workers**: Default 200 workers might be too much for free tier, consider reducing
6. **Keep Logs Clean**: Excessive logging can fill up disk space

---

## 📱 After Deployment

Once deployed, test your bot:
1. Send `/start` to your bot
2. Try uploading a file to test rename functionality
3. Check if custom thumbnails work
4. Test admin commands
5. Verify force subscribe is working if configured

---

## 🆘 Support

If you encounter issues:
- Check the logs first
- Review environment variables
- Consult the main [README.md](README.md)
- Open an issue on GitHub

---

## 🎉 Congratulations!

Your Auto-Rename Bot should now be running 24/7 for free! Enjoy automated file renaming! 🚀
