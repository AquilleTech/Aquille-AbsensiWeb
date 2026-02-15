# 🚀 Installation Instructions - START HERE

## For Termux Users (Easiest)

### Option 1: Automatic Setup (Recommended)
```bash
cd absensiweb_production
python setup.py
```
This will automatically:
- Check your Python version
- Install all dependencies
- Create necessary directories
- Initialize data files
- Ask if you want to start the server

### Option 2: Manual Setup
```bash
cd absensiweb_production
pip install -r requirements.txt
python start_server.py
```

## Access Your Application

After starting the server:

1. **Local Access**: http://localhost:5000
2. **Network Access**: http://YOUR_IP:5000
   - Find your IP: `ifconfig` or `ip addr`

## First Time Setup

1. Visit: http://localhost:5000/setup
2. Create your Super Admin account
3. Login and start using the system!

## Run in Background (Termux)

### Using tmux (Recommended)
```bash
# Install tmux if needed
pkg install tmux

# Start new session
tmux new -s absensi

# Run server
python start_server.py

# Detach from session: Press Ctrl+B, then D
# Reattach later: tmux attach -t absensi
# Kill session: tmux kill-session -t absensi
```

### Using nohup
```bash
nohup python start_server.py > logs/nohup.log 2>&1 &
```

## Stopping the Server

- **Foreground**: Press `Ctrl+C`
- **Background**: `kill <PID>` or `tmux kill-session -t absensi`

## What's Different from the Original?

Your Flask app is now **production-ready**:
- ✅ Uses Gunicorn WSGI server (industry standard)
- ✅ Handles multiple concurrent users
- ✅ Better performance and stability
- ✅ Secure configuration
- ✅ Auto-restarts workers if they crash
- ✅ 99% of your code unchanged!

## Need Help?

Read these files in order:
1. **QUICK_START.md** - Quick reference commands
2. **COMPARISON.md** - What changed and why
3. **DEPLOYMENT_GUIDE.md** - Complete deployment guide
4. **README_PRODUCTION.md** - Full documentation

## System Requirements

- **Python**: 3.7 or higher
- **Memory**: 256MB minimum (512MB recommended)
- **Disk**: 50MB free space
- **Platform**: Termux, Linux, or VPS

## Troubleshooting

### Port 5000 already in use
```bash
lsof -i :5000
kill -9 <PID>
```

### Can't install dependencies
```bash
# Termux
pkg install libxml2 libxslt libjpeg-turbo
pip install -r requirements.txt
```

### Out of memory
Edit `gunicorn_config.py`:
```python
workers = 1  # Reduce from 2 to 1
```

## Quick Commands

```bash
# Start server
python start_server.py

# Start in dev mode (testing only)
python start_server.py --dev

# View logs
tail -f logs/access.log

# Backup data
tar -czf backup.tar.gz *.json secret_key.txt
```

## Important Files

- `data.json` - Student records
- `attendance.json` - Attendance data
- `users.json` - User accounts
- `settings.json` - App settings
- `secret_key.txt` - Security key (keep secret!)
- `logs/` - Server logs

## Security Notes

- ✅ Keep `secret_key.txt` secure
- ✅ Never use `--dev` mode in production
- ✅ Regular backups recommended
- ✅ Rate limiting enabled (50 req/hour per IP)

## That's It!

You're ready to deploy! 🎉

**Quick start**: `python setup.py` or `python start_server.py`

---

**Questions?** Check the documentation files or logs for errors.
