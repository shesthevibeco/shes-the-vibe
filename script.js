// She's the Vibe main JavaScript
document.addEventListener('DOMContentLoaded', function () {
  var NEWSLETTER_URL = 'https://script.google.com/macros/s/AKfycbz7VpnIN4j3ts-1ZTF3OqAcJryu1PUOSgMjtwB0wOQpyNPIrC9LeVqyCh21f2Sjj3N8/exec';

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
        alert('Hmm, that didn\'t go through — please try again or email christina@shesthevibe.co directly.');
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

  // Freebie email-capture modal -> Subscribers tab, then auto-download PDF
  var freebieModal = document.getElementById('freebieModal');
  if (freebieModal) {
    var freebieForm = document.getElementById('freebieModalForm');
    var freebieNameEl = document.getElementById('freebieModalName');
    var freebieClose = document.getElementById('freebieModalClose');
    var pendingPdf = null;
    var pendingTitle = null;

    function openFreebieModal(pdf, title) {
      pendingPdf = pdf;
      pendingTitle = title;
      freebieNameEl.textContent = '\u201C' + title + '\u201D';
      freebieModal.classList.add('open');
      freebieModal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      var emailInput = document.getElementById('freebieEmail');
      if (emailInput) setTimeout(function () { emailInput.focus(); }, 120);
    }
    function closeFreebieModal() {
      freebieModal.classList.remove('open');
      freebieModal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }

    document.querySelectorAll('.freebie-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        openFreebieModal(btn.getAttribute('data-pdf'), btn.getAttribute('data-name'));
      });
    });
    freebieClose.addEventListener('click', closeFreebieModal);
    freebieModal.addEventListener('click', function (e) {
      if (e.target === freebieModal) closeFreebieModal();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && freebieModal.classList.contains('open')) closeFreebieModal();
    });

    freebieForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var nameInput = freebieForm.querySelector('[name="name"]');
      var emailInput = freebieForm.querySelector('[name="email"]');
      var name = nameInput.value.trim();
      var email = emailInput.value.trim();
      if (!email || email.indexOf('@') < 0) {
        emailInput.focus();
        return;
      }
      var btn = freebieForm.querySelector('button[type="submit"]');
      btn.disabled = true;
      var original = btn.textContent;
      btn.textContent = 'Sending...';
      fetch(NEWSLETTER_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'text/plain' },
        body: JSON.stringify({ name: name, email: email, page: window.location.pathname, source: 'freebie: ' + pendingTitle })
      }).then(function () {
        // Trigger the PDF download
        var a = document.createElement('a');
        a.href = pendingPdf;
        a.setAttribute('download', '');
        document.body.appendChild(a);
        a.click();
        a.remove();
        freebieForm.innerHTML = '<p class="join-success">It\'s on its way! Your download should start any second. Check your inbox soon for a little hello from us.</p>';
        setTimeout(closeFreebieModal, 5000);
      }).catch(function () {
        btn.disabled = false;
        btn.textContent = original;
        alert('Hmm, that didn\'t go through — please try again.');
      });
    });
  }
});
