# Welcome Email Setup — Step by Step

Your welcome email is written and saved. Now let's make it send automatically
every time someone new subscribes on your website. This takes about 5 minutes.

## What this does

Right now, when someone signs up for your newsletter on shesthevibe.co,
their email lands in your "STV Website Leads" Google Sheet — but nothing
else happens. After this setup, they'll **automatically get your welcome
email** within seconds of signing up. You don't have to do anything.

---

## Steps

### 1. Open your Apps Script project
- Go to **script.google.com** in your browser
- Click on the project called **"STV Website Leads"**

### 2. Replace the code
- You'll see your current code in the editor
- Select ALL of it (Ctrl+A or Cmd+A) and delete it
- Open the code file Talia prepared: **`apps-script-with-welcome-email.gs`**
  (she'll send it to you, or it's saved in the She's The Vibe workspace files)
- Copy ALL the text from that file
- Paste it into the Apps Script editor (replacing everything that was there)

### 3. Save
- Click the **💾 Save** icon (or press Ctrl+S / Cmd+S)
- If it asks you to name the project, call it **"STV Website Leads"**

### 4. Authorize Gmail (one-time)
- Click **▶ Run** and choose the function `doPost` from the dropdown
  (it will fail — that's expected, it needs real form data)
- Google will pop up asking for permission — click through and **Allow**
- It needs permission to: read your spreadsheet + **send email as you**
- This is what lets it send the welcome email from Shesthevibeco@gmail.com

### 5. Redeploy the web app
- Click **Deploy → Manage deployments**
- Click the **✏️ pencil icon** next to your existing deployment
- Under "Version", choose **New version**
- Click **Deploy**
- **Important:** the web app URL stays the same, so your website keeps
  working with zero changes needed there

### 6. Test it
- Go to **shesthevibe.co** and sign up for the newsletter with a test email
  (use a different email than your own so you can see what subscribers see)
- Check the "Subscribers" tab in your sheet — the test email should appear
- Check the test inbox — the welcome email should arrive within a minute

---

## What the new code does (the short version)

- **Newsletter signup** → saved to sheet + welcome email sent automatically ✨ NEW
- **Contact form** → saved to sheet (no email — unchanged)
- **Book interest** → saved to sheet (no email — unchanged)
- If someone subscribes twice with the same email, they only get the
  welcome email the first time (no duplicates!)

## If something goes wrong

- **No email arrived?** Check the test email's spam folder first
- **Error in Apps Script?** Make sure you authorized Gmail in step 4
- **Website form broken?** The web app URL didn't change, so the site
  should work exactly as before — but let Talia know and she'll check it

---

*Subject line: "Practical. Pretty. You. — Welcome to the Vibe 💛"*
*Full email text: saved in your Google Drive as "STV Newsletter Welcome Email"*
