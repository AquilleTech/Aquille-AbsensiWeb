# 🎓 Absensi Web - Production Ready

A production-ready attendance management system built with Flask and deployed using Gunicorn WSGI server. Optimized for Termux and lightweight environments.

## ✨ Features

- ✅ **Student Management**: Add, edit, delete student records
- ✅ **QR Code Attendance**: Quick check-in with QR codes
- ✅ **Manual Attendance**: Mark attendance manually
- ✅ **Leave Requests**: Submit and manage leave applications
- ✅ **Late Tracking**: Automatic late detection
- ✅ **Reporting**: Export attendance data to CSV/Excel
- ✅ **Multi-user System**: Role-based access control
- ✅ **Telegram Notifications**: Real-time alerts
- ✅ **CSRF Protection**: Secure forms
- ✅ **Rate Limiting**: DDoS protection
- ✅ **Production Ready**: Gunicorn WSGI server

## 🚀 Quick Start (Termux)

### 1. Install Python
```bash
pkg update && pkg upgrade
pkg install python
```

### 2. Install Dependencies
```bash
cd absensiweb_production
pip install -r requirements.txt
```

### 3. Start Server
```bash
python start_server.py
```

Server runs on: **http://0.0.0.0:5000**

### 4. First Time Setup
Visit: **http://localhost:5000/setup**
- Create your super admin account
- Configure settings at `/admin/settings`

## 📚 Documentation

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete deployment instructions
- **[QUICK_START.md](QUICK_START.md)** - Command reference cheat sheet

## 🔧 Configuration

### Change Port
Edit `gunicorn_config.py`:
```python
bind = "0.0.0.0:8000"  # Change to your preferred port
```

### Adjust Workers (Memory)
Edit `gunicorn_config.py`:
```python
workers = 1  # Reduce for low memory devices
```

### Application Settings
Configure via web interface: `/admin/settings`

## 📂 Project Structure

```
absensiweb_production/
├── app.py                 # Main application
├── wsgi.py                # WSGI entry point
├── gunicorn_config.py     # Server configuration
├── start_server.py        # Startup script (Python)
├── start.sh               # Startup script (Bash)
├── requirements.txt       # Dependencies
├── static/                # CSS, images
├── templates/             # HTML templates
└── logs/                  # Server logs
```

## 🎭 User Roles

| Role | Permissions |
|------|-------------|
| **Super Admin** | Full system access, user management |
| **Admin** | Manage students, settings, attendance |
| **Teacher** | View and mark attendance |
| **Viewer** | Read-only access |

## 🔐 Security Features

- ✅ CSRF token protection
- ✅ Werkzeug password hashing
- ✅ Rate limiting (50 requests/hour per IP)
- ✅ Input sanitization (XSS prevention)
- ✅ Persistent secret key generation
- ✅ Session management

## 🌐 Deployment Options

### 1. Termux Only (Recommended for Beginners)
```bash
python start_server.py
```

### 2. Background with tmux
```bash
tmux new -s absensi
python start_server.py
# Detach: Ctrl+B then D
```

### 3. VPS/Server with Nginx
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete instructions.

## 📊 Monitoring

### View Logs
```bash
tail -f logs/access.log  # HTTP requests
tail -f logs/error.log   # Errors
```

### Check Process
```bash
ps aux | grep gunicorn
```

## 🔄 Maintenance

### Backup Data
```bash
tar -czf backup_$(date +%Y%m%d).tar.gz *.json secret_key.txt
```

### Update Application
```bash
# Stop server (Ctrl+C)
git pull  # If using git
pip install -r requirements.txt
python start_server.py
```

## 🐛 Troubleshooting

**Port already in use:**
```bash
lsof -i :5000
kill -9 <PID>
```

**Can't access from network:**
- Verify binding to 0.0.0.0 (not 127.0.0.1)
- Check firewall settings
- Find your IP: `ifconfig` or `ip addr`

**Out of memory:**
- Reduce workers to 1 in `gunicorn_config.py`

## 📱 Telegram Notifications

1. Create a bot via [@BotFather](https://t.me/botfather)
2. Get your Chat ID via [@userinfobot](https://t.me/userinfobot)
3. Configure in `/admin/settings`
4. Test connection using the test button

## 🛠️ Tech Stack

- **Flask 3.0.0** - Web framework
- **Gunicorn 21.2.0** - WSGI HTTP server
- **Flask-Limiter** - Rate limiting
- **Werkzeug** - Security utilities
- **QRCode** - QR code generation
- **OpenPyXL** - Excel export
- **Requests** - HTTP client

## 📋 Requirements

- Python 3.7+
- 512MB RAM minimum (2 workers)
- 256MB RAM minimum (1 worker)
- 50MB disk space

## 🔮 Future Enhancements

- [ ] PostgreSQL/MySQL support
- [ ] API endpoints for mobile app
- [ ] Face recognition check-in
- [ ] Advanced analytics dashboard
- [ ] Multi-school support
- [ ] Email notifications

## 📄 License

This project is open source. Feel free to use and modify.

## 🙏 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

Having issues? Check:
1. [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Detailed instructions
2. [QUICK_START.md](QUICK_START.md) - Command reference
3. `logs/error.log` - Error messages

## 🎉 Credits

Original Flask app converted to production-ready WSGI deployment.

---

**Status**: ✅ Production Ready  
**Version**: 3.2 (WSGI)  
**Platform**: Termux / Linux / VPS

Start your server: `python start_server.py` 🚀
