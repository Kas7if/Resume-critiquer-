# Resume Critiquer 📄

An AI-powered resume analysis tool built with Streamlit and OpenAI that helps you improve your resume with constructive feedback.

## Features

- 📤 **Multi-Format Upload**: Upload your resume in PDF, Word (DOCX), or TXT format
- 🤖 **AI Analysis**: Get detailed feedback using OpenAI's GPT models
- 📊 **Comprehensive Review**: Analysis covers structure, content, skills, and more
- 🎨 **User-Friendly Interface**: Clean, intuitive Streamlit interface

## Setup

### Prerequisites

- Python 3.13+
- OpenAI API key

### Installation

1. **Clone or download this project**

2. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

3. **Install dependencies (already done):**
   ```bash
   uv sync
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file

### Running the Application

1. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

2. **Run the Streamlit app:**
   ```bash
   streamlit run main.py
   ```

3. **Open your browser** and go to the URL shown in the terminal (usually `http://localhost:8501`)

## Usage

1. **Enter your OpenAI API key** in the sidebar
2. **Upload a resume file** (PDF, DOCX, or TXT) using the file uploader
3. **Click "Analyze Resume"** to get AI-powered feedback
4. **Review the analysis** and improve your resume accordingly

## Project Structure

```
rescriq/
├── .venv/              # Virtual environment
├── main.py             # Main Streamlit application
├── pyproject.toml      # Project dependencies
├── uv.lock            # Locked dependency versions
├── .env.example       # Environment variables template
└── README.md          # This file
```

## Dependencies

- **Streamlit**: Web application framework
- **OpenAI**: AI analysis capabilities
- **PyPDF2**: PDF text extraction
- **python-docx**: Word document text extraction
- **python-dotenv**: Environment variable management

## Getting an OpenAI API Key

1. Go to [OpenAI's website](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to the API section
4. Create a new API key
5. Copy the key and add it to your `.env` file

## Tips for Best Results

- Upload a well-formatted resume (PDF, DOCX, or TXT)
- Ensure your resume text is clear and readable
- The AI works best with resumes that have good structure
- Consider the feedback as suggestions, not absolute rules

## Troubleshooting

- **"Error reading file"**: Make sure your file is not password-protected and contains extractable text
- **"Error analyzing resume"**: Check that your OpenAI API key is correct and has sufficient credits
- **App won't start**: Make sure you've activated the virtual environment and installed all dependencies

## Next Steps

This is a basic implementation. You can enhance it by:
- Adding more analysis criteria
- Implementing resume scoring
- Adding comparison features
- Creating user accounts and saving analysis history
- Adding more file format support (DOCX, TXT, etc.)
