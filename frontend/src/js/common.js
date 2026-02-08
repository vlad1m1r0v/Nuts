// инициализируем параллакс
jQuery(document).ready(function ($) {
    "use strict";

    $.Scrollax();

    const mapElement = document.getElementById('map');

    const longitude = parseFloat(mapElement.dataset.longitude);
    const latitude = parseFloat(mapElement.dataset.latitude);

    const map = L.map('map').setView([longitude, latitude], 13);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    const marker = L.marker([longitude, latitude]).addTo(map);
});

(function ($) {
    // :: PreventDefault a Click
    $("a[href='#']").on("click", function ($) {
        $.preventDefault();
    });

    // создаем html под мобильное меню
    // $(".top-header").before(
    //     '<div class="mobile-menu d-lg-none"><div class="row"><div class="col-12"><a href="/" class="logo"><img src="img/logo.png" alt="alt"><span>ОРЕХ<br> ПРИЧЕРНОМОРЬЯ</span></a><i class="nut-icon icons-close-button">'
    // );

    // клонируем меню
    $(".menu_top").clone().appendTo(".mobile-menu");

    // показать/скрыть меню
    $(".mobile-menu-button, .mobile-menu .icons-close-button").click(function () {
        $(".mobile-menu").stop().slideToggle();
        $(".top-header").toggleClass("d-none");
    });

    // наполняем блок с меню другими элементами
    $(".logo_tel_mobile").insertBefore(".lang-menu");
    $(".logo_button_mobile").insertBefore(".lang-menu");
    $(".line_social").clone().appendTo(".mobile-line");
    $(".log_in").clone().appendTo(".mobile-line");
    $(".mobile-line ul.log_in").removeClass("d-none");

    // переносим навигацию слайдера
    $(".news-container .swiper-button-next").insertBefore(
        ".news .wrap .navigation"
    );
    $(".news-container .swiper-button-prev").insertBefore(
        ".news .wrap .navigation"
    );

    // модальное окно на плашке товара cо слайдером
    // $('.products-container .swiper-slide a').simpleLightbox();

    // инициализация таймера при скролле к блоку
    var blockScrolled = $(".timer");

    $(window).on("scroll", function () {
        if (
            $(window).scrollTop() >
            blockScrolled.offset().top - $(window).height() / 2
        ) {
            $(".timer__single").countTo();
            $(window).off("scroll");
        }
    });
    // $('.timer__single').countTo();

    // tabs

    $("ul.tabs__caption").on("click", "li:not(.active)", function () {
        $(this)
            .addClass("active")
            .siblings()
            .removeClass("active")
            .closest("div.tabs")
            .find("div.tabs__content")
            .removeClass("active")
            .eq($(this).index())
            .addClass("active");
    });

    //В зависимости от выбранной радио кнопки показ блока

    $(document).ready(function () {
        $('.radio__wrap input[type="radio"]').click(function () {
            var inputValue = $(this).attr("value");

            var targetBox = $("." + inputValue);

            $(".box").not(targetBox).hide();

            $(targetBox).show();
        });
    });

    $(document).ready(function () {
        $('.radio__wrapper_click input[type="radio"]').click(function () {
            var inputValue = $(this).attr("value");

            var targetBox = $("." + inputValue);

            $(".box").not(targetBox).hide();

            $(targetBox).show();
        });

        $(".radio__wrapper_click .radio-custom_last").click(function () {
            $(".box").css("display", "none");
        });
    });

    // tooltip

    $(".tooltip").tooltipster({
        animation: "fade",
        delay: 200,
        // trigger: 'click',
        maxWidth: 106,
    });

    // tables responsive
    $("#table").basictable();

    $("#table-breakpoint").basictable({
        breakpoint: 768,
    });

    $("#table-container-breakpoint").basictable({
        containerBreakpoint: 485,
    });

    $("#table-swap-axis").basictable({
        swapAxis: true,
    });

    $("#table-force-off").basictable({
        forceResponsive: false,
    });

    $("#table-no-resize").basictable({
        noResize: true,
    });

    $("#table-two-axis").basictable();

    $("#table-max-height").basictable({
        tableWrapper: true,
    });

    // окно корзины

    $(".logo_number").click(function () {
        $(".popup__cart").stop().slideToggle("swing");
    });

    $(document).mouseup(function (e) {
        // событие клика по веб-документу
        var div = $(".popup__cart"); // тут указываем класс элемента
        if (
            !div.is(e.target) && // если клик был не по нашему блоку
            div.has(e.target).length === 0
        ) {
            // и не по его дочерним элементам
            div.slideUp(); // скрываем его
        }
    });

    // if ($(window).width() <= '992'){
    // 	$('.popup__cart').clone().appendTo('.top-header');
    // }

    // fixed sidebar
    var elements = $(".sticky");
    Stickyfill.add(elements);
    // $('#sidebar').stickySidebar({
    // 	containerSelector: '#main-content',
    // 	// innerWrapperSelector: '.sidebar__inner',
    // 	topSpacing: 20,
    // 	bottomSpacing: 20
    // });

    // выпадающий список выбора языков
    var menuElem = document.getElementById("lang-menu"),
        titleElem = menuElem.querySelector(".title");
    document.onclick = function (event) {
        var target = (elem = event.target);
        while (target != this) {
            if (target == menuElem) {
                if (elem.tagName == "A") {
                    titleElem.innerHTML = elem.textContent;
                    titleElem.style.backgroundImage = getComputedStyle(elem, null)[
                        "backgroundImage"
                        ];
                }
                menuElem.classList.toggle("open");
                return;
            }
            target = target.parentNode;
        }
        menuElem.classList.remove("open");
    };

    // $(document).ready(function(){

    // $('.header').before('<div class="mobile-menu d-lg-none">');
    // $('.menu').clone().appendTo('.mobile-menu');
    // $('.convizit-hamburger-box').click(function() {
    // 	$('.mobile-menu').stop().slideToggle();
    // });

    // });

    //initialize swiper when document ready
    var swiper = new Swiper(".news-container", {
        slidesPerView: 3,
        spaceBetween: 30,
        loop: true,
        observer: true,
        observeParents: true,
        // pagination: {
        //   el: '.swiper-pagination',
        //   type: 'fraction',
        // },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        autoplay: {
            delay: 2500,
            disableOnInteraction: false,
        },
        breakpoints: {
            1024: {
                slidesPerView: 3,
                spaceBetween: 30,
            },
            920: {
                slidesPerView: 2,
                spaceBetween: 30,
            },
            578: {
                slidesPerView: 1,
                spaceBetween: 10,
            },
        },
    });

    $(".swiper-container").hover(
        function () {
            this.swiper.autoplay.stop();
        },
        function () {
            this.swiper.autoplay.start();
        }
    );

    //initialize swiper when document ready
    var swiper = new Swiper(".manufacturer-container", {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        speed: 400,
        observer: true,
        observeParents: true,
        // pagination: {
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        autoplay: {
            delay: 2500,
            disableOnInteraction: false,
        },
        breakpoints: {
            1024: {
                slidesPerView: 1,
                spaceBetween: 30,
            },
            920: {
                slidesPerView: 1,
                spaceBetween: 30,
            },
            578: {
                slidesPerView: 1,
                spaceBetween: 10,
            },
        },
    });

    //initialize swiper when document ready
    var swiper = new Swiper(".products-container", {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        speed: 400,
        // pagination: {
        //   el: '.swiper-pagination',
        //   type: 'fraction',
        // },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        autoplay: 10000000,
        zoom: true,
        // autoplayDisableOnInteraction: false,
        // noSwiping: true,
        noSwiping: false,
        breakpoints: {
            1024: {
                slidesPerView: 1,
                spaceBetween: 30,
            },
            920: {
                slidesPerView: 1,
                spaceBetween: 30,
            },
            578: {
                slidesPerView: 1,
                spaceBetween: 10,
            },
        },
    });

    // задаем класс и data по дукументации плагина скролла

    $(".manufacturer .wrapper")
        .addClass("mCustomScrollbar")
        .attr("data-mcs-theme", "dark");
    $(".manufacturer .wrapper").mCustomScrollbar({
        theme: "dark",
    });
    // select

    $("select").each(function () {
        var $this = $(this),
            numberOfOptions = $(this).children("option").length;

        $this.addClass("select-hidden");
        $this.wrap('<div class="select"></div>');
        $this.after('<div class="select-styled"></div>');

        var $styledSelect = $this.next("div.select-styled");

        var $selectedOption = $this.children("option:selected").length
            ? $this.children("option:selected")
            : $this.children("option").eq(0);

        $styledSelect.text($selectedOption.text());

        var $list = $("<ul />", {
            class: "select-options",
        }).insertAfter($styledSelect);

        for (var i = 0; i < numberOfOptions; i++) {
            $("<li />", {
                text: $this.children("option").eq(i).text(),
                rel: $this.children("option").eq(i).val(),
            }).appendTo($list);
        }

        var $listItems = $list.children("li");

        $styledSelect.click(function (e) {
            e.stopPropagation();
            $("div.select-styled.active")
                .not(this)
                .each(function () {
                    $(this).removeClass("active").next("ul.select-options").hide();
                });
            $(this).toggleClass("active").next("ul.select-options").toggle();
        });

        $listItems.click(function (e) {
            e.stopPropagation();
            $styledSelect.text($(this).text()).removeClass("active");
            $this.val($(this).attr("rel"));
            $list.hide();
            //console.log($this.val());
        });

        $(document).click(function () {
            $styledSelect.removeClass("active");
            $list.hide();
        });
    });
})(jQuery);
