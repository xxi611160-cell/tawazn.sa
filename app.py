import streamlit as st
import sqlite3

st.set_page_config(page_title="المنصة الوطنية", layout="wide")

# 📦 قاعدة البيانات
conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    job_name TEXT,
    created_by TEXT
)
""")

conn.commit()

# 🔐 تسجيل الدخول
st.sidebar.title("🔐 تسجيل الدخول")

username = st.sidebar.text_input("اسم المستخدم")
password = st.sidebar.text_input("كلمة المرور", type="password")

login = st.sidebar.button("دخول")
register = st.sidebar.button("تسجيل")

if register:
    c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    conn.commit()
    st.sidebar.success("تم إنشاء الحساب")

if login:
    user = c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
    if user:
        st.session_state["user"] = username
    else:
        st.sidebar.error("خطأ في البيانات")

# 🧠 إذا مسجل دخول
if "user" in st.session_state:

    st.sidebar.success(f"مرحبًا {st.session_state['user']}")

    page = st.sidebar.radio("القائمة", [
        "الرئيسية",
        "إضافة وظيفة",
        "الوظائف"
    ])

    if page == "الرئيسية":
        st.title("🏛️ لوحة التحكم")
        st.info("نظام رقابي ذكي لتحليل عدالة التوظيف")

    elif page == "إضافة وظيفة":
        st.title("➕ إضافة وظيفة")

        job_name = st.text_input("اسم الوظيفة")

        if st.button("حفظ"):
            c.execute("INSERT INTO jobs VALUES (?, ?)", (job_name, st.session_state["user"]))
            conn.commit()
            st.success("تم حفظ الوظيفة")

    elif page == "الوظائف":
        st.title("📋 الوظائف")

        jobs = c.execute("SELECT * FROM jobs").fetchall()

        for job in jobs:
            st.markdown(f"### {job[0]}")
            st.write(f"بواسطة: {job[1]}")

else:
    st.title("🏛️ المنصة الوطنية")
    st.warning("الرجاء تسجيل الدخول")
