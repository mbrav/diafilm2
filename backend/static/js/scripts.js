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
	return slides
}

w = window.innerWidth;
h = window.innerHeight;
window.addEventListener(
	"resize",
	function (event) {
		w = window.innerWidth;
		h = window.innerHeight;

		if (document.fullscreenElement !== null) {
			slides = cleanSlideStyles()

			for (let index = 0; index < slides.length; index++) {
				if (w > h) {
					slides[index].style.height = h + "px";
					slides[index].style.width = null;
				} else {
					slides[index].style.height = null;
					slides[index].style.width = w + "px";
				}
			}
		}
	},
	true
);

function diafilmFullScreenToggle() {
	diafilmCarousel.requestFullscreen();
}

document.onfullscreenchange = function (event) {
	cleanSlideStyles();
};

document.getElementById("full-screen-toggle").onclick = diafilmFullScreenToggle;


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
