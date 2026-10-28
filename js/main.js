(function () {
  "use strict";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- header: hide on scroll down, show on scroll up ---------- */
  var nav = $(".nav"), lastY = 0;
  window.addEventListener("scroll", function () {
    var y = window.scrollY;
    if (nav) nav.classList.toggle("hide", y > lastY && y > 240 && !$(".mobile-menu.open"));
    lastY = y;
  }, { passive: true });

  /* ---------- mobile menu ---------- */
  var burger = $(".burger"), mm = $(".mobile-menu");
  if (burger && mm) {
    burger.addEventListener("click", function () {
      var o = !mm.classList.contains("open");
      mm.classList.toggle("open", o); burger.classList.toggle("open", o);
      document.body.style.overflow = o ? "hidden" : "";
    });
    $$("a", mm).forEach(function (a) { a.addEventListener("click", function () { mm.classList.remove("open"); burger.classList.remove("open"); document.body.style.overflow = ""; }); });
  }

  /* ---------- scroll reveal ---------- */
  var io = "IntersectionObserver" in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { threshold: .12, rootMargin: "0px 0px -6% 0px" }) : null;
  $$(".rv").forEach(function (el) { io ? io.observe(el) : el.classList.add("in"); });
  // elements at the very bottom of the page (footer) can never scroll far enough to cross the observer margin: reveal them near the end
  var revealTail = function () {
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 6) {
      $$(".rv:not(.in)").forEach(function (el) { if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add("in"); });
    }
  };
  window.addEventListener("scroll", revealTail, { passive: true });
  window.addEventListener("load", revealTail);

  /* ---------- count-up stats ---------- */
  var cio = "IntersectionObserver" in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      cio.unobserve(e.target);
      var el = e.target, end = parseFloat(el.dataset.to), t0 = null, dur = 1800;
      (function tick(t) {
        if (!t0) t0 = t;
        var p = Math.min((t - t0) / dur, 1), v = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(end * v);
        if (p < 1) requestAnimationFrame(tick);
      })(performance.now());
    });
  }, { threshold: .6 }) : null;
  $$("[data-to]").forEach(function (el) { cio && cio.observe(el); });

  /* ---------- FAQ accordion ---------- */
  $$(".qa").forEach(function (q) {
    $("button", q).addEventListener("click", function () {
      var open = q.classList.contains("open");
      $$(".qa", q.parentNode).forEach(function (o) { o.classList.remove("open"); $("button", o).setAttribute("aria-expanded", "false"); });
      if (!open) { q.classList.add("open"); $("button", q).setAttribute("aria-expanded", "true"); }
    });
  });

  /* ---------- pricing toggle ---------- */
  var seg = $(".seg");
  if (seg) {
    var btns = $$("button", seg), knob = $(".knob", seg);
    var place = function (b) { knob.style.width = b.offsetWidth + "px"; knob.style.transform = "translateX(" + (b.offsetLeft - 5) + "px)"; };
    var setMode = function (b) {
      btns.forEach(function (x) { x.classList.toggle("on", x === b); }); place(b);
      var yearly = b.dataset.mode === "yearly";
      $$("[data-m]").forEach(function (p) {
        var m = parseFloat(p.dataset.m), v = yearly ? m * 0.75 : m;
        p.textContent = "$" + (m === 0 ? "0" : v.toFixed(2).replace(/\.00$/, ""));
      });
    };
    btns.forEach(function (b) { b.addEventListener("click", function () { setMode(b); }); });
    window.addEventListener("load", function () { setMode(btns[0]); });
    window.addEventListener("resize", function () { place($("button.on", seg)); });
    setMode(btns[0]);
  }

  /* ---------- stacked benefit cards ---------- */
  var stack = $(".stack");
  if (stack) {
    var cards = $$(".scard", stack), n = cards.length, cur = 2;
    var K = [[0, 0, 0, 0], [120, 20, 6.5, .1], [211, 48, 14, .42]];   // [x, y, rotation, content fade] per distance from the front card (381px-wide design)
    var layout = function () {
      var k = cards[0].offsetWidth / 381;
      cards.forEach(function (c, i) {
        var d = ((i - cur) % n + n) % n; if (d > n / 2) d -= n;
        var ad = Math.abs(d), sg = d < 0 ? -1 : 1, m = K[Math.min(ad, 2)];
        c.style.transform = "translate3d(" + (sg * m[0] * k) + "px," + (m[1] * k) + "px,0) rotate(" + (sg * m[2]) + "deg)";
        c.style.zIndex = 10 - ad; c.style.opacity = ad > 2 ? 0 : 1; c.style.setProperty("--fade", m[3]);
        c.style.pointerEvents = d === 0 ? "auto" : "none";
      });
    };
    window.addEventListener("resize", layout);
    var go = function (k) { cur = (cur + k + n) % n; layout(); };
    var prev = $(".arr.prev", stack.parentNode), next = $(".arr.next", stack.parentNode);
    prev && prev.addEventListener("click", function () { go(-1); });
    next && next.addEventListener("click", function () { go(1); });
    layout();
  }

  /* ---------- institution modules tree: scale the 1000px stage to fit ---------- */
  var tstage = $(".tree-stage");
  if (tstage) {
    var tfit = function () {
      var box = tstage.parentNode, small = window.innerWidth < 700, s = small ? 1 : Math.min(1, box.clientWidth / 1000);
      tstage.style.transform = s < 1 ? "scale(" + s + ")" : "";
      box.style.height = small ? "auto" : Math.round(tstage.offsetHeight * s) + "px";
    };
    tfit(); window.addEventListener("resize", tfit); window.addEventListener("load", tfit);
  }

  /* ---------- testimonial slider ---------- */
  var tt = $(".ttrack");
  if (tt) {
    var ti = 0, tcs = $$(".tcard", tt), step = function () { return tcs[0].offsetWidth + 24; };
    var tslide = function (k) {
      var vis = Math.floor(tt.parentNode.offsetWidth / step()) || 1;
      var max = Math.max(tcs.length - vis, 0);
      ti = ti + k; if (ti > max) ti = 0; if (ti < 0) ti = max;
      tt.style.transform = "translateX(" + (-ti * step()) + "px)";
    };
    var tp = $(".arr.prev", tt.closest(".sec")), tn = $(".arr.next", tt.closest(".sec"));
    tp && tp.addEventListener("click", function () { tslide(-1); });
    tn && tn.addEventListener("click", function () { tslide(1); });
    setInterval(function () { tslide(1); }, 5000);
  }

  /* ---------- blog filter + load more ---------- */
  var chips = $$(".chip");
  chips.forEach(function (c) {
    c.addEventListener("click", function () {
      chips.forEach(function (x) { x.classList.remove("on"); }); c.classList.add("on");
      var cat = c.dataset.cat;
      $$(".post[data-cat]").forEach(function (p) { p.style.display = (cat === "all" || p.dataset.cat === cat) ? "" : "none"; });
    });
  });
  var sq = $(".search input");
  sq && sq.addEventListener("input", function () {
    var q = sq.value.toLowerCase();
    $$(".post[data-cat]").forEach(function (p) { p.style.display = p.textContent.toLowerCase().indexOf(q) > -1 ? "" : "none"; });
  });
  var more = $("#loadmore");
  more && more.addEventListener("click", function (e) {
    e.preventDefault();
    $$(".post.hidden").forEach(function (p, k) {
      p.classList.remove("hidden"); p.style.display = ""; p.style.setProperty("--d", (k * .08) + "s");
      requestAnimationFrame(function () { requestAnimationFrame(function () { p.classList.add("in"); }); });   // let the browser paint the start state so the rise-in plays
    });
    more.style.display = "none";
  });

  /* ---------- forms ---------- */
  function toast(msg) {
    var t = $(".toast") || document.body.appendChild(Object.assign(document.createElement("div"), { className: "toast" }));
    t.textContent = msg; t.classList.add("show"); clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove("show"); }, 3200);
  }
  var cf = $("#contactForm");
  cf && cf.addEventListener("submit", function (e) {
    e.preventDefault(); var ok = true;
    $$("[required]", cf).forEach(function (f) {
      var bad = f.type === "checkbox" ? !f.checked : !f.value.trim() || (f.type === "email" && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value));
      f.closest("label").classList.toggle("bad", bad); if (bad) ok = false;
    });
    if (ok) { toast("Thanks! Your message has been sent."); cf.reset(); }
  });
  $$(".subscribe").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault(); var i = $("input", f);
      if (/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(i.value)) { toast("You're subscribed. Welcome to Nexivo!"); f.reset(); } else toast("Please enter a valid email address.");
    });
  });

  /* ---------- hero cards: scroll-linked fly-in (both directions) ---------- */
  var hero = $(".hero"), pf = $(".float.pf"), ts = $(".float.ts"), hv = $(".hero-visual");
  if (hero && pf && ts && hv) {
    var G = {}, cur = 0, goal = 0, raf = 0;
    var lerp = function (a, b, t) { return a + (b - a) * t; };
    var ease = function (t) { return .5 - Math.cos(Math.PI * t) / 2; };
    var measure = function () {
      var offY = function (el) { var t = 0; while (el && el !== hero) { t += el.offsetTop; el = el.offsetParent; } return t; };
      var vw = hero.clientWidth, h1 = $("h1 b", hero);
      var h1c = offY(h1) + h1.offsetHeight / 2, dt = offY(hv), dl = (vw - hv.offsetWidth) / 2;   // layout values: unaffected by reveal transforms
      G.vw = vw;
      G.D = Math.max(dt - 115, 300);                         // scroll distance until the cards have landed
      var bz = 10, sc = (hv.offsetWidth - 2 * bz) / 1592;     // dashboard screenshot scale inside the bezel
      G.pf = { w: 222, h: 203, x0: -7, y0: h1c + 0, r0: 22, s0: 1.2, x1: dl + bz + 712.5 * sc, y1: dt + bz + 376 * sc, s1: sc };   // Active Staff card
      G.ts = { w: 222, h: 203, x0: vw + 27, y0: h1c - 95, r0: -20, s0: 1.2, x1: dl + bz + 471 * sc, y1: dt + bz + 376 * sc, s1: sc };  // Active Trainees card
      G.on = window.innerWidth >= 1100;
    };
    var place = function (el, g, p) {
      var e = ease(p), x = lerp(g.x0, g.x1, e), yy = lerp(g.y0, g.y1, e), r = lerp(g.r0, 0, e), s = lerp(g.s0, g.s1, e);
      el.style.transform = "translate3d(" + (x - g.w / 2) + "px," + (yy - g.h / 2) + "px,0) rotate(" + r + "deg) scale(" + s + ")";
    };
    var draw = function () {
      raf = 0; cur = goal;                                   // direct scroll mapping: identical forwards and backwards
      var p = G.on ? cur : 1;
      place(pf, G.pf, Math.min(p / .9, 1));                  // Performance lands first, on top...
      place(ts, G.ts, p);                                     // ...Time Spent trails slightly
    };
    var update = function () { goal = G.on ? Math.min(Math.max(window.scrollY / G.D, 0), 1) : 1; draw(); };
    var remeasure = function () { measure(); update(); };
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", remeasure);
    window.addEventListener("load", function () { remeasure(); cur = goal; draw(); });
    measure(); goal = G.on ? Math.min(Math.max(window.scrollY / G.D, 0), 1) : 1; cur = goal; draw();
  }

  var tt = document.querySelector(".totop");
  if (tt) {
    var ttShow = function () { tt.classList.toggle("show", window.scrollY > 400); };
    window.addEventListener("scroll", ttShow, { passive: true }); ttShow();
    tt.addEventListener("click", function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: "smooth" }); });
  }
})();
