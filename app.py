import streamlit as st
import sqlite3

st.set_page_config(page_title="المنصة الوطنية", layout="wide")

# قاعدة بيانات
conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, name TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS candidates (job_id INTEGER, name TEXT, score REAL)")
conn.commit()

# Sidebar
st.sidebar.title("🏛️ المنصة")
page = st.sidebar.radio("القائمة", ["إضافة وظيفة", "إضافة مرشحين", "تحليل"])

# إضافة وظيفة
if page == "إضافة وظيفة":
    st.title("➕ إضافة وظيفة")

    job_name = st.text_input("اسم الوظيفة")

    if st.button("حفظ"):
        c.execute("INSERT INTO jobs (name) VALUES (?)", (job_name,))
        conn.commit()
        st.success("تم حفظ الوظيفة")

# إضافة مرشحين
elif page == "إضافة مرشحين":
    st.title("👥 إضافة مرشحين")

    jobs = c.execute("SELECT * FROM jobs").fetchall()

    job_dict = {job[1]: job[0] for job in jobs}

    selected_job = st.selectbox("اختر الوظيفة", list(job_dict.keys()))

    name = st.text_input("اسم المرشح")
    score = st.slider("التقييم", 0.0, 100.0)

    if st.button("إضافة"):
        c.execute("INSERT INTO candidates VALUES (?, ?, ?)", (job_dict[selected_job], name, score))
        conn.commit()
        st.success("تمت الإضافة")

# تحليل
elif page == "تحليل":
    st.title("⚖️ تحليل")

    jobs = c.execute("SELECT * FROM jobs").fetchall()
    job_dict = {job[1]: job[0] for job in jobs}

    selected_job = st.selectbox("اختر الوظيفة", list(job_dict.keys()))

    candidates = c.execute("SELECT name, score FROM candidates WHERE job_id=?", (job_dict[selected_job],)).fetchall()

    if candidates:
        sorted_c = sorted(candidates, key=lambda x: x[1], reverse=True)

        best = sorted_c[0]
        selected = sorted_c[-1]

        st.write("### المرشحين")
        for candi in sorted_c:
            st.write(f"{candi[0]} — {candi[1]}")

        st.success(f"الأفضل: {best[0]}")
        st.error(f"المختار: {selected[0]}")

        fairness = round((selected[1] / best[1]) * 100, 1)

        st.write(f"نسبة العدالة: {fairness}%")

        if fairness < 80:
            st.error("🚨 القرار غير عادل")
        else:
            st.success("✅ القرار مقبول")
    else:
        st.warning("ما فيه مرشحين")
