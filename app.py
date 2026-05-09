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
        
    api_key_input = st.text_input("Google Gemini API Key:", type="password", value="AIzaSyArPIAouGRnlMPDzG-gPIqnWI21fYuNRR4", help="Required to activate the AI Agent. Get a free key at aistudio.google.com/app/apikey", disabled=not GENAI_AVAILABLE)
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
        section_header("🎯", "2. Define Target", "Paste a job description OR just enter a Job Title.")
        job_description = st.text_area("", height=220, placeholder="Example 1 (Title): Senior Python Developer\n\nExample 2 (Full JD): We are looking for a Senior Developer with 5+ years of experience in Python, React, and AWS... \n\n(Tip: The AI will automatically infer the required skills if you only provide a job title!)", label_visibility="collapsed", help="Paste the complete job description OR just a specific job title to maximize skill matching accuracy.")

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
                                    model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type": "application/json"})
                                    prompt = f"""You are ResumeAgent — a True AI Agent that operates in multiple steps using tools.

You are NOT a simple question-answering bot.
You THINK, PLAN, ACT, OBSERVE, and REASON across multiple steps before producing output.
Every run is completely independent — you have zero memory of previous resumes or jobs.

===============================
YOUR TOOLS:
===============================

You have access to the following tools. Call them in order:

TOOL 1 — read_resume(pdf_text: str)
  Input: Raw text extracted from the candidate's uploaded PDF resume
  Action: Parse and structure all information from the resume
  Extract: skills, tools, technologies, education, years of experience,
           job titles held, projects, certifications, achievements

TOOL 2 — search_job_requirements(job_title: str)
  Input: The job title entered by the user
  Action: Search the web for real current job postings for this role (Simulate this reasoning)
  Extract: required skills, preferred skills, education requirements,
           experience level, responsibilities, salary range if available

TOOL 3 — compare_and_score(resume_data: dict, job_requirements: dict)
  Input: Structured resume data + structured job requirements
  Action: Run a precise gap analysis — match every requirement against the resume
  Classify each requirement as:
    MET      → clearly present in the resume (cite the evidence)
    PARTIAL  → present but insufficient, outdated, or incomplete
    MISSING  → completely absent from the resume
  Calculate an honest fit score 0–10:
    9–10 → Excellent match, apply immediately
    7–8  → Strong match, minor gaps only
    5–6  → Moderate match, notable gaps
    3–4  → Weak match, major gaps
    0–2  → Not suitable yet, significant upskilling needed

TOOL 4 — generate_verdict(analysis: dict)
  Input: Full comparison analysis from Tool 3
  Action: Produce the final output — specific, honest, actionable
  Never give vague advice. Name exact skills, tools, courses, or projects.

===============================
AGENT BEHAVIOR RULES:
===============================
RULE 1 — ALWAYS run all 4 tools in sequence. Never skip a step.
RULE 2 — NEVER reuse any previous resume or job from earlier in the session.
RULE 3 — NEVER produce generic output. Every sentence must reference the specific resume text and specific job.
RULE 4 — NEVER inflate scores. Be brutally honest. A bad match is a bad match.
RULE 5 — NEVER say "improve your skills" — always name the exact skill, tool, or technology the candidate must learn.

===============================
FINAL OUTPUT FORMAT:
===============================
Output format — always return a JSON object STRICTLY with these fields:
{{
  "agent_run_log": ["✅ Resume read: ...", "✅ Job searched: ...", "✅ Requirements found: ...", "✅ Comparison complete: ..."],
  "candidate_snapshot": "3 sentences. Who is this specific person based only on their resume?",
  "job_requirements_found": [
    {{"requirement": "...", "type": "Required or Preferred"}}
  ],
  "requirements_met": [
    {{"requirement": "...", "evidence": "exact quote or direct reference from the resume"}}
  ],
  "partial_matches": [
    {{"requirement": "...", "present": "what the resume shows", "gap": "what is still needed"}}
  ],
  "missing_requirements": [
    "Bullet list of everything completely absent from the resume"
  ],
  "fit_score": 0,
  "fit_verdict": "Excellent Match / Strong Match / Moderate Match / Weak Match / Not Ready Yet",
  "fit_reasoning": "2–3 sentences. Grounded in this resume and this job only. No flattery.",
  "improvement_roadmap": [
    {{"skill": "exact skill/tool/tech", "reason": "why it matters", "how_to_learn": "course name/platform/project type"}}
  ],
  "final_recommendation_verdict": "YES - Apply Now / YES - With Preparation / MAYBE - Address Key Gaps First / NO - Significant Upskilling Needed",
  "final_recommendation_reasoning": "2 sentences. Direct and honest. What should this candidate do TODAY?"
}}

===============================
USER PROMPT TEMPLATE:
===============================
New agent task. This is a completely fresh run — ignore all previous sessions.

JOB TITLE / DESCRIPTION: {job_description}

RESUME TEXT (extracted from PDF):
{resume_text}
"""
                                    response = model.generate_content(prompt)
                                    # Fallback cleanup just in case, though response_mime_type should ensure pure JSON
                                    cleaned_response = response.text.replace('```json', '').replace('```', '').strip()
                                    agent_feedback = json.loads(cleaned_response)
                                    
                                    # --- INITIALIZE THE AGENT CHAT SESSION ---
                                    # Give the agent its core system instruction and load the user's data into its memory
                                    # We use standard model for chat since chat responses shouldn't be constrained to JSON
                                    chat_model = genai.GenerativeModel('gemini-2.5-flash')
                                    chat_session = chat_model.start_chat(history=[
                                        {"role": "user", "parts": [f"You are my elite personal AI Resume Agent. My targeted Job Description is:\n{job_description}\n\nAnd my current Resume is:\n{resume_text}\n\nKeep your answers concise, practical, and heavily tailored to getting me this specific job."]},
                                        {"role": "model", "parts": ["Context successfully loaded. I am your personal AI Resume Agent. I'm ready to iteratively rewrite your bullet points, build a cover letter, or provide interview coaching. What would you like to do first?"]}
                                    ])
                                    st.session_state.agent_chat = chat_session
                                    st.session_state.chat_history = [{"role": "assistant", "content": "Context successfully loaded! I am your personal AI Agent. I'm ready to iteratively rewrite your bullet points, build a cover letter, or provide interview coaching. What would you like to do first?"}]
                                    
                                    if not agent_feedback or "error" in agent_feedback:
                                        status.update(label="System Error Encountered", state="error", expanded=True)
                                        st.error(f"⚠️ AI Execution Error: {agent_feedback.get('error') if agent_feedback else 'Unknown error. Check API key.'}")
                                        st.stop()
                                except Exception as e:
                                    st.error(f"⚠️ AI Analysis Failed: {str(e)}")
                                    st.toast(f"Analysis Error: Falling back to Demo Mode! {str(e)[:50]}...", icon="🧪")
                                    agent_feedback = None
                            
                            # Demo Mode logic explicitly uses the requested job title
                            if not agent_feedback or "error" in agent_feedback:
                                if not st.session_state.get('gemini_key') or not GENAI_AVAILABLE:
                                    st.toast("No API Key: Running in Portfolio Demo Mode!", icon="🧪")
                                
                                job_title_display = job_description.strip().split('\n')[0][:40] if job_description else "Target Role"
                                if job_description and len(job_description.strip().split('\n')[0]) > 40:
                                    job_title_display += "..."
                                if not job_title_display:
                                    job_title_display = "Target Role"
                                
                                word_count = len(resume_text.split()) if resume_text else 0
                                
                                agent_feedback = {
                                    "agent_run_log": [f"✅ Resume read: {word_count} words extracted", f"✅ Job searched: {job_title_display}", "✅ Requirements found: Simulated requirements from demo mode", "✅ Comparison complete: Demo mode analysis"],
                                    "candidate_snapshot": f"Demo Applicant aiming for the role of {job_title_display}. This is a simulated response because the AI is running in Demo Mode.",
                                    "job_requirements_found": [
                                        {"requirement": f"Core skills relevant to {job_title_display}", "type": "Required"},
                                        {"requirement": "Professional communication and teamwork", "type": "Required"},
                                        {"requirement": "Relevant education or certifications", "type": "Preferred"}
                                    ],
                                    "requirements_met": [
                                        {"requirement": "Basic Qualifications", "evidence": "Resume indicates foundational professional experience."}
                                    ],
                                    "partial_matches": [
                                        {"requirement": "Specialized Experience", "present": "General background shown", "gap": f"Lacks explicit mention of advanced requirements for {job_title_display}."}
                                    ],
                                    "missing_requirements": [
                                        "Advanced domain-specific tools or methodologies", "Senior-level leadership (if applicable)"
                                    ],
                                    "fit_score": 6,
                                    "fit_verdict": "Moderate Match (Demo)",
                                    "fit_reasoning": f"This is a demo analysis for the {job_title_display} position. Please provide a valid Google Gemini API key in the sidebar for a real, deep AI analysis tailored specifically to your resume.",
                                    "improvement_roadmap": [
                                        {"skill": "Role-specific tools", "reason": f"Essential for success as a {job_title_display}", "how_to_learn": "Industry recognized certifications or practical projects"}
                                    ],
                                    "final_recommendation_verdict": "MAYBE - Demo Mode Active",
                                    "final_recommendation_reasoning": "Please add your API key to unlock the true power of the AI Agent and receive highly specific, actionable feedback."
                                }
                                class MockChat:
                                    def send_message(self, msg):
                                        class Resp:
                                            text = f"This is a Demo Mode response for the {job_title_display} role. Please add an API key for real AI chatting!"
                                        return Resp()
                                st.session_state.agent_chat = MockChat()
                                st.session_state.chat_history = [{"role": "assistant", "content": f"Welcome to Demo Mode! I am your mocked AI Agent for the {job_title_display} role. Please provide an API key in the sidebar for full conversational capabilities."}]
                                        
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
    
    # Scale 1-10 to 1-100 for UI purposes
    try:
        raw_score = float(agent_data.get("fit_score", 0))
    except (ValueError, TypeError):
        raw_score = 0
    score = int((raw_score / 10.0) * 100) if raw_score <= 10 else int(raw_score)
    
    extracted = agent_data.get("requirements_met", [])
    missing = agent_data.get("missing_requirements", [])
    
    with m_col1:
        st.metric("Neural Match Score", f"{score}%")
        st.progress(score/100)
        
    with m_col2:
        st.metric("Requirements Met", len(extracted))
        st.metric("Missing Requirements", len(missing))
    
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
    
    t_agent, t_gap, t_chat = st.tabs(["📊 Executive AI Report", "🎯 Match Analysis", "💬 Chat with Agent"])
    
    with t_agent:
        st.markdown("#### 🧠 Intelligent Resume AI Agent Analysis")
        st.markdown("<p style='font-size:0.95rem;' class='dynamic-text'>Comprehensive LLM evaluation based on actionable recruiting insights.</p>", unsafe_allow_html=True)
        
        # Combine Run Log into a container
        run_logs = agent_data.get("agent_run_log", [])
        log_items = "".join([f"<li>{log}</li>" for log in run_logs])
        st.markdown(f"""
        <div class='req-container' style='border-left: 4px solid var(--pri-bright); background: linear-gradient(90deg, var(--pri-light), transparent);'>
            <div class='req-point'>🤖 Agent Run Log</div>
            <details style="margin-top: 8px; cursor: pointer;">
                <summary style="font-weight: 600; color: var(--text-dim); outline: none;">See logs</summary>
                <ul style="margin-top: 8px; font-size: 0.9rem; color: var(--text-star);">
                    {log_items}
                </ul>
            </details>
        </div>
        """, unsafe_allow_html=True)
            
        st.write("")
        st.info(f"**🧑 Candidate Snapshot:**\n{agent_data.get('candidate_snapshot', 'Not provided.')}")
        
        st.write("")
        st.markdown("##### 💼 Real Job Requirements Found")
        for req in agent_data.get("job_requirements_found", []):
            badge = "★" if str(req.get("type", "")).lower() == "required" else "☆"
            st.markdown(f"""
            <div class='req-container' style='padding: 12px; margin-bottom: 10px; border-left: 3px solid var(--acc-bright);'>
                <div style='font-size: 0.95rem; font-weight: 600; color: var(--text-blaze);'>{badge} {req.get('requirement', '')} <span style='font-size: 0.8rem; font-weight: normal; color: var(--text-dim);'>({req.get('type', '')})</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        st.write("")
        # Fit score into an animated container
        fit_score = agent_data.get("fit_score", 0)
        fit_verdict = agent_data.get("fit_verdict", "")
        fit_reasoning = agent_data.get("fit_reasoning", "No reasoning provided.")
        st.markdown(f"""
        <div class='req-container' style='border-left: 4px solid var(--acc2); background: linear-gradient(90deg, var(--acc2-light), transparent);'>
            <div class='req-point'>🎯 Fit Score: {fit_score}/10 - {fit_verdict}</div>
            <details style="margin-top: 8px; cursor: pointer;" open>
                <summary style="font-weight: 600; color: var(--text-dim); outline: none;">See reasoning</summary>
                <div style="margin-top: 8px; font-size: 0.9rem; color: var(--text-star);">
                    {fit_reasoning}
                </div>
            </details>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.markdown("##### 🚀 Improvement Roadmap")
        for i, item in enumerate(agent_data.get("improvement_roadmap", [])):
            st.markdown(f"""
            <div class='req-container' style='border-left: 4px solid var(--pri);'>
                <div class='req-point'>⚡ {i+1}. {item.get('skill', '')}</div>
                <details style="margin-top: 8px; cursor: pointer;">
                    <summary style="font-weight: 600; color: var(--text-dim); outline: none;">See details</summary>
                    <div style="margin-top: 8px; font-size: 0.9rem; color: var(--text-star);">
                        <strong>Reason:</strong> {item.get('reason', '')}<br>
                        <strong>How to learn:</strong> {item.get('how_to_learn', '')}
                    </div>
                </details>
            </div>
            """, unsafe_allow_html=True)
            
        st.write("")
        st.markdown("##### ⚡ Final Recommendation")
        st.success(f"**{agent_data.get('final_recommendation_verdict', '')}**  \n{agent_data.get('final_recommendation_reasoning', '')}")
        
    with t_gap:
        col_ls, col_rs = st.columns(2)
        with col_ls:
            st.markdown("##### ✅ Requirements Met")
            extracted = agent_data.get("requirements_met", [])
            if extracted:
                for req in extracted:
                    st.markdown(f"""
                    <div class='req-container req-met'>
                        <div class='req-point'>✨ {req.get('requirement', '')}</div>
                        <details style="margin-top: 8px; cursor: pointer;">
                            <summary style="font-weight: 600; color: var(--text-dim); outline: none;">See more</summary>
                            <div style="margin-top: 8px; font-size: 0.9rem; color: var(--text-star);">
                                <strong>Evidence:</strong> {req.get('evidence', '')}
                            </div>
                        </details>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("None identified.")
            
            st.write("")
            st.markdown("##### ⚠️ Partial Matches")
            partials = agent_data.get("partial_matches", [])
            if partials:
                for req in partials:
                    st.markdown(f"""
                    <div class='req-container req-partial'>
                        <div class='req-point'>⚖️ {req.get('requirement', '')}</div>
                        <details style="margin-top: 8px; cursor: pointer;">
                            <summary style="font-weight: 600; color: var(--text-dim); outline: none;">See more</summary>
                            <div style="margin-top: 8px; font-size: 0.9rem; color: var(--text-star);">
                                <strong>Present:</strong> {req.get('present', '')}<br>
                                <strong style="color: var(--acc-bright);">Gap:</strong> {req.get('gap', '')}
                            </div>
                        </details>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("None identified.")
                
        with col_rs:
            st.markdown("##### ❌ Missing Requirements")
            missing = agent_data.get("missing_requirements", [])
            if missing:
                for req in missing:
                    st.markdown(f"""
                    <div class='req-container req-missing'>
                        <div class='req-point'>🚨 {req}</div>
                        <details style="margin-top: 8px; cursor: pointer;">
                            <summary style="font-weight: 600; color: var(--text-dim); outline: none;">See more</summary>
                            <div style="margin-top: 8px; font-size: 0.9rem; color: var(--text-star);">
                                Completely absent from your resume. Strongly consider gaining this skill.
                            </div>
                        </details>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("No missing requirements! You are a perfect match.")
    
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
