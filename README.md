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

دادهٔ فعلی مناسبت‌های ۱۴۰۵ از [مخزن alirezadesh/jalali_calendar](https://github.com/alirezadesh/jalali_calendar/blob/main/1405_data.json) نرمال‌سازی شده و [تقویم مناسبت‌های ۱۴۰۵ در TaghvimShamsi](https://taghvimshamsi.ir/occasions/1405/) به‌عنوان منبع تطبیق اولیه ثبت شده است. این منابع به‌خودی‌خود تأیید رسمی دولتی محسوب نمی‌شوند؛ بنابراین تا زمانی که تاریخ‌ها و تعطیلی‌ها با تقویم رسمی منتشرشدهٔ کشور تطبیق داده نشده‌اند، این پروژه نباید «تقویم رسمی و کاملاً تأییدشده» معرفی شود. تاریخ‌های قمری ممکن است با اعلام رسمی تغییر کنند. اسکریپت `scripts/validate_events.py` قالب تاریخ، بازهٔ پوشش، دسته‌بندی و تکراری بودن رکوردها را کنترل می‌کند؛ این کنترل ساختاری جایگزین تأیید منبع نیست.

## مجوز

کد پروژه در حال توسعه است. مجوز دادهٔ منبع باید جداگانه بررسی شود؛ فایل داده با ارجاع به منبع نگهداری شده است.
