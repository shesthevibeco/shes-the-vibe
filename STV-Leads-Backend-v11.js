/**
 * STV Website Leads - Web App Backend v11
 * Master Tracker: single row per person, every touchpoint logged.
 * Plain-text welcome email, zero emojis (encoding-safe).
 */

// ============================================================================
// CONFIG
// ============================================================================
var SHEET_ID = '1rgICMTZ-g-KDczqnpDysgP4OdcldOXF_iNRFK2Bi3JM';
var TRACKER_TAB = 'Master Tracker';
var NOTIFY_EMAIL = 'christina@shesthevibe.co';

var WELCOME_SUBJECT = 'Practical. Pretty. You. - Welcome to the Vibe';

var WELCOME_TEXT_FALLBACK = [
  'Welcome to the Vibe, babe.',
  '',
  'You just did something good for yourself, and I want you to know I\'m proud of you for it.',
  'This isn\'t some random newsletter that\'s gonna clog your inbox with stuff you don\'t need.',
  '',
  'Here\'s what you\'re actually getting from me:',
  '',
  '* First dibs on new drops - digital planners, guided journals, handmade jewelry',
  '* Exclusive offers - subscriber-only discounts, because you got here first',
  '* Real talk - the kind of honest words I wish somebody had said to me sooner',
  '* Free resources - planning tools, journal prompts, and little gifts to help you organize your life beautifully',
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

var WELCOME_HTML = [
'<!DOCTYPE html>',
'<html lang="en">',
'<head>',
'  <meta charset="utf-8">',
'  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
'  <title>Practical. Pretty. You. &mdash; Welcome to the Vibe</title>',
'</head>',
'<body style="margin:0; padding:0; background-color:#F7E7CE;">',
'  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F7E7CE; margin:0; padding:0;">',
'    <tr><td align="center" style="padding: 24px 12px;">',
'      <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px; width:100%; background-color:#FFFDF8;">',
'        <tr><td align="center" style="background-color:#451425; padding: 44px 32px 36px 32px;">',
'          <div style="font-family: Georgia, serif; font-size:38px; color:#C9A96E; font-style:italic;">She&rsquo;s The Vibe</div>',
'          <div style="font-family: Arial, sans-serif; font-size:12px; color:#F7E7CE; letter-spacing:6px; text-transform:uppercase; margin-top:12px;">Practical. Pretty. You.</div>',
'        </td></tr>',
'        <tr><td style="padding: 40px;">',
'          <div style="font-family: Georgia, serif; font-size:26px; color:#451425; text-align:center; font-style:italic; margin-bottom:24px;">Welcome to the Vibe, babe.</div>',
'          <div style="font-family: Arial, sans-serif; font-size:16px; line-height:1.7; color:#5a2434; text-align:center; margin-bottom:28px;">You just did something good for yourself, and I want you to know I&rsquo;m proud of you for it.</div>',
'          <div style="text-align:center; margin-bottom:32px;"><a href="https://www.etsy.com/shop/ShesTheVibe" style="display:inline-block; background-color:#451425; color:#C9A96E; font-size:16px; font-weight:bold; text-decoration:none; padding:16px 44px;">Explore the Shop</a></div>',
'          <div style="font-family: Georgia, serif; font-size:22px; color:#451425; text-align:center; font-style:italic;">With love, Christina</div>',
'          <div style="font-family: Arial, sans-serif; font-size:12px; color:#8a6a4a; text-align:center;">Founder, She&rsquo;s The Vibe &middot; A Wood Family Creations LLC Brand</div>',
'        </td></tr>',
'      </table>',
'    </td></tr>',
'  </table>',
'</body>',
'</html>'
].join('\n');

// Column indices (1-based) in Master Tracker
var COL = {
  EMAIL: 1, NAME: 2, FIRST_SEEN: 3, LAST_ACTIVITY: 4,
  NEWSLETTER: 5, WELCOME_SENT: 6,
  FREEBIE_PROMPTS: 7, FREEBIE_RESET: 8, FREEBIE_BOUNDARY: 9,
  CONTACT: 10, BOOK: 11, COACHING: 12,
  SOURCE_PAGE: 13, NOTES: 14
};

// ============================================================================
// MAIN ENTRY POINT
// ============================================================================
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var type = (data.type || 'newsletter').toLowerCase();
    var ss = SpreadsheetApp.openById(SHEET_ID);
    var timestamp = new Date();
    var email = (data.email || '').trim().toLowerCase();

    if (!email) throw new Error('Missing email.');

    var actionLabel = '';
    var actionCol = 0;

    if (type === 'newsletter' || type === 'subscribe' || type === 'subscriber') {
      actionLabel = 'Newsletter signup';
      actionCol = COL.NEWSLETTER;
    } else if (type === 'contact') {
      actionLabel = 'Contact form message';
      actionCol = COL.CONTACT;
    } else if (type === 'book' || type === 'bookinterest' || type === 'book-interest') {
      actionLabel = 'Book interest signup';
      actionCol = COL.BOOK;
    } else if (type === 'coaching' || type === 'coaching-inquiry') {
      actionLabel = 'Coaching inquiry';
      actionCol = COL.COACHING;
    } else if (type === 'freebie') {
      var freebieName = (data.freebie || '').toLowerCase();
      if (freebieName.indexOf('prompt') >= 0) {
        actionLabel = 'Freebie: 50 Journal Prompts';
        actionCol = COL.FREEBIE_PROMPTS;
      } else if (freebieName.indexOf('reset') >= 0 || freebieName.indexOf('morning') >= 0) {
        actionLabel = 'Freebie: 5-Min Morning Reset';
        actionCol = COL.FREEBIE_RESET;
      } else if (freebieName.indexOf('boundary') >= 0) {
        actionLabel = 'Freebie: Boundary Scripts';
        actionCol = COL.FREEBIE_BOUNDARY;
      } else {
        actionLabel = 'Freebie download: ' + (data.freebie || 'unknown');
        actionCol = COL.FREEBIE_PROMPTS;
      }
    } else {
      actionLabel = 'Newsletter signup';
      actionCol = COL.NEWSLETTER;
    }

    var result = upsertPerson(ss, data, email, timestamp, actionCol);

    // Send welcome email only on very first contact
    var welcomeSent = '';
    if (result.isNew) {
      sendWelcomeEmail(email);
      welcomeSent = new Date();
      var tracker = ss.getSheetByName(TRACKER_TAB);
      tracker.getRange(result.row, COL.WELCOME_SENT).setValue(welcomeSent);
    }

    // Notify Christina ASAP with full details
    var notifyBody = [
      'Action: ' + actionLabel,
      'Email: ' + email,
      'Name: ' + (data.name || '(not provided)'),
      'Page: ' + (data.page || '(unknown)'),
      'Time: ' + timestamp,
      '',
      result.isNew ? 'This is a NEW person (welcome email sent).' : 'Returning person (no duplicate welcome email).',
      '',
      'View tracker: https://docs.google.com/spreadsheets/d/' + SHEET_ID + '/edit'
    ].join('\n');

    if (type === 'contact' && data.message) {
      notifyBody += '\n\nMessage:\n' + data.message;
    }

    GmailApp.sendEmail(NOTIFY_EMAIL,
      '[STV] ' + actionLabel + ': ' + email,
      notifyBody,
      { name: "She's The Vibe Alerts" });

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true, isNew: result.isNew, action: actionLabel }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Find person by email in Master Tracker, or create new row.
 * Updates the action column with timestamp. Returns {row, isNew}.
 */
function upsertPerson(ss, data, email, timestamp, actionCol) {
  var sheet = ss.getSheetByName(TRACKER_TAB);
  var lastRow = sheet.getLastRow();
  var row = -1;
  var isNew = false;

  if (lastRow > 1) {
    var emails = sheet.getRange(2, COL.EMAIL, lastRow - 1, 1).getValues().flat();
    for (var i = 0; i < emails.length; i++) {
      if (String(emails[i]).trim().toLowerCase() === email) {
        row = i + 2;
        break;
      }
    }
  }

  if (row === -1) {
    // New person
    isNew = true;
    row = lastRow + 1;
    sheet.getRange(row, COL.EMAIL).setValue(email);
    sheet.getRange(row, COL.NAME).setValue(data.name || '');
    sheet.getRange(row, COL.FIRST_SEEN).setValue(timestamp);
    sheet.getRange(row, COL.SOURCE_PAGE).setValue(data.page || data.source || '');
  } else {
    // Returning person - update name if we didn't have it
    if (data.name) {
      var existingName = sheet.getRange(row, COL.NAME).getValue();
      if (!existingName) sheet.getRange(row, COL.NAME).setValue(data.name);
    }
  }

  // Always update last activity and the specific action column
  sheet.getRange(row, COL.LAST_ACTIVITY).setValue(timestamp);
  if (actionCol > 0) {
    sheet.getRange(row, actionCol).setValue(timestamp);
  }

  // Also log to legacy tabs for backwards compat
  logToLegacyTab(ss, data, email, timestamp);

  return { row: row, isNew: isNew };
}

/**
 * Keep old tabs updated too (so nothing breaks).
 */
function logToLegacyTab(ss, data, email, timestamp) {
  try {
    var type = (data.type || 'newsletter').toLowerCase();
    if (type === 'contact') {
      var cs = ss.getSheetByName('Contact Messages');
      if (cs) cs.appendRow([timestamp, data.name || '', email, data.message || '']);
    } else if (type === 'book' || type === 'bookinterest') {
      var bs = ss.getSheetByName('Book Interest');
      if (bs) bs.appendRow([timestamp, data.name || '', email]);
    } else {
      var ns = ss.getSheetByName('Subscribers');
      if (ns) ns.appendRow([timestamp, email, data.name || '']);
    }
  } catch (e) { /* non-fatal */ }
}

function sendWelcomeEmail(toEmail) {
  GmailApp.sendEmail(toEmail, WELCOME_SUBJECT, WELCOME_TEXT_FALLBACK, {
    name: "She's The Vibe",
    htmlBody: WELCOME_HTML
  });
}

function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({ ok: true, service: 'STV Website Leads v11' }))
    .setMimeType(ContentService.MimeType.JSON);
}
