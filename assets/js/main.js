/* Purinton Analytics — small progressive-enhancement script */
(function () {
  "use strict";

  // Mobile nav toggle
  var toggle = document.querySelector(".nav-toggle");
  var menu = document.getElementById("nav-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    // Close menu when a link is tapped
    menu.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        menu.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  // Header shadow on scroll
  var header = document.getElementById("site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // Scroll-reveal with light per-group stagger
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var SEL = ".reveal, .card, .feature, .section-head, .stat, .steps > li, .faq-item, " +
            ".incl-list > li, .cred-list > li, .edu-list > li, .aside-card, .pill, .legal > *";
  var targets = Array.prototype.slice.call(document.querySelectorAll(SEL));

  if (reduce || !("IntersectionObserver" in window)) {
    targets.forEach(function (el) { el.classList.add("is-visible"); });
    return;
  }

  var io = new IntersectionObserver(function (entries, obs) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      // stagger by position among its siblings (capped)
      var sibs = el.parentNode ? el.parentNode.children : [el];
      var i = Array.prototype.indexOf.call(sibs, el);
      el.style.transitionDelay = (Math.min(i, 7) * 70) + "ms";
      el.classList.add("is-visible");
      obs.unobserve(el);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

  targets.forEach(function (el) {
    // Elements already in view on load reveal immediately (no scroll needed)
    io.observe(el);
  });
})();
