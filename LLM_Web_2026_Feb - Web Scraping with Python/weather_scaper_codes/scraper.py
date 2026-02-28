import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

# Website က Bot လို့ မသတ်မှတ်အောင် Browser တစ်ခုလို ဟန်ဆောင်ဖို့ Header သတ်မှတ်ခြင်း
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

BASE_URL = "https://en.allmetsat.com/metar-taf/asia.php?icao={}"


def fetch_metar(icao: str) -> dict:
    # သတ်မှတ်ထားတဲ့ လေဆိပ်ကုဒ်အတွက် URL ကို တည်ဆောက်ပြီး Data တောင်းဆိုခြင်း
    url = BASE_URL.format(icao)
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:  # အကယ်၍ connection မအောင်မြင်ရင် ဘာမှပြန်မပေးဘူး
        return None

    # HTML တွေကို နားလည်အောင် BeautifulSoup နဲ့ Parse လုပ်ခြင်း
    soup = BeautifulSoup(response.text, "html.parser")
    # ရာသီဥတုအချက်အလက်ရှိတဲ့ div ကို ရှာခြင်း
    weather_box = soup.find("div", class_="c1b")

    if not weather_box:
        return None

    lines = weather_box.find_all("div", class_="mt")
    data = {"icao": icao}

    for line in lines:
        text = line.text.strip()

        # အစီရင်ခံတဲ့အချိန် (UTC) ကို ရှာဖွေပြီး Local Time (KST) သို့ ပြောင်းလဲခြင်း
        if text.startswith("The report was made"):
            # Extract UTC time from full sentence
            # Example: "The report was made 34 minutes ago, at 00:30 UTC"
            utc_time = text.split("at ")[1].split(" UTC")[0].strip()

            # Get current UTC date safely (timezone-aware)
            now_utc = datetime.now(timezone.utc)

            # ယနေ့ရက်စွဲနဲ့ website ကရတဲ့ အချိန်ကို ပေါင်းစပ်ခြင်း
            utc_dt = now_utc.replace(
                hour=int(utc_time.split(":")[0]),
                minute=int(utc_time.split(":")[1]),
                second=0,
                microsecond=0
            )

            # UTC မှ ကိုရီးယားစံတော်ချိန် (UTC+9) သို့ ပြောင်းခြင်း
            kst_dt = utc_dt.astimezone(
                timezone(timedelta(hours=9))
            )
            data["created_at"] = datetime.now(
                kst_dt.tzinfo).strftime("%Y-%m-%d %H:%M:%S")
            data["report_time_utc"] = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
            data["report_time_kst"] = kst_dt.strftime("%Y-%m-%d %H:%M:%S")

        # လေတိုက်နှုန်းနှင့် လမ်းကြောင်းကို ရှာခြင်း
        elif text.startswith("Wind"):
            bolds = line.find_all("b")
            data["wind_speed_kt"] = bolds[0].text
            data["wind_direction"] = bolds[1].text

        # အပူချိန်ကို ရှာခြင်း
        elif text.startswith("Temperature"):
            data["temperature_C"] = line.find("b").text

        # စိုထိုင်းဆကို ရှာခြင်း
        elif text.startswith("Humidity"):
            data["humidity_percent"] = line.find("b").text

        # လေဖိအားကို ရှာခြင်း
        elif text.startswith("Pressure"):
            data["pressure_hPa"] = line.find("b").text

        # မြင်ကွင်းအကွာအဝေးကို ရှာခြင်း
        elif text.startswith("Visibility"):
            data["visibility"] = "CAVOK" if "10 km or more" in text else text

    return data
