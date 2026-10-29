/* Shared header + footer for every page. Replaces Python-side templating:
   each page carries empty <div id="site-header"></div> / <div id="site-footer"></div>
   placeholders, and this script injects the markup and marks the active link.
   Loaded BEFORE main.js so the injected elements exist when main.js binds to them. */
(function () {
  var header = `<header class="nav"><div class="nav-in">
<a class="logo" href="index.html" aria-label="Nexivo home"><img src="assets/img/nexivo-logo.svg" alt="Nexivo"  loading="lazy" decoding="async" style="height:28px"><span class="pwr">Powered by <b>Nexum</b></span></a>
<nav class="menu" aria-label="Main"><a href="index.html">Home</a><a href="features.html">Features</a><a href="about-us.html">About us</a><a href="pricing.html">Pricing</a><a href="blog.html">Blog</a></nav>
<a class="btn btn-line btn-sm" href="contact-us.html"><span class="ic"><svg viewBox="2 2 12 12" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3.2 3.2L7.8 8l-4.6 4.8M8.2 3.2L12.8 8l-4.6 4.8"/></svg></span><span class="lb">Contact Us</span></a>
<button class="burger" aria-label="Menu"><i></i><i></i><i></i></button></div></header>
<div class="mobile-menu"><a href="index.html">Home</a><a href="features.html">Features</a><a href="about-us.html">About us</a><a href="pricing.html">Pricing</a><a href="blog.html">Blog</a><a href="contact-us.html">Contact Us</a></div>`;

  var footer = `<footer class="foot" id="top-footer"><div class="wrap"><div class="foot-top">
<div class="fb rv"><a class="logo" href="index.html"><img src="assets/img/nexivo-logo.svg" alt="Nexivo"  loading="lazy" decoding="async" ></a>
<p>Nexivo is a complete, customizable learning management solution for educational institutions and organizations — schools, colleges, academies, companies and training teams alike.</p></div>
<div class="rv" style="--d:.08s"><h4>Useful Links</h4><ul><li><a href="index.html">Home</a></li><li><a href="features.html">Features</a></li><li><a href="about-us.html">About Us</a></li><li><a href="pricing.html">Pricing Plan</a></li></ul></div>
<div class="rv" style="--d:.16s"><h4>Quick Links</h4><ul><li><a href="contact-us.html">Contact Us</a></li><li><a href="blog.html">Blog & Articles</a></li><li><a href="terms-of-use.html">Terms of Use</a></li><li><a href="privacy-policy.html">Privacy Policy</a></li><li><a href="404.html">404</a></li></ul></div>
<div class="rv" style="--d:.24s"><h4>Let’s Connect</h4><ul class="soc"><li><a href="#" aria-label="Instagram"><img src="assets/img/gN3zRJ2if0XmUwlsvkjmn3Qb0.svg" alt=""  width=20 height=20 loading="lazy" decoding="async" >Instagram</a></li><li><a href="#" aria-label="x.com"><img src="assets/img/qFQLrwy2LQwiQsYewoLRIvcwCgU.svg" alt=""  width=20 height=20 loading="lazy" decoding="async" >x.com</a></li><li><a href="#" aria-label="LinkedIn"><img src="assets/img/DVeOb1eqYJJ5sqZqpBb42ALKE.svg" alt=""  width=20 height=20 loading="lazy" decoding="async" >LinkedIn</a></li><li><a href="#" aria-label="Facebook"><img src="assets/img/Y5nB02Dtnt6itSCLVH7ugawaGIE.svg" alt=""  width=20 height=20 loading="lazy" decoding="async" >Facebook</a></li></ul></div></div>
<div class="foot-bar rv" style="--d:.3s"><p>© 2026 Nexivo. All rights reserved.</p><p class="powered">Powered by <b>Nexum</b></p></div></div></footer>
<a class="totop" href="#" aria-label="Back to top"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M6 11l6-6 6 6"/></svg></a>`;

  function inject(id, markup) {
    var el = document.getElementById(id);
    if (el) el.outerHTML = markup;
  }
  inject("site-header", header);
  inject("site-footer", footer);

  // Mark the current page's link active, reproducing the old per-page class="on".
  var page = location.pathname.split("/").pop() || "index.html";
  var links = document.querySelectorAll(".menu a, .foot a");
  for (var i = 0; i < links.length; i++) {
    if (links[i].getAttribute("href") === page) links[i].classList.add("on");
  }
})();
