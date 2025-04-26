(function() {
    document.addEventListener("DOMContentLoaded", () => {
        try {
            const slider = document.querySelector('.slider-container');

            // بررسی وجود تمام المان‌های ضروری
            if (!slider) {
                console.warn('Slider container not found');
                return;
            }

            const slidesContainer = slider.querySelector('.slides');
            const slides = Array.from(slidesContainer?.children || []);

            if (!slidesContainer || slides.length === 0) {
                console.warn('Slides not initialized properly');
                return;
            }

            let currentIndex = 0;
            let autoSlideInterval;
            const SLIDE_DURATION = 5000;

            const goToSlide = index => {
                currentIndex = (index + slides.length) % slides.length;
                slidesContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
            };

            const startAutoPlay = () => {
                if (autoSlideInterval) clearInterval(autoSlideInterval);
                autoSlideInterval = setInterval(() => goToSlide(currentIndex + 1), SLIDE_DURATION);
            };

            const stopAutoPlay = () => {
                if (autoSlideInterval) {
                    clearInterval(autoSlideInterval);
                    autoSlideInterval = null;
                }
            };

            window.changeSlide = direction => {
                stopAutoPlay();
                goToSlide(currentIndex + direction);
                startAutoPlay();
            };

            // مدیریت حافظه و خطاها
            slider.addEventListener('mouseenter', stopAutoPlay);
            slider.addEventListener('mouseleave', startAutoPlay);
            window.addEventListener('beforeunload', stopAutoPlay);
            window.addEventListener('resize', () => goToSlide(currentIndex));

            // مقداردهی اولیه ایمن
            slidesContainer.style.transform = 'translateX(0)';
            currentIndex = 0;
            startAutoPlay();

        } catch (error) {
            console.error('Slider initialization error:', error);
        }
    });
})();