from pyrogram import Client, filters
from datetime import datetime
import json
import os

# ------------------ تنظیمات ربات ------------------

api_id = 25470012
api_hash = "0fcfbf4b6311835062b1f052c5b5a708"
bot_token = "8769258261:AAEORKxpra7uTz2JYhO0P7jybEutJ-W_YTA"

app = Client(
    "sub_helper_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

# ------------------ فایل ذخیره ------------------

SUB_FILE = "subs.json"

# ------------------ متن اشتراک ------------------

SERVICE_TEXT = """✅ سرویس با موفقیت ایجاد شد

👤 نام کاربری سرویس : {username}
🔑 رمز عبور سرویس : {password}
🌿 نام سرویس:  ⚡️ پلن S ( ماهه)  حجم: 5 گیگ
‏🇺🇳 لوکیشن: Magic_VIP-OpenVPN
⏳ مدت زمان: 30  روز
🗜 حجم سرویس:  5 گیگابایت"""

# ------------------ ساخت فایل ------------------

if not os.path.exists(SUB_FILE):

    with open(SUB_FILE, "w", encoding="utf-8") as f:

        json.dump([], f)

# ------------------ لود اشتراک‌ها ------------------

def load_subs():

    with open(SUB_FILE, "r", encoding="utf-8") as f:

        return json.load(f)

# ------------------ ذخیره اشتراک‌ها ------------------

def save_subs(data):

    with open(SUB_FILE, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

# ------------------ افزودن اشتراک ------------------

@app.on_message(
    filters.text
    & filters.regex(r"^(addsub|Addsub)$")
)
async def add_sub(client, message):

    if not message.reply_to_message:

        await message.reply_text(
            "⚠️ روی پیام اشتراک‌ها ریپلای کن"
        )

        return

    txt = message.reply_to_message.text.strip()

    lines = []

    for line in txt.splitlines():

        line = line.strip()

        if line:

            lines.append(line)

    if len(lines) < 2:

        await message.reply_text(
            "⚠️ فرمت اشتراک اشتباه است"
        )

        return

    subs = load_subs()

    added = 0
    duplicated = 0

    for i in range(0, len(lines), 2):

        try:

            username = lines[i]
            password = lines[i + 1]

        except:

            break

        exists = False

        for sub in subs:

            if sub["username"] == username:

                exists = True
                break

        if exists:

            duplicated += 1
            continue

        subs.append({

            "username": username,
            "password": password,
            "used": False,
            "date": datetime.now().strftime("%Y/%m/%d - %H:%M")

        })

        added += 1

    save_subs(subs)

    await message.reply_text(

        f"✅ ثبت شد : {added}\n"
        f"⚠️ تکراری : {duplicated}"

    )

# ------------------ دریافت اشتراک ------------------

@app.on_message(
    filters.text
    & filters.regex(r"^(getsub|اشتراک)$")
)
async def get_sub(client, message):

    subs = load_subs()

    for sub in subs:

        if not sub["used"]:

            sub["used"] = True

            save_subs(subs)

            text = SERVICE_TEXT.format(

                username=sub["username"],
                password=sub["password"]

            )

            await message.reply_text(text)

            return

    await message.reply_text(
        "❌ اشتراکی باقی نمانده"
    )

# ------------------ آمار + لیست اشتراک‌ها ------------------

@app.on_message(
    filters.text
    & filters.regex(r"^(subs|اشتراک ها)$")
)
async def subs_stats(client, message):

    subs = load_subs()

    total = len(subs)

    used = 0
    left = 0

    txt = f"📦 کل اشتراک‌ها : {total}\n\n"

    txt += "━━━━━━━━━━━━━━\n\n"

    for i, sub in enumerate(subs, start=1):

        if sub["used"]:

            status = " ❌مصرف شده"
            used += 1

        else:

            status = "🟢 باقی مانده"
            left += 1

        txt += (

            f"{i}. "
            f"{sub['username']} | "
            f"{sub['password']}\n"
            f"{status}\n"
            f"📅 {sub.get('date', 'قدیمی')}\n\n"

        )

    txt += (
        "━━━━━━━━━━━━━━\n\n"
        f"❌ مصرف شده : {used}\n"
        f"🟢 باقی مانده : {left}"
    )

    await message.reply_text(txt)

# ------------------ نمایش باقی‌مانده‌ها ------------------

@app.on_message(
    filters.text
    & filters.regex(r"^(leftsubs|باقی مانده)$")
)
async def left_subs(client, message):

    subs = load_subs()

    txt = ""

    count = 0

    for sub in subs:

        if not sub["used"]:

            count += 1

            txt += (

                f"{count}. "
                f"{sub['username']} | "
                f"{sub['password']}\n"
                f"📅 {sub.get('date', 'قدیمی')}\n\n"

            )

    if not txt:

        txt = "❌ اشتراک باقی نمانده"

    await message.reply_text(txt)

# ------------------ نمایش مصرف‌شده‌ها ------------------

@app.on_message(
    filters.text
    & filters.regex(r"^(usedsubs|مصرف شده)$")
)
async def used_subs(client, message):

    subs = load_subs()

    txt = ""

    count = 0

    for sub in subs:

        if sub["used"]:

            count += 1

            txt += (

                f"{count}. "
                f"{sub['username']} | "
                f"{sub['password']}\n"
                f"📅 {sub.get('date', 'قدیمی')}\n\n"

            )

    if not txt:

        txt = "❌ اشتراک مصرف شده وجود ندارد"

    await message.reply_text(txt)

# ------------------ حذف اشتراک ------------------

@app.on_message(
    filters.text
    & filters.regex(r"^(delsub|حذف اشتراک)$")
)
async def del_sub(client, message):

    if not message.reply_to_message:

        await message.reply_text(
            "⚠️ روی یوزرنیم ریپلای کن"
        )

        return

    username = message.reply_to_message.text.strip()

    subs = load_subs()

    new_subs = []

    deleted = False

    for sub in subs:

        if sub["username"] == username:

            deleted = True
            continue

        new_subs.append(sub)

    save_subs(new_subs)

    if deleted:

        await message.reply_text(
            "✅ اشتراک حذف شد"
        )

    else:

        await message.reply_text(
            "❌ اشتراک پیدا نشد"
        )

# ------------------ پاک کردن همه اشتراک‌ها ------------------

@app.on_message(
    filters.text
    & filters.regex(r"^(clearsubs|کلر اشتراک)$")
)
async def clear_subs(client, message):

    save_subs([])

    await message.reply_text(
        "✅ همه اشتراک‌ها پاک شدند"
    )

# ------------------ پاک کردن باقی‌مانده‌ها ------------------

@app.on_message(
    filters.text
    & filters.regex(r"^(clearleft|کلر باقی مانده)$")
)
async def clear_left(client, message):

    subs = load_subs()

    new_subs = []

    for sub in subs:

        if sub["used"]:

            new_subs.append(sub)

    save_subs(new_subs)

    await message.reply_text(
        "✅ اشتراک‌های باقی‌مانده پاک شدند"
    )

# ------------------ ران ------------------

print("Bot Started ✅")

app.run()