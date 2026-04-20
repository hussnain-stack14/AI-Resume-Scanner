import streamlit as st
import tempfile
import os
import pandas as pd
from utils import extract_text_from_pdf, clean_text, calculate_similarity, get_keyword_density
from skills import extract_skills, get_missing_skills

# --- SEO & PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ResumeAI Pro | Premium ATS Scanner", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Meta tags for SEO through raw HTML (Best effort mapping to SEO in Streamlit)
st.markdown("""
    <head>
        <meta name="description" content="Premium AI Resume Scanner. Optimize your resume for ATS systems and secure your dream job.">
        <meta name="keywords" content="AI, Resume Scanner, ATS, Career, Developer Portfolio">
        <meta name="author" content="Hussnain">
    </head>
""", unsafe_allow_html=True)

# --- CSS LOADING ---
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            
local_css("style.css")

# --- UI COMPONENTS ---
st.markdown("""
    <div class="custom-navbar">
        <div class="nav-brand">
            <span class="highlight">ResumeAI</span> <span class="nav-badge">PRO</span>
        </div>
    </div>
""", unsafe_allow_html=True)

def draw_footer():
    st.markdown("""
        <div class="custom-footer">
            <div class="footer-header">⚡ ResumeAI Pro</div>
            <div>Architected with precision using Python, NLP & Modern UI/UX principles.</div>
            <div style="margin-top: 15px;">
                Designed for optimal performance • <a href="https://github.com/hussnain-stack14" class="footer-link" target="_blank">View GitHub Profile</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'view' not in st.session_state:
    st.session_state.view = 'input'
if 'results' not in st.session_state:
    st.session_state.results = None

# --- CORE APPLICATION FLOW ---

if st.session_state.view == 'input':
    # --- HERO SECTION ---
    st.write("")
    st.title("Optimize Your Career Trajectory")
    st.markdown("<p style='font-size: 1.2rem; max-width: 800px;' class='dynamic-text'>Leverage advanced Natural Language Processing to analyze your resume against targeted job descriptions. Uncover missing skills and beat the ATS algorithms instantly.</p>", unsafe_allow_html=True)
    
    with st.expander("💡 Pro Optimization Tips & Settings"):
        st.markdown("""
        - **Quantify Impact**: Use metrics (e.g., "Increased sales by 20%").
        - **Density matters**: Include primary keywords 2-3 times naturally.
        - **Clean Structure**: Avoid complex multi-column layouts that confuse parsers.
        - **Standard Headings**: Use standard section names like *Experience*, *Education*.
        """)

    st.write("")
    st.write("")
    
    # 2 Column Layout
    col1, col2 = st.columns([1, 1], gap="large")

    # Custom Section Header Helper
    def section_header(icon, title, desc):
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
            <div style="background: var(--primary-lighter); width: 55px; height: 55px; border-radius: 14px; display: flex; justify-content: center; align-items: center; font-size: 1.8rem; box-shadow: var(--shadow-sm); border: 2px solid var(--primary-light); flex-shrink: 0;">
                {icon}
            </div>
            <div>
                <h3 style="margin: 0 !important; padding: 0 !important; font-size: 1.4rem !important; letter-spacing: -0.5px;">{title}</h3>
                <p style='font-size: 0.9rem; margin: 0; padding-top: 2px;' class='dynamic-text'>{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        section_header("📄", "1. Upload Resume", "Upload your current professional resume in PDF format.")
        uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed", help="Supported formats: PDF. Ensure your document is a text-based PDF and not a scanned image.")

    with col2:
        section_header("🎯", "2. Define Target", "Paste the exact requirements and skills of your dream job.")
        job_description = st.text_area("", height=220, placeholder="Example: We are looking for a Senior Developer with 5+ years of experience in Python, React, and AWS... \n\n(Tip: Copy/paste the entire JD here)", label_visibility="collapsed", help="Paste the complete job description text to maximize skill matching accuracy.")

    st.write("")
    st.write("")
    
    # Call to Action (CTA)
    cta_col1, cta_col2, cta_col3 = st.columns([1, 2, 1])
    with cta_col2:
        if st.button("🚀 Execute Neural Analysis", use_container_width=True):
            if not uploaded_file:
                st.error("⚠️ Action Required: Please upload your resume PDF.")
            elif not job_description.strip():
                st.error("⚠️ Action Required: Please paste the target job description.")
            elif len(job_description.split()) < 20:
                st.warning("⚠️ The job description appears too short for an accurate analysis. Consider pasting the fully detailed requirements.")
            else:
                with st.status("🧠 Initializing deep semantic scanning protocol...", expanded=True) as status:
                    try:
                        st.write("📄 Processing Resume PDF Structure...")
                        # Secure & Optimized File Handling
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                            temp_file.write(uploaded_file.read())
                            temp_pdf_path = temp_file.name

                        resume_text = extract_text_from_pdf(temp_pdf_path)
                        if os.path.exists(temp_pdf_path): 
                            os.remove(temp_pdf_path)

                        if resume_text:
                            st.write("✨ Applying NLP text sanitization...")
                            # Clean and Process data via utils.py and skills.py
                            c_res = clean_text(resume_text)
                            c_jd = clean_text(job_description)
                            
                            st.write("🧩 Extracting entities and computing semantic distance...")
                            st.session_state.results = {
                                "score": calculate_similarity(c_res, c_jd),
                                "found": extract_skills(c_res),
                                "missing": get_missing_skills(extract_skills(c_res), extract_skills(c_jd)),
                                "keywords": get_keyword_density(c_jd),
                                "cleaned_res": c_res,
                                "jd_skills": extract_skills(c_jd)
                            }
                            status.update(label="Neural Scan Complete! Rendering Dashboard...", state="complete", expanded=False)
                            st.toast("Analysis Successful!", icon="🎉")
                            st.session_state.view = 'result'
                            st.rerun()
                        else:
                            status.update(label="Extraction Failed", state="error", expanded=True)
                            st.error("❌ Extraction Failed: Unable to read text from the provided PDF. Try a digitally generated or flattened text PDF.")
                    except Exception as e:
                        status.update(label="System Error Encountered", state="error", expanded=True)
                        st.error(f"⚠️ Core Engine Error: {str(e)}")

elif st.session_state.view == 'result' and st.session_state.results:
    # --- RESULT DASHBOARD ---
    res = st.session_state.results
    
    # Dashboard Header Bar
    h_col1, h_col2 = st.columns([4, 1])
    with h_col1:
        st.title("📊 Intelligence Report")
        st.markdown("<p style='font-size: 1.1rem; margin-top: -15px;' class='dynamic-text'>Comprehensive breakdown of your ATS compatibility.</p>", unsafe_allow_html=True)
    with h_col2:
        st.write("")
        if st.button("⬅️ Modify Inputs", use_container_width=True):
            st.session_state.view = 'input'
            st.rerun()

    st.write("")

    # Highlight Metric Block
    m_col1, m_col2, m_col3 = st.columns([1.5, 1, 2.5], gap="large")
    
    with m_col1:
        score = res["score"]
        st.metric("Neural Match Score", f"{score}%")
        st.progress(score/100)
        
    with m_col2:
        total_found = sum(len(s) for s in res["found"].values())
        missing_total = sum(len(s) for s in res["missing"].values())
        st.metric("Verified Skills", total_found)
        st.metric("Missing Skills", missing_total)
    
    with m_col3:
        st.markdown("### System Verdict")
        if score >= 80:
            st.success(f"🌟 **Elite Fit Identified!** An {score}% compatibility places you in the top tier of applicants. You are highly protected against automated ATS filtration triggers.")
            st.balloons()
        elif score >= 50:
            st.warning(f"⚖️ **Competitive Potential.** At {score}%, you demonstrate core competency. Strategic injection of missing semantic keywords will elevate this to an elite score.")
        else:
            st.error(f"📉 **Critical Gap Detected.** A {score}% score indicates substantial divergence from expected profiles. A targeted structural rewrite is strongly recommended.")

    st.write("")
    st.divider()
    
    # Tabbed Interface for Advanced Interaction
    st.markdown("### 🛠️ Extracted Metadata Analysis")
    t1, t2, t3 = st.tabs(["🚀 Verified Strengths", "🎯 Missing Requirements", "📈 Keyword Distribution"])
    
    # Helper to generate tags
    def generate_tags(skills_list, css_class):
        html = '<div class="skill-container">'
        icon = "✨" if "found" in css_class else "⚠️"
        for s in sorted(skills_list):
            html += f'<span class="skill-tag {css_class}"><span style="margin-right: 4px;">{icon}</span> {s.title()}</span>'
        html += '</div>'
        return html

    with t1:
        total = sum(len(s) for s in res["found"].values())
        if total == 0:
            st.info("No industry-specific technical entities were detected. Try adopting more standard professional nomenclature.")
        else:
            st.markdown(f"<p style='margin-bottom: 20px;' class='dynamic-text'>Engine identified <b>{total}</b> verified competencies mapped to industry standards.</p>", unsafe_allow_html=True)
            for cat, skills in res["found"].items():
                if skills:
                    with st.expander(f"📦 {cat} ({len(skills)} verified)", expanded=True):
                        st.markdown(generate_tags(skills, "skill-found"), unsafe_allow_html=True)

    with t2:
        jd_skills = res["jd_skills"]
        has_jd_skills = any(len(s) > 0 for s in jd_skills.values())
        
        if not has_jd_skills:
            st.info("Target Job Description lacks parsable strict-match keywords for categorical gap mapping. Rely on Frequency Keywords below.")
        else:
            missing_total = sum(len(s) for s in res["missing"].values())
            if missing_total == 0:
                st.success("🎯 Flawless alignment. You cover 100% of the explicitly outlined domain technologies.")
            else:
                st.markdown(f"<p style='font-weight: 600;' class='skill-missing-text'>Identified {missing_total} critical capability voids. Resolving these will dramatically improve ATS parseability.</p>", unsafe_allow_html=True)
                
                # Downloadable Action Plan
                missing_report = "--- RESUME OPTIMIZATION PLAN ---\n\nMissing Skills by Category:\n"
                for cat, skills in res["missing"].items():
                    if skills:
                        missing_report += f"\n[{cat}]\n- " + "\n- ".join(sorted(skills)) + "\n"
                        with st.expander(f"⚠️ Void in {cat} ({len(skills)} missing)", expanded=True):
                            st.markdown(generate_tags(skills, "skill-missing"), unsafe_allow_html=True)
                
                st.write("")
                st.download_button(
                    label="📥 Download Action Plan (.txt)",
                    data=missing_report,
                    file_name="resume_action_plan.txt",
                    mime="text/plain",
                    help="Download this list to use as a checklist when updating your resume."
                )
        
        # Keyword Fallback Mechanism
        missing_kw = [k for k, v in res["keywords"] if k.lower() not in res["cleaned_res"]]
        if missing_kw:
            st.write("")
            st.markdown("#### 🔍 High-Frequency Keywords Required")
            st.markdown("<p style='font-size: 0.9rem;' class='dynamic-text'>These conceptual keywords appeared frequently in the JD but are entirely absent from your document:</p>", unsafe_allow_html=True)
            st.markdown(generate_tags(missing_kw[:15], "skill-missing"), unsafe_allow_html=True)

    with t3:
        st.markdown("<p style='margin-bottom: 20px;' class='dynamic-text'>Semantic entity density inside the Job Description. Use this to prioritize which keywords to heavily emphasize.</p>", unsafe_allow_html=True)
        if res["keywords"]:
            df = pd.DataFrame(res["keywords"][:20], columns=["Entity Map", "Repetition Impact"])
            # Modern bar chart integration
            st.bar_chart(df.set_index("Entity Map"), color="#059669", height=400)
        else:
            st.info("Data insufficient for robust visualization parameters.")

# --- FOOTER INJECTION ---
draw_footer()
