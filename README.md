# تقویم فارسی ایران

یک فید اشتراکی واحد با تاریخ شمسی روزانه و مناسبت‌های ثبت‌شده، برای Apple Calendar، Google Calendar، Outlook و برنامه‌های سازگار با iCalendar.

## لینک‌ها

- صفحهٔ پروژه: https://aliimor.github.io/persian-calendar/
- فید اشتراک: https://aliimor.github.io/persian-calendar/calendars/persian.ics
- فایل مستقیم GitHub: https://raw.githubusercontent.com/aliimor/persian-calendar/main/calendars/persian.ics

> GitHub Pages باید در تنظیمات مخزن فعال شود تا لینک وب‌سایت کار کند. Workflow تقویم پس از اولین اجرا فایل ICS را می‌سازد.

## ساختار

- \`index.html\`: صفحهٔ معرفی و لینک اشتراک
- \`data/events.json\`: مناسبت‌ها و تعطیلات قابل ویرایش
- \`scripts/generate_calendar.py\`: تولید فایل iCalendar
- \`calendars/persian.ics\`: فید واحد خروجی
- \`.github/workflows/update-calendar.yml\`: تولید خودکار روزانه و با هر تغییر داده/اسکریپت

## اجرای محلی

\`\`\`bash
python -m pip install -r requirements.txt
python scripts/generate_calendar.py
\`\`\`

## افزودن یا اصلاح مناسبت

در \`data/events.json\` یک مورد به آرایهٔ \`events\` اضافه کنید:

\`\`\`json
{
  "date": "1405/07/16",
  "title": "عنوان مناسبت",
  "category": "official-holiday"
}
\`\`\`

تاریخ به قالب \`YYYY/MM/DD\` هجری شمسی است. برای مناسبت‌های غیرتعطیل، از دسته‌ای مانند \`iranian-observance\` استفاده کنید. پس از Commit، Workflow فایل ICS را دوباره تولید می‌کند.

## منابع و دقت

دادهٔ اولیهٔ تعطیلات ۱۴۰۵ از [IranHollidaysJSON](https://github.com/iyazdanicharati/IranHollidaysJSON/blob/main/1405.json) دریافت شده است. این منبع، منبع رسمی دولتی نیست؛ قبل از اعلام تقویم به‌عنوان «کامل و رسمی»، داده باید با تقویم رسمی کشور بررسی و در صورت نیاز اصلاح شود. تاریخ‌های قمری و اعلامیه‌های رسمی ممکن است تغییر کنند.

## مجوز

کد پروژه در حال توسعه است. مجوز دادهٔ منبع باید جداگانه بررسی شود؛ فایل داده با ارجاع به منبع نگهداری شده است.
