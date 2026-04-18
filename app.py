import streamlit as st
import tempfile
import os
import pandas as pd
from utils import extract_text_from_pdf, clean_text, calculate_similarity, get_keyword_density
from skills import extract_skills, get_missing_skills

# Set up page configurations
st.set_page_config(page_title="AI Resume Scanner | Premium", page_icon="📄", layout="wide")

# Load Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if os.path.exists("style.css"):
    local_css("style.css")

# Navbar
st.markdown("""
    <div class="navbar">
        <div class="nav-logo">📄 AI RESUME SCANNER</div>
        <div style="color: #666; font-size: 0.8rem;">PREMIUM AI ANALYSIS</div>
    </div>
""", unsafe_allow_html=True)

# Footer Function
def draw_footer():
    st.markdown("""
        <div class="footer">
            <div class="footer-text">
                <b>AI Resume Scanner</b> • Build with Precision & NLP<br>
                © 2026 Professional Career Insights • All Rights Reserved
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'view' not in st.session_state:
    st.session_state.view = 'input'
if 'results' not in st.session_state:
    st.session_state.results = None

# Sidebar Content
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/942/942748.png", width=80)
    st.title("Settings")
    
    if st.session_state.view == 'result':
        if st.button("🔄 New Analysis", use_container_width=True):
            st.session_state.view = 'input'
            st.session_state.results = None
            st.rerun()
            
    st.divider()
    st.markdown("""
    ### Tips for Excellence
    1. **Quantify Results**: Use numbers in your experience.
    2. **Skill Density**: Mention primary tools 2-3 times.
    3. **Clean Formatting**: Avoid complex tables in PDFs.
    """)

# --- MAIN APP LOGIC ---

if st.session_state.view == 'input':
    # --- INPUT VIEW ---
    st.title("📄 AI Resume Scanner")
    st.markdown("##### Upload your resume and paste the job targets to generate your AI compatibility report.")
    
    st.write("")
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 📁 Your Resume")
        uploaded_file = st.file_uploader("Upload PDF version", type=["pdf"])

    with col2:
        st.markdown("### 💼 Job Targets")
        job_description = st.text_area("Paste job requirements here", height=200, placeholder="We are looking for a candidate who...")

    st.write("")
    if st.button("✨ Generate Profile Report", use_container_width=True):
        if not uploaded_file or not job_description.strip():
            st.warning("Please provide both a resume and a job description.")
        else:
            with st.spinner("🧠 AI involves deep analysis of your fit..."):
                try:
                    # File Processing
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                        temp_file.write(uploaded_file.read())
                        temp_pdf_path = temp_file.name

                    resume_text = extract_text_from_pdf(temp_pdf_path)
                    if os.path.exists(temp_pdf_path): os.remove(temp_pdf_path)

                    if resume_text:
                        # Computation
                        c_res = clean_text(resume_text)
                        c_jd = clean_text(job_description)
                        
                        st.session_state.results = {
                            "score": calculate_similarity(c_res, c_jd),
                            "found": extract_skills(c_res),
                            "missing": get_missing_skills(extract_skills(c_res), extract_skills(c_jd)),
                            "keywords": get_keyword_density(c_jd),
                            "cleaned_res": c_res,
                            "jd_skills": extract_skills(c_jd)
                        }
                        st.session_state.view = 'result'
                        st.rerun()
                    else:
                        st.error("Error reading PDF content.")
                except Exception as e:
                    st.error(f"Analysis Error: {str(e)}")

elif st.session_state.view == 'result' and st.session_state.results:
    # --- RESULT VIEW (The Report Dashboard) ---
    res = st.session_state.results
    
    # Header Action Bar
    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.title("📊 Analysis Report")
    with h_col2:
        if st.button("⬅️ Edit Inputs", use_container_width=True):
            st.session_state.view = 'input'
            st.rerun()

    st.divider()

    # Impact Row (Integrated Verdict)
    m_col1, m_col2 = st.columns([1.5, 2.5])
    with m_col1:
        score = res["score"]
        st.metric("Compatibility Match", f"{score}%")
        st.progress(score/100)
    
    with m_col2:
        # Integrated verdict instead of a giant box
        if score >= 80:
            st.success(f"**Elite Fit Identified!** {score}% compatibility means your profile is exceptional for this role. You are safe from most ATS filtration.")
            st.balloons()
        elif score >= 50:
            st.warning(f"**Good Potential.** At {score}%, you have the core skillset. Focus on adding the specific keywords highlighted in the analysis below.")
        else:
            st.error(f"**Gap Detected.** Your {score}% score suggests major missing keywords. We recommend a strategic rewrite to match the requirements.")

    st.write("")
    st.divider()
    
    # Interactive Analysis Tabs
    st.markdown("### 🛠️ Strategic Analysis Dashboard")
    t1, t2, t3 = st.tabs(["🚀 Skills Detected", "📉 Missing Gaps", "🔥 JD Keywords"])
    
    with t1:
        total = sum(len(s) for s in res["found"].values())
        if total == 0:
            st.info("No industry-specific skills were detected. Ensure your resume uses standard professional terminology.")
        else:
            st.caption(f"We identified {total} strengths in your profile. Click each category to explore:")
            for cat, skills in res["found"].items():
                if skills:
                    with st.expander(f"📦 {cat} ({len(skills)} found)", expanded=True):
                        skill_html = "".join([f'<span class="skill-tag skill-found">{s.title()}</span>' for s in sorted(skills)])
                        st.markdown(skill_html, unsafe_allow_html=True)

    with t2:
        jd_skills = res["jd_skills"]
        has_jd_skills = any(len(s) > 0 for s in jd_skills.values())
        
        if not has_jd_skills:
            st.info("The provided JD lacks specific technical keyword targets for Categorized Gaps.")
        else:
            missing_total = sum(len(s) for s in res["missing"].values())
            if missing_total == 0:
                st.success("Perfect alignment! You possess all specific industry skills required.")
            else:
                st.caption(f"Critical Gaps: Found {missing_total} missing skill targets. Expanding your profile in these areas will boost your score.")
                for cat, skills in res["missing"].items():
                    if skills:
                        with st.expander(f"⚠️ Missing {cat} ({len(skills)})", expanded=True):
                            skill_html = "".join([f'<span class="skill-tag skill-missing">{s.title()}</span>' for s in sorted(skills)])
                            st.markdown(skill_html, unsafe_allow_html=True)
        
        # Keyword Fallback (Always useful)
        missing_kw = [k for k, v in res["keywords"] if k.lower() not in res["cleaned_res"]]
        if missing_kw:
            st.write("")
            st.markdown("#### 🔍 Essential Keywords to Inject")
            st.caption("These words are frequent in the Job Description but missing from your resume:")
            kw_html = "".join([f'<span class="skill-tag" style="background: rgba(255,103,0,0.1); color: var(--accent-color); border: 1px solid rgba(255,103,0,0.2);">{k.title()}</span>' for k in missing_kw[:12]])
            st.markdown(kw_html, unsafe_allow_html=True)

    with t3:
        if res["keywords"]:
            st.markdown("#### Mentions Density")
            df = pd.DataFrame(res["keywords"], columns=["Keyword", "Count"])
            st.bar_chart(df.set_index("Keyword"), color="#005a32")
        else:
            st.info("Insufficient data for visualization.")

# End of script - Draw Footer
draw_footer()
