from database import init_db
from scheduler import start_scheduler

if __name__ == "__main__":
    init_db()  # Database အရင်ပြင်ဆင်မယ်
    start_scheduler()  # Scheduler စတင်မယ်
