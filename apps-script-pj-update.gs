/**
 * ============================================================================
 * STV Website Leads - Permanent Jewelry ADDENDUM for Backend v11
 * ============================================================================
 * This is NOT a standalone script. Do NOT paste it as a second doPost.
 * The live backend must contain exactly ONE doPost (the v11 one in
 * STV-Leads-Backend-v11.js). Merge the five snippets below into that file
 * at the marked spots, then redeploy the web app.
 *
 * DEPLOY NOTES (same as v11):
 * - Deploy as a Web App with "Execute as: Me" so sheet + Gmail run under
 *   Christina's account.
 * - After editing the script, create a NEW deployment version (Deploy >
 *   Manage deployments > Edit > New version) or the live /exec URL keeps
 *   running the old code.
 * - Encoding: HTML entities only in email copy (&#9670; etc.) - no raw
 *   emojis anywhere in this file, same rule as v11.
 * - New sheet setup needed ONCE before this goes live:
 *   1. In the "Master Tracker" tab, put the header "Permanent Jewelry"
 *      in column O (column 15).
 *   2. Nothing else - the "Permanent Jewelry" detail tab is created
 *      automatically (with headers) the first time a booking request
 *      comes in.
 * ============================================================================
 */

// ============================================================================
// SNIPPET 1 of 5 - Master Tracker column map
// In v11, find the COL object and add the PERMANENT_JEWELRY line so it reads:
// ============================================================================
/*
var COL = {
  EMAIL: 1, NAME: 2, FIRST_SEEN: 3, LAST_ACTIVITY: 4,
  NEWSLETTER: 5, WELCOME_SENT: 6,
  FREEBIE_PROMPTS: 7, FREEBIE_RESET: 8, FREEBIE_BOUNDARY: 9,
  CONTACT: 10, BOOK: 11, COACHING: 12,
  SOURCE_PAGE: 13, NOTES: 14,
  PERMANENT_JEWELRY: 15
};
*/

// ============================================================================
// SNIPPET 2 of 5 - doPost routing branch
// In doPost, add this branch to the if / else chain that sets actionLabel,
// e.g. right after the "coaching" branch:
// ============================================================================
/*
    } else if (type === 'permanent-jewelry' || type === 'pj-booking') {
      actionLabel = 'Permanent jewelry booking request';
      actionCol = COL.PERMANENT_JEWELRY;
*/

// ============================================================================
// SNIPPET 3 of 5 - doPost additions AFTER the upsertPerson(...) call
// and BEFORE the "Notify Christina" GmailApp.sendEmail call.
// The booking details then ride along in Christina's notification email,
// mirroring how contact-form messages are appended in v11.
// ============================================================================
/*
    // Permanent jewelry: send the client their next-steps email on EVERY
    // booking request (separate from the one-time welcome email).
    if (type === 'permanent-jewelry' || type === 'pj-booking') {
      sendPjBookingEmail(data);
    }
*/
// ...and inside the notify-body build, right after the existing block
//     if (type === 'contact' && data.message) { ... }
// add:
/*
    if (type === 'permanent-jewelry' || type === 'pj-booking') {
      notifyBody += '\n\nBooking details:\n' + pjDetailsText(data);
    }
*/

// ============================================================================
// SNIPPET 4 of 5 - detail logging branch for logToLegacyTab()
// Add this as the FIRST branch inside logToLegacyTab, before the existing
// "contact" branch. It appends the full booking request to a dedicated
// "Permanent Jewelry" tab (Master Tracker itself only stores timestamps,
// same as every other action type in v11).
// ============================================================================
/*
    if (type === 'permanent-jewelry' || type === 'pj-booking') {
      var pj = ss.getSheetByName('Permanent Jewelry');
      if (!pj) {
        pj = ss.insertSheet('Permanent Jewelry');
        pj.appendRow(['Timestamp', 'Name', 'Email', 'Phone', 'Lane', 'Piece',
          'Chain Style', 'Metal', 'Size', 'Quantity', 'Addons', 'City',
          'Distance', 'Outlet', 'Inspo URL', 'Waiver', 'Notes', 'Page']);
      }
      pj.appendRow([timestamp, data.name || '', email, data.phone || '',
        data.lane || '', data.piece || '', data.chain_style || '',
        data.metal || '', data.size || '', data.quantity || '',
        data.addons || '', data.city || '', data.distance || '',
        data.outlet || '', data.inspo_url || '', data.waiver || '',
        data.notes || '', data.page || '']);
    } else if (type === 'contact') {
      ... (rest of the existing function stays exactly as-is)
*/

// ============================================================================
// SNIPPET 5 of 5 - new functions. Paste these at the END of the v11 file,
// e.g. right after sendWelcomeEmail(). These are complete, ready to run.
// ============================================================================

var PJ_BOOKING_PAGE = 'https://shesthevibe.co/permanent-jewelry-book.html';
var PJ_INFO_PAGE = 'https://shesthevibe.co/permanent-jewelry.html';
var PJ_PACKET_PDF = 'https://shesthevibe.co/permanent-jewelry-before-your-appointment.pdf';
var PJ_RELEASE_PDF = 'https://shesthevibe.co/permanent-jewelry-release.pdf';
var PJ_AFTERCARE_PDF = 'https://shesthevibe.co/permanent-jewelry-aftercare.pdf';

var PJ_SUBJECT = 'Your Permanent Jewelry Next Steps - She\'s The Vibe';

/**
 * One-line-per-field plain-text summary of a booking request.
 * Used in Christina's notification email.
 */
function pjDetailsText(data) {
  var lines = [
    'Phone: ' + (data.phone || '(not provided)'),
    'Lane: ' + (data.lane || '(not provided)'),
    'Piece: ' + (data.piece || '(not provided)'),
    'Chain style: ' + (data.chain_style || '(not provided)'),
    'Metal: ' + (data.metal || '(not provided)'),
    'Size: ' + (data.size || '(not provided)'),
    'Quantity: ' + (data.quantity || '1'),
    'Charms/connectors: ' + (data.addons || '(none noted)'),
    'City: ' + (data.city || '(not provided)'),
    'Distance from Silverado: ' + (data.distance || '(not provided)'),
    'Outlet available: ' + (data.outlet || '(not provided)'),
    'Inspo pic: ' + (data.inspo_url || '(none - may be emailed separately)'),
    'Waiver acknowledged: ' + (data.waiver || 'no')
  ];
  if (data.notes) lines.push('Notes: ' + data.notes);
  return lines.join('\n');
}

/**
 * Plain-text fallback for the PJ next-steps email.
 */
function pjEmailText(data) {
  var first = (data.name || '').split(' ')[0] || 'beautiful';
  return [
    'Hi ' + first + ',',
    '',
    'Your permanent jewelry booking request is in - I read every single one myself.',
    'Here\'s how we get you welded:',
    '',
    '1. BOOK + START WITH YOUR DEPOSIT:',
    '   Head to the booking page and grab your spot in my calendar. Your deposit',
    '   ($25 for The Standards, $75 for Custom Elite) is what lets me order your',
    '   chain and materials, and it\'s credited toward your total:',
    '   ' + PJ_BOOKING_PAGE,
    '',
    '2. READ YOUR PACKET:',
    '   Everything about how it works, pricing, travel, and setup is in here:',
    '   ' + PJ_PACKET_PDF,
    '',
    '3. SIGN YOUR RELEASE:',
    '   Quick, plain language, done before appointment day so there\'s zero',
    '   paperwork energy when I get there:',
    '   ' + PJ_RELEASE_PDF,
    '',
    '4. SEND YOUR INSPO PIC (custom girls, this one\'s you):',
    '   Just reply to this email with your picture, or send it to',
    '   christina@shesthevibe.co with your name.',
    '',
    'Once your chain arrives, I\'ll confirm your final quote and appointment',
    'details. Then I come to you - all I need is a small work area and a power',
    'outlet (no outlet? I can run it from my car).',
    '',
    'And for after your appointment, your care sheet lives here:',
    PJ_AFTERCARE_PDF,
    '',
    'Want to browse chains and pricing again?',
    PJ_INFO_PAGE,
    '',
    'With love,',
    'Christina',
    '',
    'Founder, She\'s The Vibe',
    'A Wood Family Creations LLC Brand'
  ].join('\n');
}

/**
 * Branded HTML version of the PJ next-steps email.
 * Same burgundy / cream / gold shell as the v11 welcome email.
 * Entities only - no raw emojis.
 */
function pjEmailHtml(data) {
  var first = (data.name || '').split(' ')[0] || 'beautiful';
  var pieceLine = '';
  if (data.piece) {
    pieceLine = ' You told me you&rsquo;re dreaming about: <strong>' +
      String(data.piece) + '</strong>' +
      (data.chain_style ? ' in <strong>' + String(data.chain_style) + '</strong>' : '') +
      (data.metal ? ' (' + String(data.metal) + ')' : '') + '.';
  }
  return [
'<!DOCTYPE html>',
'<html lang="en" xmlns="http://www.w3.org/1999/xhtml">',
'<head>',
'  <meta charset="utf-8">',
'  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
'  <title>Your Permanent Jewelry Next Steps</title>',
'</head>',
'<body style="margin:0; padding:0; background-color:#F7E7CE;">',
'  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F7E7CE; margin:0; padding:0;">',
'    <tr>',
'      <td align="center" style="padding: 24px 12px;">',
'        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px; width:100%; background-color:#FFFDF8; border-radius:12px; overflow:hidden;">',
'          <tr>',
'            <td align="center" style="background-color:#451425; padding: 44px 32px 36px 32px;">',
'              <div style="font-family: Georgia, \'Times New Roman\', serif; font-size:38px; color:#C9A96E; letter-spacing:2px; font-style:italic; line-height:1.2;">She&rsquo;s The Vibe</div>',
'              <div style="font-family: Arial, Helvetica, sans-serif; font-size:12px; color:#F7E7CE; letter-spacing:6px; text-transform:uppercase; margin-top:12px;">Practical. Pretty. You.</div>',
'              <div style="margin-top:20px; color:#C9A96E; font-size:16px; letter-spacing:8px;">&#9670;&nbsp;&mdash;&nbsp;&#9670;&nbsp;&mdash;&nbsp;&#9670;</div>',
'            </td>',
'          </tr>',
'          <tr>',
'            <td style="padding: 40px 40px 32px 40px; font-family: Arial, Helvetica, sans-serif; color:#5a2434;">',
'              <div style="font-family: Georgia, \'Times New Roman\', serif; font-size:26px; color:#451425; text-align:center; margin:0 0 24px 0; font-style:italic;">You&rsquo;re on your way to welded, ' + first + '.</div>',
'              <div style="font-size:16px; line-height:1.7; text-align:center; margin:0 0 28px 0;">Your booking request is in, and I read every single one myself.' + pieceLine + ' Here&rsquo;s how we get your piece on you:</div>',
'              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 28px 0;">',
'                <tr><td valign="top" style="padding:4px 0; font-size:15px; line-height:1.6;"><strong style="color:#451425;">1. Book + start with your deposit.</strong> Grab your spot in my calendar from the booking page. Your deposit ($25 Standards / $75 Custom Elite) lets me order your chain, and it&rsquo;s credited toward your total.</td></tr>',
'                <tr><td valign="top" style="padding:4px 0; font-size:15px; line-height:1.6;"><strong style="color:#451425;">2. Read your packet.</strong> How it works, pricing, travel, and setup — all in the Before Your Appointment packet below.</td></tr>',
'                <tr><td valign="top" style="padding:4px 0; font-size:15px; line-height:1.6;"><strong style="color:#451425;">3. Sign your release.</strong> Quick and plain-language, done before appointment day.</td></tr>',
'                <tr><td valign="top" style="padding:4px 0; font-size:15px; line-height:1.6;"><strong style="color:#451425;">4. Send your inspo pic.</strong> Going custom? Reply to this email with your picture, or send it to christina@shesthevibe.co with your name.</td></tr>',
'              </table>',
'              <div style="text-align:center; margin:0 0 16px 0;">',
'                <a href="' + PJ_BOOKING_PAGE + '" target="_blank" rel="noopener" style="display:inline-block; background-color:#451425; color:#C9A96E; font-size:16px; font-weight:bold; letter-spacing:2px; text-transform:uppercase; text-decoration:none; padding:16px 44px; border-radius:40px; border:2px solid #C9A96E;">Book Your Appointment</a>',
'              </div>',
'              <div style="text-align:center; font-size:15px; margin:0 0 28px 0;">',
'                <a href="' + PJ_PACKET_PDF + '" target="_blank" rel="noopener" style="color:#451425; font-weight:bold; text-decoration:underline;">Before Your Appointment packet</a>',
'                <span style="color:#C9A96E; padding:0 10px;">&#9670;</span>',
'                <a href="' + PJ_RELEASE_PDF + '" target="_blank" rel="noopener" style="color:#451425; font-weight:bold; text-decoration:underline;">Release &amp; Waiver</a>',
'                <span style="color:#C9A96E; padding:0 10px;">&#9670;</span>',
'                <a href="' + PJ_AFTERCARE_PDF + '" target="_blank" rel="noopener" style="color:#451425; font-weight:bold; text-decoration:underline;">Aftercare Sheet</a>',
'              </div>',
'              <div style="font-size:15px; line-height:1.7; text-align:center; margin:0;">Once your chain arrives I&rsquo;ll confirm your final quote and appointment details — then I come to you. All I need is a small work area and a power outlet (no outlet? I can run it from my car).</div>',
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
'              <div style="font-family: Arial, Helvetica, sans-serif; font-size:11px; color:#F7E7CE; letter-spacing:3px; text-transform:uppercase; margin:0;">&copy; 2026 She&rsquo;s The Vibe &middot; A Wood Family Creations LLC Brand. All rights reserved.</div>',
'            </td>',
'          </tr>',
'        </table>',
'      </td>',
'    </tr>',
'  </table>',
'</body>',
'</html>'
  ].join('\n');
}

/**
 * Send the PJ next-steps email to the client.
 */
function sendPjBookingEmail(data) {
  var toEmail = (data.email || '').trim().toLowerCase();
  if (!toEmail) return;
  GmailApp.sendEmail(toEmail, PJ_SUBJECT, pjEmailText(data), {
    name: "She's The Vibe",
    htmlBody: pjEmailHtml(data)
  });
}
