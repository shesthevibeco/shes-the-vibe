// She's the Vibe main JavaScript
document.addEventListener('DOMContentLoaded', function () {
  var NEWSLETTER_URL = 'https://script.google.com/macros/s/AKfycbwvFvI0t4kHhZqg2K_y7s_0LUxv2JOsrkm5UNBs26dQ8ackKnsnHgvnlDhdiDJOSDk2/exec';

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

  // Newsletter forms -> Google Sheet via Apps Script (Subscribers tab)
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

  // Contact form -> Contact Messages tab
  document.querySelectorAll('.contact-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = form.querySelector('[name="name"]').value.trim();
      var email = form.querySelector('[name="email"]').value.trim();
      var message = form.querySelector('[name="message"]').value.trim();
      if (!name || !email || !message) return;
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      var original = btn.textContent;
      btn.textContent = 'Sending...';
      fetch(NEWSLETTER_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'text/plain' },
        body: JSON.stringify({ type: 'contact', name: name, email: email, message: message, page: window.location.pathname })
      }).then(function () {
        form.innerHTML = '<p class="join-success">Message sent! I read everything myself and will get back to you soon.</p>';
      }).catch(function () {
        btn.disabled = false;
        btn.textContent = original;
        alert('Hmm, that didn\'t go through — please try again or email Shesthevibeco@gmail.com directly.');
      });
    });
  });

  // Book waitlist form -> Book Interest tab
  document.querySelectorAll('.book-interest-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = form.querySelector('[name="name"]').value.trim();
      var email = form.querySelector('[name="email"]').value.trim();
      if (!name || !email) return;
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      var original = btn.textContent;
      btn.textContent = 'Adding you...';
      fetch(NEWSLETTER_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'text/plain' },
        body: JSON.stringify({ type: 'book-interest', name: name, email: email, page: window.location.pathname })
      }).then(function () {
        form.innerHTML = '<p class="join-success">You\'re on the list! You\'ll be first to know when the book drops.</p>';
      }).catch(function () {
        btn.disabled = false;
        btn.textContent = original;
        alert('Hmm, that didn\'t go through — please try again.');
      });
    });
  });
});
