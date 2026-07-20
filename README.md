یل
# 🚗 Auto Oil Store — Django E-commerce Platform

<div align="center">

![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge\&logo=django\&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge\&logo=bootstrap\&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge\&logo=sqlite\&logoColor=white)

### فروشگاه اینترنتی روغن‌های تخصصی خودرو

پلتفرم فروش آنلاین روغن موتور، روغن گیربکس، روغن هیدرولیک و سایر روانکارهای تخصصی خودرو با پنل مدیریت قدرتمند، بخش مقالات آموزشی و صفحات ارتباط با مشتری.

</div>

---

## ✨ امکانات اصلی

### 🛒 فروشگاه اینترنتی

* نمایش محصولات به‌صورت دسته‌بندی‌شده
* جستجوی سریع محصولات
* صفحه جزئیات محصول با توضیحات کامل
* مدیریت موجودی کالا
* نمایش قیمت و مشخصات فنی روغن‌ها

### 📰 بخش مقالات

* انتشار مقالات آموزشی و تخصصی خودرو
* دسته‌بندی مقالات
* بهینه‌سازی برای موتورهای جستجو (SEO Friendly)
* صفحه جزئیات مقاله با طراحی خوانا

### 📞 ارتباط با مشتری

* فرم تماس با ما
* ذخیره پیام‌های کاربران در پنل مدیریت
* صفحه درباره ما با معرفی فروشگاه و خدمات
* اطلاعات تماس و پشتیبانی

### ⚙️ پنل مدیریت

* مدیریت محصولات و دسته‌بندی‌ها
* مدیریت مقالات
* مشاهده پیام‌های تماس
* مدیریت کاربران و سفارش‌ها
* رابط کاربری ساده و کاربردی

---

## 🏗️ معماری پروژه

<pre><code>auto_oil_store/
├── account_module/        # مدیریت کاربران
├── product_module/        # محصولات و دسته‌بندی‌ها
├── article_module/        # مقالات وبلاگ
├── contact_module/        # فرم تماس با ما
├── home_module/           # صفحه اصلی
├── templates/             # قالب‌های HTML
├── static/                # فایل‌های CSS و JS
├── media/                 # تصاویر محصولات و مقالات
├── manage.py
└── requirements.txt
</code></pre>

---

## 🛠️ تکنولوژی‌های استفاده‌شده

| بخش               | تکنولوژی                 |
| ----------------- | ------------------------ |
| Backend           | Django 5.x               |
| زبان برنامه‌نویسی | Python 3.12+             |
| Frontend          | HTML5, CSS3, Bootstrap 5 |
| پایگاه داده       | SQLite                   |
| مدیریت فایل       | Django Media             |
| قالب‌ها           | Django Templates         |

---

## 🚀 راه‌اندازی پروژه

### 1) کلون کردن پروژه

<pre><code>git clone https://github.com/your-username/auto-oil-store.git
cd auto-oil-store
</code></pre>

### 2) ساخت محیط مجازی

<pre><code>python -m venv .venv
</code></pre>

فعال‌سازی در ویندوز:

<pre><code>.venv\\Scripts\\activate
</code></pre>

فعال‌سازی در لینوکس / مک:

<pre><code>source .venv/bin/activate
</code></pre>

### 3) نصب وابستگی‌ها

<pre><code>pip install -r requirements.txt
</code></pre>

### 4) اعمال مایگریشن‌ها

<pre><code>python manage.py migrate
</code></pre>

### 5) ساخت ادمین

<pre><code>python manage.py createsuperuser
</code></pre>

### 6) اجرای سرور

<pre><code>python manage.py runserver
</code></pre>

اکنون پروژه در آدرس زیر در دسترس است:

<pre><code>http://127.0.0.1:8000/
</code></pre>

---

## 🔐 ورود به پنل مدیریت

پس از اجرای پروژه، برای ورود به پنل مدیریت از آدرس زیر استفاده کنید:

<pre><code>http://127.0.0.1:8000/admin/
</code></pre>

---

## 📸 صفحات اصلی

* 🏠 **صفحه اصلی** — معرفی فروشگاه و محصولات ویژه
* 🛍️ **فروشگاه** — لیست کامل روغن‌های خودرو
* 📄 **جزئیات محصول** — مشخصات فنی و توضیحات
* 📰 **وبلاگ** — مقالات آموزشی خودرو و نگهداری موتور
* 📞 **تماس با ما** — ارسال پیام و اطلاعات ارتباطی
* ℹ️ **درباره ما** — معرفی فروشگاه و اهداف مجموعه

---

## 📦 نمونه فایل requirements.txt

<pre><code>Django>=5.0
Pillow>=10.0
</code></pre>

---

## 🌟 ویژگی‌های طراحی

* طراحی **واکنش‌گرا (Responsive)** برای موبایل و دسکتاپ
* رابط کاربری مدرن و مینیمال
* سرعت بارگذاری مناسب
* ساختار مناسب برای توسعه و افزودن امکانات جدید
* کدنویسی ماژولار و قابل نگهداری

---

## 🔮 توسعه‌های پیشنهادی

* اتصال درگاه پرداخت
* سیستم سبد خرید پیشرفته
* ثبت و پیگیری سفارش
* سیستم نظرات کاربران
* فیلتر محصولات بر اساس برند و گرانروی
* جستجوی Ajax
* API با Django REST Framework

---

## 🤝 مشارکت در پروژه

اگر پیشنهادی برای بهبود پروژه دارید:

<pre><code>git checkout -b feature/amazing-feature
git commit -m "Add amazing feature"
git push origin feature/amazing-feature
</code></pre>

سپس Pull Request ایجاد کنید.

---

## 📄 لایسنس

این پروژه تحت لایسنس **MIT** منتشر شده است و استفاده، ویرایش و توسعه آن آزاد است.

---

<div align="center">

### 💡 درباره پروژه

این پروژه با هدف ارائه یک **فروشگاه اینترنتی تخصصی روغن خودرو** طراحی شده و تلاش شده است تا علاوه بر فروش محصولات، محتوای آموزشی مفیدی نیز در اختیار کاربران قرار گیرد.

**اگر این پروژه برای شما مفید بود، ⭐ ستاره دادن به مخزن فراموش نشود!**

</div>
