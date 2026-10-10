/**
 * STV Website Leads - Web App Backend v9
 * Plain-text welcome email, zero emojis (encoding-safe).
 */

// ============================================================================
// CONFIG
// ============================================================================
var SHEET_ID = '1rgICMTZ-g-KDczqnpDysgP4OdcldOXF_iNRFK2Bi3JM';

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
'<body style="margin:0; padding:0; background-color:#F7E7CE; -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%;">',
'  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F7E7CE; margin:0; padding:0;">',
'    <tr>',
'      <td align="center" style="padding: 24px 12px;">',
'        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px; width:100%; background-color:#FFFDF8;">',
'          <tr>',
'            <td align="center" style="background-color:#451425; padding: 44px 32px 36px 32px;">',
'              <div style="font-family: Georgia, \'Times New Roman\', serif; font-size:38px; color:#C9A96E; letter-spacing:2px; font-style:italic; line-height:1.2;">She&rsquo;s The Vibe</div>',
'              <div style="font-family: Arial, Helvetica, sans-serif; font-size:12px; color:#F7E7CE; letter-spacing:6px; text-transform:uppercase; margin-top:12px;">Practical. Pretty. You.</div>',
'              <div style="margin-top:20px; color:#C9A96E; font-size:16px; letter-spacing:8px;">&#9670;&nbsp;&mdash;&nbsp;&#9670;&nbsp;&mdash;&nbsp;&#9670;</div>',
'            </td>',
'          </tr>',
'          <tr>',
'            <td style="padding: 40px 40px 32px 40px;">',
'              <div style="font-family: Georgia, \'Times New Roman\', serif; font-size:26px; color:#451425; text-align:center; margin:0 0 24px 0; font-style:italic;">Welcome to the Vibe, babe.</div>',
'              <div style="font-family: Arial, Helvetica, sans-serif; font-size:16px; line-height:1.7; color:#5a2434; text-align:center; margin:0 0 28px 0;">You just did something good for yourself, and I want you to know I&rsquo;m proud of you for it. This isn&rsquo;t some random newsletter that&rsquo;s gonna clog your inbox with stuff you don&rsquo;t need.</div>',
'              <div style="text-align:center; color:#C9A96E; font-size:14px; letter-spacing:6px; margin:0 0 28px 0;">&#10022;&nbsp;&#10022;&nbsp;&#10022;</div>',
'              <div style="font-family: Georgia, \'Times New Roman\', serif; font-size:18px; color:#451425; text-align:center; margin:0 0 20px 0; font-style:italic;">Here&rsquo;s what you&rsquo;re actually getting from me:</div>',
'              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 28px 0;">',
'                <tr>',
'                  <td width="28" valign="top" style="color:#C9A96E; font-size:14px; padding:6px 8px 6px 0;">&#9670;</td>',
'                  <td valign="top" style="font-family: Arial, Helvetica, sans-serif; font-size:15px; line-height:1.6; color:#5a2434; padding:4px 0;"><strong style="color:#451425;">First dibs</strong> on new drops &mdash; digital planners, guided journals, handmade jewelry</td>',
'                </tr>',
'                <tr><td colspan="2" style="height:10px; line-height:10px;">&nbsp;</td></tr>',
'                <tr>',
'                  <td width="28" valign="top" style="color:#C9A96E; font-size:14px; padding:6px 8px 6px 0;">&#9670;</td>',
'                  <td valign="top" style="font-family: Arial, Helvetica, sans-serif; font-size:15px; line-height:1.6; color:#5a2434; padding:4px 0;"><strong style="color:#451425;">Exclusive offers</strong> &mdash; subscriber-only discounts, because you got here first</td>',
'                </tr>',
'                <tr><td colspan="2" style="height:10px; line-height:10px;">&nbsp;</td></tr>',
'                <tr>',
'                  <td width="28" valign="top" style="color:#C9A96E; font-size:14px; padding:6px 8px 6px 0;">&#9670;</td>',
'                  <td valign="top" style="font-family: Arial, Helvetica, sans-serif; font-size:15px; line-height:1.6; color:#5a2434; padding:4px 0;"><strong style="color:#451425;">Real talk</strong> &mdash; the kind of honest words I wish somebody had said to me sooner</td>',
'                </tr>',
'                <tr><td colspan="2" style="height:10px; line-height:10px;">&nbsp;</td></tr>',
'                <tr>',
'                  <td width="28" valign="top" style="color:#C9A96E; font-size:14px; padding:6px 8px 6px 0;">&#9670;</td>',
'                  <td valign="top" style="font-family: Arial, Helvetica, sans-serif; font-size:15px; line-height:1.6; color:#5a2434; padding:4px 0;"><strong style="color:#451425;">Free resources</strong> &mdash; planning tools, journal prompts, and little gifts to help you organize your life beautifully</td>',
'                </tr>',
'              </table>',
'              <div style="text-align:center; color:#C9A96E; font-size:14px; letter-spacing:6px; margin:0 0 28px 0;">&#10022;&nbsp;&#10022;&nbsp;&#10022;</div>',
'              <div style="font-family: Georgia, \'Times New Roman\', serif; font-size:16px; line-height:1.8; color:#5a2434; text-align:center; font-style:italic; margin:0 0 20px 0;">I built She&rsquo;s The Vibe because I needed a space like this growing up &mdash; a place where you don&rsquo;t have to dim yourself to fit in. Where you&rsquo;re allowed to be soft <em>and</em> disciplined, creative <em>and</em> practical. All of it. All of you.</div>',
'              <div style="font-family: Georgia, \'Times New Roman\', serif; font-size:20px; color:#451425; text-align:center; margin:0 0 32px 0; letter-spacing:1px;">That&rsquo;s the vibe. <span style="color:#C9A96E;">Practical. Pretty. You.</span></div>',
'              <div style="text-align:center; margin:0 0 32px 0;">',
'                <a href="https://www.etsy.com/shop/ShesTheVibe" target="_blank" rel="noopener" style="display:inline-block; background-color:#451425; color:#C9A96E; font-family: Arial, Helvetica, sans-serif; font-size:16px; font-weight:bold; letter-spacing:2px; text-transform:uppercase; text-decoration:none; padding:16px 44px; border:2px solid #C9A96E;">Explore the Shop</a>',
'              </div>',
'              <div style="font-family: Arial, Helvetica, sans-serif; font-size:15px; line-height:1.7; color:#5a2434; text-align:center; margin:0 0 12px 0;">And come say hi &mdash; I&rsquo;m most active here:</div>',
'              <div style="text-align:center; margin:0 0 28px 0; font-family: Arial, Helvetica, sans-serif; font-size:15px;">',
'                <a href="https://instagram.com/shesthevibeco" target="_blank" rel="noopener" style="color:#451425; text-decoration:underline; font-weight:bold;">Instagram</a>',
'                <span style="color:#C9A96E; padding:0 12px;">&#9670;</span>',
'                <a href="https://shesthevibe.co" target="_blank" rel="noopener" style="color:#451425; text-decoration:underline; font-weight:bold;">Website</a>',
'              </div>',
'              <div style="font-family: Georgia, \'Times New Roman\', serif; font-size:16px; color:#451425; text-align:center; font-style:italic; margin:0;">Stick around. We&rsquo;re just getting started.</div>',
'            </td>',
'          </tr>',
'          <tr>',
'            <td align="center" style="padding: 8px 40px 40px 40px;">',
'              <div style="font-family: Georgia, \'Times New Roman\', serif; font-size:22px; color:#451425; font-style:italic; margin:0 0 6px 0;">With love, Christina</div>',
'              <div style="font-family: Arial, Helvetica, sans-serif; font-size:12px; color:#8a6a4a; letter-spacing:1px; margin:0;">Founder, She&rsquo;s The Vibe &middot; A Wood Family Creations LLC Brand</div>',
'            </td>',
'          </tr>',
'          <tr>',
'            <td align="center" style="background-color:#451425; padding: 28px 32px;">',
'              <div style="font-family: Georgia, \'Times New Roman\', serif; font-size:20px; color:#C9A96E; font-style:italic; margin:0 0 8px 0;">She&rsquo;s The Vibe</div>',
'              <div style="font-family: Arial, Helvetica, sans-serif; font-size:11px; color:#F7E7CE; letter-spacing:3px; text-transform:uppercase; margin:0 0 16px 0;">Practical. Pretty. You.</div>',
'              <div style="font-family: Arial, Helvetica, sans-serif; font-size:12px; margin:0 0 16px 0;">',
'                <a href="https://www.etsy.com/shop/ShesTheVibe" target="_blank" rel="noopener" style="color:#C9A96E; text-decoration:none; padding:0 10px;">Shop</a>',
'                <span style="color:#C9A96E;">|</span>',
'                <a href="https://instagram.com/shesthevibeco" target="_blank" rel="noopener" style="color:#C9A96E; text-decoration:none; padding:0 10px;">Instagram</a>',
'                <span style="color:#C9A96E;">|</span>',
'                <a href="https://shesthevibe.co" target="_blank" rel="noopener" style="color:#C9A96E; text-decoration:none; padding:0 10px;">Website</a>',
'              </div>',
'              <div style="font-family: Arial, Helvetica, sans-serif; font-size:11px; color:#a88968; line-height:1.6; margin:0;">You&rsquo;re receiving this because you subscribed at shesthevibe.co.<br>&copy; 2026 She&rsquo;s The Vibe &middot; A Wood Family Creations LLC Brand. All rights reserved.</div>',
'            </td>',
'          </tr>',
'        </table>',
'      </td>',
'    </tr>',
'  </table>',
'</body>',
'</html>'
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
  GmailApp.sendEmail(toEmail, WELCOME_SUBJECT, WELCOME_TEXT_FALLBACK, {
    name: "She's The Vibe",
    htmlBody: WELCOME_HTML
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
