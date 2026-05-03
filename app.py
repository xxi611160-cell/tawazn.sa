import streamlit as st

st.title("نظام تقييم عدالة التوظيف (توازن AI)")

st.header("بيانات الوظيفة")
required_experience = st.number_input("عدد سنوات الخبرة المطلوبة", min_value=1, max_value=20, value=5)

def score_candidate(exp, match, lang, ach):
    score = 0
    score += min(exp / required_experience, 1) * 30
    score += 25 if match else 10
    lang_score = {"ضعيف": 5, "جيد": 12, "ممتاز": 20}
    score += lang_score[lang]
    score += ach * 5
    return round(score, 2)

st.header("أدخل المرشحين")

candidates = []

for i in range(3):
    st.subheader(f"مرشح {i+1}")
    name = st.text_input(f"اسم المرشح {i+1}", key=i)
    exp = st.number_input(f"الخبرة {i+1}", 0, 20, key=f"exp{i}")
    match = st.checkbox(f"خبرة مطابقة {i+1}", key=f"match{i}")
    lang = st.selectbox(f"اللغة {i+1}", ["ضعيف", "جيد", "ممتاز"], key=f"lang{i}")
    ach = st.slider(f"الإنجازات {i+1}", 0, 5, key=f"ach{i}")

    candidates.append({
        "name": name,
        "score": score_candidate(exp, match, lang, ach)
    })

if st.button("تحليل"):
    sorted_candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)

    st.subheader("النتائج")

    for c in sorted_candidates:
        st.write(f"{c['name']} - {c['score']}")

    best = sorted_candidates[0]
    selected = sorted_candidates[-1]

    st.write("------")
    st.success(f"الأفضل: {best['name']}")
    st.error(f"المختار: {selected['name']}")

    if selected["score"] < best["score"] * 0.8:
        st.warning("🚨 القرار مشبوه")
    else:
        st.success("✅ القرار منطقي")
