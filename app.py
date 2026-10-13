import os
import sqlite3
from datetime import datetime
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "responses.db"

st.set_page_config(
    page_title="A little note for you 💗",
    page_icon="💗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

def get_secret(name, default=""):
    try:
        value = st.secrets.get(name, default)
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name, default)

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                mood TEXT NOT NULL,
                message TEXT,
                contact_ok INTEGER NOT NULL DEFAULT 0
            )
        """)

def save_response(mood, message, contact_ok):
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            "INSERT INTO responses (created_at, mood, message, contact_ok) VALUES (?, ?, ?, ?)",
            (datetime.now().astimezone().isoformat(timespec="seconds"), mood, message.strip(), int(contact_ok)),
        )

def send_email_notification(mood, message):
    """Optional email alert; works only after SMTP settings are configured."""
    import smtplib
    from email.message import EmailMessage

    host = get_secret("SMTP_HOST")
    port = int(get_secret("SMTP_PORT", "587"))
    sender = get_secret("SMTP_SENDER")
    password = get_secret("SMTP_PASSWORD")
    recipient = get_secret("NOTIFY_EMAIL")
    if not all([host, sender, password, recipient]):
        return False, "Email notification isn't configured yet."
    msg = EmailMessage()
    msg["Subject"] = "A new response to your apology page 💌"
    msg["From"] = sender
    msg["To"] = recipient
    msg.set_content(
        f"New response: {mood}\n\nMessage:\n{message or '(No written message)'}\n\n"
        "This notification was sent because the visitor submitted the form."
    )
    try:
        with smtplib.SMTP(host, port, timeout=15) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        return True, "Email notification sent."
    except Exception as exc:
        return False, f"Email could not be sent: {exc}"

init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
:root { --pink:#ff6f9f; --rose:#b8426c; --ink:#593647; }
.stApp {
 background: radial-gradient(circle at 12% 8%, #fff4f7 0, transparent 34%),
             radial-gradient(circle at 92% 30%, #ffe1ec 0, transparent 36%),
             linear-gradient(160deg, #fff9fb, #ffeaf1 55%, #fff7fa);
 color:var(--ink); font-family:'DM Sans',sans-serif;
}
.block-container {max-width:760px;padding-top:1.2rem;padding-bottom:4rem;}
h1,h2,h3 {font-family:'Playfair Display',serif !important;color:#8f3458;}
.hero {text-align:center;padding:2rem 1.1rem;border:1px solid #ffd1e0;border-radius:28px;
 background:rgba(255,255,255,.78);box-shadow:0 16px 45px rgba(176,66,108,.10);}
.hero h1 {font-size:clamp(2.2rem,7vw,3.5rem);line-height:1.1;margin:.5rem 0;}
.hero p {font-size:1.03rem;line-height:1.8;max-width:560px;margin:.7rem auto;}
.eyebrow {letter-spacing:.15em;text-transform:uppercase;font-size:.72rem;font-weight:700;color:#c05b80;}
.section {margin:1rem 0;padding:1.3rem;border-radius:22px;background:rgba(255,255,255,.82);
 border:1px solid #ffdae6;box-shadow:0 8px 25px rgba(176,66,108,.06);}
.section p {line-height:1.85;font-size:1rem;}
.floaties {font-size:1.7rem;letter-spacing:.3rem;animation:bob 2.4s ease-in-out infinite;}
.heart {display:inline-block;animation:heartbeat 1.5s ease-in-out infinite;transform-origin:center;}
@keyframes heartbeat {0%,100%{transform:scale(1)}15%{transform:scale(1.18)}30%{transform:scale(1)}45%{transform:scale(1.1)}}
@keyframes bob {0%,100%{transform:translateY(0) rotate(-2deg)}50%{transform:translateY(-8px) rotate(2deg)}}
.stButton>button {border-radius:999px!important;border:1px solid #f4b3ca!important;background:#fff!important;
 color:#923c60!important;font-weight:700!important;min-height:2.9rem;padding:.5rem 1.1rem!important;}
.stButton>button:hover {background:#fff0f5!important;border-color:#e982a8!important;transform:translateY(-2px);}
div[data-testid="stForm"] {background:rgba(255,255,255,.76);padding:1rem;border:1px solid #ffdae6;border-radius:20px;}
footer,#MainMenu {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

components.html("""
<div style="position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden" aria-hidden="true">
 <div style="position:absolute;left:6%;top:18%;animation:drift 7s ease-in-out infinite;font-size:22px">💗</div>
 <div style="position:absolute;right:8%;top:42%;animation:drift 5s ease-in-out infinite 1s;font-size:18px">✨</div>
 <div style="position:absolute;left:10%;bottom:12%;animation:drift 6s ease-in-out infinite 2s;font-size:20px">🌷</div>
 <div style="position:absolute;right:12%;bottom:20%;animation:drift 8s ease-in-out infinite .5s;font-size:22px">💕</div>
</div>
<style>@keyframes drift{0%,100%{transform:translateY(0) rotate(-8deg)}50%{transform:translateY(-22px) rotate(10deg)}}</style>
""", height=0)

st.markdown("""
<div class="hero">
 <div class="floaties">🌷 💗 🦋 💗 🌷</div>
 <div class="eyebrow">a little corner of the internet, just for you</div>
 <h1>I'm sorry, my love <span class="heart">♡</span></h1>
 <p>I made this little page because you matter to me. Meri Pyariiiii DEVIII</p>
 <div style="font-size:1.8rem">🧸 💌 🌸</div>
</div>
""", unsafe_allow_html=True)

st.markdown(" ")
st.progress(0.12, text="A little journey, one gentle step at a time 💗")

# Interactive note cards
with st.expander("💌 Open the letter I wrote for you", expanded=True):
    st.markdown("""
    <div class="section">
    <h2>First, I'm genuinely sorry.</h2>
    <p>I'm sorry for hurting you. I know saying “sorry” doesn't magically undo what happened, and I don't expect a few sweet words to fix everything. Your feelings are real, and you deserved more care from me.</p>
    <p>I want to understand what hurt you instead of getting defensive or making excuses. I'm sorry for my part in making you feel this way.</p>
    </div>
    """, unsafe_allow_html=True)

with st.expander("🌧️ What I wish I could explain calmly"):
    st.markdown("""
    <div class="section">
    <p>You mean so much to me. I love the little things about you and the way ordinary moments can feel special when I share them with you.</p>
    <p>But love isn't just saying the right things when I'm afraid of losing you. It means listening, respecting you, and showing through my actions that I can do better.</p>
    </div>
    """, unsafe_allow_html=True)

with st.expander("🦋 You don't have to be okay right now"):
    st.markdown("""
    <div class="section">
    <p>You're allowed to be angry. You're allowed to need space. You don't owe me an instant reply, forgiveness, or reassurance.</p>
    <p>I made this to express my heart, not because I expect you to respond a certain way. If you need time, I'll respect that.</p>
    </div>
    """, unsafe_allow_html=True)

with st.expander("🐻 A tiny(very big) virtual hug"):
    st.markdown("""
    <div style="text-align:center;padding:1rem">
      <div style="font-size:4rem;animation:bob 2.4s ease-in-out infinite">🧸</div>
      <h3>Sending you a gentle hug</h3>
      <p>No pressure to hug back. Just a little reminder that you matter to me. 💗</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("✨ Sprinkle a little magic", use_container_width=True):
        st.balloons()
        st.toast("A tiny shower of love, just for you 💖")

st.markdown("""
<div class="section" style="text-align:center">
 <div class="floaties">🐻‍❄️ 💐 🐻‍❄️</div>
 <h2>One tiny promise</h2>
 <p>I can't promise to never make a mistake. I can promise to take your feelings seriously, own my actions, and work on the things that hurt you.</p>
 <p style="font-family:'Playfair Display',serif;font-size:1.25rem;color:#a33e67">I love you so much. I'm sorry. ♡</p>
</div>
""", unsafe_allow_html=True)

st.markdown("## 💗 Whenever you're ready")
st.write("If you want to, you can tell me how you're feeling. You can also close this page and take your time.")

with st.form("response_form", clear_on_submit=False):
    mood = st.radio(
        "Choose the answer that feels most honest for you:",
        [
            "Mai bahaut bura hu na",
            "Tum mujhe bahaut marogi",
            "Unblock karne jaa rahi",
            "Itne pyaar se manaoge to manungi hi na"
        ],
        index=0,
    )
    message = st.text_area(
        "Anything you'd like me to know? (optional)",
        placeholder="I miss you so so very muchhhh meri pyari pagal",
        max_chars=2000,
        height=130,
    )
    contact_ok = st.checkbox("It's okay for you to reply to me about this.")
    submitted = st.form_submit_button("Send my response 💌", use_container_width=True)

if submitted:
    save_response(mood, message, contact_ok)
    email_ok, email_status = send_email_notification(mood, message)
    st.success("Your response has been saved. Thank you for telling me honestly. 💗")
    if email_ok:
        st.caption("Your response was sent successfully.")
    else:
        st.caption("Your response was recorded. (Email alerts may not be configured.)")

st.caption("You can choose what feels right for you. No answer is required, and there's no pressure to forgive me right away. 💕")

# Private owner-only response viewer. Configure APOLOGY_ADMIN_PASSWORD in Streamlit secrets.
with st.expander("🔒 Private owner area"):
    st.caption("This area is for the site owner. Set APOLOGY_ADMIN_PASSWORD in Streamlit secrets before deploying.")
    admin_pass = st.text_input("Owner password", type="password", key="admin_password")
    expected = get_secret("APOLOGY_ADMIN_PASSWORD")
    if admin_pass and expected and admin_pass == expected:
        with sqlite3.connect(DB_PATH) as con:
            rows = con.execute(
                "SELECT created_at, mood, message, contact_ok FROM responses ORDER BY id DESC"
            ).fetchall()
        st.subheader("Responses")
        if rows:
            for created_at, response_mood, response_message, may_reply in rows:
                st.markdown(f"**{created_at}** · {response_mood}")
                st.write(response_message or "No written message.")
                st.caption("Permission to reply: " + ("Yes" if may_reply else "Not given"))
                st.divider()
            st.download_button(
                "Download responses as CSV",
                data="created_at,mood,message,contact_ok\n" + "\n".join(
                    '"' + str(a).replace('"','""') + '","' + str(b).replace('"','""') + '","' +
                    str(c or '').replace('"','""') + '",' + str(d)
                    for a,b,c,d in rows
                ),
                file_name="apology_responses.csv",
                mime="text/csv",
                use_container_width=True,
            )
        else:
            st.info("No responses yet.")
    elif admin_pass and not expected:
        st.warning("Owner password is not configured. Set APOLOGY_ADMIN_PASSWORD in .streamlit/secrets.toml or Streamlit Cloud Secrets.")
    elif admin_pass:
        st.error("That password doesn't match.")
