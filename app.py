import streamlit as st
import tempfile
import os
import pandas as pd
import json
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
from utils import extract_text_from_pdf, clean_text

# --- SEO & PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ResumeAI Pro | Premium ATS Scanner", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Meta tags for SEO through raw HTML (Best effort mapping to SEO in Streamlit)
st.markdown("""
    <head>
        <meta name="description" content="Premium AI Resume Scanner. Optimize your resume for ATS systems and secure your dream job.">
        <meta name="keywords" content="AI, Resume Scanner, ATS, Career, Developer Portfolio">
        <meta name="author" content="Hussnain">
    </head>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'

if 'view' not in st.session_state:
    st.session_state.view = 'input'
if 'results' not in st.session_state:
    st.session_state.results = None

# --- AI AGENT CONFIGURATION ---
with st.sidebar:
    st.markdown("### 🤖 Generative AI Agent")
    st.markdown("Enable the AI Agent to generate actionable, personalized resume improvement strategies.")
    
    if not GENAI_AVAILABLE:
        st.error("⚠️ AI module missing. Check internet & run: `pip install google-generativeai`")
        
    api_key_input = st.text_input("Google Gemini API Key:", type="password", help="Required to activate the AI Agent. Get a free key at aistudio.google.com/app/apikey", disabled=not GENAI_AVAILABLE)
    if api_key_input and GENAI_AVAILABLE:
        st.session_state.gemini_key = api_key_input
        genai.configure(api_key=api_key_input)
        st.success("Agent Active!")
    else:
        st.session_state.gemini_key = None
        if GENAI_AVAILABLE:
            st.info("Input API Key to activate AI Agent")

# --- CSS LOADING ---
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            
if st.session_state.theme == 'Light':
    local_css("style_light.css")
else:
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

# --- CORE APPLICATION FLOW ---

if st.session_state.view == 'input':
    # --- HERO SECTION ---
    st.write("")
    h_c1, h_c2 = st.columns([5, 1])
    with h_c1:
        st.title("Optimize Your Career Trajectory")
    with h_c2:
        st.write("")
        is_light = st.toggle("☀️ Light Theme", value=(st.session_state.theme == 'Light'), key="theme_t1")
        if is_light and st.session_state.theme != 'Light':
            st.session_state.theme = 'Light'
            st.rerun()
        elif not is_light and st.session_state.theme != 'Dark':
            st.session_state.theme = 'Dark'
            st.rerun()
        st.write("")
            
    st.markdown("<p style='font-size: 1.2rem; max-width: 800px;' class='dynamic-text'>Leverage an advanced Generative AI Agent to deeply analyze your resume against targeted job descriptions. Uncover missing skills, instantly rewrite bullets, and beat the ATS algorithms.</p>", unsafe_allow_html=True)
    
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
                            
                            agent_feedback = None
                            if st.session_state.get('gemini_key') and GENAI_AVAILABLE:
                                st.write("🧠 AI Agent analyzing context for personalized feedback...")
                                try:
                                    model = genai.GenerativeModel('gemini-1.5-flash')
                                    prompt = f"""You are an intelligent resume scanning agent embedded in a hiring platform. Your job is to analyze uploaded resumes and job descriptions, then provide structured, actionable insights.

## Your capabilities
- Extract key information from resumes: skills, experience, education, certifications, and contact details.
- Parse job descriptions to identify required qualifications, preferred skills, and role expectations.
- Score resume-to-job match on a scale of 0-100, broken into: skills match, experience relevance, education fit, and keyword alignment.
- Identify skill gaps and suggest concrete improvements the candidate can make.
- Flag ATS (Applicant Tracking System) issues: missing keywords, poor formatting signals, or weak action verbs.
- Rank and compare multiple resumes against a single job description when provided.

## Behavior rules
- Always respond in structured JSON unless the user explicitly asks for plain text.
- Never fabricate information. If a section is missing from the resume, state it as "not found."
- Be specific and concise — avoid vague feedback like "improve your resume." Give exact suggestions.
- Keep a neutral, professional tone. Do not judge the candidate personally.
- If the input is unclear or incomplete, ask a targeted clarifying question before proceeding. Ensure the response does not contain any markdown wrapping like ```json.

## Output format (default)
Return a JSON object STRICTLY with these fields:
{{
  "candidate_name": "",
  "overall_match_score": 0,
  "score_breakdown": {{
    "skills_match": 0,
    "experience_relevance": 0,
    "education_fit": 0,
    "keyword_alignment": 0
  }},
  "extracted_skills": [],
  "missing_skills": [],
  "ats_issues": [],
  "top_strengths": [],
  "improvement_suggestions": [],
  "summary": ""
}}

## Context
Job description: {job_description[:2000]}
Resume text: {resume_text[:2000]}"""
                                    response = model.generate_content(prompt)
                                    cleaned_response = response.text.replace('```json', '').replace('```', '').strip()
                                    agent_feedback = json.loads(cleaned_response)
                                    
                                    # --- INITIALIZE THE AGENT CHAT SESSION ---
                                    # Give the agent its core system instruction and load the user's data into its memory
                                    chat_session = model.start_chat(history=[
                                        {"role": "user", "parts": [f"You are my elite personal AI Resume Agent. My targeted Job Description is:\n{job_description[:2000]}\n\nAnd my current Resume is:\n{resume_text[:2000]}\n\nKeep your answers concise, practical, and heavily tailored to getting me this specific job."]},
                                        {"role": "model", "parts": ["Context successfully loaded. I am your personal AI Resume Agent. I'm ready to iteratively rewrite your bullet points, build a cover letter, or provide interview coaching. What would you like to do first?"]}
                                    ])
                                    st.session_state.agent_chat = chat_session
                                    st.session_state.chat_history = [{"role": "assistant", "content": "Context successfully loaded! I am your personal AI Agent. I'm ready to iteratively rewrite your bullet points, build a cover letter, or provide interview coaching. What would you like to do first?"}]
                                    
                                    if not agent_feedback or "error" in agent_feedback:
                                        status.update(label="System Error Encountered", state="error", expanded=True)
                                        st.error(f"⚠️ AI Execution Error: {agent_feedback.get('error') if agent_feedback else 'Unknown error. Check API key.'}")
                                        st.stop()
                                except Exception as e:
                                    st.toast(f"Invalid API Key: Falling back to Demo Mode!", icon="🧪")
                                    agent_feedback = {
                                        "candidate_name": "Demo Applicant",
                                        "overall_match_score": 85,
                                        "score_breakdown": {
                                            "skills_match": 88,
                                            "experience_relevance": 82,
                                            "education_fit": 90,
                                            "keyword_alignment": 80
                                        },
                                        "extracted_skills": ["Python", "React", "AWS", "Machine Learning"],
                                        "missing_skills": ["Docker", "Kubernetes", "GraphQL"],
                                        "ats_issues": ["Missing exact phrase 'Software Engineer'", "Use stronger action verbs"],
                                        "top_strengths": ["Strong core languages", "Good educational background"],
                                        "improvement_suggestions": ["Add Docker to your skills section", "Quantify your React experience"],
                                        "summary": "This is a Portfolio Demo Mode summary. The candidate shows strong potential but lacks cloud orchestration skills."
                                    }
                                    class MockChat:
                                        def send_message(self, msg):
                                            class Resp:
                                                text = "This is a Demo Mode response. Please add an API key for real AI chatting!"
                                            return Resp()
                                    st.session_state.agent_chat = MockChat()
                                    st.session_state.chat_history = [{"role": "assistant", "content": "Welcome to Demo Mode! Your API key was invalid. Please provide a valid key in the sidebar for full conversational capabilities."}]
                            else:
                                st.toast("No API Key: Running in Portfolio Demo Mode!", icon="🧪")
                                agent_feedback = {
                                    "candidate_name": "Demo Applicant",
                                    "overall_match_score": 85,
                                    "score_breakdown": {
                                        "skills_match": 88,
                                        "experience_relevance": 82,
                                        "education_fit": 90,
                                        "keyword_alignment": 80
                                    },
                                    "extracted_skills": ["Python", "React", "AWS", "Machine Learning"],
                                    "missing_skills": ["Docker", "Kubernetes", "GraphQL"],
                                    "ats_issues": ["Missing exact phrase 'Software Engineer'", "Use stronger action verbs"],
                                    "top_strengths": ["Strong core languages", "Good educational background"],
                                    "improvement_suggestions": ["Add Docker to your skills section", "Quantify your React experience"],
                                    "summary": "This is a Portfolio Demo Mode summary. The candidate shows strong potential but lacks cloud orchestration skills."
                                }
                                class MockChat:
                                    def send_message(self, msg):
                                        class Resp:
                                            text = "This is a Demo Mode response. Please add an API key for real AI chatting!"
                                        return Resp()
                                st.session_state.agent_chat = MockChat()
                                st.session_state.chat_history = [{"role": "assistant", "content": "Welcome to Demo Mode! I am your mocked AI Agent. Please provide an API key in the sidebar for full conversational capabilities."}]
                                        
                            st.session_state.results = {
                                "agent_feedback": agent_feedback
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
    h_col1, h_col2, h_col3 = st.columns([5, 1.5, 1.5])
    with h_col1:
        st.title("📊 Intelligence Report")
        st.markdown("<p style='font-size: 1.1rem; margin-top: -15px;' class='dynamic-text'>Comprehensive breakdown of your ATS compatibility.</p>", unsafe_allow_html=True)
    with h_col2:
        st.write("")
        st.write("")
        st.write("")
        is_light_r = st.toggle("☀️ Light Theme", value=(st.session_state.theme == 'Light'), key="theme_t2")
        if is_light_r and st.session_state.theme != 'Light':
            st.session_state.theme = 'Light'
            st.rerun()
        elif not is_light_r and st.session_state.theme != 'Dark':
            st.session_state.theme = 'Dark'
            st.rerun()
    with h_col3:
        st.write("")
        st.write("")
        if st.button("⬅️ Modify Inputs", use_container_width=True):
            st.session_state.view = 'input'
            st.rerun()

    st.write("")

    # Highlight Metric Block
    m_col1, m_col2, m_col3 = st.columns([1.5, 1, 2.5], gap="large")
    agent_data = res.get("agent_feedback") or {}
    score = int(agent_data.get("overall_match_score", 0))
    
    with m_col1:
        st.metric("Neural Match Score", f"{score}%")
        st.progress(score/100)
        
    with m_col2:
        extracted = agent_data.get("extracted_skills", [])
        missing = agent_data.get("missing_skills", [])
        st.metric("Extracted Skills", len(extracted))
        st.metric("Missing Skills", len(missing))
    
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
    
    t_agent, t_gap, t_chat = st.tabs(["📊 Executive AI Report", "🎯 Skill Gap & Strengths", "💬 Chat with Agent"])
    
    with t_agent:
        st.markdown("#### 🧠 Intelligent Resume AI Agent Analysis")
        st.markdown("<p style='font-size:0.95rem;' class='dynamic-text'>Comprehensive LLM evaluation based on actionable recruiting insights.</p>", unsafe_allow_html=True)
        
        c_exec, c_score = st.columns([3, 1])
        with c_exec:
            st.info(f"**Candidate:** {agent_data.get('candidate_name', 'Not Found')}\n\n**Agent Summary:** {agent_data.get('summary', 'No summary provided.')}")
        with c_score:
            st.metric("Agent Overall Match", f"{score}/100")
        
        st.write("")
        st.markdown("##### 📊 Match Score Breakdown")
        bdown = agent_data.get('score_breakdown', {})
        col_b1, col_b2, col_b3, col_b4 = st.columns(4)
        col_b1.metric("Skills", bdown.get('skills_match', 0))
        col_b2.metric("Experience", bdown.get('experience_relevance', 0))
        col_b3.metric("Education", bdown.get('education_fit', 0))
        col_b4.metric("Keywords", bdown.get('keyword_alignment', 0))
        
        st.write("")
        st.markdown("##### 💡 Actionable Improvements")
        for imp in agent_data.get("improvement_suggestions", []):
            st.info(f"**Suggestion:** {imp}")
        st.write("")
        
    with t_gap:
        col_ls, col_rs = st.columns(2)
        with col_ls:
            st.markdown("##### 🌟 Top Strengths")
            for s in agent_data.get("top_strengths", []):
                st.markdown(f"<p style='margin-bottom:5px;' class='dynamic-text'>✅ {s}</p>", unsafe_allow_html=True)
            
            st.write("")
            st.markdown("##### 🛠️ Extracted Skills")
            if extracted:
                html = '<div class="skill-container">' + "".join([f'<span class="skill-tag skill-found">✨ {s}</span>' for s in extracted]) + '</div>'
                st.markdown(html, unsafe_allow_html=True)
                
        with col_rs:
            st.markdown("##### ⚠️ ATS Issues")
            ats_issues = agent_data.get("ats_issues", [])
            if ats_issues:
                for alt in ats_issues:
                    st.markdown(f"<p style='margin-bottom:5px; color: var(--accent-main);' class='dynamic-text'>🚨 {alt}</p>", unsafe_allow_html=True)
            else:
                st.success("No ATS issues detected.")
                
            st.write("")
            st.markdown("##### 🎯 Missing Requirements")
            if missing:
                html = '<div class="skill-container">' + "".join([f'<span class="skill-tag skill-missing">⚠️ {s}</span>' for s in missing]) + '</div>'
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.success("No critical missing skills!")
    
    with t_chat:
        st.markdown("#### 🤖 Interactive Resume Agent")
        st.markdown("<p style='font-size:0.95rem;' class='dynamic-text'>Your Agent has memorized your Resume and the Job Description. Ask it to do the heavy lifting for you!</p>", unsafe_allow_html=True)
        
        if 'chat_history' in st.session_state:
            chat_container = st.container(height=400)
            with chat_container:
                for msg in st.session_state.chat_history:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])
            
            user_query = st.chat_input("Ask the agent to write a cover letter, rewrite a bullet, etc...")
            if user_query:
                st.session_state.chat_history.append({"role": "user", "content": user_query})
                with chat_container:
                    with st.chat_message("user"):
                        st.markdown(user_query)
                    with st.chat_message("assistant"):
                        with st.spinner("Agent is running task..."):
                            try:
                                response = st.session_state.agent_chat.send_message(user_query)
                                msg_text = response.text
                            except Exception as e:
                                msg_text = f"Agent encountered an error: {e}"
                            st.markdown(msg_text)
                st.session_state.chat_history.append({"role": "assistant", "content": msg_text})
                st.rerun()

# --- FOOTER INJECTION ---
draw_footer()
