// She's the Vibe main JavaScript
document.addEventListener('DOMContentLoaded', function () {
  var NEWSLETTER_URL = 'https://script.google.com/macros/s/AKfycbxop8zHkF8OSOPbudVL-qFzUOOSi_OkMBWWjwkl9ojhS-qyvKJ2uphe6g1ncmaI6mS3/exec';

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
    var STV_SUBSCRIBER_KEY = 'stv_subscriber';

    // Remember-me: keep the subscriber's name/email in localStorage so repeat
    // freebie downloads skip the modal but still get tracked in the sheet.
    function getStoredSubscriber() {
      try {
        var raw = localStorage.getItem(STV_SUBSCRIBER_KEY);
        if (!raw) return null;
        var s = JSON.parse(raw);
        if (s && s.email && s.email.indexOf('@') > 0) return s;
      } catch (e) { /* localStorage unavailable */ }
      return null;
    }
    function saveSubscriber(name, email) {
      try {
        localStorage.setItem(STV_SUBSCRIBER_KEY, JSON.stringify({
          name: name || '',
          email: email,
          captured: true,
          capturedAt: new Date().toISOString()
        }));
      } catch (e) { /* localStorage unavailable */ }
    }
    function downloadPdf(pdf) {
      var a = document.createElement('a');
      a.href = pdf;
      a.setAttribute('download', '');
      document.body.appendChild(a);
      a.click();
      a.remove();
    }
    function postFreebieSignup(name, email, title) {
      return fetch(NEWSLETTER_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'text/plain' },
        body: JSON.stringify({ type: 'freebie', freebie: title, name: name, email: email, page: window.location.pathname })
      });
    }

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
        var pdf = btn.getAttribute('data-pdf');
        var title = btn.getAttribute('data-name');
        var sub = getStoredSubscriber();
        if (sub) {
          // Already signed up: track this download, then download directly — no modal.
          postFreebieSignup(sub.name, sub.email, title).then(function () {
            downloadPdf(pdf);
          }).catch(function () {
            // Track failed but still give them the PDF.
            downloadPdf(pdf);
          });
          return;
        }
        openFreebieModal(pdf, title);
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
      postFreebieSignup(name, email, pendingTitle).then(function () {
        // Remember this visitor so future freebie downloads skip the modal.
        saveSubscriber(name, email);
        // Trigger the PDF download
        downloadPdf(pendingPdf);
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

// ============ SITE SEARCH ============
(function() {
  var overlay = document.getElementById('searchOverlay');
  if (!overlay) return;
  var input = document.getElementById('searchOverlayInput');
  var results = document.getElementById('searchOverlayResults');
  var closeBtn = document.getElementById('searchOverlayClose');
  var trigger = document.getElementById('searchTrigger');
  var searchIndex = null;

  function openSearch() {
    overlay.classList.add('open');
    overlay.setAttribute('aria-hidden', 'false');
    if (!searchIndex) {
      fetch('search-index.json')
        .then(function(r) { return r.json(); })
        .then(function(data) { searchIndex = data; });
    }
    setTimeout(function() { input.focus(); }, 100);
  }
  function closeSearch() {
    overlay.classList.remove('open');
    overlay.setAttribute('aria-hidden', 'true');
    input.value = '';
    results.innerHTML = '';
  }

  if (trigger) {
    trigger.addEventListener('click', function(e) { e.preventDefault(); openSearch(); });
  }
  if (closeBtn) closeBtn.addEventListener('click', closeSearch);
  overlay.addEventListener('click', function(e) { if (e.target === overlay) closeSearch(); });
  document.addEventListener('keydown', function(e) { if (e.key === 'Escape') closeSearch(); });

  input.addEventListener('input', function() {
    var q = input.value.trim().toLowerCase();
    if (!q || q.length < 2 || !searchIndex) {
      results.innerHTML = q.length >= 2 ? '<p class="no-results">Loading...</p>' : '';
      return;
    }
    var matches = searchIndex.filter(function(page) {
      var haystack = (page.title + ' ' + page.headings.join(' ') + ' ' + page.desc).toLowerCase();
      return q.split(/\s+/).every(function(word) { return haystack.indexOf(word) >= 0; });
    }).slice(0, 8);

    if (!matches.length) {
      results.innerHTML = '<p class="no-results">No matches found. Try "coaching", "journal", or "shop".</p>';
      return;
    }
    results.innerHTML = matches.map(function(page) {
      return '<a href="' + page.url + '"><div class="result-title">' + page.title + '</div>' +
        (page.desc ? '<div class="result-desc">' + page.desc + '</div>' : '') + '</a>';
    }).join('');
  });
})();
