
import json
from datetime import datetime
import numpy as np
import pandas as pd
import streamlit as st
from supabase import create_client
from google import genai

st.set_page_config(page_title="CareerFit AI", page_icon="🧭", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
#MainMenu,footer,header{visibility:hidden}
.block-container{max-width:1180px;padding-top:1.4rem;padding-bottom:4rem}
.hero{background:linear-gradient(135deg,#0f1f3d,#1a2f56);color:#fff;padding:3rem;border-radius:24px;margin-bottom:1.4rem}
.hero h1{font-size:3rem;line-height:1.06;margin:.5rem 0 1rem;white-space:pre-line}.hero p{color:#d9e0eb;font-size:1.08rem;max-width:780px}
.eyebrow{text-transform:uppercase;letter-spacing:.12em;font-size:.76rem;color:#d8bf86;font-weight:700}
.card,.role-card{background:#fff;border:1px solid #e5e7eb;border-radius:20px;padding:1.2rem;box-shadow:0 8px 28px rgba(15,31,61,.06)}
.soft-card{background:#f5f6f8;border-radius:18px;padding:1.1rem;height:100%}
.gold-card{background:#f6f0e3;border:1px solid #eadbb8;border-radius:18px;padding:1.2rem}
.badge{display:inline-block;background:#eef2f7;color:#26364f;border-radius:999px;padding:.35rem .65rem;margin:.15rem .2rem .15rem 0;font-size:.83rem;font-weight:600}
.gold-badge{background:#f6f0e3;color:#7b612c}.muted{color:#667085}.brand{font-size:1.35rem;font-weight:800;color:#0f1f3d}
.score{font-size:1.6rem;font-weight:800;color:#b89a5b}
div.stButton>button{border-radius:12px;border:none;background:#0f1f3d;color:#fff;font-weight:700}
div.stButton>button:hover{background:#1b3159;color:#fff}
</style>
""", unsafe_allow_html=True)

LANGS={"English":"en","中文":"zh","Bahasa Melayu":"ms"}
TXT={
"en":{"proto":"Career OS prototype · Talentbank Tech Hackathon 2026","hero":"Know where you fit.\nSee where you can go.","body":"CareerFit AI converts personal strengths, career interests, skills and readiness into explainable career pathways, actionable development plans and organisation-level talent insights.","cand":"Candidate Portal","org":"Organisation Portal","enter_c":"Enter Candidate Portal","enter_o":"Enter Organisation Portal","back":"← Back to Home","assess":"Assessment","load":"Load Existing Profile","profile":"Career Profile","paths":"Career Pathways","plan":"Skill Plan","report":"Career Report","name":"Full name","email":"Email","uni":"University","major":"Major / field of study","year":"Graduation year","gen":"Generate and Save My Career Profile","saved":"Profile saved to the CareerFit database.","invalid":"Enter a valid name and email.","load_btn":"Load My Career Profile","not_found":"No saved profile was found for this email.","loaded":"Saved profile loaded.","complete":"Complete the assessment or load an existing profile.","identity":"Career Identity","ready":"Career Readiness","top":"Top Match","fit":"Top Fit","strengths":"Core Strengths","gaps":"Priority Skill Gaps","action":"90-Day Action Plan","org_code":"Organisation access code","org_hint":"Enter the organisation access code to view candidate and cohort data.","no_records":"No candidate records are available yet.","emp":"Employer View","univ":"University View","pool":"Talent Pool","jobready":"Job-ready","developing":"Developing","intervention":"Require intervention","matches":"Candidate Matches","records":"Candidate Records","avg":"Average Readiness","share":"Job-ready Share","common":"Most Common Path","dist":"Career Path Distribution","common_gaps":"Most Common Skill Gaps","demo":"Create Demo Candidate","lang":"Language"},
"zh":{"proto":"职业操作系统原型 · Talentbank 技术黑客马拉松 2026","hero":"了解你适合哪里。\n看见你可以走向哪里。","body":"CareerFit AI 将个人优势、职业兴趣、技能和职业准备度转化为可解释的职业路径、行动计划和组织端人才洞察。","cand":"候选人端口","org":"组织端口","enter_c":"进入候选人端口","enter_o":"进入组织端口","back":"← 返回首页","assess":"测评","load":"加载已有档案","profile":"职业画像","paths":"职业路径","plan":"技能计划","report":"职业报告","name":"姓名","email":"邮箱","uni":"大学","major":"专业 / 研究领域","year":"毕业年份","gen":"生成并保存我的职业画像","saved":"职业画像已保存到 CareerFit 数据库。","invalid":"请输入有效姓名和邮箱。","load_btn":"加载我的职业画像","not_found":"未找到该邮箱对应的职业档案。","loaded":"已加载保存的职业档案。","complete":"请先完成测评或加载已有档案。","identity":"职业身份","ready":"职业准备度","top":"最佳匹配","fit":"最高匹配度","strengths":"核心优势","gaps":"优先技能缺口","action":"90天行动计划","org_code":"组织端访问码","org_hint":"请输入组织端访问码以查看候选人与群体数据。","no_records":"目前还没有候选人记录。","emp":"雇主视图","univ":"高校视图","pool":"人才池","jobready":"可就业","developing":"发展中","intervention":"需要干预","matches":"候选人匹配","records":"候选人记录","avg":"平均准备度","share":"可就业比例","common":"最常见路径","dist":"职业路径分布","common_gaps":"最常见技能缺口","demo":"创建模拟候选人","lang":"语言"},
"ms":{"proto":"Prototaip Career OS · Talentbank Tech Hackathon 2026","hero":"Ketahui kesesuaian anda.\nLihat hala tuju kerjaya anda.","body":"CareerFit AI menukar kekuatan kerja, minat kerjaya, kemahiran dan kesediaan kerjaya kepada laluan kerjaya yang boleh dijelaskan, pelan tindakan dan cerapan bakat organisasi.","cand":"Portal Calon","org":"Portal Organisasi","enter_c":"Masuk Portal Calon","enter_o":"Masuk Portal Organisasi","back":"← Kembali ke Laman Utama","assess":"Penilaian","load":"Muat Profil Sedia Ada","profile":"Profil Kerjaya","paths":"Laluan Kerjaya","plan":"Pelan Kemahiran","report":"Laporan Kerjaya","name":"Nama penuh","email":"Emel","uni":"Universiti","major":"Bidang pengajian","year":"Tahun graduasi","gen":"Jana dan Simpan Profil Kerjaya Saya","saved":"Profil telah disimpan ke pangkalan data CareerFit.","invalid":"Masukkan nama dan emel yang sah.","load_btn":"Muat Profil Kerjaya Saya","not_found":"Tiada profil tersimpan ditemui untuk emel ini.","loaded":"Profil tersimpan telah dimuat.","complete":"Lengkapkan penilaian atau muat profil sedia ada.","identity":"Identiti Kerjaya","ready":"Kesediaan Kerjaya","top":"Padanan Terbaik","fit":"Skor Padanan","strengths":"Kekuatan Teras","gaps":"Jurang Kemahiran Utama","action":"Pelan Tindakan 90 Hari","org_code":"Kod akses organisasi","org_hint":"Masukkan kod akses organisasi untuk melihat data calon dan kohort.","no_records":"Tiada rekod calon tersedia.","emp":"Paparan Majikan","univ":"Paparan Universiti","pool":"Kumpulan Bakat","jobready":"Sedia Kerja","developing":"Sedang Membangun","intervention":"Perlu Intervensi","matches":"Padanan Calon","records":"Rekod Calon","avg":"Purata Kesediaan","share":"Peratus Sedia Kerja","common":"Laluan Paling Lazim","dist":"Taburan Laluan Kerjaya","common_gaps":"Jurang Kemahiran Lazim","demo":"Cipta Calon Demo","lang":"Bahasa"}}
if "lang" not in st.session_state: st.session_state.lang="en"
def tr(k): return TXT[st.session_state.lang].get(k,TXT["en"].get(k,k))


QUESTION_TEXT = {
    "en": {
        "core_strengths_section": "Work Strengths",
        "interests_section": "Career Interests",
        "skills_section": "Current Skills",
        "values_readiness_section": "Work Values and Career Readiness",
        "analyse": "I enjoy analysing complex information.",
        "plan": "I prefer turning ideas into structured plans.",
        "people": "I gain energy from working with people.",
        "create": "I enjoy creating new solutions.",
        "uncertain": "I stay calm when decisions are uncertain.",
        "data_interest": "Analysing data and solving problems",
        "help": "Helping, teaching or supporting people",
        "lead": "Leading initiatives and influencing decisions",
        "creative": "Creating content, designs or new ideas",
        "organise": "Organising processes and managing details",
        "comm": "Communication",
        "data_skill": "Data analysis",
        "problem": "Problem solving",
        "present": "Presentation",
        "digital": "Digital tools",
        "write": "Writing",
        "coord": "Project coordination",
        "research": "Research",
        "growth": "Growth",
        "stability": "Stability",
        "income": "Income",
        "impact": "Impact",
        "autonomy": "Autonomy",
        "leadership": "Leadership",
        "resume": "Resume readiness",
        "interview": "Interview confidence",
        "portfolio": "Portfolio evidence",
        "clarity": "Role clarity",
        "search": "Job-search consistency",
    },
    "zh": {
        "core_strengths_section": "工作优势",
        "interests_section": "职业兴趣",
        "skills_section": "当前技能",
        "values_readiness_section": "工作价值观与职业准备度",
        "analyse": "我喜欢分析复杂信息。",
        "plan": "我倾向于把想法转化为结构化计划。",
        "people": "我从与他人合作中获得动力。",
        "create": "我喜欢创造新的解决方案。",
        "uncertain": "在不确定的情况下，我仍能保持冷静。",
        "data_interest": "分析数据并解决问题",
        "help": "帮助、教学或支持他人",
        "lead": "领导项目并影响决策",
        "creative": "创作内容、设计或新想法",
        "organise": "组织流程并管理细节",
        "comm": "沟通能力",
        "data_skill": "数据分析",
        "problem": "问题解决",
        "present": "展示表达",
        "digital": "数字工具",
        "write": "写作能力",
        "coord": "项目协调",
        "research": "研究能力",
        "growth": "成长",
        "stability": "稳定性",
        "income": "收入",
        "impact": "影响力",
        "autonomy": "自主性",
        "leadership": "领导力",
        "resume": "简历准备度",
        "interview": "面试信心",
        "portfolio": "作品集证据",
        "clarity": "岗位清晰度",
        "search": "求职持续性",
    },
    "ms": {
        "core_strengths_section": "Kekuatan Kerja",
        "interests_section": "Minat Kerjaya",
        "skills_section": "Kemahiran Semasa",
        "values_readiness_section": "Nilai Kerja dan Kesediaan Kerjaya",
        "analyse": "Saya suka menganalisis maklumat yang kompleks.",
        "plan": "Saya lebih suka menukar idea kepada pelan yang berstruktur.",
        "people": "Saya mendapat tenaga daripada bekerja dengan orang lain.",
        "create": "Saya suka mencipta penyelesaian baharu.",
        "uncertain": "Saya kekal tenang apabila keputusan tidak pasti.",
        "data_interest": "Menganalisis data dan menyelesaikan masalah",
        "help": "Membantu, mengajar atau menyokong orang lain",
        "lead": "Memimpin inisiatif dan mempengaruhi keputusan",
        "creative": "Mencipta kandungan, reka bentuk atau idea baharu",
        "organise": "Mengatur proses dan mengurus perincian",
        "comm": "Komunikasi",
        "data_skill": "Analisis data",
        "problem": "Penyelesaian masalah",
        "present": "Pembentangan",
        "digital": "Alat digital",
        "write": "Penulisan",
        "coord": "Koordinasi projek",
        "research": "Penyelidikan",
        "growth": "Pertumbuhan",
        "stability": "Kestabilan",
        "income": "Pendapatan",
        "impact": "Impak",
        "autonomy": "Autonomi",
        "leadership": "Kepimpinan",
        "resume": "Kesediaan resume",
        "interview": "Keyakinan temu duga",
        "portfolio": "Bukti portfolio",
        "clarity": "Kejelasan peranan",
        "search": "Konsistensi pencarian kerja",
    },
}

def qtr(key: str) -> str:
    return QUESTION_TEXT.get(st.session_state.lang, QUESTION_TEXT["en"]).get(key, QUESTION_TEXT["en"].get(key, key))


ROLES={
"Business Analyst":{"salary":"RM 3,500–5,500 / month","time":"4–6 months","w":{"a":.25,"s":.20,"c":.15,"d":.20,"e":.10,"r":.10},"g":["SQL","Dashboard storytelling","Business requirements"],"n":"Build a small business dashboard and explain the problem, metric and recommendation."},
"Data Analyst":{"salary":"RM 3,200–5,000 / month","time":"5–7 months","w":{"a":.30,"s":.15,"c":.08,"d":.30,"e":.05,"r":.12},"g":["SQL","Python","Portfolio evidence"],"n":"Complete one public-data project and present three actionable findings."},
"Product Operations Associate":{"salary":"RM 3,500–5,200 / month","time":"3–5 months","w":{"a":.12,"s":.25,"c":.22,"d":.10,"e":.18,"r":.13},"g":["Product metrics","Process mapping","Cross-functional execution"],"n":"Map one product workflow and define three operational KPIs."},
"UX Research Assistant":{"salary":"RM 3,200–4,800 / month","time":"4–6 months","w":{"a":.18,"s":.10,"c":.25,"d":.08,"e":.14,"r":.25},"g":["Interview synthesis","Journey mapping","Portfolio case study"],"n":"Interview five users and convert findings into a journey map."}}


FEATURED_JOBS = [
    {
        "tag": "🔥 High-Demand",
        "role": "Data Analyst",
        "company": "FinTech Growth Lab",
        "location": "Kuala Lumpur",
        "salary": "RM 3,500–5,200 / month",
        "urgency": "24 openings",
        "match": "Strong fit for analytical profiles",
        "skills": ["SQL", "Excel", "Dashboarding"]
    },
    {
        "tag": "🔥 High-Demand",
        "role": "Business Analyst",
        "company": "Regional Consulting Partner",
        "location": "Selangor",
        "salary": "RM 3,800–5,800 / month",
        "urgency": "18 openings",
        "match": "Strong fit for structured problem-solvers",
        "skills": ["Requirements analysis", "Communication", "Power BI"]
    },
    {
        "tag": "⚡ Urgently Hiring",
        "role": "Product Operations Associate",
        "company": "Digital Platform Startup",
        "location": "Hybrid · Malaysia",
        "salary": "RM 3,300–5,000 / month",
        "urgency": "Interviewing this week",
        "match": "Good fit for organised and execution-oriented candidates",
        "skills": ["Process mapping", "Metrics", "Coordination"]
    },
    {
        "tag": "⚡ Urgently Hiring",
        "role": "Graduate Talent Associate",
        "company": "Employer Branding Agency",
        "location": "Petaling Jaya",
        "salary": "RM 3,000–4,500 / month",
        "urgency": "Immediate intake",
        "match": "Good fit for people-centred profiles",
        "skills": ["Communication", "Event support", "Candidate engagement"]
    },
]

def featured_jobs_section(title: str = "Featured Opportunities"):
    st.markdown(f"### {title}")
    st.caption("Simulated job advertising area for the hackathon prototype. In production, this area can connect to Talentbank job listings or employer campaigns.")
    cols = st.columns(2)
    for i, job in enumerate(FEATURED_JOBS):
        with cols[i % 2]:
            st.markdown(
                f"""
<div class="role-card" style="margin-bottom:1rem">
    <div class="eyebrow" style="color:#8a6b2f">{job['tag']}</div>
    <h3 style="margin-bottom:.2rem">{job['role']}</h3>
    <p class="muted">{job['company']} · {job['location']}</p>
    <p><b>{job['salary']}</b></p>
    <p><b>Status:</b> {job['urgency']}</p>
    <p><b>Why shown:</b> {job['match']}</p>
    <p><b>Key skills:</b> {", ".join(job['skills'])}</p>
</div>
""",
                unsafe_allow_html=True,
            )



def fallback_ai_style_explanation(profile, candidate):
    ranked_roles = profile.get("ranked", [])
    top_role = ranked_roles[0][0] if ranked_roles else "the recommended role"
    top_score = ranked_roles[0][1] if ranked_roles else 0
    strengths = ", ".join(profile.get("strengths", []))
    gaps = ", ".join(profile.get("gaps", []))

    return f"""
**1. Career identity explanation**

{candidate.get("name", "This candidate")} is identified as an **{profile.get("identity", "Adaptive Problem Solver")}**. This suggests a profile with visible strengths in structured thinking, problem solving, and career-oriented self-development.

**2. Why the top role fits**

The strongest current match is **{top_role}** with a fit score of **{top_score}%**. This indicates that the candidate's current strengths and interests align reasonably well with the requirements of this pathway, especially in areas such as {strengths}.

**3. Main skill gaps**

The main development priorities are **{gaps}**. These gaps do not mean the candidate is unsuitable. They indicate where focused preparation would make the profile more competitive.

**4. 30-day next step**

In the next 30 days, the candidate should complete one small portfolio task related to **{top_role}**, document the process, and prepare a short explanation of the problem, method, and result.

*Note: Gemini API quota was unavailable, so this explanation was generated using the built-in fallback explanation layer.*
"""

def generate_ai_explanation(profile, candidate):
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
        if not api_key:
            return fallback_ai_style_explanation(profile, candidate)

        client = genai.Client(api_key=api_key)

        ranked_roles = profile.get("ranked", [])
        role_text = ", ".join([f"{role} ({score}% fit)" for role, score in ranked_roles])

        prompt = f"""
You are a professional graduate career advisor.

Write a concise, practical career explanation for the candidate below.
Do not invent qualifications. Use only the provided data.
Do not make deterministic claims. Use careful wording such as "suggests", "indicates", and "may fit".

Candidate:
Name: {candidate.get("name", "")}
University: {candidate.get("university", "")}
Major: {candidate.get("major", "")}
Career identity: {profile.get("identity", "")}
Career readiness score: {profile.get("readiness", "")}/100
Top role matches: {role_text}
Core strengths: {", ".join(profile.get("strengths", []))}
Priority skill gaps: {", ".join(profile.get("gaps", []))}

Output structure:
1. Career identity explanation
2. Why the top role fits
3. Main skill gaps
4. 30-day next step

Keep it under 180 words.
Use clear English.
"""

        models_to_try = [
            "gemini-3-flash-preview",
            "gemini-2.5-flash",
            "gemini-2.0-flash",
        ]

        last_error = None
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                if response and response.text:
                    return response.text
            except Exception as model_error:
                last_error = model_error
                continue

        return fallback_ai_style_explanation(profile, candidate)

    except Exception:
        return fallback_ai_style_explanation(profile, candidate)


def db():
    try: return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    except Exception: return None
DB=db()
def nav():
    c1,c2=st.columns([3,1])
    with c1:
        st.markdown(f'<div class="brand">🧭 CareerFit AI</div><div class="muted">{tr("proto")}</div>',unsafe_allow_html=True)
    with c2:
        choice=st.selectbox(tr("lang"),list(LANGS.keys()),index=list(LANGS.values()).index(st.session_state.lang))
        st.session_state.lang=LANGS[choice]
def go(v): st.session_state.view=v; st.rerun()
def m(vals): return float(np.mean(vals)/5*100)
def calc(ans):
    dims={"a":m([ans["str"]["analyse"],ans["int"]["data"],ans["skill"]["problem"],ans["skill"]["research"]]),"s":m([ans["str"]["plan"],ans["int"]["organise"],ans["skill"]["coord"]]),"c":m([ans["str"]["people"],ans["int"]["help"],ans["skill"]["comm"],ans["skill"]["present"],ans["skill"]["write"]]),"d":m([ans["int"]["data"],ans["skill"]["data"],ans["skill"]["digital"],ans["skill"]["research"]]),"e":m([ans["int"]["lead"],ans["val"]["leadership"],ans["val"]["autonomy"],ans["str"]["create"]]),"r":m(list(ans["ready"].values()))}
    scores={role:int(round(min(97,max(55,sum(dims[k]*w for k,w in info["w"].items()))))) for role,info in ROLES.items()}
    ranked=sorted(scores.items(),key=lambda x:x[1],reverse=True)[:3]
    identity="Analytical Strategist" if dims["a"]>=78 and dims["s"]>=68 else "Evidence-Driven Explorer" if dims["d"]>=78 else "Adaptive Problem Solver"
    strengths=["Problem solving","Communication","Research","Data analysis"]
    gaps=list(dict.fromkeys(ROLES[ranked[0][0]]["g"]+["Portfolio evidence"]))[:5]
    roadmap=[{"period":"Week 1–2","title":"Clarify target role","action":f"Review 10 {ranked[0][0]} vacancies."},{"period":"Week 3–5","title":"Close priority gap","action":f"Develop {gaps[0]} with one applied exercise."},{"period":"Week 6–8","title":"Create portfolio evidence","action":ROLES[ranked[0][0]]["n"]},{"period":"Week 9–12","title":"Apply and prepare","action":"Apply to 20 aligned roles and prepare six STAR stories."}]
    return {"identity":identity,"readiness":int(round(dims["r"])),"ranked":ranked,"strengths":strengths,"gaps":gaps,"roadmap":roadmap,"dims":dims}
def save(prof,ans):
    if DB is None: return False,"Database connection is not available."
    r=prof["ranked"]; c=st.session_state.candidate
    rec={"name":c["name"],"email":c["email"].lower(),"university":c["university"],"major":c["major"],"graduation_year":int(c["year"]),"career_identity":prof["identity"],"readiness_score":prof["readiness"],"top_role":r[0][0],"top_role_score":r[0][1],"second_role":r[1][0],"second_role_score":r[1][1],"third_role":r[2][0],"third_role_score":r[2][1],"strengths":{"items":prof["strengths"],"dimensions":prof["dims"]},"interests":ans["int"],"skills":ans["skill"],"work_values":ans["val"],"readiness_answers":ans["ready"],"skill_gaps":prof["gaps"],"roadmap":prof["roadmap"],"updated_at":datetime.utcnow().isoformat()}
    try: DB.table("candidates").upsert(rec,on_conflict="email").execute(); return True,tr("saved")
    except Exception as e: return False,f"Database save failed: {e}"
def load(email):
    if DB is None: return None
    try:
        res=DB.table("candidates").select("*").eq("email",email.lower().strip()).limit(1).execute()
        return res.data[0] if res.data else None
    except Exception: return None
def allc():
    if DB is None: return pd.DataFrame()
    try: return pd.DataFrame(DB.table("candidates").select("*").order("updated_at",desc=True).execute().data or [])
    except Exception: return pd.DataFrame()

if "view" not in st.session_state: st.session_state.view="home"
if "candidate" not in st.session_state: st.session_state.candidate={"name":"","email":"","university":"","major":"","year":2026}
if "profile" not in st.session_state: st.session_state.profile=None
if "record" not in st.session_state: st.session_state.record=None

def demo():
    st.session_state.candidate={"name":"Chen Test","email":"chentest2026@example.com","university":"Universiti Pendidikan Sultan Idris","major":"Business Analytics","year":2026}
    ans={"str":{"analyse":5,"plan":4,"people":3,"create":4,"uncertain":3},"int":{"data":5,"help":3,"lead":4,"creative":3,"organise":4},"skill":{"comm":4,"data":4,"problem":5,"present":3,"digital":4,"write":4,"coord":3,"research":4},"val":{"growth":5,"stability":3,"income":4,"impact":4,"autonomy":4,"leadership":3},"ready":{"resume":4,"interview":3,"portfolio":2,"clarity":4,"search":3}}
    prof=calc(ans); st.session_state.profile=prof; return save(prof,ans)

def home():
    nav()
    st.markdown(f'<div class="hero"><div class="eyebrow">{tr("cand")} / {tr("org")}</div><h1>{tr("hero")}</h1><p>{tr("body")}</p></div>',unsafe_allow_html=True)
    featured_jobs_section("Featured Opportunities: High-Demand and Urgently Hiring Roles")
    st.divider()
    c1,c2=st.columns(2)
    with c1:
        st.markdown(f'<div class="card"><h3>{tr("cand")}</h3><p class="muted">{TXT[st.session_state.lang]["candidate_card_body"] if "candidate_card_body" in TXT[st.session_state.lang] else ""}</p></div>',unsafe_allow_html=True)
        if st.button(tr("enter_c"),use_container_width=True): go("candidate")
    with c2:
        st.markdown(f'<div class="card"><h3>{tr("org")}</h3><p class="muted">{TXT[st.session_state.lang]["org_card_body"] if "org_card_body" in TXT[st.session_state.lang] else ""}</p></div>',unsafe_allow_html=True)
        if st.button(tr("enter_o"),use_container_width=True): go("org")
def candidate():
    nav()
    if st.button(tr("back")): go("home")
    st.markdown(f"## {tr('cand')}")
    tabs=st.tabs([tr("assess"),tr("load"),tr("profile"),tr("paths"),"Featured Jobs",tr("plan"),tr("report")])
    with tabs[0]:
        if st.button(tr("demo"),use_container_width=True):
            ok,msg=demo()
            if ok:
                st.success(msg)
            else:
                st.warning(msg)
        st.divider()
        with st.form("f"):
            c1,c2=st.columns(2)
            with c1:
                name=st.text_input(tr("name"),st.session_state.candidate["name"]); email=st.text_input(tr("email"),st.session_state.candidate["email"]); uni=st.text_input(tr("uni"),st.session_state.candidate["university"])
            with c2:
                major=st.text_input(tr("major"),st.session_state.candidate["major"]); year=st.number_input(tr("year"),2020,2035,int(st.session_state.candidate["year"]))
            st.markdown(f"#### {qtr('core_strengths_section')}")
            s1=st.slider(qtr("analyse"),1,5,4); s2=st.slider(qtr("plan"),1,5,4); s3=st.slider(qtr("people"),1,5,3); s4=st.slider(qtr("create"),1,5,4); s5=st.slider(qtr("uncertain"),1,5,3)
            st.markdown(f"#### {qtr('interests_section')}")
            i1=st.slider(qtr("data_interest"),1,5,5); i2=st.slider(qtr("help"),1,5,3); i3=st.slider(qtr("lead"),1,5,4); i4=st.slider(qtr("creative"),1,5,3); i5=st.slider(qtr("organise"),1,5,4)
            st.markdown(f"#### {qtr('skills_section')}")
            k1=st.slider(qtr("comm"),1,5,4); k2=st.slider(qtr("data_skill"),1,5,3); k3=st.slider(qtr("problem"),1,5,4); k4=st.slider(qtr("present"),1,5,3); k5=st.slider(qtr("digital"),1,5,3); k6=st.slider(qtr("write"),1,5,4); k7=st.slider(qtr("coord"),1,5,3); k8=st.slider(qtr("research"),1,5,4)
            st.markdown(f"#### {qtr('values_readiness_section')}")
            v1=st.slider(qtr("growth"),1,5,5); v2=st.slider(qtr("stability"),1,5,3); v3=st.slider(qtr("income"),1,5,4); v4=st.slider(qtr("impact"),1,5,4); v5=st.slider(qtr("autonomy"),1,5,4); v6=st.slider(qtr("leadership"),1,5,3)
            r1=st.slider(qtr("resume"),1,5,3); r2=st.slider(qtr("interview"),1,5,3); r3=st.slider(qtr("portfolio"),1,5,2); r4=st.slider(qtr("clarity"),1,5,4); r5=st.slider(qtr("search"),1,5,3)
            sub=st.form_submit_button(tr("gen"),use_container_width=True)
        if sub:
            if not name or "@" not in email: st.error(tr("invalid")); return
            st.session_state.candidate={"name":name,"email":email,"university":uni,"major":major,"year":year}
            ans={"str":{"analyse":s1,"plan":s2,"people":s3,"create":s4,"uncertain":s5},"int":{"data":i1,"help":i2,"lead":i3,"creative":i4,"organise":i5},"skill":{"comm":k1,"data":k2,"problem":k3,"present":k4,"digital":k5,"write":k6,"coord":k7,"research":k8},"val":{"growth":v1,"stability":v2,"income":v3,"impact":v4,"autonomy":v5,"leadership":v6},"ready":{"resume":r1,"interview":r2,"portfolio":r3,"clarity":r4,"search":r5}}
            prof=calc(ans)
            st.session_state.profile=prof
            ok,msg=save(prof,ans)
            if ok:
                st.success(msg)
            else:
                st.warning(msg)
    with tabs[1]:
        em=st.text_input(tr("email"),key="load_email")
        if st.button(tr("load_btn")):
            rec=load(em); st.session_state.record=rec
            if rec:
                st.success(tr("loaded"))
            else:
                st.error(tr("not_found"))
    with tabs[2]:
        prof=st.session_state.profile; rec=st.session_state.record
        if not prof and not rec: st.info(tr("complete")); return
        if prof:
            r=prof["ranked"]; c1,c2,c3,c4=st.columns(4); c1.metric(tr("identity"),prof["identity"]); c2.metric(tr("ready"),f'{prof["readiness"]}/100'); c3.metric(tr("top"),r[0][0]); c4.metric(tr("fit"),f'{r[0][1]}%')
            st.markdown("".join(f'<span class="badge">{x}</span>' for x in prof["strengths"]),unsafe_allow_html=True)
        else:
            c1,c2,c3,c4=st.columns(4); c1.metric(tr("identity"),rec.get("career_identity")); c2.metric(tr("ready"),f'{rec.get("readiness_score")}/100'); c3.metric(tr("top"),rec.get("top_role")); c4.metric(tr("fit"),f'{int(rec.get("top_role_score") or 0)}%')

        if prof:
            st.divider()
            st.markdown("### AI Career Explanation")
            st.caption("Gemini is used as an optional explanation layer. If API quota is unavailable, a built-in fallback explanation is shown. Role-fit scoring remains rule-based and transparent.")
            if st.button("Generate AI Career Explanation", use_container_width=True):
                ai_text = generate_ai_explanation(st.session_state.profile, st.session_state.candidate)
                st.markdown(ai_text)
    with tabs[3]:
        prof=st.session_state.profile; rec=st.session_state.record
        ranked=prof["ranked"] if prof else ([(rec.get("top_role"),int(rec.get("top_role_score") or 0)),(rec.get("second_role"),int(rec.get("second_role_score") or 0)),(rec.get("third_role"),int(rec.get("third_role_score") or 0))] if rec else [])
        if not ranked: st.info(tr("complete")); return
        for role,score in ranked:
            info=ROLES.get(role,{})
            st.markdown(f'<div class="role-card" style="margin-bottom:1rem"><h3>{role} <span class="score">{score}%</span></h3><p class="muted">{info.get("salary","")} · {info.get("time","")}</p><p><b>{tr("gaps")}:</b> {", ".join(info.get("g",[]))}</p><p><b>Next:</b> {info.get("n","")}</p></div>',unsafe_allow_html=True)
    with tabs[4]:
        featured_jobs_section("Featured Jobs: High-Demand and Urgently Hiring Roles")
    with tabs[5]:
        prof=st.session_state.profile; rec=st.session_state.record
        roadmap=prof["roadmap"] if prof else (rec.get("roadmap",[]) if rec else [])
        if not roadmap: st.info(tr("complete")); return
        for item in roadmap:
            st.markdown(f'<div class="soft-card" style="margin-bottom:.75rem"><div class="eyebrow" style="color:#8a6b2f">{item["period"]}</div><h4>{item["title"]}</h4><p class="muted">{item["action"]}</p></div>',unsafe_allow_html=True)
    with tabs[6]:
        prof=st.session_state.profile
        rec=st.session_state.record

        if not prof and not rec:
            st.info(tr("complete"))
            return

        st.markdown("### CareerFit AI Career Report")

        if prof:
            ranked=prof["ranked"]
            identity=prof["identity"]
            readiness=prof["readiness"]
            strengths=prof["strengths"]
            gaps=prof["gaps"]
            roadmap=prof["roadmap"]
        else:
            ranked=[
                (rec.get("top_role"), int(rec.get("top_role_score") or 0)),
                (rec.get("second_role"), int(rec.get("second_role_score") or 0)),
                (rec.get("third_role"), int(rec.get("third_role_score") or 0)),
            ]
            identity=rec.get("career_identity","—")
            readiness=rec.get("readiness_score",0)
            strengths_data=rec.get("strengths") or {}
            strengths=strengths_data.get("items",[]) if isinstance(strengths_data,dict) else []
            gaps=rec.get("skill_gaps") or []
            roadmap=rec.get("roadmap") or []

        candidate=st.session_state.candidate
        top_role=ranked[0][0] if ranked else "—"
        top_score=ranked[0][1] if ranked else 0

        c1,c2,c3=st.columns(3)
        c1.metric("Career Identity", identity)
        c2.metric("Readiness Score", f"{readiness}/100")
        c3.metric("Top Role", f"{top_role} ({top_score}%)")

        st.markdown("#### Candidate Information")
        info_df=pd.DataFrame([
            {"Field":"Name","Value":candidate.get("name","—")},
            {"Field":"Email","Value":candidate.get("email","—")},
            {"Field":"University","Value":candidate.get("university","—")},
            {"Field":"Major / Field","Value":candidate.get("major","—")},
            {"Field":"Graduation Year","Value":candidate.get("year","—")},
        ])
        st.dataframe(info_df, hide_index=True, use_container_width=True)

        st.markdown("#### Top Career Matches")
        role_df=pd.DataFrame([
            {"Rank":i+1,"Role":role,"Fit Score":f"{score}%","Estimated Preparation":ROLES.get(role,{}).get("time","—"),"Indicative Salary":ROLES.get(role,{}).get("salary","—")}
            for i,(role,score) in enumerate(ranked) if role
        ])
        st.dataframe(role_df, hide_index=True, use_container_width=True)

        st.markdown("#### Core Strengths")
        st.markdown("".join(f'<span class="badge">{x}</span>' for x in strengths), unsafe_allow_html=True)

        st.markdown("#### Priority Skill Gaps")
        st.markdown("".join(f'<span class="badge gold-badge">{x}</span>' for x in gaps), unsafe_allow_html=True)

        st.markdown("#### 90-Day Development Roadmap")
        for item in roadmap:
            st.markdown(
                f'<div class="soft-card" style="margin-bottom:.75rem">'
                f'<div class="eyebrow" style="color:#8a6b2f">{item.get("period","")}</div>'
                f'<h4>{item.get("title","")}</h4>'
                f'<p class="muted">{item.get("action","")}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

        explanation = fallback_ai_style_explanation(
            {
                "identity": identity,
                "readiness": readiness,
                "ranked": ranked,
                "strengths": strengths,
                "gaps": gaps,
            },
            candidate,
        )

        st.markdown("#### Career Explanation Summary")
        st.markdown(explanation)

        report_lines=[
            "CareerFit AI Career Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "Candidate Information",
            f"Name: {candidate.get('name','—')}",
            f"Email: {candidate.get('email','—')}",
            f"University: {candidate.get('university','—')}",
            f"Major / Field: {candidate.get('major','—')}",
            f"Graduation Year: {candidate.get('year','—')}",
            "",
            "Career Profile",
            f"Career Identity: {identity}",
            f"Career Readiness Score: {readiness}/100",
            "",
            "Top Career Matches",
        ]

        for i,(role,score) in enumerate(ranked, start=1):
            if role:
                report_lines.append(f"{i}. {role} — {score}% fit")

        report_lines.extend([
            "",
            "Core Strengths",
            *[f"- {x}" for x in strengths],
            "",
            "Priority Skill Gaps",
            *[f"- {x}" for x in gaps],
            "",
            "90-Day Development Roadmap",
        ])

        for item in roadmap:
            report_lines.append(f"- {item.get('period','')}: {item.get('title','')} — {item.get('action','')}")

        report_lines.extend([
            "",
            "Career Explanation Summary",
            explanation.replace("**",""),
            "",
            "Note: This report is generated for career exploration and employability planning. It should not be treated as a deterministic employment decision.",
        ])

        report_text="\n".join(report_lines)

        st.download_button(
            "Download Career Report",
            report_text.encode("utf-8"),
            "CareerFit_AI_Career_Report.txt",
            "text/plain",
            use_container_width=True,
        )

def safe_display_df(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """Return a Streamlit-safe dataframe by selecting columns and normalising mixed values."""
    if df is None or df.empty:
        return pd.DataFrame()

    out = df.copy()
    if columns:
        existing = [c for c in columns if c in out.columns]
        out = out[existing].copy()

    for col in out.columns:
        if out[col].dtype == "object":
            out[col] = out[col].apply(
                lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, (dict, list)) else ("" if x is None else str(x))
            )

    for col in out.columns:
        if col in ["top_role_score", "second_role_score", "third_role_score", "readiness_score", "graduation_year"]:
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0).astype(int)

    return out


def org():
    nav()
    if st.button(tr("back")): go("home")
    st.markdown(f"## {tr('org')}")
    st.info("Demo access code for judges: CareerFit2026")
    if st.text_input(tr("org_code"),type="password")!=str(st.secrets.get("ORG_ACCESS_CODE","CareerFit2026")):
        st.info(tr("org_hint")); return
    df=allc()
    if df.empty: st.warning(tr("no_records")); return
    tabs=st.tabs([tr("emp"),tr("univ")])
    readiness=pd.to_numeric(df["readiness_score"],errors="coerce").fillna(0)
    with tabs[0]:
        c1,c2,c3,c4=st.columns(4); c1.metric(tr("pool"),len(df)); c2.metric(tr("jobready"),int((readiness>=75).sum())); c3.metric(tr("developing"),int(((readiness>=50)&(readiness<75)).sum())); c4.metric(tr("intervention"),int((readiness<50).sum()))
        display_df = safe_display_df(df, ["name","university","major","top_role","top_role_score","readiness_score"])
        display_df = display_df.rename(columns={
            "name":"Candidate",
            "university":"University",
            "major":"Major",
            "top_role":"Top Role",
            "top_role_score":"Fit Score",
            "readiness_score":"Readiness Score",
        })
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    with tabs[1]:
        top=df["top_role"].mode().iloc[0] if not df["top_role"].dropna().empty else "—"
        c1,c2,c3,c4=st.columns(4); c1.metric(tr("records"),len(df)); c2.metric(tr("avg"),f"{readiness.mean():.0f}/100"); c3.metric(tr("share"),f"{readiness.ge(75).mean()*100:.0f}%"); c4.metric(tr("common"),top)
        vc=df["top_role"].astype(str).value_counts().rename_axis("Career Path").reset_index(name="Candidates")
        st.dataframe(vc, use_container_width=True, hide_index=True)
        st.bar_chart(vc.set_index("Career Path"))
routes={"home":home,"candidate":candidate,"org":org}
_ = routes.get(st.session_state.view, home)()
