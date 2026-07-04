
import json
from datetime import datetime
from typing import Any

import numpy as np
import pandas as pd
import streamlit as st
from supabase import Client, create_client

st.set_page_config(
    page_title="CareerFit AI",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
:root{--navy:#0f1f3d;--gold:#b89a5b;--light:#f5f6f8;--muted:#667085;--border:#e5e7eb}
#MainMenu,footer,header{visibility:hidden}
.block-container{max-width:1180px;padding-top:1.4rem;padding-bottom:4rem}
.hero{background:linear-gradient(135deg,#0f1f3d,#1a2f56);color:#fff;padding:3rem;border-radius:24px;margin-bottom:1.4rem}
.hero h1{font-size:3rem;line-height:1.06;margin:.5rem 0 1rem}.hero p{color:#d9e0eb;font-size:1.08rem;max-width:780px}
.eyebrow{text-transform:uppercase;letter-spacing:.12em;font-size:.76rem;color:#d8bf86;font-weight:700}
.card,.role-card{background:#fff;border:1px solid var(--border);border-radius:20px;padding:1.2rem;box-shadow:0 8px 28px rgba(15,31,61,.06)}
.soft-card{background:var(--light);border-radius:18px;padding:1.1rem;height:100%}
.gold-card{background:#f6f0e3;border:1px solid #eadbb8;border-radius:18px;padding:1.2rem}
.badge{display:inline-block;background:#eef2f7;color:#26364f;border-radius:999px;padding:.35rem .65rem;margin:.15rem .2rem .15rem 0;font-size:.83rem;font-weight:600}
.gold-badge{background:#f6f0e3;color:#7b612c}.muted{color:var(--muted)}
.navbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:1.2rem}.brand{font-size:1.35rem;font-weight:800;color:var(--navy)}
.score{font-size:1.6rem;font-weight:800;color:var(--gold)}
div.stButton>button{border-radius:12px;border:none;background:#0f1f3d;color:#fff;font-weight:700}
div.stButton>button:hover{background:#1b3159;color:#fff}
</style>
""",
    unsafe_allow_html=True,
)

ROLE_LIBRARY = {
    "Business Analyst": {
        "salary": "RM 3,500–5,500 / month",
        "time": "4–6 months",
        "weights": {"analytical": 0.25, "structure": 0.20, "communication": 0.15, "data": 0.20, "enterprise": 0.10, "readiness": 0.10},
        "gaps": ["SQL", "Dashboard storytelling", "Business requirements"],
        "next": "Build a small business dashboard and explain the problem, metric and recommendation.",
    },
    "Data Analyst": {
        "salary": "RM 3,200–5,000 / month",
        "time": "5–7 months",
        "weights": {"analytical": 0.30, "structure": 0.15, "communication": 0.08, "data": 0.30, "enterprise": 0.05, "readiness": 0.12},
        "gaps": ["SQL", "Python", "Portfolio evidence"],
        "next": "Complete one public-data project and present three actionable findings.",
    },
    "Product Operations Associate": {
        "salary": "RM 3,500–5,200 / month",
        "time": "3–5 months",
        "weights": {"analytical": 0.12, "structure": 0.25, "communication": 0.22, "data": 0.10, "enterprise": 0.18, "readiness": 0.13},
        "gaps": ["Product metrics", "Process mapping", "Cross-functional execution"],
        "next": "Map one product workflow and define three operational KPIs.",
    },
    "UX Research Assistant": {
        "salary": "RM 3,200–4,800 / month",
        "time": "4–6 months",
        "weights": {"analytical": 0.18, "structure": 0.10, "communication": 0.25, "data": 0.08, "enterprise": 0.14, "readiness": 0.25},
        "gaps": ["Interview synthesis", "Journey mapping", "Portfolio case study"],
        "next": "Interview five users and convert the findings into a one-page journey map.",
    },
    "Talent Development Associate": {
        "salary": "RM 3,000–4,800 / month",
        "time": "3–5 months",
        "weights": {"analytical": 0.08, "structure": 0.14, "communication": 0.30, "data": 0.06, "enterprise": 0.18, "readiness": 0.24},
        "gaps": ["Facilitation", "Learning evaluation", "Stakeholder engagement"],
        "next": "Design a short graduate development workshop with measurable learning outcomes.",
    },
}

def top_nav() -> None:
    st.markdown(
        '<div class="navbar"><div class="brand">🧭 CareerFit AI</div>'
        '<div class="muted">Career OS prototype · Talentbank Tech Hackathon 2026</div></div>',
        unsafe_allow_html=True,
    )

def get_supabase() -> Client | None:
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception:
        return None

db = get_supabase()

def go(view: str) -> None:
    st.session_state.view = view
    st.rerun()

def mean100(values: list[int]) -> float:
    return float(np.mean(values) / 5 * 100)

def calculate_profile(answers: dict[str, Any]) -> dict[str, Any]:
    analytical = mean100([
        answers["strengths"]["analyse_complex"],
        answers["interests"]["analyse_data"],
        answers["skills"]["problem_solving"],
        answers["skills"]["research"],
    ])
    structure = mean100([
        answers["strengths"]["structured_plans"],
        answers["interests"]["organise_processes"],
        answers["skills"]["project_coordination"],
    ])
    communication = mean100([
        answers["strengths"]["people_energy"],
        answers["interests"]["help_people"],
        answers["skills"]["communication"],
        answers["skills"]["presentation"],
        answers["skills"]["writing"],
    ])
    data = mean100([
        answers["interests"]["analyse_data"],
        answers["skills"]["data_analysis"],
        answers["skills"]["digital_tools"],
        answers["skills"]["research"],
    ])
    enterprise = mean100([
        answers["interests"]["lead_initiatives"],
        answers["values"]["leadership"],
        answers["values"]["autonomy"],
        answers["strengths"]["new_solutions"],
    ])
    readiness = mean100(list(answers["readiness"].values()))

    dimensions = {
        "analytical": analytical,
        "structure": structure,
        "communication": communication,
        "data": data,
        "enterprise": enterprise,
        "readiness": readiness,
    }

    scores = {}
    for role, role_info in ROLE_LIBRARY.items():
        raw = sum(dimensions[k] * w for k, w in role_info["weights"].items())
        scores[role] = int(round(min(97, max(55, raw))))

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]

    if analytical >= 78 and structure >= 68:
        identity = "Analytical Strategist"
    elif communication >= 78 and enterprise >= 65:
        identity = "People-Centred Builder"
    elif data >= 78:
        identity = "Evidence-Driven Explorer"
    elif structure >= 76:
        identity = "Structured Operations Planner"
    else:
        identity = "Adaptive Problem Solver"

    skill_map = answers["skills"]
    skill_labels = {
        "communication": "Communication",
        "data_analysis": "Data analysis",
        "problem_solving": "Problem solving",
        "presentation": "Presentation",
        "digital_tools": "Digital tools",
        "writing": "Writing",
        "project_coordination": "Project coordination",
        "research": "Research",
    }
    strengths = [skill_labels[k] for k, v in sorted(skill_map.items(), key=lambda x: x[1], reverse=True)[:4]]
    weak_skills = [skill_labels[k] for k, v in sorted(skill_map.items(), key=lambda x: x[1])[:3]]
    role_gaps = ROLE_LIBRARY[ranked[0][0]]["gaps"]
    gaps = list(dict.fromkeys(role_gaps + weak_skills))[:5]

    roadmap = [
        {"period": "Week 1–2", "title": "Clarify the target role", "action": f"Review 10 {ranked[0][0]} vacancies and identify repeated requirements."},
        {"period": "Week 3–5", "title": "Close the priority gap", "action": f"Develop {gaps[0]} through a focused short course and one applied exercise."},
        {"period": "Week 6–8", "title": "Create portfolio evidence", "action": ROLE_LIBRARY[ranked[0][0]]["next"]},
        {"period": "Week 9–12", "title": "Apply and prepare", "action": "Apply to 20 aligned roles and prepare six STAR interview stories."},
    ]

    return {
        "career_identity": identity,
        "readiness_score": int(round(readiness)),
        "ranked_roles": ranked,
        "strengths": strengths,
        "skill_gaps": gaps,
        "roadmap": roadmap,
        "dimensions": dimensions,
    }

def save_candidate(profile_data: dict[str, Any], answers: dict[str, Any]) -> tuple[bool, str]:
    if db is None:
        return False, "Database connection is not available. Check Streamlit Secrets."
    ranked = profile_data["ranked_roles"]
    record = {
        "name": st.session_state.candidate["name"].strip(),
        "email": st.session_state.candidate["email"].strip().lower(),
        "university": st.session_state.candidate["university"].strip(),
        "major": st.session_state.candidate["major"].strip(),
        "graduation_year": int(st.session_state.candidate["graduation_year"]),
        "career_identity": profile_data["career_identity"],
        "readiness_score": profile_data["readiness_score"],
        "top_role": ranked[0][0],
        "top_role_score": ranked[0][1],
        "second_role": ranked[1][0],
        "second_role_score": ranked[1][1],
        "third_role": ranked[2][0],
        "third_role_score": ranked[2][1],
        "strengths": {"items": profile_data["strengths"], "dimensions": profile_data["dimensions"]},
        "interests": answers["interests"],
        "skills": answers["skills"],
        "work_values": answers["values"],
        "readiness_answers": answers["readiness"],
        "skill_gaps": profile_data["skill_gaps"],
        "roadmap": profile_data["roadmap"],
        "updated_at": datetime.utcnow().isoformat(),
    }
    try:
        db.table("candidates").upsert(record, on_conflict="email").execute()
        return True, "Profile saved to the CareerFit database."
    except Exception as exc:
        return False, f"Database save failed: {exc}"

def load_candidate(email: str) -> dict[str, Any] | None:
    if db is None or not email.strip():
        return None
    try:
        response = db.table("candidates").select("*").eq("email", email.strip().lower()).limit(1).execute()
        return response.data[0] if response.data else None
    except Exception:
        return None

def all_candidates() -> pd.DataFrame:
    if db is None:
        return pd.DataFrame()
    try:
        response = db.table("candidates").select("*").order("updated_at", desc=True).execute()
        return pd.DataFrame(response.data or [])
    except Exception:
        return pd.DataFrame()

if "view" not in st.session_state:
    st.session_state.view = "home"
if "candidate" not in st.session_state:
    st.session_state.candidate = {
        "name": "",
        "email": "",
        "university": "",
        "major": "",
        "graduation_year": 2026,
    }
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "profile" not in st.session_state:
    st.session_state.profile = None
if "loaded_record" not in st.session_state:
    st.session_state.loaded_record = None

def render_home() -> None:
    top_nav()
    st.markdown(
        """
<div class="hero">
<div class="eyebrow">Career intelligence for graduates and organisations</div>
<h1>Know where you fit.<br>See where you can go.</h1>
<p>CareerFit AI converts personal strengths, career interests, skills and readiness into explainable career pathways, actionable development plans and organisation-level talent insights.</p>
</div>
""",
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """<div class="card"><div class="eyebrow" style="color:#8a6b2f">Candidate Portal</div>
<h3>Create your own career profile</h3><p class="muted">Enter your details, complete the assessment, generate personalised role matches and save your profile.</p>
<span class="badge">Dynamic scoring</span><span class="badge">Saved profile</span><span class="badge">90-day plan</span></div>""",
            unsafe_allow_html=True,
        )
        if st.button("Enter Candidate Portal", use_container_width=True):
            go("candidate")
    with c2:
        st.markdown(
            """<div class="card"><div class="eyebrow" style="color:#8a6b2f">Organisation Portal</div>
<h3>Use real candidate data for decisions</h3><p class="muted">Review candidate-role fit, readiness, talent-pool patterns and university-level skill gaps.</p>
<span class="badge">Employer view</span><span class="badge">University view</span><span class="badge">Database analytics</span></div>""",
            unsafe_allow_html=True,
        )
        if st.button("Enter Organisation Portal", use_container_width=True):
            go("organisation")

def assessment_form() -> None:
    st.markdown("### Create Your Career Profile")
    with st.form("candidate_assessment"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full name", value=st.session_state.candidate["name"])
            email = st.text_input("Email", value=st.session_state.candidate["email"])
            university = st.text_input("University", value=st.session_state.candidate["university"])
        with c2:
            major = st.text_input("Major / field of study", value=st.session_state.candidate["major"])
            graduation_year = st.number_input("Graduation year", min_value=2020, max_value=2035, value=int(st.session_state.candidate["graduation_year"]))

        st.markdown("#### 1. Work Strengths")
        s1 = st.slider("I enjoy analysing complex information.", 1, 5, 4)
        s2 = st.slider("I prefer turning ideas into structured plans.", 1, 5, 4)
        s3 = st.slider("I gain energy from working with people.", 1, 5, 3)
        s4 = st.slider("I enjoy creating new solutions.", 1, 5, 4)
        s5 = st.slider("I stay calm when decisions are uncertain.", 1, 5, 3)

        st.markdown("#### 2. Career Interests")
        i1 = st.slider("Analysing data and solving problems", 1, 5, 5)
        i2 = st.slider("Helping, teaching or supporting people", 1, 5, 3)
        i3 = st.slider("Leading initiatives and influencing decisions", 1, 5, 4)
        i4 = st.slider("Creating content, designs or new ideas", 1, 5, 3)
        i5 = st.slider("Organising processes and managing details", 1, 5, 4)

        st.markdown("#### 3. Current Skills")
        c1, c2 = st.columns(2)
        with c1:
            k1 = st.slider("Communication", 1, 5, 4)
            k2 = st.slider("Data analysis", 1, 5, 3)
            k3 = st.slider("Problem solving", 1, 5, 4)
            k4 = st.slider("Presentation", 1, 5, 3)
        with c2:
            k5 = st.slider("Digital tools", 1, 5, 3)
            k6 = st.slider("Writing", 1, 5, 4)
            k7 = st.slider("Project coordination", 1, 5, 3)
            k8 = st.slider("Research", 1, 5, 4)

        st.markdown("#### 4. Work Values")
        v1 = st.slider("Growth", 1, 5, 5)
        v2 = st.slider("Stability", 1, 5, 3)
        v3 = st.slider("Income", 1, 5, 4)
        v4 = st.slider("Impact", 1, 5, 4)
        v5 = st.slider("Autonomy", 1, 5, 4)
        v6 = st.slider("Leadership", 1, 5, 3)

        st.markdown("#### 5. Career Readiness")
        r1 = st.slider("Resume readiness", 1, 5, 3)
        r2 = st.slider("Interview confidence", 1, 5, 3)
        r3 = st.slider("Portfolio evidence", 1, 5, 2)
        r4 = st.slider("Role clarity", 1, 5, 4)
        r5 = st.slider("Job-search consistency", 1, 5, 3)

        submitted = st.form_submit_button("Generate and Save My Career Profile", use_container_width=True)

    if submitted:
        if not name.strip() or not email.strip() or "@" not in email:
            st.error("Enter a valid name and email.")
            return
        st.session_state.candidate = {
            "name": name,
            "email": email,
            "university": university,
            "major": major,
            "graduation_year": int(graduation_year),
        }
        answers = {
            "strengths": {
                "analyse_complex": s1,
                "structured_plans": s2,
                "people_energy": s3,
                "new_solutions": s4,
                "uncertainty": s5,
            },
            "interests": {
                "analyse_data": i1,
                "help_people": i2,
                "lead_initiatives": i3,
                "creative_work": i4,
                "organise_processes": i5,
            },
            "skills": {
                "communication": k1,
                "data_analysis": k2,
                "problem_solving": k3,
                "presentation": k4,
                "digital_tools": k5,
                "writing": k6,
                "project_coordination": k7,
                "research": k8,
            },
            "values": {
                "growth": v1,
                "stability": v2,
                "income": v3,
                "impact": v4,
                "autonomy": v5,
                "leadership": v6,
            },
            "readiness": {
                "resume": r1,
                "interview": r2,
                "portfolio": r3,
                "role_clarity": r4,
                "job_search": r5,
            },
        }
        profile = calculate_profile(answers)
        st.session_state.answers = answers
        st.session_state.profile = profile
        ok, message = save_candidate(profile, answers)
        if ok:
            st.success(message)
        else:
            st.warning(message)
        st.info("Open the Career Profile and Career Pathways tabs to review the personalised results.")

def render_loaded_profile(record: dict[str, Any]) -> None:
    st.markdown(f"### {record.get('name', 'Candidate')}")
    st.caption(f"{record.get('major') or 'Graduate'} · {record.get('university') or 'University not provided'}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Career Identity", record.get("career_identity") or "—")
    c2.metric("Career Readiness", f"{record.get('readiness_score') or 0}/100")
    c3.metric("Top Match", record.get("top_role") or "—")
    c4.metric("Top Fit", f"{int(record.get('top_role_score') or 0)}%")
    strengths = record.get("strengths") or {}
    strength_items = strengths.get("items", []) if isinstance(strengths, dict) else []
    if strength_items:
        st.markdown("#### Core Strengths")
        st.markdown("".join(f'<span class="badge">{x}</span>' for x in strength_items), unsafe_allow_html=True)
    st.markdown(
        """<div class="gold-card"><h4>How this profile was generated</h4>
<p>CareerFit AI compares five assessment dimensions with transparent role requirements. It generates relative fit scores, identifies priority gaps and produces an action plan.</p>
<p class="muted"><small>This prototype supports exploration and should not be treated as a deterministic employment decision.</small></p></div>""",
        unsafe_allow_html=True,
    )

def render_candidate() -> None:
    top_nav()
    if st.button("← Back to Home"):
        go("home")
    st.markdown("## Candidate Portal")
    tabs = st.tabs(["Assessment", "Load Existing Profile", "Career Profile", "Career Pathways", "Skill Plan", "Career Report"])

    with tabs[0]:
        assessment_form()

    with tabs[1]:
        st.markdown("### Load a Saved Profile")
        load_email = st.text_input("Email used for the assessment", key="load_email")
        if st.button("Load My Career Profile"):
            record = load_candidate(load_email)
            if record:
                st.session_state.loaded_record = record
                st.session_state.candidate = {
                    "name": record.get("name", ""),
                    "email": record.get("email", ""),
                    "university": record.get("university", ""),
                    "major": record.get("major", ""),
                    "graduation_year": record.get("graduation_year") or 2026,
                }
                st.success("Saved profile loaded.")
            else:
                st.error("No saved profile was found for this email.")

    record = st.session_state.loaded_record
    profile = st.session_state.profile

    with tabs[2]:
        if profile:
            ranked = profile["ranked_roles"]
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Career Identity", profile["career_identity"])
            c2.metric("Career Readiness", f"{profile['readiness_score']}/100")
            c3.metric("Top Match", ranked[0][0])
            c4.metric("Top Fit", f"{ranked[0][1]}%")
            st.markdown("#### Core Strengths")
            st.markdown("".join(f'<span class="badge">{x}</span>' for x in profile["strengths"]), unsafe_allow_html=True)
        elif record:
            render_loaded_profile(record)
        else:
            st.info("Complete the assessment or load an existing profile.")

    with tabs[3]:
        if profile:
            ranked = profile["ranked_roles"]
        elif record:
            ranked = [
                (record.get("top_role"), int(record.get("top_role_score") or 0)),
                (record.get("second_role"), int(record.get("second_role_score") or 0)),
                (record.get("third_role"), int(record.get("third_role_score") or 0)),
            ]
        else:
            ranked = []

        if not ranked:
            st.info("Complete the assessment or load a saved profile.")
        else:
            st.markdown("### Personalised Career Pathways")
            for role, score in ranked:
                info = ROLE_LIBRARY.get(role, {})
                st.markdown(
                    f"""<div class="role-card" style="margin-bottom:1rem">
<div style="display:flex;justify-content:space-between"><div><h3>{role}</h3>
<div class="muted">{info.get('salary','')} · {info.get('time','')} preparation</div></div>
<div class="score">{score}% fit</div></div>
<p><b>Priority gaps:</b> {", ".join(info.get('gaps', []))}</p>
<p><b>Next best move:</b> {info.get('next','')}</p></div>""",
                    unsafe_allow_html=True,
                )

    with tabs[4]:
        roadmap = profile["roadmap"] if profile else (record.get("roadmap", []) if record else [])
        gaps = profile["skill_gaps"] if profile else (record.get("skill_gaps", []) if record else [])
        if not roadmap:
            st.info("Complete the assessment or load a saved profile.")
        else:
            st.markdown("### Priority Skill Gaps")
            st.markdown("".join(f'<span class="badge gold-badge">{x}</span>' for x in gaps), unsafe_allow_html=True)
            st.markdown("### 90-Day Action Plan")
            for item in roadmap:
                st.markdown(
                    f'<div class="soft-card" style="margin-bottom:.75rem"><div class="eyebrow" style="color:#8a6b2f">{item["period"]}</div>'
                    f'<h4>{item["title"]}</h4><p class="muted">{item["action"]}</p></div>',
                    unsafe_allow_html=True,
                )

    with tabs[5]:
        if profile:
            ranked = profile["ranked_roles"]
            identity = profile["career_identity"]
            readiness = profile["readiness_score"]
            strengths = profile["strengths"]
            gaps = profile["skill_gaps"]
        elif record:
            ranked = [(record.get("top_role"), int(record.get("top_role_score") or 0))]
            identity = record.get("career_identity")
            readiness = record.get("readiness_score")
            strengths_obj = record.get("strengths") or {}
            strengths = strengths_obj.get("items", []) if isinstance(strengths_obj, dict) else []
            gaps = record.get("skill_gaps") or []
        else:
            ranked = []

        if not ranked:
            st.info("Complete the assessment or load a saved profile.")
        else:
            report = f"""CareerFit AI Candidate Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
Candidate: {st.session_state.candidate["name"]}
Email: {st.session_state.candidate["email"]}
University: {st.session_state.candidate["university"]}
Major: {st.session_state.candidate["major"]}

Career Identity: {identity}
Career Readiness: {readiness}/100
Top Career Match: {ranked[0][0]} ({ranked[0][1]}%)

Core Strengths:
- """ + "\n- ".join(strengths) + """

Priority Skill Gaps:
- """ + "\n- ".join(gaps)
            st.text_area("Report preview", report, height=340)
            st.download_button("Download Career Report", report.encode("utf-8"), "CareerFit_AI_Report.txt", "text/plain", use_container_width=True)

def render_organisation() -> None:
    top_nav()
    if st.button("← Back to Home"):
        go("home")
    st.markdown("## Organisation Portal")
    expected = str(st.secrets.get("ORG_ACCESS_CODE", ""))
    entered = st.text_input("Organisation access code", type="password")
    if not expected or entered != expected:
        st.info("Enter the organisation access code to view candidate and cohort data.")
        return

    df = all_candidates()
    if df.empty:
        st.warning("No candidate records are available yet.")
        return

    tabs = st.tabs(["Employer View", "University View"])
    with tabs[0]:
        total = len(df)
        ready = int((pd.to_numeric(df["readiness_score"], errors="coerce").fillna(0) >= 75).sum())
        developing = int(((pd.to_numeric(df["readiness_score"], errors="coerce").fillna(0) >= 50) & (pd.to_numeric(df["readiness_score"], errors="coerce").fillna(0) < 75)).sum())
        intervention = total - ready - developing
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Talent Pool", total)
        c2.metric("Job-ready", ready)
        c3.metric("Developing", developing)
        c4.metric("Require intervention", intervention)

        display_cols = ["name", "university", "major", "top_role", "top_role_score", "readiness_score"]
        st.markdown("### Candidate Matches")
        st.dataframe(df[display_cols].rename(columns={
            "name": "Candidate",
            "university": "University",
            "major": "Major",
            "top_role": "Top Role",
            "top_role_score": "Fit",
            "readiness_score": "Readiness",
        }), hide_index=True, use_container_width=True)

    with tabs[1]:
        readiness = pd.to_numeric(df["readiness_score"], errors="coerce").fillna(0)
        top_role = df["top_role"].mode().iloc[0] if not df["top_role"].dropna().empty else "—"
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Candidate Records", len(df))
        c2.metric("Average Readiness", f"{readiness.mean():.0f}/100")
        c3.metric("Job-ready Share", f"{(readiness.ge(75).mean()*100):.0f}%")
        c4.metric("Most Common Path", top_role)

        role_counts = df["top_role"].value_counts().rename_axis("Career Path").reset_index(name="Candidates")
        st.markdown("### Career Path Distribution")
        st.dataframe(role_counts, hide_index=True, use_container_width=True)
        st.bar_chart(role_counts.set_index("Career Path"))

        all_gaps: list[str] = []
        for item in df["skill_gaps"].dropna():
            if isinstance(item, list):
                all_gaps.extend(item)
            elif isinstance(item, str):
                try:
                    parsed = json.loads(item)
                    if isinstance(parsed, list):
                        all_gaps.extend(parsed)
                except Exception:
                    pass
        if all_gaps:
            gaps_df = pd.Series(all_gaps).value_counts().head(10).rename_axis("Skill Gap").reset_index(name="Candidates")
            st.markdown("### Most Common Skill Gaps")
            st.dataframe(gaps_df, hide_index=True, use_container_width=True)

def main() -> None:
    routes = {"home": render_home, "candidate": render_candidate, "organisation": render_organisation}
    routes.get(st.session_state.view, render_home)()

main()
