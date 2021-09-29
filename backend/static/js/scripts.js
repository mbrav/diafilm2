/*!
 * Start Bootstrap - Δиа Фильм² v1.0.0 (https://github.com/mbrav)
 * Copyright 2013-2021 mbrav
 * Licensed under MIT (https://github.com/StartBootstrap/dia-film2/blob/master/LICENSE)
 */

var diafilmCarousel = document.getElementById("diafilm-carousel");

function cleanSlideStyles() {
	slides = document.querySelectorAll(".carousel-item > img");
	for (let index = 0; index < slides.length; index++) {
		slides[index].style.width = "100%";
		slides[index].style.height = null;
	}
	return slides;
}

function updateImgSizes() {
	slides = cleanSlideStyles();
	if (document.fullscreenElement !== null) {
		w = window.innerWidth;
		h = window.innerHeight;
		currentSlide = document.querySelector(".carousel .active img");
		sw = currentSlide.width;
		sh = currentSlide.height;

		console.log("w:" + w, " h:" + h, " sw:" + sw, " sh:" + sh);

		for (let index = 0; index < slides.length; index++) {
			if (sh < h) {
				slides[index].style.width = w + "px";
				slides[index].style.height = null;
			} else {
				slides[index].style.height = h + "px";
				slides[index].style.width = null;
			}
		}
	}
}

function diafilmFullScreenToggle() {
	if (diafilmCarousel.requestFullscreen) {
		diafilmCarousel.requestFullscreen();
	}
	if (diafilmCarousel.webkitRequestFullscreen) {
		diafilmCarousel.webkitRequestFullscreen();
	}
	if (diafilmCarousel.mozRequestFullScreen) {
		diafilmCarousel.mozRequestFullScreen();
	}
	if (diafilmCarousel.msRequestFullscreen) {
		diafilmCarousel.msRequestFullscreen();
	}
}

document.getElementById("full-screen-toggle").onclick = diafilmFullScreenToggle;

document.onfullscreenchange = function (event) {
	updateImgSizes();
};

window.addEventListener(
	"resize",
	function (event) {
		updateImgSizes();
	},
	true
);

window.addEventListener("DOMContentLoaded", () => {
	let scrollPos = 0;
	const mainNav = document.getElementById("mainNav");
	const headerHeight = mainNav.clientHeight;
	window.addEventListener("scroll", function () {
		const currentTop = document.body.getBoundingClientRect().top * -1;
		if (currentTop < scrollPos) {
			// Scrolling Up
			if (currentTop > 0 && mainNav.classList.contains("is-fixed")) {
				mainNav.classList.add("is-visible");
			} else {
				console.log(123);
				mainNav.classList.remove("is-visible", "is-fixed");
			}
		} else {
			// Scrolling Down
			mainNav.classList.remove(["is-visible"]);
			if (
				currentTop > headerHeight &&
				!mainNav.classList.contains("is-fixed")
			) {
				mainNav.classList.add("is-fixed");
			}
		}
		scrollPos = currentTop;
	});
});
