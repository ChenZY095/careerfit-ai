
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="CareerFit AI", page_icon="🧭", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
:root{--navy:#0f1f3d;--gold:#b89a5b;--light:#f5f6f8;--muted:#667085;--border:#e5e7eb}
#MainMenu,footer,header{visibility:hidden}
.block-container{max-width:1180px;padding-top:1.5rem;padding-bottom:4rem}
.hero{background:linear-gradient(135deg,#0f1f3d,#1a2f56);color:#fff;padding:3rem;border-radius:24px;margin-bottom:1.5rem}
.hero h1{font-size:3rem;line-height:1.05;margin-bottom:1rem}.hero p{color:#d9e0eb;font-size:1.1rem;max-width:760px}
.eyebrow{text-transform:uppercase;letter-spacing:.12em;font-size:.78rem;color:#d8bf86;font-weight:700}
.card,.role-card{background:#fff;border:1px solid var(--border);border-radius:20px;padding:1.2rem;box-shadow:0 8px 28px rgba(15,31,61,.06)}
.soft-card{background:var(--light);border-radius:18px;padding:1.1rem;height:100%}
.gold-card{background:#f6f0e3;border:1px solid #eadbb8;border-radius:18px;padding:1.2rem}
.badge{display:inline-block;background:#eef2f7;color:#26364f;border-radius:999px;padding:.35rem .65rem;margin:.15rem .2rem .15rem 0;font-size:.83rem;font-weight:600}
.gold-badge{background:#f6f0e3;color:#7b612c}.muted{color:var(--muted)}
.navbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:1.2rem}.brand{font-size:1.35rem;font-weight:800;color:var(--navy)}
.score{font-size:1.6rem;font-weight:800;color:var(--gold)}
div.stButton>button{border-radius:12px;border:none;background:#0f1f3d;color:white;font-weight:700}
div.stButton>button:hover{background:#1b3159;color:white}
</style>
""", unsafe_allow_html=True)

ROLES = {
"Business Analyst":{"fit":91,"salary":"RM 3,500–5,500 / month","time":"4–6 months","strengths":"Problem solving, communication, Excel fundamentals","gaps":"SQL and dashboard storytelling","why":"Your analytical thinking, structured planning and communication strengths align strongly with business analysis tasks.","next":"Build one small business dashboard project and document the problem, metrics and recommendation."},
"Data Analyst":{"fit":86,"salary":"RM 3,200–5,000 / month","time":"5–7 months","strengths":"Analytical reasoning, attention to detail, research orientation","gaps":"SQL, Python and portfolio evidence","why":"Your investigative interests and evidence-based judgement support entry-level data analysis work.","next":"Complete one public-data project and present three actionable findings."},
"Product Operations Associate":{"fit":81,"salary":"RM 3,500–5,200 / month","time":"3–5 months","strengths":"Coordination, structured execution, communication","gaps":"Product metrics and cross-functional project experience","why":"Your planning and communication strengths support product operations work.","next":"Create a product workflow map and define three operational KPIs."}
}

CANDIDATES = pd.DataFrame([
["Aisyah Rahman","Business Analyst",91,72,"Ready with gaps"],
["Daniel Lim","Data Analyst",88,78,"Job-ready"],
["Nurul Hana","Product Operations Associate",84,69,"Developing"],
["Marcus Lee","UX Research Assistant",82,74,"Ready with gaps"],
["Siti Amina","Business Analyst",80,65,"Developing"]],
columns=["Candidate","Target Role","Fit","Readiness","Status"])

COHORT = pd.DataFrame({"Skill":["SQL","Interview confidence","Portfolio evidence","Dashboarding","Role clarity"],"Gap %":[42,38,35,31,28]})

if "view" not in st.session_state: st.session_state.view="home"
if "name" not in st.session_state: st.session_state.name="Aisyah Rahman"

def nav():
    st.markdown('<div class="navbar"><div class="brand">🧭 CareerFit AI</div><div class="muted">Career OS prototype · Talentbank Tech Hackathon 2026</div></div>',unsafe_allow_html=True)

def go(v):
    st.session_state.view=v
    st.rerun()

def home():
    nav()
    st.markdown("""<div class="hero"><div class="eyebrow">Career intelligence for graduates and organisations</div><h1>Know where you fit.<br>See where you can go.</h1><p>CareerFit AI turns work strengths, career interests, skills and readiness into explainable career pathways, practical next steps and organisation-level talent insights.</p></div>""",unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        st.markdown("""<div class="card"><div class="eyebrow" style="color:#8a6b2f">Candidate Portal</div><h3>Discover your strongest career pathways</h3><p class="muted">Complete a structured assessment, compare realistic graduate roles, identify skill gaps and generate a 90-day plan.</p><span class="badge">Career profile</span><span class="badge">Role fit</span><span class="badge">Skill plan</span></div>""",unsafe_allow_html=True)
        if st.button("Enter Candidate Portal",use_container_width=True): go("candidate")
    with c2:
        st.markdown("""<div class="card"><div class="eyebrow" style="color:#8a6b2f">Organisation Portal</div><h3>Turn candidate data into talent decisions</h3><p class="muted">Explore employer matching, candidate readiness, cohort skill gaps and university employability insights.</p><span class="badge">Employer view</span><span class="badge">University view</span><span class="badge">Talent insights</span></div>""",unsafe_allow_html=True)
        if st.button("Enter Organisation Portal",use_container_width=True): go("organisation")
    st.markdown("### How it works")
    cols=st.columns(4)
    for col,(n,t,d) in zip(cols,[("01","Discover","Understand strengths, interests, skills and readiness."),("02","Match","Compare your profile with realistic career pathways."),("03","Improve","Identify priority gaps and next best actions."),("04","Progress","Track readiness and connect growth with opportunity.")]):
        with col: st.markdown(f'<div class="soft-card"><div class="eyebrow" style="color:#8a6b2f">{n}</div><h4>{t}</h4><p class="muted">{d}</p></div>',unsafe_allow_html=True)

def candidate():
    nav()
    if st.button("← Back to Home"): go("home")
    st.markdown("## Candidate Portal")
    tabs=st.tabs(["Assessment","Career Profile","Career Pathways","Skill Plan","Career Report"])
    with tabs[0]:
        st.markdown("### Discover Your Fit")
        st.caption("Use 1–5 ratings. Results use transparent simulated scoring.")
        st.session_state.name=st.text_input("Candidate name",st.session_state.name)
        with st.expander("1. Work Strengths",expanded=True):
            a=[st.slider(q,1,5,v) for q,v in [
            ("I enjoy analysing complex information.",4),("I prefer turning ideas into structured plans.",4),("I gain energy from working with people.",3),("I enjoy creating new solutions.",4),("I stay calm when decisions are uncertain.",3)]]
        with st.expander("2. Career Interests"):
            b=[st.slider(q,1,5,v) for q,v in [
            ("Analysing data and solving problems",5),("Helping, teaching or supporting people",3),("Leading initiatives and influencing decisions",4),("Creating content, designs or new ideas",3),("Organising processes and managing details",4)]]
        with st.expander("3. Current Skills"):
            c=[st.slider(q,1,5,v) for q,v in [("Communication",4),("Data analysis",3),("Problem solving",4),("Presentation",3),("Digital tools",3),("Writing",4),("Project coordination",3),("Research",4)]]
        with st.expander("4. Work Values"):
            d=[st.slider(q,1,5,v) for q,v in [("Growth",5),("Stability",3),("Income",4),("Impact",4),("Autonomy",4),("Leadership",3)]]
        with st.expander("5. Career Readiness"):
            e=[st.slider(q,1,5,v) for q,v in [("Resume readiness",3),("Interview confidence",3),("Portfolio evidence",2),("Role clarity",4),("Job-search consistency",3)]]
        if st.button("Generate My Career Profile",use_container_width=True):
            st.session_state.readiness=int(round(np.mean(e)/5*100))
            st.success("Career profile generated. Open the Career Profile tab.")
    with tabs[1]:
        r=st.session_state.get("readiness",72)
        st.markdown(f"### {st.session_state.name}")
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Career Identity","Analytical Problem Solver");c2.metric("Career Readiness",f"{r}/100");c3.metric("Top Match","Business Analyst");c4.metric("Preparation","4–6 months")
        st.markdown("#### Core Strengths")
        st.markdown('<span class="badge">Structured thinking</span><span class="badge">Evidence-based judgement</span><span class="badge">Clear communication</span><span class="badge">Learning agility</span>',unsafe_allow_html=True)
        st.markdown("#### Career Interest Profile")
        st.markdown('<span class="badge gold-badge">Investigative</span><span class="badge gold-badge">Enterprising</span><span class="badge gold-badge">Conventional</span>',unsafe_allow_html=True)
        st.markdown("""<div class="gold-card"><h4>How this profile was generated</h4><p>CareerFit AI combines work strengths, career interests, current skills, work values and career readiness. These inputs are compared with simulated role requirements to generate an explainable fit score, identify skill gaps and suggest next steps.</p><p class="muted"><small>This prototype uses simulated data and transparent scoring logic. It supports exploration rather than deterministic career decisions.</small></p></div>""",unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({"Dimension":["Work Strengths","Career Interests","Skills","Work Values","Career Readiness"],"Weight":["20%","25%","30%","15%","10%"]}),hide_index=True,use_container_width=True)
    with tabs[2]:
        st.markdown("### Top Career Pathways")
        for role,x in ROLES.items():
            st.markdown(f"""<div class="role-card" style="margin-bottom:1rem"><div style="display:flex;justify-content:space-between"><div><h3>{role}</h3><div class="muted">{x['salary']} · {x['time']} preparation</div></div><div class="score">{x['fit']}% fit</div></div><p><b>Why it fits:</b> {x['why']}</p><p><b>Existing strengths:</b> {x['strengths']}</p><p><b>Priority gaps:</b> {x['gaps']}</p></div>""",unsafe_allow_html=True)
        q=st.radio("Ask CareerFit AI",["Why is Business Analyst my strongest match?","What should I learn next?","What is my best move this month?"])
        if q.startswith("Why"): st.info(ROLES["Business Analyst"]["why"])
        elif q.startswith("What should"): st.info("Focus on SQL fundamentals and dashboard storytelling. These skills appear across your strongest matched roles.")
        else: st.info(ROLES["Business Analyst"]["next"])
    with tabs[3]:
        st.markdown("### Skill Gap and 90-Day Action Plan")
        gaps=pd.DataFrame({"Skill":["SQL","Dashboard storytelling","Portfolio evidence","Interview confidence"],"Current":[40,50,35,55],"Target":[75,75,70,75]})
        gaps["Gap"]=gaps["Target"]-gaps["Current"]
        st.dataframe(gaps,hide_index=True,use_container_width=True)
        for p,t,a in [("Week 1–2","Clarify target role","Review 10 Business Analyst job descriptions and rewrite your resume around repeated requirements."),("Week 3–5","Close priority skill gaps","Learn SQL fundamentals and create one simple dashboard."),("Week 6–8","Build portfolio evidence","Document one portfolio case with problem, method, output and business value."),("Week 9–12","Apply and prepare","Apply to 20 aligned roles and prepare six STAR interview stories.")]:
            st.markdown(f'<div class="soft-card" style="margin-bottom:.75rem"><div class="eyebrow" style="color:#8a6b2f">{p}</div><h4>{t}</h4><p class="muted">{a}</p></div>',unsafe_allow_html=True)
    with tabs[4]:
        r=st.session_state.get("readiness",72)
        report=f"""CareerFit AI Candidate Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Candidate: {st.session_state.name}

Career Identity: Analytical Problem Solver
Career Readiness: {r}/100
Top Career Match: Business Analyst (91%)

Core Strengths:
- Structured thinking
- Evidence-based judgement
- Clear communication
- Learning agility

Priority Skill Gaps:
- SQL
- Dashboard storytelling
- Portfolio evidence

Next Best Move:
Build one small business dashboard project and document the problem, metrics and recommendation.
"""
        st.text_area("Report preview",report,height=320)
        st.download_button("Download Career Report",report.encode(),"CareerFit_AI_Report.txt","text/plain",use_container_width=True)

def organisation():
    nav()
    if st.button("← Back to Home"): go("home")
    st.markdown("## Organisation Portal")
    t1,t2=st.tabs(["Employer View","University View"])
    with t1:
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Talent Pool","126");c2.metric("Job-ready","48");c3.metric("Developing","52");c4.metric("Require intervention","26")
        st.markdown("### Top Candidate Matches")
        st.dataframe(CANDIDATES,hide_index=True,use_container_width=True)
        selected=st.selectbox("Select candidate",CANDIDATES["Candidate"])
        row=CANDIDATES[CANDIDATES["Candidate"]==selected].iloc[0]
        c1,c2,c3=st.columns(3)
        c1.metric("Target Role",row["Target Role"]);c2.metric("Fit",f"{row['Fit']}%");c3.metric("Readiness",f"{row['Readiness']}/100")
        st.markdown("""<div class="gold-card"><h4>Suggested Interview Focus</h4><ul><li>Ask for evidence of analytical thinking.</li><li>Probe how the candidate translates data into recommendations.</li><li>Assess readiness to close the priority skill gap.</li><li>Discuss preferred working style and feedback needs.</li></ul></div>""",unsafe_allow_html=True)
    with t2:
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Cohort Size","420");c2.metric("Average Readiness","68/100");c3.metric("Job-ready Students","37%");c4.metric("Top Career Path","Business Analyst")
        st.markdown("### Cohort Skill Gaps")
        st.dataframe(COHORT,hide_index=True,use_container_width=True)
        st.bar_chart(COHORT.set_index("Skill"))
        st.markdown("""<div class="gold-card"><h4>Curriculum Recommendations</h4><ul><li>Introduce a six-week applied SQL and dashboard module.</li><li>Add employer-led mock interviews.</li><li>Require one portfolio-ready capstone project.</li><li>Use cohort readiness data to target career support.</li></ul></div>""",unsafe_allow_html=True)

{"home":home,"candidate":candidate,"organisation":organisation}[st.session_state.view]()
