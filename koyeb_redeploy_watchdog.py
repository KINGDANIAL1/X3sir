import requests
import time
import os
from datetime import datetime

API_TOKEN = os.getenv("KOYEB_API_TOKEN")
SERVICE_ID = "2d8c350c"

if not API_TOKEN:
    raise RuntimeError("❌ KOYEB_API_TOKEN غير موجود")

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def get_service_status():
    url = f"https://app.koyeb.com/v1/services/{SERVICE_ID}"
    r = requests.get(url, headers=HEADERS, timeout=10)
    if r.status_code != 200:
        raise RuntimeError(r.text)

    return r.json()["service"]["status"]

def redeploy_service():
    url = f"https://app.koyeb.com/v1/services/{SERVICE_ID}/redeploy"
    r = requests.post(url, headers=HEADERS, timeout=10)

    if r.status_code == 200:
        log("♻️ Redeploy تم بنجاح")
    else:
        log(f"❌ فشل Redeploy: {r.text}")

def main():
    log("🚀 Redeploy Watchdog بدأ العمل")

    while True:
        try:
            status = get_service_status()
            log(f"📡 حالة السيرفس: {status}")

            if status in ["ERROR", "CRASHED", "STOPPED"]:
                log("⚠️ خلل مكتشف → Redeploy")
                redeploy_service()
                time.sleep(180)  # انتظار بعد redeploy
            else:
                time.sleep(60)

        except Exception as e:
            log(f"❌ خطأ: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
