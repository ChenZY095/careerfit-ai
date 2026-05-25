
import streamlit as st
import pandas as pd
import numpy as np
import math
from datetime import datetime
import io

st.set_page_config(
    page_title="CareerFit AI | Multi-Dimensional Career Fit Engine",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Data model
# -----------------------------
ROLES = {
    "Business Analyst": {
        "family": "Business & Strategy",
        "description": "Transforms business problems into structured requirements, insights, and solutions.",
        "personality": {"conscientiousness": 0.75, "openness": 0.65, "extraversion": 0.55, "agreeableness": 0.50, "emotional_stability": 0.65},
        "riasec": {"I": 0.35, "E": 0.25, "C": 0.25, "S": 0.10, "A": 0.03, "R": 0.02},
        "skills": {"Excel": 85, "SQL": 70, "Communication": 75, "Problem Solving": 85, "Dashboarding": 70, "Writing": 65},
        "values": {"growth": 0.25, "stability": 0.20, "income": 0.20, "impact": 0.15, "autonomy": 0.10, "leadership": 0.10},
        "entry_titles": ["Junior Business Analyst", "Management Trainee", "Operations Analyst"],
        "portfolio": "Map a real business process and build a dashboard showing bottlenecks, KPIs, and recommendations."
    },
    "Data Analyst": {
        "family": "Data & Analytics",
        "description": "Uses data to identify patterns, build dashboards, and support evidence-based decisions.",
        "personality": {"conscientiousness": 0.80, "openness": 0.65, "extraversion": 0.35, "agreeableness": 0.45, "emotional_stability": 0.70},
        "riasec": {"I": 0.45, "C": 0.30, "R": 0.10, "E": 0.08, "A": 0.04, "S": 0.03},
        "skills": {"Excel": 90, "SQL": 85, "Python": 75, "Dashboarding": 85, "Problem Solving": 80, "Writing": 55},
        "values": {"growth": 0.25, "income": 0.25, "stability": 0.20, "autonomy": 0.15, "impact": 0.10, "leadership": 0.05},
        "entry_titles": ["Junior Data Analyst", "Reporting Analyst", "BI Analyst"],
        "portfolio": "Create a data dashboard using public job-market or e-commerce data and explain three actionable insights."
    },
    "UX Researcher": {
        "family": "Product & User Research",
        "description": "Studies user needs, behaviours, and pain points to improve digital products and services.",
        "personality": {"conscientiousness": 0.60, "openness": 0.80, "extraversion": 0.55, "agreeableness": 0.80, "emotional_stability": 0.60},
        "riasec": {"S": 0.30, "I": 0.30, "A": 0.20, "E": 0.10, "C": 0.07, "R": 0.03},
        "skills": {"Communication": 85, "Writing": 80, "Problem Solving": 75, "Figma": 65, "Research Methods": 85, "Presentation": 75},
        "values": {"impact": 0.25, "growth": 0.20, "autonomy": 0.20, "stability": 0.15, "leadership": 0.10, "income": 0.10},
        "entry_titles": ["UX Research Assistant", "User Research Intern", "Product Research Associate"],
        "portfolio": "Conduct five user interviews, synthesize themes, and present a user journey map with design recommendations."
    },
    "Product Manager": {
        "family": "Product & Innovation",
        "description": "Coordinates user needs, business goals, and technical execution into product decisions.",
        "personality": {"conscientiousness": 0.70, "openness": 0.75, "extraversion": 0.70, "agreeableness": 0.60, "emotional_stability": 0.65},
        "riasec": {"E": 0.30, "I": 0.25, "A": 0.15, "S": 0.15, "C": 0.10, "R": 0.05},
        "skills": {"Communication": 90, "Problem Solving": 85, "Writing": 70, "Dashboarding": 65, "Figma": 60, "Presentation": 85},
        "values": {"leadership": 0.25, "growth": 0.25, "impact": 0.20, "autonomy": 0.15, "income": 0.10, "stability": 0.05},
        "entry_titles": ["Associate Product Manager", "Product Executive", "Product Operations Associate"],
        "portfolio": "Write a product requirements document for a career-tech feature and include user stories, metrics, and wireframes."
    },
    "Marketing Executive": {
        "family": "Marketing & Growth",
        "description": "Plans campaigns, communicates value, and converts audience attention into measurable growth.",
        "personality": {"conscientiousness": 0.60, "openness": 0.75, "extraversion": 0.75, "agreeableness": 0.60, "emotional_stability": 0.55},
        "riasec": {"E": 0.35, "A": 0.25, "S": 0.15, "I": 0.10, "C": 0.10, "R": 0.05},
        "skills": {"Communication": 90, "Writing": 85, "Presentation": 80, "Excel": 60, "Dashboarding": 55, "Problem Solving": 70},
        "values": {"growth": 0.25, "impact": 0.20, "income": 0.20, "autonomy": 0.15, "leadership": 0.10, "stability": 0.10},
        "entry_titles": ["Marketing Executive", "Digital Marketing Associate", "Content Marketing Associate"],
        "portfolio": "Design a 2-week campaign with target audience, message, channels, content samples, and performance metrics."
    },
    "HR / Talent Development Associate": {
        "family": "People & Organisation",
        "description": "Supports employee growth, recruitment readiness, learning programmes, and people processes.",
        "personality": {"conscientiousness": 0.65, "openness": 0.60, "extraversion": 0.65, "agreeableness": 0.85, "emotional_stability": 0.65},
        "riasec": {"S": 0.40, "E": 0.25, "C": 0.15, "I": 0.10, "A": 0.07, "R": 0.03},
        "skills": {"Communication": 90, "Writing": 75, "Presentation": 75, "Excel": 65, "Problem Solving": 70, "Research Methods": 60},
        "values": {"impact": 0.25, "stability": 0.20, "growth": 0.20, "leadership": 0.15, "autonomy": 0.10, "income": 0.10},
        "entry_titles": ["Talent Development Associate", "HR Executive", "Graduate Recruitment Associate"],
        "portfolio": "Design a graduate onboarding or training plan with learning objectives, activities, and evaluation metrics."
    },
    "Operations Executive": {
        "family": "Operations & Process",
        "description": "Improves processes, coordinates resources, and ensures work is delivered reliably and efficiently.",
        "personality": {"conscientiousness": 0.85, "openness": 0.45, "extraversion": 0.50, "agreeableness": 0.55, "emotional_stability": 0.75},
        "riasec": {"C": 0.35, "R": 0.20, "E": 0.15, "I": 0.15, "S": 0.10, "A": 0.05},
        "skills": {"Excel": 85, "Communication": 75, "Problem Solving": 80, "Dashboarding": 70, "Writing": 60, "Presentation": 65},
        "values": {"stability": 0.25, "growth": 0.20, "income": 0.20, "leadership": 0.15, "impact": 0.10, "autonomy": 0.10},
        "entry_titles": ["Operations Executive", "Project Coordinator", "Process Improvement Associate"],
        "portfolio": "Create an operations improvement plan showing workflow, pain points, proposed changes, and measurable KPIs."
    },
    "Content Strategist": {
        "family": "Creative & Communication",
        "description": "Builds content systems that connect audience insight, message strategy, and platform growth.",
        "personality": {"conscientiousness": 0.55, "openness": 0.85, "extraversion": 0.60, "agreeableness": 0.60, "emotional_stability": 0.55},
        "riasec": {"A": 0.35, "E": 0.25, "S": 0.15, "I": 0.10, "C": 0.10, "R": 0.05},
        "skills": {"Writing": 90, "Communication": 85, "Presentation": 70, "Dashboarding": 55, "Problem Solving": 70, "Figma": 55},
        "values": {"autonomy": 0.25, "impact": 0.20, "growth": 0.20, "income": 0.15, "leadership": 0.10, "stability": 0.10},
        "entry_titles": ["Content Strategist", "Social Media Executive", "Brand Content Associate"],
        "portfolio": "Build a content calendar with audience persona, content pillars, sample posts, and success metrics."
    }
}

BIG5_ITEMS = {
    "openness": [
        ("I enjoy learning new concepts even when they are abstract.", 1),
        ("I prefer familiar routines over new possibilities.", -1),
        ("I like exploring creative or unconventional solutions.", 1),
    ],
    "conscientiousness": [
        ("I plan my tasks carefully and follow through.", 1),
        ("I often start tasks without finishing them.", -1),
        ("I feel responsible for meeting deadlines.", 1),
    ],
    "extraversion": [
        ("I gain energy from discussion and collaboration.", 1),
        ("I prefer to work quietly without much interaction.", -1),
        ("I am comfortable presenting ideas to others.", 1),
    ],
    "agreeableness": [
        ("I try to understand other people's needs before making decisions.", 1),
        ("I am comfortable competing even if others feel pressured.", -1),
        ("I prefer cooperative work environments.", 1),
    ],
    "emotional_stability": [
        ("I stay calm when facing uncertainty or pressure.", 1),
        ("I often feel overwhelmed by career decisions.", -1),
        ("I can recover quickly after setbacks.", 1),
    ],
}

RIASEC_ITEMS = {
    "R": ["Building, fixing, or working with practical tools", "Operating systems, equipment, or physical processes"],
    "I": ["Researching, analysing data, and solving complex problems", "Finding patterns and explaining why things happen"],
    "A": ["Creating designs, stories, visuals, or original content", "Expressing ideas through creative formats"],
    "S": ["Helping, teaching, coaching, or understanding people", "Supporting others' growth or wellbeing"],
    "E": ["Persuading, leading, selling, or starting initiatives", "Pitching ideas and influencing decisions"],
    "C": ["Organising information, following procedures, and managing details", "Working with records, reports, and structured systems"],
}

VALUE_ITEMS = {
    "growth": "Fast learning and career progression",
    "stability": "Stable work and predictable structure",
    "income": "High earning potential",
    "impact": "Meaningful contribution to people or society",
    "autonomy": "Freedom and flexibility",
    "leadership": "Influence, responsibility, and leadership"
}

SKILL_LIST = ["Excel", "SQL", "Python", "Communication", "Writing", "Presentation", "Problem Solving", "Dashboarding", "Figma", "Research Methods"]

IDENTITY_RULES = [
    ("Analytical Strategist", lambda big5, riasec, values: big5["conscientiousness"] >= 65 and riasec["I"] >= 60),
    ("Structured Operations Planner", lambda big5, riasec, values: big5["conscientiousness"] >= 70 and riasec["C"] >= 55),
    ("People-Centred Developer", lambda big5, riasec, values: big5["agreeableness"] >= 70 and riasec["S"] >= 60),
    ("Creative Market Builder", lambda big5, riasec, values: big5["openness"] >= 70 and (riasec["A"] >= 55 or riasec["E"] >= 55)),
    ("Product-Oriented Problem Solver", lambda big5, riasec, values: big5["openness"] >= 60 and riasec["I"] >= 50 and riasec["E"] >= 45),
]

IDENTITY_FALLBACK = "Adaptive Career Explorer"

# -----------------------------
# Utility functions
# -----------------------------
def normalize_likert(score, reverse=False):
    if reverse:
        score = 6 - score
    return (score - 1) / 4 * 100

def cosine_similarity(a, b):
    keys = sorted(set(a.keys()) | set(b.keys()))
    av = np.array([a.get(k, 0) for k in keys], dtype=float)
    bv = np.array([b.get(k, 0) for k in keys], dtype=float)
    denom = np.linalg.norm(av) * np.linalg.norm(bv)
    if denom == 0:
        return 0
    return float(np.dot(av, bv) / denom)

def score_big5(responses):
    scores = {}
    for trait, items in BIG5_ITEMS.items():
        vals = []
        for text, direction in items:
            val = responses.get(f"big5::{trait}::{text}", 3)
            vals.append(normalize_likert(val, reverse=(direction == -1)))
        scores[trait] = int(round(np.mean(vals)))
    return scores

def score_riasec(responses):
    scores = {}
    for code, items in RIASEC_ITEMS.items():
        vals = []
        for item in items:
            vals.append(responses.get(f"riasec::{code}::{item}", 3))
        scores[code] = int(round((np.mean(vals) - 1) / 4 * 100))
    return scores

def score_values(responses):
    scores = {}
    for key, label in VALUE_ITEMS.items():
        scores[key] = int(round((responses.get(f"value::{key}", 3) - 1) / 4 * 100))
    total = sum(scores.values()) or 1
    normalized = {k: v / total for k, v in scores.items()}
    return scores, normalized

def infer_mbti_style(big5):
    # This is not a clinical MBTI classifier. It creates a simple work-style signal for demo purposes.
    e_i = "E" if big5["extraversion"] >= 55 else "I"
    s_n = "N" if big5["openness"] >= 55 else "S"
    t_f = "F" if big5["agreeableness"] >= 60 else "T"
    j_p = "J" if big5["conscientiousness"] >= 60 else "P"
    return e_i + s_n + t_f + j_p

def infer_identity(big5, riasec, values_raw):
    for name, rule in IDENTITY_RULES:
        if rule(big5, riasec, values_raw):
            return name
    return IDENTITY_FALLBACK

def calculate_role_matches(big5, riasec, skills, values_norm, readiness):
    user_big5 = {k: v / 100 for k, v in big5.items()}
    user_riasec = {k: v / 100 for k, v in riasec.items()}
    user_skills = {k: v for k, v in skills.items()}
    rows = []

    for role, data in ROLES.items():
        personality_fit = cosine_similarity(user_big5, data["personality"]) * 100
        interest_fit = cosine_similarity(user_riasec, data["riasec"]) * 100

        required = data["skills"]
        skill_fit_components = []
        missing = []
        for skill, req in required.items():
            current = user_skills.get(skill, 0)
            fit = min(current / req, 1.0) * 100 if req > 0 else 100
            skill_fit_components.append(fit)
            gap = max(req - current, 0)
            if gap >= 20:
                missing.append((skill, current, req, "High"))
            elif gap >= 10:
                missing.append((skill, current, req, "Medium"))
            elif gap > 0:
                missing.append((skill, current, req, "Low"))

        skill_fit = float(np.mean(skill_fit_components)) if skill_fit_components else 0
        value_fit = cosine_similarity(values_norm, data["values"]) * 100
        readiness_fit = readiness

        total = (
            personality_fit * 0.22
            + interest_fit * 0.23
            + skill_fit * 0.30
            + value_fit * 0.15
            + readiness_fit * 0.10
        )

        rows.append({
            "Role": role,
            "Family": data["family"],
            "Fit Score": round(total, 1),
            "Personality Fit": round(personality_fit, 1),
            "Interest Fit": round(interest_fit, 1),
            "Skill Fit": round(skill_fit, 1),
            "Value Fit": round(value_fit, 1),
            "Readiness Fit": round(readiness_fit, 1),
            "Description": data["description"],
            "Entry Titles": ", ".join(data["entry_titles"]),
            "Portfolio Project": data["portfolio"],
            "Missing": missing
        })

    return pd.DataFrame(rows).sort_values("Fit Score", ascending=False).reset_index(drop=True)

def build_skill_gap_df(role_name, skills):
    required = ROLES[role_name]["skills"]
    rows = []
    for skill, req in required.items():
        current = skills.get(skill, 0)
        gap = max(req - current, 0)
        if gap >= 20:
            level = "High"
        elif gap >= 10:
            level = "Medium"
        elif gap > 0:
            level = "Low"
        else:
            level = "Ready"
        rows.append({"Skill": skill, "Current": current, "Required": req, "Gap": gap, "Gap Level": level})
    return pd.DataFrame(rows).sort_values(["Gap", "Required"], ascending=False)

def generate_roadmap(top_role, skill_gap_df):
    high_gaps = skill_gap_df[skill_gap_df["Gap Level"].isin(["High", "Medium"])]["Skill"].tolist()
    priority_skills = high_gaps[:3] if high_gaps else skill_gap_df["Skill"].head(3).tolist()
    portfolio = ROLES[top_role]["portfolio"]

    return [
        {
            "Period": "Week 1–2",
            "Goal": "Clarify target positioning",
            "Actions": [
                f"Choose {top_role} as the primary target role and select one secondary role.",
                "Rewrite resume headline and LinkedIn summary around the target role family.",
                f"Review 10 job descriptions and extract repeated requirements for {top_role}."
            ]
        },
        {
            "Period": "Week 3–5",
            "Goal": "Close priority skill gaps",
            "Actions": [
                f"Focus on: {', '.join(priority_skills)}.",
                "Complete one compact learning module or tutorial for each priority skill.",
                "Create short evidence notes showing how each skill is used in real work."
            ]
        },
        {
            "Period": "Week 6–8",
            "Goal": "Build employability evidence",
            "Actions": [
                portfolio,
                "Document the project with problem, method, output, and business value.",
                "Ask one peer, mentor, or lecturer to review the project."
            ]
        },
        {
            "Period": "Week 9–12",
            "Goal": "Convert readiness into applications",
            "Actions": [
                "Apply to 20 aligned entry-level roles or graduate programmes.",
                "Prepare 6 STAR interview stories linked to strengths and project evidence.",
                "Track applications weekly and refine keywords, resume, and portfolio."
            ]
        }
    ]

def make_report_text(name, identity, mbti_style, big5, riasec, values_raw, matches_df, top_role, gap_df, roadmap):
    lines = []
    lines.append("CareerFit AI Candidate Report")
    lines.append("=" * 34)
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Candidate: {name or 'Demo Candidate'}")
    lines.append("")
    lines.append(f"Career Identity: {identity}")
    lines.append(f"MBTI-inspired work-style signal: {mbti_style}")
    lines.append("")
    lines.append("Big Five Profile")
    for k, v in big5.items():
        lines.append(f"- {k.replace('_', ' ').title()}: {v}/100")
    lines.append("")
    lines.append("RIASEC Interest Profile")
    for k, v in sorted(riasec.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"- {k}: {v}/100")
    lines.append("")
    lines.append("Work Values")
    for k, v in sorted(values_raw.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"- {VALUE_ITEMS[k]}: {v}/100")
    lines.append("")
    lines.append("Top Role Matches")
    for _, row in matches_df.head(5).iterrows():
        lines.append(f"- {row['Role']}: {row['Fit Score']}% | {row['Description']}")
    lines.append("")
    lines.append(f"Skill Gap Diagnosis for {top_role}")
    for _, row in gap_df.iterrows():
        lines.append(f"- {row['Skill']}: current {row['Current']}, required {row['Required']}, gap {row['Gap']} ({row['Gap Level']})")
    lines.append("")
    lines.append("90-Day Roadmap")
    for block in roadmap:
        lines.append(f"{block['Period']} | {block['Goal']}")
        for action in block["Actions"]:
            lines.append(f"- {action}")
    return "\n".join(lines)

def default_responses():
    responses = {}
    for trait, items in BIG5_ITEMS.items():
        for text, _direction in items:
            responses[f"big5::{trait}::{text}"] = 3
    for code, items in RIASEC_ITEMS.items():
        for item in items:
            responses[f"riasec::{code}::{item}"] = 3
    for key in VALUE_ITEMS.keys():
        responses[f"value::{key}"] = 3
    return responses

# -----------------------------
# Session state
# -----------------------------
if "responses" not in st.session_state:
    st.session_state.responses = default_responses()
if "skills" not in st.session_state:
    st.session_state.skills = {skill: 50 for skill in SKILL_LIST}
if "readiness" not in st.session_state:
    st.session_state.readiness = {
        "resume": 50,
        "portfolio": 30,
        "interview": 40,
        "job_search": 35,
        "industry_clarity": 45
    }

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🧭 CareerFit AI")
st.sidebar.caption("Multi-dimensional career identity and role-fit engine")
page = st.sidebar.radio(
    "Navigation",
    ["1. Assessment", "2. Career Profile", "3. Role Matching", "4. Skill Gap & Roadmap", "5. Employer Dashboard", "6. Export Report"]
)
st.sidebar.divider()
candidate_name = st.sidebar.text_input("Candidate name", value="Demo Candidate")
target_market = st.sidebar.selectbox("Target market", ["Malaysia", "China", "Singapore", "APAC", "Global"], index=0)
st.sidebar.caption("Note: This demo uses transparent scoring rules. AI API integration can be added later for dynamic narrative generation.")

# -----------------------------
# Header
# -----------------------------
st.title("CareerFit AI")
st.subheader("A multi-dimensional career identity and role-fit engine for graduates")
st.write(
    "This prototype combines MBTI-inspired work-style signals, Big Five personality, RIASEC interests, skills, work values, "
    "and career readiness to generate role-fit scores, skill gaps, a 90-day roadmap, and employer-facing candidate summaries."
)

# -----------------------------
# Page 1: Assessment
# -----------------------------
if page == "1. Assessment":
    st.header("1. Multi-Dimensional Assessment")
    st.info("Use the sliders to simulate a graduate career assessment. The current version is rule-based and explainable, suitable for a hackathon demo.")

    tab1, tab2, tab3, tab4 = st.tabs(["Personality", "Career Interests", "Skills", "Values & Readiness"])

    with tab1:
        st.subheader("Big Five Personality Signals")
        st.write("1 = Strongly disagree, 5 = Strongly agree")
        for trait, items in BIG5_ITEMS.items():
            st.markdown(f"**{trait.replace('_', ' ').title()}**")
            for text, _direction in items:
                key = f"big5::{trait}::{text}"
                st.session_state.responses[key] = st.slider(text, 1, 5, st.session_state.responses.get(key, 3), key=key)

    with tab2:
        st.subheader("RIASEC / Holland-Style Career Interests")
        st.write("1 = Not interested, 5 = Very interested")
        riasec_names = {
            "R": "Realistic",
            "I": "Investigative",
            "A": "Artistic",
            "S": "Social",
            "E": "Enterprising",
            "C": "Conventional"
        }
        for code, items in RIASEC_ITEMS.items():
            st.markdown(f"**{code} — {riasec_names[code]}**")
            for item in items:
                key = f"riasec::{code}::{item}"
                st.session_state.responses[key] = st.slider(item, 1, 5, st.session_state.responses.get(key, 3), key=key)

    with tab3:
        st.subheader("Current Skill Profile")
        st.write("0 = no exposure, 100 = strong evidence of ability")
        cols = st.columns(2)
        for idx, skill in enumerate(SKILL_LIST):
            with cols[idx % 2]:
                st.session_state.skills[skill] = st.slider(skill, 0, 100, st.session_state.skills.get(skill, 50), 5, key=f"skill::{skill}")

    with tab4:
        st.subheader("Work Values")
        st.write("1 = Low priority, 5 = Very high priority")
        cols = st.columns(2)
        for idx, (key_name, label) in enumerate(VALUE_ITEMS.items()):
            with cols[idx % 2]:
                key = f"value::{key_name}"
                st.session_state.responses[key] = st.slider(label, 1, 5, st.session_state.responses.get(key, 3), key=key)

        st.subheader("Career Readiness")
        st.write("0 = not ready, 100 = highly ready")
        for key_name, label in {
            "resume": "Resume / CV readiness",
            "portfolio": "Portfolio or project evidence",
            "interview": "Interview confidence",
            "job_search": "Job-search routine",
            "industry_clarity": "Industry and role clarity"
        }.items():
            st.session_state.readiness[key_name] = st.slider(label, 0, 100, st.session_state.readiness.get(key_name, 50), 5, key=f"readiness::{key_name}")

    st.success("Assessment data updated. Open the Career Profile page to see the generated result.")

# Calculate outputs
big5 = score_big5(st.session_state.responses)
riasec = score_riasec(st.session_state.responses)
values_raw, values_norm = score_values(st.session_state.responses)
readiness_score = int(round(np.mean(list(st.session_state.readiness.values()))))
mbti_style = infer_mbti_style(big5)
identity = infer_identity(big5, riasec, values_raw)
matches_df = calculate_role_matches(big5, riasec, st.session_state.skills, values_norm, readiness_score)
top_role = matches_df.iloc[0]["Role"]
gap_df = build_skill_gap_df(top_role, st.session_state.skills)
roadmap = generate_roadmap(top_role, gap_df)

# -----------------------------
# Page 2: Career Profile
# -----------------------------
if page == "2. Career Profile":
    st.header("2. Career Identity Profile")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Career Identity", identity)
    c2.metric("MBTI-style signal", mbti_style)
    c3.metric("Career Readiness", f"{readiness_score}/100")
    c4.metric("Top Role", top_role)

    st.divider()

    left, right = st.columns([1, 1])

    with left:
        st.subheader("Big Five Profile")
        big5_df = pd.DataFrame({"Trait": [k.replace("_", " ").title() for k in big5.keys()], "Score": list(big5.values())})
        st.bar_chart(big5_df.set_index("Trait"))

    with right:
        st.subheader("RIASEC Interest Profile")
        riasec_names = {"R": "Realistic", "I": "Investigative", "A": "Artistic", "S": "Social", "E": "Enterprising", "C": "Conventional"}
        riasec_df = pd.DataFrame({
            "Dimension": [f"{k} - {riasec_names[k]}" for k in riasec.keys()],
            "Score": list(riasec.values())
        })
        st.bar_chart(riasec_df.set_index("Dimension"))

    st.subheader("Work Values Ranking")
    values_df = pd.DataFrame({
        "Value": [VALUE_ITEMS[k] for k in values_raw.keys()],
        "Score": list(values_raw.values())
    }).sort_values("Score", ascending=False)
    st.dataframe(values_df, use_container_width=True, hide_index=True)

    st.subheader("Interpretive Summary")
    top_traits = sorted(big5.items(), key=lambda x: x[1], reverse=True)[:2]
    top_interests = sorted(riasec.items(), key=lambda x: x[1], reverse=True)[:2]
    top_values = sorted(values_raw.items(), key=lambda x: x[1], reverse=True)[:2]
    st.write(
        f"{candidate_name} is currently classified as **{identity}**. The strongest personality signals are "
        f"**{top_traits[0][0].replace('_',' ').title()}** and **{top_traits[1][0].replace('_',' ').title()}**. "
        f"The strongest career interest codes are **{top_interests[0][0]}** and **{top_interests[1][0]}**. "
        f"The highest work values are **{VALUE_ITEMS[top_values[0][0]]}** and **{VALUE_ITEMS[top_values[1][0]]}**. "
        f"The MBTI-inspired work-style signal is **{mbti_style}**, used here only as a communication-friendly profile label rather than a clinical or deterministic assessment."
    )

# -----------------------------
# Page 3: Role Matching
# -----------------------------
if page == "3. Role Matching":
    st.header("3. Role-Fit Matching Engine")
    st.write("Role Fit Score = Personality Fit × 22% + Interest Fit × 23% + Skill Fit × 30% + Value Fit × 15% + Readiness Fit × 10%")

    display_cols = ["Role", "Family", "Fit Score", "Personality Fit", "Interest Fit", "Skill Fit", "Value Fit", "Readiness Fit", "Entry Titles"]
    st.dataframe(matches_df[display_cols], use_container_width=True, hide_index=True)

    st.subheader("Top 3 Recommendations")
    cols = st.columns(3)
    for idx, (_, row) in enumerate(matches_df.head(3).iterrows()):
        with cols[idx]:
            st.metric(row["Role"], f"{row['Fit Score']}%")
            st.caption(row["Family"])
            st.write(row["Description"])
            st.markdown("**Entry-level titles**")
            st.write(row["Entry Titles"])

    st.subheader("Fit Composition")
    selected_role = st.selectbox("Select a role to inspect", matches_df["Role"].tolist())
    selected = matches_df[matches_df["Role"] == selected_role].iloc[0]
    composition = pd.DataFrame({
        "Component": ["Personality Fit", "Interest Fit", "Skill Fit", "Value Fit", "Readiness Fit"],
        "Score": [selected["Personality Fit"], selected["Interest Fit"], selected["Skill Fit"], selected["Value Fit"], selected["Readiness Fit"]]
    })
    st.bar_chart(composition.set_index("Component"))

# -----------------------------
# Page 4: Skill Gap & Roadmap
# -----------------------------
if page == "4. Skill Gap & Roadmap":
    st.header("4. Skill Gap Diagnosis and 90-Day Roadmap")
    selected_role = st.selectbox("Select target role", matches_df["Role"].tolist(), index=0)
    selected_gap_df = build_skill_gap_df(selected_role, st.session_state.skills)
    selected_roadmap = generate_roadmap(selected_role, selected_gap_df)

    st.subheader(f"Skill Gap for {selected_role}")
    st.dataframe(selected_gap_df, use_container_width=True, hide_index=True)

    st.subheader("Priority Development Areas")
    priority = selected_gap_df[selected_gap_df["Gap Level"].isin(["High", "Medium"])]
    if priority.empty:
        st.success("No major skill gap detected. The candidate is relatively ready for this role.")
    else:
        for _, row in priority.head(5).iterrows():
            st.warning(f"{row['Skill']}: current {row['Current']} / required {row['Required']} — {row['Gap Level']} gap")

    st.subheader("90-Day Career Readiness Roadmap")
    for block in selected_roadmap:
        with st.expander(f"{block['Period']} — {block['Goal']}", expanded=True):
            for action in block["Actions"]:
                st.write(f"- {action}")

# -----------------------------
# Page 5: Employer Dashboard
# -----------------------------
if page == "5. Employer Dashboard":
    st.header("5. Employer-Facing Talent Fit Dashboard")

    c1, c2, c3 = st.columns(3)
    c1.metric("Candidate", candidate_name)
    c2.metric("Best-Fit Role", top_role)
    c3.metric("Fit Score", f"{matches_df.iloc[0]['Fit Score']}%")

    st.subheader("Candidate Fit Summary")
    st.write(
        f"**{candidate_name}** shows the strongest fit for **{top_role}** in the **{matches_df.iloc[0]['Family']}** family. "
        f"The candidate's profile suggests a **{identity}** orientation, with strongest evidence in "
        f"**{sorted(big5.items(), key=lambda x: x[1], reverse=True)[0][0].replace('_',' ').title()}** and "
        f"**{sorted(riasec.items(), key=lambda x: x[1], reverse=True)[0][0]}-type career interests**."
    )

    left, right = st.columns([1, 1])
    with left:
        st.subheader("Role Suitability")
        top5 = matches_df.head(5)[["Role", "Fit Score"]].set_index("Role")
        st.bar_chart(top5)

    with right:
        st.subheader("Readiness Signals")
        readiness_df = pd.DataFrame({
            "Area": [k.replace("_", " ").title() for k in st.session_state.readiness.keys()],
            "Score": list(st.session_state.readiness.values())
        })
        st.dataframe(readiness_df, use_container_width=True, hide_index=True)

    st.subheader("Suggested Interview Focus")
    interview_questions = [
        f"Ask the candidate to describe a project where they demonstrated skills relevant to {top_role}.",
        f"Probe the main skill gap for {top_role}: {gap_df.iloc[0]['Skill']} if the candidate has limited evidence in this area.",
        "Ask for a STAR example showing how the candidate handles uncertainty, deadlines, or collaboration.",
        "Assess whether the candidate prefers structured guidance, autonomy, people interaction, or analytical depth.",
        f"Ask the candidate to explain how their {identity} profile would contribute to the team."
    ]
    for i, q in enumerate(interview_questions, 1):
        st.write(f"{i}. {q}")

    st.subheader("Platform Value for Talentbank")
    st.info(
        "This module can support Career OS by converting graduate self-assessment into structured candidate profiles, "
        "role-fit scores, skill-gap diagnostics, and employer-readable interview guidance. It creates value for students, employers, and the platform."
    )

# -----------------------------
# Page 6: Export
# -----------------------------
if page == "6. Export Report":
    st.header("6. Export Candidate Report")
    report_text = make_report_text(
        candidate_name,
        identity,
        mbti_style,
        big5,
        riasec,
        values_raw,
        matches_df,
        top_role,
        gap_df,
        roadmap
    )

    st.text_area("Report Preview", report_text, height=520)

    st.download_button(
        label="Download TXT Report",
        data=report_text.encode("utf-8"),
        file_name=f"CareerFit_AI_Report_{candidate_name.replace(' ', '_')}.txt",
        mime="text/plain"
    )

    csv_buffer = io.StringIO()
    matches_df.drop(columns=["Missing"]).to_csv(csv_buffer, index=False)
    st.download_button(
        label="Download Role Matching CSV",
        data=csv_buffer.getvalue().encode("utf-8"),
        file_name=f"CareerFit_AI_Role_Matches_{candidate_name.replace(' ', '_')}.csv",
        mime="text/csv"
    )

st.divider()
st.caption(
    "Prototype note: This demo is designed for hackathon presentation. The scoring model is transparent and explainable. "
    "For a production version, psychometric validation, benchmark datasets, privacy controls, and API-based career intelligence should be added."
)
