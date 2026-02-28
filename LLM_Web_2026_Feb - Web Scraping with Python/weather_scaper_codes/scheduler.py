from apscheduler.schedulers.background import BackgroundScheduler
from scraper import fetch_metar
from database import save_to_db
import time

ICAOS = ["RKSI", "RKPC", "RKSS"]  # စစ်ဆေးမည့် လေဆိပ်ကုဒ်များ


def metar_job():
    print("Running METAR job...")

    for icao in ICAOS:
        data = fetch_metar(icao)  # Website မှ ဒေတာယူမယ်
        inserted = save_to_db(data)  # Database ထဲ သိမ်းမယ်

        if inserted:
            print(f"Saved {icao}")
        else:
            # ရှိပြီးသားဆိုရင် ကျော်သွားမယ်
            print(f"Skipped {icao} (duplicate)")


def start_scheduler():
    metar_job()  # စစချင်းမှာ တစ်ကြိမ်ချက်ချင်း run မယ်

    # နောက်ကွယ်မှာ အလုပ်လုပ်မယ့် Scheduler တစ်ခု တည်ဆောက်မယ်
    scheduler = BackgroundScheduler()
    # ၁၀ မိနစ်တစ်ခါ metar_job ကို run ဖို့ သတ်မှတ်မယ်
    scheduler.add_job(metar_job, "interval", minutes=10)
    # scheduler.add_job(metar_job, "cron", minute=32)
    # scheduler.add_job(metar_job, "cron", hour=13, minute=0)

    scheduler.start()
    try:
        # ပရိုဂရမ် မပိတ်သွားအောင် ၁ စက္ကန့်တစ်ခါ loop ပတ်ပြီး စောင့်နေမယ်
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        # Ctrl+C နှိပ်ရင် ပုံမှန်အတိုင်း ပိတ်သွားအောင် လုပ်ခြင်း
        print("Shutting down...")
        scheduler.shutdown()
