/**
 * STV Website Leads - Web App Backend v9
 * Plain-text welcome email, zero emojis (encoding-safe).
 */

// ============================================================================
// CONFIG
// ============================================================================
var SHEET_ID = '1rgICMTZ-g-KDczqnpDysgP4OdcldOXF_iNRFK2Bi3JM';

var WELCOME_SUBJECT = 'Practical. Pretty. You. - Welcome to the Vibe';

var WELCOME_BODY = [
  'Welcome to the Vibe, babe.',
  '',
  'You just did something good for yourself, and I want you to know I\'m proud of you for it.',
  'This isn\'t some random newsletter that\'s gonna clog your inbox with stuff you don\'t need.',
  '',
  'Here\'s what you\'re actually getting from me:',
  '',
  '- First dibs on new drops: digital planners, guided journals, handmade jewelry',
  '- Exclusive offers: subscriber-only discounts, because you got here first',
  '- Real talk: the kind of honest words I wish somebody had said to me sooner',
  '- Free resources: planning tools, journal prompts, and little gifts to help you organize your life beautifully',
  '',
  'I built She\'s The Vibe because I needed a space like this growing up -',
  'a place where you don\'t have to dim yourself to fit in.',
  'Where you\'re allowed to be soft *and* disciplined, creative *and* practical.',
  'All of it. All of you.',
  '',
  'That\'s the vibe. Practical. Pretty. You.',
  '',
  'Want to start exploring? Check out the shop:',
  'https://www.etsy.com/shop/ShesTheVibe',
  '',
  'And come say hi - I\'m most active here:',
  'Instagram: https://instagram.com/shesthevibeco',
  'Website: https://shesthevibe.co',
  '',
  'Stick around. We\'re just getting started.',
  '',
  'With love,',
  'Christina',
  '',
  'Founder, She\'s The Vibe',
  'A Wood Family Creations LLC Brand'
].join('\n');

// ============================================================================
// MAIN ENTRY POINT
// ============================================================================
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var type = (data.type || 'newsletter').toLowerCase();

    var ss = SpreadsheetApp.openById(SHEET_ID);
    var timestamp = new Date();

    if (type === 'newsletter' || type === 'subscribe' || type === 'subscriber') {
      handleNewSubscriber(ss, data, timestamp);
    } else if (type === 'contact') {
      handleContactMessage(ss, data, timestamp);
    } else if (type === 'book' || type === 'bookinterest') {
      handleBookInterest(ss, data, timestamp);
    } else {
      handleNewSubscriber(ss, data, timestamp);
    }

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function handleNewSubscriber(ss, data, timestamp) {
  var sheet = ss.getSheetByName('Subscribers');
  var email = (data.email || '').trim();
  if (!email) throw new Error('Missing email for newsletter signup.');

  var existing = sheet.getRange(1, 2, sheet.getLastRow(), 1).getValues().flat();
  var alreadySubscribed = existing.some(function(cell) {
    return String(cell).trim().toLowerCase() === email.toLowerCase();
  });

  sheet.appendRow([timestamp, email, data.name || '']);

  if (!alreadySubscribed) {
    sendWelcomeEmail(email);
  }
}

function sendWelcomeEmail(toEmail) {
  GmailApp.sendEmail(toEmail, WELCOME_SUBJECT, WELCOME_BODY, {
    name: "She's The Vibe"
  });
}

function handleContactMessage(ss, data, timestamp) {
  var sheet = ss.getSheetByName('Contact Messages');
  sheet.appendRow([timestamp, data.name || '', data.email || '', data.message || '']);
}

function handleBookInterest(ss, data, timestamp) {
  var sheet = ss.getSheetByName('Book Interest');
  sheet.appendRow([timestamp, data.name || '', data.email || '']);
}
