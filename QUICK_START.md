# 🚀 Quick Reference - Absensi Web

## Start Server (Termux)
```bash
python start_server.py
```

## Stop Server
```
Press Ctrl+C
```

## Run in Background (tmux)
```bash
# Start
tmux new -s absensi
python start_server.py

# Detach: Ctrl+B then D
# Reattach
tmux attach -t absensi
```

## View Logs
```bash
tail -f logs/access.log   # HTTP requests
tail -f logs/error.log    # Errors
```

## Backup Data
```bash
tar -czf backup_$(date +%Y%m%d).tar.gz *.json secret_key.txt
```

## Change Port
Edit `gunicorn_config.py`:
```python
bind = "0.0.0.0:8000"  # Change from 5000 to 8000
```

## Reduce Memory Usage
Edit `gunicorn_config.py`:
```python
workers = 1  # Reduce from 2 to 1
```

## Development Mode
```bash
python start_server.py --dev
```

## Access URLs
- Local: http://localhost:5000
- Network: http://YOUR_IP:5000
- Setup: http://localhost:5000/setup (first time only)
- Login: http://localhost:5000/login
- Dashboard: http://localhost:5000/dashboard

## Default Roles
- **super_admin**: Full access
- **admin**: Manage students & settings
- **teacher**: View & mark attendance
- **viewer**: Read-only access

## Troubleshooting

### Port in use
```bash
lsof -i :5000          # Find process
kill -9 <PID>          # Kill it
```

### Can't connect from other devices
- Check firewall
- Verify binding to 0.0.0.0 not 127.0.0.1
- Get IP: `ifconfig` or `ip addr`

### Out of memory
- Reduce workers to 1 in gunicorn_config.py
- Close other apps

### Dependencies error
```bash
pip install -r requirements.txt --force-reinstall
```

## Important Files
- `data.json` - Student database
- `attendance.json` - Attendance records
- `users.json` - User accounts
- `settings.json` - App settings
- `secret_key.txt` - Security key (DO NOT SHARE!)

## Security Notes
- ✅ CSRF protection enabled
- ✅ Password hashing
- ✅ Rate limiting (50/hour per IP)
- ⚠️ Keep secret_key.txt secure!
- ⚠️ Never use --dev in production!
