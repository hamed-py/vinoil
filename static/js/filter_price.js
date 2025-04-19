document.addEventListener("DOMContentLoaded", function () {
    const getElements = () => ({
        priceRange: document.getElementById("priceRange"),
        priceMin: document.getElementById("price-min"),
        priceMax: document.getElementById("price-max"),
        amountMin: document.getElementById("amount-min"),
        sliderTrack: document.getElementById("slider-track"),
        resetButton: document.getElementById("reset-filter")
    });

    const elements = getElements();

    // نمایش وضعیت المنت‌ها در کنسول برای دیباگ
    console.log("عناصر دریافت شده:", elements);

    // اگر یکی از عناصر ضروری در DOM وجود نداشت، اسکریپت را متوقف کن
    if (!elements.priceRange || !elements.priceMin || !elements.priceMax || !elements.amountMin) {
        console.warn('خطا: یکی از عناصر ضروری در DOM وجود ندارد!');
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

            // انیمیشن برای اسلایدر
            elements.sliderTrack.style.transition = "all 0.3s ease";
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

        // به‌روزرسانی اسلایدر گرافیکی
        updateSliderGraphic(minValue, maxValue);

        isUpdating = false;
    };

    // افزودن رویداد
    const addEvent = (element, event, handler) => {
        if (element) element.addEventListener(event, handler);
    };

    // رویدادها
    addEvent(elements.priceRange, 'input', () => {
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

    // رویداد دکمه ریست فیلتر
    addEvent(elements.resetButton, 'click', (event) => {
        event.preventDefault();
        // بازنشانی مقادیر
        elements.priceMin.value = 0;
        elements.priceMax.value = bdMaxPrice;
        elements.priceRange.value = 0;
        elements.amountMin.textContent = 0;
        updateSlider();
    });

    // مقداردهی اولیه
    elements.priceMin.value = validateInput(elements.priceMin.value);
    elements.priceMax.value = validateInput(elements.priceMax.value, true);
    updateSlider();
});
