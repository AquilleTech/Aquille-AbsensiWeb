#!/usr/bin/env python3
"""
Automatic setup script for Absensi Web
Handles first-time installation and configuration
"""

import os
import sys
import subprocess
import platform

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def run_command(cmd, description, ignore_errors=False):
    """Run a command with error handling"""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            check=not ignore_errors,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return True
        else:
            if not ignore_errors:
                print(f"❌ {description} - Failed")
                if result.stderr:
                    print(f"   Error: {result.stderr[:200]}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed: {e}")
        return False

def check_python_version():
    """Check if Python version is adequate"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ required. Current version:", 
              f"{version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def detect_platform():
    """Detect if running on Termux"""
    if os.path.exists('/data/data/com.termux'):
        return 'termux'
    elif platform.system() == 'Linux':
        return 'linux'
    else:
        return 'other'

def main():
    print_header("🎓 Absensi Web - Automatic Setup")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Detect platform
    plat = detect_platform()
    print(f"📱 Platform detected: {plat.upper()}")
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("\n❌ Error: app.py not found!")
        print("Please run this script from the project directory.")
        sys.exit(1)
    
    print("\n📦 Starting installation...\n")
    
    # 1. Upgrade pip
    run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Upgrading pip",
        ignore_errors=True
    )
    
    # 2. Install dependencies
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    ):
        print("\n⚠️  Some dependencies failed to install.")
        print("   You may need to install system packages first.")
        if plat == 'termux':
            print("\n   Try running:")
            print("   pkg install libxml2 libxslt libjpeg-turbo")
    
    # 3. Create necessary directories
    print("\n📁 Creating directories...")
    os.makedirs('logs', exist_ok=True)
    print("✅ Created logs/ directory")
    
    # 4. Initialize data files
    print("\n💾 Initializing data files...")
    try:
        from wsgi import init_data_files
        init_data_files()
        print("✅ Data files initialized")
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize data files: {e}")
    
    # 5. Make scripts executable
    print("\n🔧 Setting permissions...")
    scripts = ['start_server.py', 'start.sh']
    for script in scripts:
        if os.path.exists(script):
            try:
                os.chmod(script, 0o755)
                print(f"✅ Made {script} executable")
            except:
                pass
    
    # 6. Display completion message
    print_header("✨ Setup Complete!")
    
    print("📝 Quick Start Guide:\n")
    print("1️⃣  Start the server:")
    print(f"   python start_server.py\n")
    
    print("2️⃣  Access the application:")
    print("   http://localhost:5000\n")
    
    print("3️⃣  First-time setup:")
    print("   Visit: http://localhost:5000/setup")
    print("   Create your super admin account\n")
    
    print("4️⃣  Run in background (optional):")
    if plat == 'termux':
        print("   pkg install tmux  # If not installed")
        print("   tmux new -s absensi")
        print("   python start_server.py")
        print("   # Press Ctrl+B then D to detach\n")
    else:
        print("   nohup python start_server.py > logs/nohup.log 2>&1 &\n")
    
    print("📚 Documentation:")
    print("   DEPLOYMENT_GUIDE.md - Complete deployment guide")
    print("   QUICK_START.md      - Command reference")
    print("   README_PRODUCTION.md - Overview\n")
    
    # Ask if user wants to start now
    try:
        response = input("🚀 Start the server now? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            print("\n" + "=" * 60)
            print("Starting server... Press Ctrl+C to stop")
            print("=" * 60 + "\n")
            subprocess.run([sys.executable, 'start_server.py'])
    except KeyboardInterrupt:
        print("\n\n👋 Setup complete! Start server with: python start_server.py")
        sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)
