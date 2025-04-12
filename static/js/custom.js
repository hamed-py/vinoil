$(document).ready(function () {
    $('#articleCommentForm').on('submit', function (e) {
        e.preventDefault();  // جلوگیری از ارسال فرم به صورت پیش‌فرض (و رفرش صفحه)

        // غیرفعال کردن دکمه ارسال به منظور جلوگیری از چندبار کلیک
        var submitButton = $(this).find('button[type="submit"]');
        if (submitButton.prop('disabled')) return;
        submitButton.prop('disabled', true);

        var comment = $('#commentText').val();
        var parentid = $('#parent_id').val();
        var articleId = $('input[name="article_id"]').val();
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            url: '/articles/add-article-comment',
            method: 'POST',
            data: {
                article_comment: comment,
                article_id: articleId,
                parent_id: parentid,
                csrfmiddlewaretoken: csrfToken
            },
            success: function (response) {
                // به روز رسانی ناحیه نظرات؛ فرض می‌کنیم که پاسخ شامل partial HTML کامل است
                $('#comments_container').html(response);
                // پاکسازی فرم پس از موفقیت
                $('#commentText').val('');
                $('#parent_id').val('');
                // اسکرول نرم به ناحیه نظرات
                document.getElementById('comments_container').scrollIntoView({behavior: 'smooth'});
            },
            error: function (xhr, status, error) {
                console.error("خطا در ارسال نظر: ", error);
                alert("خطایی در ارسال نظر رخ داده است.");
            },
            complete: function () {
                // فعالسازی مجدد دکمه ارسال
                submitButton.prop('disabled', false);
            }
        });
    });
});

function fillParentId(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById('comment_form').scrollIntoView({behavior: 'smooth'});
    document.getElementById('commentText').focus();
}

function filterProducts() {
    const filterPrice = $('#amount').text();
    const start_price = filterPrice.split(',')[0];
    const end_price = filterPrice.split(',')[1];
    $('#start_price').val(start_price);
    $('#end_price').val(end_price);
    $('#filter_form').submit();
}

function fillPage(page) {
    $('#page').val(page);
    $('#filter_form').submit();
}

$(document).ready(function () {
    $('#addToCartBtn').on('click', function (e) {
        e.preventDefault();
        // گرفتن اطلاعات فرم
        var quantity = $('#quantity').val();
        var volume = $('#volume').val();


        // ارسال درخواست Ajax به ویو ثبت سفارش
        $.ajax({
            url: addProductUrl,
            data: {
                product_id: productId,
                count: quantity,
                volume: volume  // اگر نیاز دارید حجم هم ارسال شود؛ در کد ویو نمونه اصلی استفاده نشده، ولی می‌توانید آن را به مدل اضافه کنید
            },
            dataType: 'json',
            method: 'GET',
            success: function (response) {
                Swal.fire({
                    title: "اعلان",
                    text: response.text,
                    icon: response.icon,
                    confirmButtonColor: "#3085d6",
                    confirmButtonText: response.confirm_button_text
                }).then((result) => {
                    if (result.isConfirmed && result.status === 'not_auth') {
                        window.location.href = '/login';
                    }
                });
            },
            error: function () {
                Swal.fire({
                    title: "اعلان",
                    text: "خطا در ارسال درخواست! لطفا مجددا تلاش نمایید",
                    icon: "error",
                    confirmButtonColor: "#3085d6",
                    confirmButtonText: "باشه ممنون"
                });
            }
        });
    });
});

$(document).ready(function () {
    // کد افزایش تعداد محصول
    $('.quantity-right-plus').click(function (e) {
        e.preventDefault();
        var quantity = parseInt($('#quantity').val());
        // محدودیت بالا را نیز در نظر بگیرید
        if (quantity < parseInt($('#quantity').attr('max'))) {
            $('#quantity').val(quantity + 1);
        }
    });

    // کد کاهش تعداد محصول
    $('.quantity-left-minus').click(function (e) {
        e.preventDefault();
        var quantity = parseInt($('#quantity').val());
        if (quantity > parseInt($('#quantity').attr('min'))) {
            $('#quantity').val(quantity - 1);
        }
    });
});

function removeOrderDetail(detailId) {
    $.get('/user/remove-order/?detail_id=' + detailId).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    });
}

function changeOrderDetailCount(detailId, state) {
    $.get('/user/change-order-detail?detail_id=' + detailId + '&state=' + state).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    });
}

function updateOrderQuantity(detailId, newQuantity) {
    // اعتبارسنجی مقدار ورودی (به عنوان نمونه)
    newQuantity = parseInt(newQuantity);
    if (isNaN(newQuantity) || newQuantity < 1) {
        newQuantity = 1;
    }
    $.get('/user/update-order-detail?detail_id=' + detailId + '&quantity=' + newQuantity)
        .then(res => {
            if (res.status === 'success') {
                $('#order-detail-content').html(res.body);
            }
        });
}

function setParentId(commentId) {
    $('#parentId').val(commentId);
    $('#comment_form_section').get(0).scrollIntoView({behavior: 'smooth'});
    $('#cancelReplyBtn').show();
}

function clearParentId() {
    $('#parentId').val('');
    $('#cancelReplyBtn').hide();
}

function handleTextareaClick(e) {
    e.stopPropagation();
    const textarea = e.target;
    setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = textarea.value.length;
    }, 0);
}

function updateComments(data) {
    const commentsList = $('#comments_list');
    const scrollPos = $(window).scrollTop();

    commentsList.hide().html(data.comments_html).fadeIn(300, () => {
        $(window).scrollTop(scrollPos); // حفظ موقعیت اسکرول
    });
}

// توابع کمکی
function showToast(type, message) {
    // پیاده‌سازی نمایش نوتیفیکیشن
}

let page = 1;
let loading = false;
let hasMore = true;

window.addEventListener('scroll', () => {
    const {scrollTop, scrollHeight, clientHeight} = document.documentElement;

    if (scrollTop + clientHeight >= scrollHeight - 500 && !loading && hasMore) {
        loadMoreProducts();
    }
});

async function loadMoreProducts() {
    loading = true;
    showLoadingIndicator();

    try {
        page++;

        // حفظ تمام پارامترهای URL + اضافه کردن صفحه جدید
        const params = new URLSearchParams(window.location.search);
        params.set('page', page);
        const url = `?${params.toString()}`;

        const response = await fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (!response.ok) throw new Error();

        const html = await response.text();
        if (html.trim() === '') {
            hasMore = false;
            hideLoadingIndicator();
            return;
        }

        document.querySelector('.product-grid').insertAdjacentHTML('beforeend', html);
    } catch (error) {
        hasMore = false;
        console.error('خطا در بارگیری محصولات');
        showErrorToast('خطا در دریافت داده‌ها!');
    } finally {
        loading = false;
        hideLoadingIndicator();
    }
}

function showLoadingIndicator() {
    // نمایش اسپینر یا متن در حال بارگیری
}

function hideLoadingIndicator() {
    // مخفی کردن اسپینر
}

document.addEventListener("DOMContentLoaded", function () {
    const dragHandle = document.getElementById('drag-handle');
    const container = document.querySelector('.sidebar-container'); // یا هر ظرفی که قراره اسکرول بشه

    if (!dragHandle || !container) {
        console.warn("drag-handle یا container پیدا نشد!");
        return;
    }

    let isDragging = false;
    let startY, scrollTop;

    dragHandle.addEventListener('mousedown', function (e) {
        isDragging = true;
        dragHandle.classList.add('active');
        startY = e.pageY;
        scrollTop = container.scrollTop;
        e.preventDefault();
    });

    document.addEventListener('mousemove', function (e) {
        if (!isDragging) return;
        const distance = e.pageY - startY;
        container.scrollTop = scrollTop - distance;
    });

    document.addEventListener('mouseup', function () {
        if (!isDragging) return;
        isDragging = false;
        dragHandle.classList.remove('active');
    });
});


$(document).ready(function () {
    function getCSRFToken() {
        let csrfToken = null;
        document.cookie.split(';').forEach(function (cookie) {
            if (cookie.trim().startsWith('csrftoken=')) {
                csrfToken = cookie.trim().substring('csrftoken='.length);
            }
        });
        return csrfToken;
    }

    $('#productCommentForm').on('submit', function (e) {
        e.preventDefault();

        const $form = $(this);
        const data = $form.serialize();
        const url = $form.attr('action');

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            success: function (response) {
                $('#comments_list').html(response);
                $form[0].reset();
                $('#parentId').val('');
                $('#cancelReplyBtn').hide();
            },
            error: function () {
                alert('خطا در ارسال نظر!');
            }
        });
    });

    $('#commentText').on('focus', function () {
        const textarea = this;
        setTimeout(function () {
            textarea.setSelectionRange(0, 0);
        }, 0);
    });

});



