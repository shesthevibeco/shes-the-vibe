// She's the Vibe main JavaScript
document.addEventListener('DOMContentLoaded', function () {
  // Mobile menu toggle
  var toggle = document.querySelector('.menu-toggle');
  var menu = document.getElementById('mobileMenu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    // Close menu when a link is tapped
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        menu.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Newsletter forms -> Google Sheet via Apps Script
  var NEWSLETTER_URL = 'https://script.google.com/macros/s/AKfycbwX4P7tXfv6QadbwGLJLfiFuLtxZuKTiTIXVofPooTxU_5qFaVBY2J-vRdypUbxXLLJuA/exec';
  document.querySelectorAll('.join-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = form.querySelector('input[type="email"]');
      var btn = form.querySelector('button[type="submit"]');
      var email = input.value.trim();
      if (!email) return;
      btn.disabled = true;
      var original = btn.textContent;
      btn.textContent = 'Joining...';
      fetch(NEWSLETTER_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'text/plain' },
        body: JSON.stringify({ email: email, page: window.location.pathname })
      }).then(function () {
        form.innerHTML = '<p class="join-success">You\'re in, beautiful! Check your inbox soon.</p>';
      }).catch(function () {
        btn.disabled = false;
        btn.textContent = original;
        alert('Hmm, that didn\'t go through — please try again.');
      });
    });
  });
});
