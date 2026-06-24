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

  // Contact form: AJAX submit to Web3Forms with graceful fallback
  var form = document.querySelector('form[data-ajax="web3forms"]');
  if (form && window.fetch) {
    var status = form.querySelector(".form-status");
    form.addEventListener("submit", function (e) {
      var key = form.querySelector('input[name="access_key"]');
      if (!key || !key.value) return; // no key configured yet — allow normal POST
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      var data = new FormData(form);
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = "Sending…"; }
      fetch("https://api.web3forms.com/submit", {
        method: "POST", body: data, headers: { Accept: "application/json" }
      })
        .then(function (r) { return r.json(); })
        .then(function (json) {
          if (!status) return;
          status.hidden = false;
          if (json.success) {
            status.className = "form-status ok";
            status.textContent = "Thank you — your request has been sent. We will be in touch shortly.";
            form.reset();
          } else {
            status.className = "form-status err";
            status.textContent = (json && json.message) || "Something went wrong. Please email jason@pa-expert.com.";
          }
        })
        .catch(function () {
          if (!status) return;
          status.hidden = false;
          status.className = "form-status err";
          status.textContent = "Network error. Please email jason@pa-expert.com.";
        })
        .finally(function () {
          if (btn) { btn.disabled = false; if (btn.dataset.label) btn.textContent = btn.dataset.label; }
        });
    });
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
