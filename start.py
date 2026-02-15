#!/usr/bin/env python3
import os
import subprocess
import requests
import re
import time

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Jalankan app.py
    print("🚀 Starting Flask application...")
    app_proc = subprocess.Popen(["python3", os.path.join(base_dir, "app.py")])

    # Tunggu Flask siap
    print("⏳ Waiting for Flask to start...")
    time.sleep(5)

    # Jalankan cloudflared tunnel ke localhost:5000
    print("🌐 Starting Cloudflare tunnel...")
    cmd = ["cloudflared", "tunnel", "--url", "http://localhost:5000"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    tunnel_url = None
    # Cari URL dari output cloudflared
    for line in proc.stdout:
        print(line.strip())
        match = re.search(r"(https://[a-z0-9\-]+\.trycloudflare\.com)", line)
        if match:
            tunnel_url = match.group(1)
            break

    if not tunnel_url:
        print("❌ Gagal mendapatkan URL Cloudflared")
        return

    print(f"\n✅ Cloudflared URL: {tunnel_url}")

    # Shorten URL pakai spoo.me
    try:
        print("🔗 Creating short URL...")
        response = requests.post(
            "https://spoo.me",
            headers={"Accept": "application/json"},
            data={"url": tunnel_url},
            timeout=10
        )
        if response.status_code == 200:
            short_url = response.json().get("short_url")
            print(f"✅ Short URL: {short_url}")
        else:
            print(f"❌ Error shortening URL: {response.text}")
    except Exception as e:
        print(f"❌ Exception during URL shortening: {e}")

    print("\n" + "="*50)
    print("🎉 Application is running!")
    print(f"🌐 Access via: {tunnel_url}")
    print("="*50 + "\n")

    # Biarkan proses tetap jalan
    try:
        proc.wait()
    except KeyboardInterrupt:
        print("\n⚠️  Stopping application...")
        proc.terminate()
        app_proc.terminate()
        print("✅ Application stopped")

if __name__ == "__main__":
    main()
