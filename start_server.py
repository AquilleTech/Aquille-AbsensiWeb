#!/usr/bin/env python3
"""
Alternative startup script for systems without bash
For Termux: python start_server.py
"""

import os
import sys
import subprocess

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Error: {description} failed")
        return False
    print(f"✅ {description} completed")
    return True

def main():
    print("=" * 50)
    print("🎓 Absensi Web - Production Server Startup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found. Please run this script from the project directory.")
        sys.exit(1)
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Check for development mode
    dev_mode = '--dev' in sys.argv
    
    if dev_mode:
        print("\n🔧 Starting in DEVELOPMENT mode...")
        subprocess.run([sys.executable, 'app.py', '--dev'])
    else:
        print("\n🚀 Starting in PRODUCTION mode...")
        
        # Install dependencies if needed
        print("\n📦 Installing dependencies...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '--upgrade', 'pip'])
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '-r', 'requirements.txt'])
        
        # Initialize data files
        print("\n📁 Initializing data files...")
        from wsgi import init_data_files
        init_data_files()
        
        print("\n" + "=" * 50)
        print("🌐 Server starting on http://0.0.0.0:5000")
        print("=" * 50)
        print("\n📝 Logs will be written to:")
        print("   - logs/access.log")
        print("   - logs/error.log")
        print("\n⏹️  Press Ctrl+C to stop the server\n")
        
        # Start Gunicorn
        subprocess.run([
            sys.executable, '-m', 'gunicorn',
            '-c', 'gunicorn_config.py',
            'wsgi:application'
        ])

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
