import sqlite3


def init_db():
    # weather.db ဆိုတဲ့ database ဖိုင်ကို ချိတ်ဆက်မယ် (မရှိရင် အသစ်ဆောက်မယ်)
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()

    # metar_weather ဆိုတဲ့ table မရှိသေးရင် တည်ဆောက်မယ်
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metar_weather (
        icao TEXT,                      -- လေဆိပ်ကုဒ် (ဥပမာ RKSI)
        report_time_kst TEXT,           -- ကိုရီးယားစံတော်ချိန်
        wind_speed_kt TEXT,             -- လေတိုက်နှုန်း
        wind_direction TEXT,            -- လေတိုက်ရာအရပ်      
        temperature_C TEXT,             -- အပူချိန် (Celsius)
        humidity_percent TEXT,          -- စိုထိုင်းမှု (ရာခိုင်နှုန်း) 
        pressure_hPa TEXT,              -- လေဖိအား (hPa)
        visibility TEXT,                -- မြင်ကွင်း (ဥပမာ CAVOK)
        created_at TEXT,                -- ဒေတာထည့်သွင်းချိန် (KST)   
        UNIQUE(icao, report_time_kst)   -- လေဆိပ်ကုဒ်နှင့် အချိန်တူရင် ဒေတာ duplicate မဖြစ်အောင် ကန့်သတ်ခြင်း
    )
    """)

    conn.commit()   # ပြောင်းလဲမှုများကို အတည်ပြုသိမ်းဆည်းမယ်
    conn.close()    # ချိတ်ဆက်မှုကို ပိတ်မယ်


def save_to_db(data: dict):
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()

    # ဒေတာအသစ်ထည့်မယ်၊ အချိန်နဲ့ နေရာတူနေရင် ignore လုပ်မယ် (မသိမ်းတော့ဘူး)
    cursor.execute("""
    INSERT OR IGNORE INTO metar_weather
    VALUES (?,?,?,?,?,?,?,?,?)
    """, (
        data.get("icao"),
        data.get("report_time_kst"),
        data.get("wind_speed_kt"),
        data.get("wind_direction"),
        data.get("temperature_C"),
        data.get("humidity_percent"),
        data.get("pressure_hPa"),
        data.get("visibility"),
        data.get("created_at")
    ))

    conn.commit()

    # rowcount == 1 ဆိုရင် ဒေတာအသစ် အောင်အောင်မြင်မြင် ထည့်ပြီးကြောင်း (True) ပြန်ပေးမယ်
    inserted = cursor.rowcount == 1
    conn.close()
    return inserted
