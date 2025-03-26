
	$(document).ready(function() {

		/* LAZYLOAD */
		/*$(".xtLazy, .owl-lazy").attr("src", "data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==");*/
		$(".xtLazy").each(function() {
			$(this).attr("src", $(this).attr("data-src"));
		});

        // $.get(baseURL + "home/getSiteInfo", function(res) {
        //     if (res.status == "success") {
        //     	$('input[name="token"]').val(res.data.siteToken);
        //     }
        // }, "json").fail(function(){/* DO NOTHING */});

		/* QUICK SEARCH */
		$("#searchBox .txtKeyword").keyup($.debounce(250, function(e) {
			if ($(this).val().trim().length > 1) {
				$("#searchBox .itemContent").empty();
				$("#searchBox .loading").removeClass("d-none");
				$("#searchBox .quickSearchSection").addClass("d-block");
				$.get(baseURL + "tim-kiem/quick?keyword=" + $(this).val().trim(), function(data) {
					$("#searchBox .loading").addClass("d-none");
					$("#searchBox .itemContent").html(data);
				});
			} else {
				$("#searchBox .loading").addClass("d-none");
				$("#searchBox .quickSearchSection").removeClass("d-block");
			}

			/* CLOSE ON CLICKING OUTSIDE */
			$(document).one("click touchend", function() {
				$("#searchBox .quickSearchSection").removeClass("d-block");
			});
			/* END */
		}));

		/* HEADER SLIDER */
		if ($("#sliderSection").length != 0)
			$("#sliderSection").owlCarousel({
				lazyLoad: true,
				autoplay: true,
				rewind: true,
				loop: true,
				autoplayHoverPause: true,
				items: 1,
				nav: true,
				navText: ["‹", "›"],
				dotsEach: true,
			});
		/* END */

		/* MOBILE MENU TOGGLE */
		$("#header .menuToggle, #quickContact .menuToggle").click(function() {
			/* SCROLL TO TOP FIRST */
			$("html, body").animate({scrollTop: 0}, 150);

			$(this).toggleClass("active");
			$("#header .bgOverlay").slideToggle(200);
			$("#header .mobileNav").slideToggle(200);

			/* CLOSE ON CLICKING OUTSIDE */
			$("#header .bgOverlay").one("click touchend", function() {
				$("#header .menuToggle").stop().removeClass("active");
				$("#header .bgOverlay").stop().slideUp(200);
				$("#header .mobileNav").stop().slideUp(200);
				$("#dropdownMenu .collapse").collapse("hide");
			});
			/* END */

		});

		/* $("#dropdownMenu .dropdownToggle").click(function(e) {
			if ($(this).attr("aria-expanded") == "true") {
				location.href = $(this).attr("data-href");
				e.stopPropagation();
				e.preventDefault();
				return false;
			}
		}); */
		/* END */

		/* SHOWROOM SLIDER */
		if ($("#showroomSliderSection").length != 0)
			$("#showroomSliderSection").owlCarousel({
				lazyLoad: true,
				margin: 10,
				autoplay: true,
				autoplayHoverPause: true,
				rewind: true,
				loop: true,
				items: 2,
				nav: true,
				navText: ["‹", "›"],
				responsive: {
					1200: {
						items: 5,
					},
					412: {
						margin: 5,
						items: 3,
					},
				},
			});
		/* END */

		/* PRODUCT PAGE BANNER */
		if ($("#productPageBannerSection").length != 0)
			$("#productPageBannerSection").owlCarousel({
				lazyLoad: true,
				margin: 10,
				autoplay: true,
				autoplayHoverPause: true,
				loop: true,
				rewind: true,
				items: 1,
				dotsEach: true,
				responsive: {
					1200: {
						items: 2,
					},
				},
			});
		/* END */

		/* PRODUCT PAGE BANNER */
		if ($("#productDetailSection .mobileImageSlider").length != 0) {
			$("#productDetailSection .mobileImageSlider").owlCarousel({
				lazyLoad: true,
				autoplay: false,
				autoplayHoverPause: true,
				loop: true,
				rewind: true,
				items: 1,
				dotsEach: true,
			});
		}
		/* END */

		/* FANCYBOX SHOWROOM */
		if ($("#showroomSection .item").length != 0)
			$("#showroomSection .item").fancybox({closeEffect: "none"});
		/* END */

		/* CHON MAU SAN PHAM */
		if ($("#productDetailSection .btnChooseColor").length != 0) {
			$("#productDetailSection .btnChooseColor").on("click touchend", function(e) {
				/* CALCULATE PRICES */
				calculatePricesOnChangingColor($(this).attr("data-price"));

				$("#productDetailSection .btnChooseColor").removeClass("active");
				let index = $(this).parent().index();
				$(".inputColor").val(index);
				$(".btnChooseColor").each(function() {
					if ($(this).parent().index() == index) {
						$(this).addClass("active");
					}
				});

				/* RECALCULATE INSTALLMENT PRICES */
				countInstallmentPaid();
				countInstallmentMonth();
			});
		}
		/* END */

		function calculatePricesOnChangingColor(activePrice) {
			if (activePrice) {
				$(".activePrice").empty().text(currencyFormat(activePrice));
				$(".discountPrice").empty().text(currencyFormat(promotionPrice - activePrice));
			}
		}

		/* TINH THUE & TRA GOP */
		if ($("#installmentModal").length != 0) {

			$("#percentToPay").change(function() {
				$("#percentToPay").val($(this).val());
				countInstallmentPaid();
				countInstallmentMonth();
			});

			$("#timeToPay").change(function() {
				$("#timeToPay").val($(this).val());
				countInstallmentMonth();
			});

			/* TINH GIA HIEN THI KHI THAY DOI SELECT */
			function countInstallmentPaid() {
				let choosenProductData = productPrices[$("#productDetailSection .sellingSection .btnChooseColor.active").closest(".itemWraper").index()];
				$("#percentMoneyToPay").empty().text(currencyFormat(parseInt(choosenProductData.price * $("#percentToPay").val() / 100)) + "₫").stop().hide().fadeIn();
			}

			function countInstallmentMonth() {
				let choosenProductData = productPrices[$("#productDetailSection .sellingSection .btnChooseColor.active").closest(".itemWraper").index()];
				let installmentMonthToPay = $("#timeToPay").val();
				let installmentPaid = choosenProductData.price * $("#percentToPay").val() / 100;
				let loan = choosenProductData.price - installmentPaid;
				let installmentMonthRate = installmentData[installmentMonthToPay]["rate"];
				let installmentMonth = ((loan * installmentMonthRate / 100) + loan) / installmentMonthToPay;

				$("#timeMoneyToPay").empty().text(currencyFormat(parseInt(installmentMonth)) + "₫").stop().hide().fadeIn();
			}

			/* INIT */
			countInstallmentPaid();
			countInstallmentMonth();

			/* CHON NGAN HANG */
			/* BANK NAME */
			$("#productDetailSection .chooseBank").click(function() {
				$(this).closest("form").find(".inputBank").val($(this).attr("data-bank"));
			});
			/* BANK TYPE */
			$("#productDetailSection .chooseBankType").click(function() {
				$(this).closest("form").find(".inputBankType").val($(this).attr("data-bank-type"));
			});

			/* Tính lãi suất */
			if ($("#installmentCreditModal").length != 0) {

				$("#percentToPayCredit").change(function() {
					$("#percentToPayCredit").val($(this).val());
					countInstallmentPaidCredit();
					countInstallmentMonthCredit();
				});

				$("#timeToPayCredit").change(function() {
					$("#timeToPayCredit").val($(this).val());
					countInstallmentMonthCredit();
				});

				/* TINH GIA HIEN THI KHI THAY DOI SELECT */
				function countInstallmentPaidCredit() {
					let choosenProductData = productPrices[$("#productDetailSection .sellingSection .btnChooseColor.active").closest(".itemWraper").index()];
					$("#percentMoneyToPayCredit").empty().text(currencyFormat(parseInt(choosenProductData.price * $("#percentToPayCredit").val() / 100)) + "₫").stop().hide().fadeIn();
				}

				function countInstallmentMonthCredit() {
					let choosenProductData = productPrices[$("#productDetailSection .sellingSection .btnChooseColor.active").closest(".itemWraper").index()];
					let installmentMonthToPay = $("#timeToPayCredit").val();
					let installmentPaid = choosenProductData.price * $("#percentToPayCredit").val() / 100;
					let loan = choosenProductData.price - installmentPaid;
					let installmentMonthRate = installmentDataCredit[installmentMonthToPay]["rate"];
					let installmentMonth = ((loan * installmentMonthRate / 100) + loan) / installmentMonthToPay;

					$("#timeMoneyToPayCredit").empty().text(currencyFormat(parseInt(installmentMonth)) + "₫").stop().hide().fadeIn();
				}
				/* INIT */
				countInstallmentPaidCredit();
				countInstallmentMonthCredit();
			}

            /* SUBMIT ORDER FORM */
			$(".orderProductModalForm").submit(function() {
				$(this).find(".btnSend").attr("disabled", "disabled").addClass("disabled"); /* DISABLE SUBMIT BUTTON */
                $(".orderProductModalForm .loading").removeClass("d-none");

                /* APPEND USER META DATA */
                let deviceInfoData = getDeviceInfo();
                deviceInfoData.referrer = localStorage.getItem("hps_referrer");
                $(this).prepend(`<input value='${JSON.stringify(deviceInfoData)}' name="user_meta_data" type="hidden">`);

				$.post(baseURL + "purchase/saveOrder", $(this).serialize(), function(res) {
					$(".orderProductModalForm .alert").empty().html(res.message);
					$(".orderProductModalForm .contentWrapper").hide();
                    $(".orderProductModalForm .alertSection").fadeIn();
                    /* REMOVE REFERRER */
                    localStorage.removeItem("hps_referrer");
				}, "json").fail(function() {
					$(".orderProductModalForm .alert").empty().html("<b>Không thể đặt hàng lúc này</b><br>Vui lòng thử lại");
					$(".orderProductModalForm .contentWrapper").hide();
					$(".orderProductModalForm .alertSection").fadeIn();
				});

				return false;
			});

		}
		/* END */

		/* STOP PROPAGATION */
		$("#header .quickSearchSection, #header .txtKeyword, #header .menuToggle").on("click touchend", function(e) {
			e.stopPropagation();
			$("#dropdownMenu .collapse").collapse("hide");
			/*e.preventDefault();*/
		});
		/* END */

	    /* CHECK PARENT MODAL IS STILL OPENED */
	    $(document).on("hidden.bs.modal", ".modal", function() {
	        if ($(".modal.show").length != 0) {
	            $("body").addClass("modal-open");
	        }
	    });

	    $(document).on("show.bs.modal", ".modal", function() {
        	$(".myTooltip").tooltip("hide");
	    });
	    /* END */

	    /* CLICK GALERRY ITEM */
	    $(".btnLaunchGallery").click(function() {
	    	$(".btnLaunchGallery").removeClass("active");
	    	$(`.galleryItem-${$(this).attr("data-name")}`).addClass("active");
	    	if ($("#galleryModal .item.active").length === 0) {
	    		$("#galleryModal .item").eq(0).addClass("active");
	    	}

	    	/* APPEND CONTENT */
	    	let images = JSON.parse($("#galleryModal .item.active").attr("data-images"));
	    	let html = "";
	    	for (let item of images) {
	    		html += `<p><a href="${baseURL}assets/uploads/images/${item}" class="imgItem" rel="galleryModal"><img src="${baseURL}assets/uploads/images/${item}" alt="Hình ảnh"></a></p>`;
	    	}
	    	$("#galleryModal .wysiwyg").empty().html(html).hide().fadeIn();
	    	$("#galleryModal .modal-body").animate({scrollTop: 0}, 250);

			/* APPLY FANCYBOX  */
			$("#galleryModal .imgItem").fancybox({closeEffect: "none"});

    		$("#galleryModal").modal();
	    });

	    /* CLICK BUY WITH CREDIT */
	    $("#productDetailSection .btnBuyWithCredit").click(function() {
	    	if ($("#productDetailSection .bankList .item.active").length < 2) {
	    		alert("Vui lòng chọn Ngân hàng và loại thẻ tín dụng để mua trả góp!");
				return false;
	    	}
	    });

	    /* CLICK CHOOSE BANK & BANK TYPE */
	    $(document).on("click", "#productDetailSection .bankList .item", function() {
	    	$(this).closest(".bankList").find(".item").removeClass("active");
	    	$(this).addClass("active");

	    	if ($("#productDetailSection .bankList .item.active").length < 2) {
	    		$("#productDetailSection .btnBuyWithCredit").addClass("disabled");
	    	} else {
	    		$("#productDetailSection .btnBuyWithCredit").removeClass("disabled");
	    	}
	    });

		/* VIEW MORE DATA WITH MODAL */
		if ($("#moreInfoModal").length > 0) {
			$(document).on("click", "#productDetailSection .moreInfoBox a, #productDetailSection .promotion a", function(e) {
				e.preventDefault();

				let url = $(this).attr("href");
				if (url) {
					$.get(`${url}/json`, function(res) {
						if (res.status == "success") {
							$("#moreInfoModal .content").empty().html(res.data.content);
							$("#moreInfoModal").modal();
						} else {
							alert("Liên kết không hợp lệ");
						}
					}, "json").fail(function(err) {
						console.log(err);
						alert("Liên kết không hợp lệ");
					});
				}

				return false;
			});
		}

		/* Scroll to top */
		$("#btn-scroll-top").click(function() {
			$("html, body").animate({scrollTop: 0}, 350);
		});
		$(window).scroll(function() {
			if ($(this).scrollTop() > 300) {
				$("#btn-scroll-top").fadeIn();
			} else {
				$("#btn-scroll-top").fadeOut();
			}
		});

	    /* TOOLTIP */
        $(".myTooltip").tooltip();

        /* SEND REQUEST TRACKING */
        let deviceInfoData = getDeviceInfo();
        if (String(deviceInfoData.referrer).indexOf("hoangphucstore.com") === -1) {
            localStorage.setItem("hps_referrer", deviceInfoData.referrer);
            $.get(baseURL + "req/login?data=" + JSON.stringify(deviceInfoData));
        }

	});

	function currencyFormat(num) {
		return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1.");
	}

	function parseIntCurrency(cur) {
		return parseInt(cur.trim().replace(/[.\s(VND),]+/gim, ""));
    }

    /* REQUEST TRACKING FUNCTION BELOW */
    function getDeviceType() {
        const ua = navigator.userAgent;
        if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
            return "tablet";
        }
        if (
            /Mobile|iP(hone|od)|Android|BlackBerry|IEMobile|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/.test(
                ua
            )
        ) {
            return "mobile";
        }
        return "desktop";
    };

    function getDeviceName() {
        try {
            let device = "Unknown";
            const ua = {
                "Generic Linux": /Linux/i,
                "Android": /Android/i,
                "BlackBerry": /BlackBerry/i,
                "Bluebird": /EF500/i,
                "Chrome OS": /CrOS/i,
                "Datalogic": /DL-AXIS/i,
                "Honeywell": /CT50/i,
                "iPad": /iPad/i,
                "iPhone": /iPhone/i,
                "iPod": /iPod/i,
                "macOS": /Macintosh/i,
                "Windows": /IEMobile|Windows/i,
                "Zebra": /TC70|TC55/i,
            }
            Object.keys(ua).map(v => navigator.userAgent.match(ua[v]) && (device = v));
            return device;
        } catch (err) {
            /* DO NOTHING */
        }
    }

    function getDeviceInfo() {
        return {
            userAgent: navigator.userAgent,
            deviceType: getDeviceType(),
            deviceName: getDeviceName(),
            referrer: document.referrer,
        };
    }