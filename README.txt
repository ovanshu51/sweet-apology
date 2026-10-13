SWEET APOLOGY — INTERACTIVE STREAMLIT APP

LOCAL RUN
1. Open this folder in IntelliJ.
2. In its terminal, run:
   python -m pip install -r requirements.txt
   python -m streamlit run app.py

WHAT'S INCLUDED
- Scrollable pastel romantic page with expandable letters
- Floating hearts, teddy bear section, confetti button
- A response form with honest choices and an optional written message
- Local SQLite storage for submitted responses
- Password-protected owner area to read/download responses
- Optional email alerts after SMTP settings are configured

IMPORTANT ABOUT RECEIVING RESPONSES
- Local run: responses are saved in responses.db in this folder.
- To view them: configure an owner password as described below, then open "Private owner area" on the website.
- Create .streamlit/secrets.toml by copying .streamlit/secrets.toml.example and changing the password.
- If deploying to Streamlit Community Cloud, add APOLOGY_ADMIN_PASSWORD in the app's Settings > Secrets.
- Streamlit Community Cloud's local filesystem is not a reliable permanent database. For a real public deployment, use a hosted database (for example Supabase) to make responses durable across restarts/redeploys. This sample is best for local testing or a temporary demo.
- Optional email alerts: fill SMTP settings in secrets.toml. For Gmail, use a Google App Password; never put your normal account password in this file or commit secrets.toml.
- Only submitted responses are saved; don't collect more personal information than needed.

CUSTOMIZE
Edit the wording in app.py so it sounds like you. Respect her choice to reply or take space.
