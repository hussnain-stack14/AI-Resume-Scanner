import re

# Comprehensive dictionary of professional skills categorized for better insights
SKILL_CATEGORIES = {
    "Programming & Core Tech": {
        'python', 'java', 'c++', 'c', 'c#', 'sql', 'javascript', 'typescript', 'html', 'css', 
        'php', 'ruby', 'swift', 'kotlin', 'golang', 'rust', 'dart', 'matlab', 'r', 'perl',
        'bash', 'shell script', 'powershell', 'solidity', 'assembly', 'fortran', 'cobol'
    },
    "AI & Data Science": {
        'machine learning', 'deep learning', 'nlp', 'natural language processing', 
        'artificial intelligence', 'data science', 'computer vision', 'data analysis',
        'tensorflow', 'pytorch', 'scikit-learn', 'keras', 'pandas', 'numpy', 'matplotlib',
        'seaborn', 'opencv', 'spacy', 'nltk', 'llm', 'generative ai', 'prompt engineering',
        'langchain', 'huggingface', 'vector databases', 'rag', 'data engineering', 'big data'
    },
    "Web & App Development": {
        'flask', 'django', 'fastapi', 'nodejs', 'express', 'react', 'angular', 'vue', 'nextjs',
        'spring boot', 'laravel', 'flutter', 'react native', 'ionic', 'svelte', 'tailwind',
        'bootstrap', 'jquery', 'rest api', 'graphql', 'microservices', 'serverless', 'pwa'
    },
    "Cloud & DevOps": {
        'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'terraform', 'ansible',
        'jenkins', 'git', 'github', 'gitlab', 'bitbucket', 'ci/cd', 'devops', 'linux', 'ubuntu',
        'aws lambda', 'ec2', 's3', 'monitoring', 'prometheus', 'grafana', 'mulesoft'
    },
    "Cyber Security": {
        'penetration testing', 'ethical hacking', 'network security', 'cybersecurity',
        'siem', 'firewalls', 'cryptography', 'incident response', 'vulnerability assessment',
        'owasp', 'soc', 'compliance', 'iso 27001', 'gdpr', 'cloud security'
    },
    "Finance & Business": {
        'financial analysis', 'accounting', 'investment banking', 'risk management',
        'fintech', 'blockchain', 'cryptocurrency', 'taxation', 'auditing', 'economics',
        'business strategy', 'market research', 'crm', 'salesforce', 'sap', 'erp'
    },
    "Healthcare & Science": {
        'biotechnology', 'pharmacology', 'clinical research', 'bioinformatics',
        'medical coding', 'healthcare management', 'nursing', 'public health',
        'genomics', 'molecular biology', 'lab management'
    },
    "Design & Creative": {
        'ui/ux design', 'user research', 'graphic design', 'motion graphics',
        'figma', 'canva', 'adobe photoshop', 'illustrator', 'xd', 'indesign', 'premiere pro',
        'after effects', '3d modeling', 'blender', 'typography', 'branding'
    },
    "Soft Skills": {
        'communication', 'leadership', 'teamwork', 'collaboration', 'problem solving',
        'critical thinking', 'creativity', 'adaptability', 'flexibility', 'time management',
        'organization', 'presentation', 'public speaking', 'negotiation', 'emotional intelligence',
        'strategic thinking', 'decision making', 'conflict resolution', 'mentoring', 'coaching',
        'active listening', 'empathy', 'work ethic', 'reliability', 'dependability', 'project management'
    }
}

# Flatten for easy lookup
ALL_SKILLS = {skill for cat in SKILL_CATEGORIES.values() for skill in cat}

def extract_skills(text):
    """
    Extracts skills from text based on categorized skill sets.
    Returns a dictionary of found skills grouped by category.
    """
    found_categorized = {cat: set() for cat in SKILL_CATEGORIES}
    
    if not text:
        return found_categorized

    text_lower = text.lower()
    
    for category, skill_list in SKILL_CATEGORIES.items():
        for skill in skill_list:
            # Precise skill matching (handles skills like C++, C#, etc.)
            if skill.endswith('+') or skill.endswith('#'):
                pattern = r'\b' + re.escape(skill) + r'(?!\w)'
            else:
                pattern = r'\b' + re.escape(skill) + r'\b'
            
            if re.search(pattern, text_lower):
                found_categorized[category].add(skill)
            
    return found_categorized

def get_missing_skills(resume_categorized, jd_categorized):
    """
    Returns skills that are present in the job description but missing from the resume,
    grouped by category.
    """
    missing_categorized = {}
    for category in SKILL_CATEGORIES:
        resume_skills = resume_categorized.get(category, set())
        jd_skills = jd_categorized.get(category, set())
        missing = jd_skills - resume_skills
        if missing:
            missing_categorized[category] = missing
            
    return missing_categorized
