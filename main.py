import streamlit as st
import PyPDF2
import os
from dotenv import load_dotenv
import openai
from docx import Document
import io

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title=" AI Resume Critiquer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main app styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
        font-size: 1.3rem;
    }
    
    /* Upload area styling */
    .upload-area {
        border: 3px dashed #4facfe;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    }
    
    /* Success/Info boxes */
    .success-box {
        background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    .info-box {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    /* Analysis results styling */
    .analysis-results {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4facfe;
        margin: 1rem 0;
        color: #333333 !important;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .analysis-results p {
        color: #333333 !important;
        margin: 0.5rem 0;
    }
    
    .analysis-results h1, .analysis-results h2, .analysis-results h3, .analysis-results h4, .analysis-results h5, .analysis-results h6 {
        color: #2c3e50 !important;
        font-weight: bold;
    }
    
    .analysis-results ul, .analysis-results ol {
        color: #333333 !important;
    }
    
    .analysis-results li {
        color: #333333 !important;
        margin: 0.3rem 0;
    }
    
    /* Ensure all text in analysis results is readable */
    .analysis-results * {
        color: #333333 !important;
    }
    
    .analysis-results strong, .analysis-results b {
        color: #2c3e50 !important;
        font-weight: bold;
    }
    
    .analysis-results em, .analysis-results i {
        color: #34495e !important;
        font-style: italic;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background: white;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
    }
    
    /* Metrics styling */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }
    
    /* Progress bar styling */
    .progress-container {
        background: #f0f0f0;
        border-radius: 10px;
        padding: 0.5rem;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        height: 20px;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file (PDF, DOCX, or TXT)"""
    try:
        file_extension = uploaded_file.name.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            return extract_text_from_pdf(uploaded_file)
        elif file_extension == 'docx':
            return extract_text_from_docx(uploaded_file)
        elif file_extension == 'txt':
            return extract_text_from_txt(uploaded_file)
        else:
            st.error(f"Unsupported file format: {file_extension}")
            return None
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def extract_text_from_docx(docx_file):
    """Extract text from uploaded DOCX file"""
    try:
        doc = Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return None

def extract_text_from_txt(txt_file):
    """Extract text from uploaded TXT file"""
    try:
        # Reset file pointer to beginning
        txt_file.seek(0)
        text = txt_file.read().decode('utf-8')
        return text
    except Exception as e:
        st.error(f"Error reading TXT: {str(e)}")
        return None

def analyze_resume_with_openai(resume_text, target_role=None):
    """Analyze resume using OpenAI API"""
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Base prompt
        prompt = f"""
        Please analyze this resume and provide constructive feedback on:
        1. Overall structure and formatting
        2. Content quality and relevance
        3. Skills presentation
        4. Experience descriptions
        5. Areas for improvement
        6. Strengths to highlight
        """
        
        # Add role-specific feedback if target role is provided
        if target_role:
            prompt += f"""
        
        IMPORTANT: The candidate is targeting the role of "{target_role}". Please provide additional feedback on:
        7. How well the resume aligns with this specific role
        8. Missing skills or experiences relevant to {target_role}
        9. How to better position their background for {target_role}
        10. Industry-specific keywords or phrases to include for {target_role}
        """
        
        prompt += f"""
        
        Resume text:
        {resume_text}
        
        Please provide specific, actionable feedback in a clear, professional manner.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional resume reviewer with expertise in HR and recruitment."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error analyzing resume: {str(e)}")
        return None

def main():
    # Main header with custom styling
    st.markdown("""
    <div class="main-header">
        <h1>📄 AI Resume Critiquer</h1>
        <p>Upload your resume and get AI-powered feedback to improve it!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for API key input only
    with st.sidebar:
        st.markdown("""
        <div class="section-header">
            🔑 Configuration
        </div>
        """, unsafe_allow_html=True)
        
        api_key = st.text_input(
            "OpenAI API Key", 
            type="password",
            help="Enter your OpenAI API key to use the resume analysis feature"
        )
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            st.markdown("""
            <div class="success-box">
                ✅ API Key set!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter your OpenAI API key to use the analysis feature")
    
    # Role targeting section in the middle
    st.markdown("""
    <div class="section-header">
        🎯 Target Role (Optional)
    </div>
    """, unsafe_allow_html=True)
    
    col_role1, col_role2, col_role3 = st.columns([1, 2, 1])
    with col_role2:
        target_role = st.text_input(
            "What role are you targeting?",
            placeholder="e.g., Software Engineer, Data Scientist, Marketing Manager",
            help="Specify the role you're applying for to get more targeted feedback",
            key="target_role_input"
        )
        
        if target_role:
            st.markdown(f"""
            <div class="info-box">
                🎯 Targeting: **{target_role}**
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="section-header">
            📤 Upload Resume
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["pdf", "docx", "txt"],
            help="Upload your resume in PDF, Word (DOCX), or text format"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # Extract text from file
            resume_text = extract_text_from_file(uploaded_file)
            
            if resume_text:
                st.subheader("📝 Extracted Text Preview")
                st.text_area(
                    "Resume Content",
                    resume_text[:500] + "..." if len(resume_text) > 500 else resume_text,
                    height=200,
                    disabled=True
                )
    
    with col2:
        st.markdown("""
        <div class="section-header">
            🤖 AI Analysis
        </div>
        """, unsafe_allow_html=True)
        
        if uploaded_file is not None and resume_text:
            if st.button("🔍 Analyze Resume", type="primary"):
                if not api_key:
                    st.error("Please enter your OpenAI API key in the sidebar first!")
                else:
                    with st.spinner("Analyzing your resume..."):
                        analysis = analyze_resume_with_openai(resume_text, target_role)
                        
                        if analysis:
                            st.markdown("""
                            <div class="section-header">
                                📊 Analysis Results
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"""
                            <div class="analysis-results">
                                {analysis}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("Failed to analyze resume. Please check your API key and try again.")
        else:
            st.info("👆 Upload a resume file (PDF, DOCX, or TXT) to get started!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>💡 <strong>Tips:</strong> Supported formats: PDF, Word (DOCX), and TXT. Specify your target role for more targeted feedback!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
