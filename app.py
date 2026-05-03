import streamlit as st

st.set_page_config(page_title="توازن AI", layout="wide")

st.title("🚀 نظام توازن AI - تحليل عدالة التوظيف")

# بيانات الوظيفة
st.header("📌 بيانات الوظيفة")
required_experience = st.number_input("سنوات الخبرة المطلوبة", 1, 20, 5)

# عدد المرشحين
num_candidates = st.number_input("عدد المرشحين", 2, 20, 3)

def score_candidate(exp, match, lang, ach):
    score = 0
    score += min(exp / required_experience, 1) * 30
    score += 25 if match else 10
    lang_score = {"ضعيف": 5, "جيد": 12, "ممتاز": 20}
    score += lang_score[lang]
    score += ach * 5
    return round(score, 2)

st.header("👥 إدخال المرشحين")

candidates = []

for i in range(int(num_candidates)):
    with st.expander(f"مرشح {i+1}", expanded=True):
        name = st.text_input("الاسم", key=f"name{i}")
        exp = st.number_input("سنوات الخبرة", 0, 20, key=f"exp{i}")
        match = st.checkbox("خبرة مطابقة", key=f"match{i}")
        lang = st.selectbox("مستوى اللغة", ["ضعيف", "جيد", "ممتاز"], key=f"lang{i}")
        ach = st.slider("عدد الإنجازات", 0, 5, key=f"ach{i}")

        score = score_candidate(exp, match, lang, ach)

        candidates.append({
            "name": name if name else f"مرشح {i+1}",
            "score": score
        })

# اختيار الموظف
st.header("🎯 اختيار القرار")
selected_name = st.selectbox(
    "من تم توظيفه؟",
    [c["name"] for c in candidates]
)

if st.button("📊 تحليل القرار"):
    sorted_candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)

    best = sorted_candidates[0]
    selected = next(c for c in candidates if c["name"] == selected_name)

    st.subheader("📈 النتائج")

    for c in sorted_candidates:
        st.write(f"{c['name']} — {c['score']}")

    st.divider()

    st.success(f"🏆 الأفضل: {best['name']} ({best['score']})")
    st.error(f"🎯 المختار: {selected['name']} ({selected['score']})")

    # حساب نسبة العدالة
    fairness = (selected["score"] / best["score"]) * 100
    fairness = round(fairness, 1)

    st.subheader("⚖️ تقييم العدالة")

    st.write(f"نسبة العدالة: **{fairness}%**")

    if fairness < 80:
        st.error("🚨 القرار غير عادل (فيه تلاعب محتمل)")
    elif fairness < 95:
        st.warning("⚠️ القرار مقبول لكن فيه فرق واضح")
    else:
        st.success("✅ القرار عادل")

    # بار مرئي
    st.progress(int(fairness))
