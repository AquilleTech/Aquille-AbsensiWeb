# Absensi Web - Production Deployment Guide

## 🚀 Quick Start (Termux)

### 1. Install Dependencies
```bash
# Update packages
pkg update && pkg upgrade

# Install Python
pkg install python

# Install required system packages
pkg install libxml2 libxslt libjpeg-turbo
```

### 2. Setup Application
```bash
# Navigate to project directory
cd /path/to/absensiweb_production

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Start the Server

**Option A: Using Python script (Recommended for Termux)**
```bash
python start_server.py
```

**Option B: Using bash script**
```bash
./start.sh
```

**Option C: Direct Gunicorn command**
```bash
gunicorn -c gunicorn_config.py wsgi:application
```

The server will start on `http://0.0.0.0:5000`

### 4. Access the Application
- Local: http://localhost:5000
- Network: http://YOUR_IP:5000
- First time: Visit `/setup` to create super admin account

---

## 🔧 Configuration

### Gunicorn Settings (gunicorn_config.py)
```python
workers = 2              # Number of worker processes (2 for Termux)
bind = "0.0.0.0:5000"   # Server address and port
timeout = 30             # Worker timeout in seconds
```

**Adjusting for Performance:**
- **Low memory (Termux)**: Keep workers = 2
- **More powerful server**: workers = (CPU cores × 2) + 1
- **High traffic**: Increase worker_connections and max_requests

### Application Settings
Edit via web interface at `/admin/settings` (super admin only):
- School name
- Attendance times
- Late time threshold
- Telegram notifications
- Theme color
- Feature toggles

---

## 📁 File Structure
```
absensiweb_production/
├── app.py                    # Main Flask application
├── wsgi.py                   # WSGI entry point
├── gunicorn_config.py        # Gunicorn configuration
├── requirements.txt          # Python dependencies
├── start_server.py          # Python startup script
├── start.sh                 # Bash startup script
├── static/                  # CSS, images, etc.
├── templates/               # HTML templates
├── logs/                    # Application logs (created on first run)
│   ├── access.log
│   └── error.log
├── data.json               # Student data (created on first run)
├── attendance.json         # Attendance records
├── users.json              # User accounts
├── leaves.json             # Leave requests
├── settings.json           # Application settings
└── secret_key.txt          # Production secret key
```

---

## 🔐 Security Considerations

### 1. Secret Key
- Automatically generated on first run
- Stored in `secret_key.txt`
- **Keep this file secure and never commit to git!**

### 2. CSRF Protection
- Enabled by default
- All forms use CSRF tokens

### 3. Rate Limiting
- Default: 200 requests/day, 50 requests/hour per IP
- Adjust in `app.py` if needed

### 4. Password Hashing
- Uses Werkzeug's secure password hashing
- Passwords never stored in plain text

---

## 🌐 Production Deployment Options

### Option 1: Termux Only (Current Setup)
✅ Simple, lightweight, perfect for local network
```bash
python start_server.py
```

### Option 2: Termux + Nginx (Better Performance)
Install nginx in Termux:
```bash
pkg install nginx
```

Configure nginx using `nginx.conf.example` as reference.

### Option 3: VPS/Server Deployment
For deploying on a proper server:

1. **Install system dependencies:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Setup systemd service:**
```bash
# Edit absensi-web.service with your paths
sudo cp absensi-web.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable absensi-web
sudo systemctl start absensi-web
```

4. **Setup Nginx reverse proxy:**
```bash
sudo cp nginx.conf.example /etc/nginx/sites-available/absensi-web
# Edit the file with your domain/settings
sudo ln -s /etc/nginx/sites-available/absensi-web /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

5. **Optional: Setup SSL with Let's Encrypt:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 🔄 Running in Background (Termux)

### Method 1: Using tmux (Recommended)
```bash
# Install tmux
pkg install tmux

# Start new session
tmux new -s absensi

# Run the server
python start_server.py

# Detach: Press Ctrl+B, then D
# Reattach: tmux attach -t absensi
# Kill session: tmux kill-session -t absensi
```

### Method 2: Using nohup
```bash
nohup python start_server.py > logs/nohup.log 2>&1 &

# Check if running
ps aux | grep start_server

# Stop
kill <PID>
```

### Method 3: Using Termux Boot (Auto-start on device boot)
```bash
# Install Termux:Boot from F-Droid or Play Store
# Create startup script
mkdir -p ~/.termux/boot
cat > ~/.termux/boot/start-absensi.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd /path/to/absensiweb_production
python start_server.py
EOF

chmod +x ~/.termux/boot/start-absensi.sh
```

---

## 📊 Monitoring

### View Logs
```bash
# Access logs (HTTP requests)
tail -f logs/access.log

# Error logs
tail -f logs/error.log

# Both logs
tail -f logs/*.log
```

### Check Server Status
```bash
# If using systemd
sudo systemctl status absensi-web

# If running manually
ps aux | grep gunicorn
```

### Monitor Resources (Termux)
```bash
# Install htop
pkg install htop

# Run
htop
```

---

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# Stop the server (Ctrl+C or kill process)

# Pull latest changes (if using git)
git pull

# Update dependencies if requirements.txt changed
pip install -r requirements.txt

# Restart server
python start_server.py
```

### Backup Data
```bash
# Backup all JSON files
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz *.json secret_key.txt

# Restore
tar -xzf backup_YYYYMMDD_HHMMSS.tar.gz
```

### Database Migration
If you need to migrate from old version:
```bash
python migrate_passwords.py
```

---

## 🐛 Troubleshooting

### Port 5000 already in use
```bash
# Find process using port 5000
lsof -i :5000  # or: netstat -tulpn | grep 5000

# Kill the process
kill -9 <PID>

# Or use different port in gunicorn_config.py
bind = "0.0.0.0:8000"
```

### Permission Denied Errors
```bash
# Make scripts executable
chmod +x start.sh start_server.py

# Check file permissions
ls -la
```

### Module Not Found Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Memory Issues (Termux)
Reduce workers in `gunicorn_config.py`:
```python
workers = 1  # Minimum, saves memory
```

### Can't Access from Other Devices
- Check firewall settings
- Ensure binding to 0.0.0.0, not 127.0.0.1
- Get your local IP: `ifconfig` or `ip addr`

---

## 🔧 Development Mode

For testing/development:
```bash
python start_server.py --dev
# or
python app.py --dev
```

This enables:
- Debug mode
- Auto-reload on code changes
- Detailed error pages

**⚠️ Never use development mode in production!**

---

## 📝 Environment Variables (Optional)

You can set environment variables for configuration:

```bash
export FLASK_ENV=production
export GUNICORN_WORKERS=2
export BIND_ADDRESS=0.0.0.0:5000
```

---

## 📞 Support

For issues or questions:
1. Check logs: `logs/error.log`
2. Review this deployment guide
3. Check Flask/Gunicorn documentation
4. Review original README.md for application features

---

## ⚡ Performance Tips

1. **Use Nginx** as reverse proxy for static files
2. **Enable gzip** compression in Nginx
3. **Use CDN** for static assets if public-facing
4. **Monitor logs** for slow endpoints
5. **Adjust worker count** based on your hardware
6. **Use caching** for frequently accessed data (future enhancement)
7. **Regular backups** of JSON data files

---

## 🎉 You're Ready!

Your Flask app is now production-ready with WSGI/Gunicorn!

Start the server:
```bash
python start_server.py
```

Happy deploying! 🚀
