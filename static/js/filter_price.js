function updatePriceDisplay(value) {
    document.getElementById("amount").textContent = Number(value).toLocaleString('fa-IR');
}
document.addEventListener("DOMContentLoaded", function () {
    // گرفتن المنت‌های مورد نیاز از DOM
    const getElements = () => ({
        priceRange: document.getElementById("priceRange"),
        priceMin: document.getElementById("price-min"),
        priceMax: document.getElementById("price-max"),
        amountMin: document.getElementById("amount-min"),
        sliderTrack: document.getElementById("slider-track") // اختیاری
    });

    const elements = getElements();

    // برای دیباگ، نمایش وضعیت المنت‌ها در کنسول:
    console.log("عناصر دریافت شده:", elements);

    // بررسی وجود المنت‌های ضروری
    if (!elements.priceRange || !elements.priceMin || !elements.priceMax || !elements.amountMin) {
        console.error('خطا: یکی از عناصر ضروری در DOM وجود ندارد!');
        return;
    }

    // مقدار دهی اولیه
    const bdMaxPrice = parseInt(elements.priceRange.max) || 1000000; // مقدار پیش‌فرض
    let isUpdating = false; // جلوگیری از حلقه بی‌نهایت

    // تابع اعتبارسنجی ورودی‌ها
    const validateInput = (value, isMax = false) => {
        const numValue = Math.max(parseInt(value) || 0, 0);
        return isMax ? Math.min(numValue, bdMaxPrice) : numValue;
    };

    // به‌روزرسانی گرافیکی اسلایدر
    const updateSliderGraphic = (minValue, maxValue) => {
        if (elements.sliderTrack) {
            const percentMin = (minValue / bdMaxPrice) * 100;
            const percentMax = (maxValue / bdMaxPrice) * 100;
            elements.sliderTrack.style.left = `${percentMin}%`;
            elements.sliderTrack.style.width = `${percentMax - percentMin}%`;
        }
    };

    // همگام‌سازی و به‌روزرسانی ورودی‌ها و اسلایدر
    const updateSlider = () => {
        if (isUpdating) return;
        isUpdating = true;

        let minValue = validateInput(elements.priceMin.value);
        let maxValue = validateInput(elements.priceMax.value, true);

        // کنترل محدوده صحیح: اگر مقدار حد پایین از حد بالا تجاوز کرد
        if (minValue > maxValue) {
            minValue = maxValue;
            elements.priceMin.value = minValue;
            elements.priceRange.value = minValue;
        }

        if (maxValue > bdMaxPrice) {
            maxValue = bdMaxPrice;
            elements.priceMax.value = maxValue;
        }

        // به‌روزرسانی نمایش مقدار
        elements.amountMin.textContent = minValue.toLocaleString('fa-IR');

        // به‌روزرسانی اسلایدر گرافیکی در صورت وجود
        updateSliderGraphic(minValue, maxValue);

        isUpdating = false;
    };

    // تابع کمکی جهت افزودن رویداد با بررسی وجود المنت
    const addEvent = (element, event, handler) => {
        if (element) element.addEventListener(event, handler);
    };

    // تعریف رویدادهای ورودی برای همگام‌سازی عناصر
    addEvent(elements.priceRange, 'input', () => {
        // همگام سازی مقدار ورودی عددی با اسلایدر
        elements.priceMin.value = elements.priceRange.value;
        updateSlider();
    });

    addEvent(elements.priceMin, 'input', () => {
        elements.priceMin.value = validateInput(elements.priceMin.value);
        elements.priceRange.value = elements.priceMin.value;
        updateSlider();
    });

    addEvent(elements.priceMax, 'input', () => {
        elements.priceMax.value = validateInput(elements.priceMax.value, true);
        updateSlider();
    });

    // مقداردهی اولیه ورودی‌ها و به‌روزرسانی نمایش
    elements.priceMin.value = validateInput(elements.priceMin.value);
    elements.priceMax.value = validateInput(elements.priceMax.value, true);
    updateSlider();
});
