# psxGPT

A ChatGPT-like application for Pakistan Stock Exchange (PSX) financial data, which can be repurposed for any financial data including querying a data room during acquisition due diligence.

## What psxGPT Does

psxGPT allows financial analysts to query and analyze financial data using plain English. For example:

*"Get me Deposits per branch for HBL, UBL and MEBL in 2024"*

psxGPT will find the necessary information and compile a report using ONLY data found in financial reports.

**Use Cases:**
- Financial statement analysis and comparison
- Due diligence data room queries
- Regulatory filing research
- Querying Economic Survey of Pakistan or SBP Annual Report

## How It Works

psxGPT processes financial documents through an 8-step pipeline:

1. **Download PDFs** (`Step1DownloadPDFsSearch.py` or `Step1DownloadPDFsTickers.py`)
2. **Convert to Markdown** (`Step2ConvertPDFtoMarkdown.py`) - Uses LlamaParse or `Tool1Mistral_OCR.py` for scanned documents
3. **Create Chunks** (`Step3ChunkMarkdown.py`) - Splits into searchable segments
4. **Extract Metadata** (`Step4MetaDataTags.py`) - Identifies companies, dates, report types
5. **Combine Data** (`Step5CombineMetaData.py`) - Consolidates all metadata
6. **Build Search Index** (`Step6CreateEmbeddings.py`) - Creates vector embeddings for AI search
7. **Start Backend Server** (`Step7MCPServerPsxGPT.py`) - Launches the data query server
8. **Launch Web Interface** (`Step8MCPClientPsxGPT.py` for using with Anthropic API or `Step8MCPClientGemini.py` for using with Gemini API (free tier)) - Starts the user-friendly chat interface

**Quality Assurance:** Use `Tool2ValidateProcessing.py` to verify data quality after processing.

## How to Get Started

### Overview

This guide walks you through setting up psxGPT step-by-step. The process takes about 30-45 minutes and involves:

1. **Installing required software** (Git, Python, PostgreSQL, code editor)  
2. **Downloading the project** from GitHub
3. **Getting API keys** for AI services
4. **Configuring the environment** and installing dependencies
5. **Setting up the database** and starting the application

### Prerequisites

Before starting, you'll need:
- A computer with Windows, macOS, or Linux
- Internet connection for downloads
- API keys for AI services (some free, some require credit card)

### Step 1: Install Code Editor (IDE)

Choose one of these beginner-friendly code editors:
- **[Windsurf](https://www.windsurf.io/)** (Recommended - AI-powered coding assistant)
- **[Cursor](https://cursor.sh/)** (AI-powered VS Code alternative)
- **[VS Code](https://code.visualstudio.com/)** (Popular free editor)

Download and install your chosen editor following the installer instructions.

### Step 2: Install Git

**For Windows Users:**
1. **Check Your PC Type First:**
   - Press `Windows key + R` to open the Run dialog
   - Type `msinfo32` and press Enter
   - Look for "System Type" in the System Information window:
     - **x64-based PC** = Intel/AMD processor (most common)
     - **ARM64-based PC** = ARM processor (newer Surface devices, some laptops)

2. Go to [https://git-scm.com/download/win](https://git-scm.com/download/win)
3. Download the correct installer for your system:
   - **64-bit Git for Windows Setup** (for x64-based PC)
   - **ARM64 Git for Windows Setup** (for ARM64-based PC)
4. Run the installer and follow the setup wizard
5. **Installation tip:** The installer will ask many questions about editors, line endings, etc. For this project, these choices don't matter - simply keep clicking "Next" with the default options
6. When installation is complete, you can access Git through "Git Bash" or Command Prompt

**For Mac Users:**
1. **Check Your Mac Type:**
   - Click the Apple menu → "About This Mac"
   - Look at "Chip" or "Processor":
     - **Intel** = Intel-based Mac
     - **Apple M1/M2/M3** = Apple Silicon Mac (ARM-based)

2. Open Terminal (press `Cmd + Space`, type "Terminal", and press Enter)
3. Type the following command and press Enter:
   ```
   git --version
   ```
4. If Git is not installed, macOS will prompt you to install it automatically
5. Follow the installation prompts

### Step 3: Install Python 3.11.9 (64-bit)

**IMPORTANT:** You must install Python 3.11.9 specifically, and it must be the 64-bit version for maximum stability.

**For Windows Users:**
1. Go to [https://www.python.org/downloads/release/python-3119/](https://www.python.org/downloads/release/python-3119/)
2. Scroll down to "Files" section
3. Download "Windows installer (64-bit)" - make sure it says 64-bit
4. Run the installer
5. **CRITICAL:** Check the box "Add Python to PATH" during installation - this is essential for the project to work
6. Click "Install Now"

**For Mac Users:**
1. Go to [https://www.python.org/downloads/release/python-3119/](https://www.python.org/downloads/release/python-3119/)
2. Scroll down to "Files" section  
3. Download "macOS 64-bit universal2 installer"
4. Run the installer and follow the prompts
5. **Note:** Python is automatically added to PATH on macOS

### Step 4: Install PostgreSQL 14.18 Database

**For Windows Users:**
1. Visit [PostgreSQL 14.18 Downloads](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
2. Download PostgreSQL 14.18 for Windows x86-64
3. Run the installer and follow the setup wizard
4. **Component Selection:** To minimize installation size, only keep these components checked:
   - ✅ **PostgreSQL Server** (required)
   - ✅ **Command Line Tools** (required)
   - ❌ **pgAdmin 4** (uncheck - not needed, saves ~200MB)
   - ❌ **Stack Builder** (uncheck - not needed)
5. **Critical:** During installation, you'll set a password for the default "postgres" user. **Write this password down** - you'll need it for your .env file
6. **Username Note:** The default PostgreSQL username is "postgres" (not your Windows username)

**For Mac Users:**
1. Visit [PostgreSQL 14.18 Downloads](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
2. Download PostgreSQL 14.18 for macOS
3. Run the installer and follow the setup wizard
4. **Component Selection:** To minimize installation size, only keep these components checked:
   - ✅ **PostgreSQL Server** (required)
   - ✅ **Command Line Tools** (required)
   - ❌ **pgAdmin 4** (uncheck - not needed, saves ~200MB)
   - ❌ **Stack Builder** (uncheck - not needed)
5. **Critical:** During installation, you'll set a password for the default "postgres" user. **Write this password down** - you'll need it for your .env file
6. **Username Note:** The default PostgreSQL username is "postgres" (not your Mac username)

**Alternative Installation (Advanced Users):**
- **Homebrew (Mac):** `brew install postgresql@14`
- **Package Manager (Linux):** Check your distribution's package manager for PostgreSQL 14.x

### Step 5: Download and Setup psxGPT

1. **Open your code editor**
2. **Open the integrated terminal:**
   - Press `Ctrl + ` (backtick) to open the terminal inside your code editor
3. **Download the project:**

**Recommended: Fast Clone (Downloads Latest Code Only)**
```bash
git clone --depth 1 https://github.com/ishaheen10/psxgpt.git
cd psxgpt
```

**Alternative: Full History Clone (Larger Download)**
```bash
git clone https://github.com/ishaheen10/psxgpt.git
cd psxgpt
```

> **💡 Note:** The repository has been optimized for size. The shallow clone (`--depth 1`) downloads only the latest code (~19MB) instead of full history, making setup much faster for most users.

### Step 6: Get Your API Keys

You'll need to sign up for these services and get API keys:

**Required (Free - No Credit Card Needed):**

1. **[Google Gemini API](https://ai.google.dev/)** 
   - Click "Get API key in Google AI Studio"
   - Sign in with your Google account
   - Create a new API key
   - Copy the key

2. **[LlamaParse API](https://docs.cloud.llamaindex.ai/llamacloud/getting_started/api_key)**
   - Sign up for LlamaCloud
   - Go to API Keys section
   - Create a new API key
   - Copy the key (free tier includes 3,000 pages)

**Optional (Credit Card Required):**

3. **[Anthropic API](https://www.anthropic.com/)** 
   - Sign up for an Anthropic account
   - Go to your dashboard
   - Create an API key
   - Copy the key

4. **[Mistral API](https://console.mistral.ai/)** (for scanned document OCR)
   - Sign up for Mistral AI
   - Go to API Keys
   - Create a new key
   - Copy the key

**Save these keys safely** - you'll paste them into your .env file in the next step.

### Step 7: Configure Environment and Install Dependencies

1. **Create your environment file:**
   - Simply rename `.env.example` to `.env`
   - Open the `.env` file in your code editor
   - Paste in your API keys from Step 6
   - Update the DATABASE_URL with your PostgreSQL password

2. **Install dependencies:**
   ```bash
   pip install uv
   uv sync
   ```

3. **Enter virtual environment:**

   **For Windows:**
   ```bash
   .venv\Scripts\activate
   ```

   **For Mac/Linux:**
   ```bash
   source .venv/bin/activate
   ```

### Version Compatibility Note

The specified versions (Python 3.11.9, PostgreSQL 14.18, Chainlit 2.5.5) are recommended for maximum stability and have been thoroughly tested with this project. While newer versions may work, these specific versions ensure the most reliable experience and avoid potential compatibility issues.

### Step 8: Setup Database

1. **Create the database:**
   ```bash
   createdb analyst_psx
   ```

2. **Setup the database schema:**
   ```bash
   psql -d analyst_psx -f chainlit_schema_psx.sql
   ```

3. **Verify your configuration:**
   - Double-check that your DATABASE_URL in the `.env` file matches your PostgreSQL setup
   - Format: `postgresql://postgres:your_password@localhost:5432/analyst_psx`

### Step 9: Start the Application

**Option A: Use Pre-Built Data (Fastest)**

1. **Download pre-built search index** from Google Drive:
   [Download gemini_index_metadata.zip](https://drive.google.com/file/d/1yeH1ib5G1jBnqhzzoYBoZ0yz5s1y9MOP/view?usp=drive_link)

2. **Unzip and place in project directory:**
   - Unzip the file - you should see a folder called `gemini_index_metadata`
   - Copy this entire folder to your psxChatGPT project directory (same level as Python files)

3. **Start the application:**
   ```bash
   python Step6CreateEmbeddings.py
   chainlit run Step8MCPClientPsxGPT.py
   ```
   
   **Alternative (for Gemini API free tier):**
   ```bash
   chainlit run Step8MCPClientGemini.py
   ```

4. **Access the application:**
   - Open your browser to http://localhost:8000
   - Login with: `analyst@psx.com` / `analyst123`

**Option B: Process Your Own Documents**

If you want to analyze your own financial documents:

1. **Install Playwright** (for downloading PDFs from websites):
   ```bash
   playwright install
   ```

2. **Run the processing pipeline:**
   ```bash
   # Option 1: Download from PSX website
   python Step1DownloadPDFsSearch.py
   
   # Option 2: Place your own PDFs in psx_bank_reports/ folder, then run:
   python Step2ConvertPDFtoMarkdown.py
   python Step3ChunkMarkdown.py
   python Step4MetaDataTags.py
   python Step5CombineMetaData.py
   python Tool2ValidateProcessing.py   # Verify data quality
   python Step6CreateEmbeddings.py
   chainlit run Step8MCPClientPsxGPT.py
   ```
   
   **Alternative (for Gemini API free tier):**
   ```bash
   chainlit run Step8MCPClientGemini.py
   ```

*Note: Step1 scripts are designed for PSX website. For other data sources, modify the download scripts or use a browser automation tool like browser-use.*

## Customization for Other Financial Data

To adapt psxGPT for different financial datasets:

1. **Replace Data Source**: Modify `Step1DownloadPDFsSearch.py` to point to your data source
2. **Update File Paths**: Change directory paths in scripts to match your folder structure
3. **Adjust Metadata Extraction**: Modify `Step4MetaDataTags.py` for your document types
4. **Configure OCR**: For scanned documents, ensure Mistral OCR is configured in `Step2ConvertPDFtoMarkdown.py`

## Troubleshooting

**Common Issues:**
- **Scanned PDFs**: Use Mistral OCR option in Step 2 for better text extraction
- **Large Files**: LlamaParse free tier has 3,000 page limit
- **Database Connection**: Verify PostgreSQL is running and credentials in `.env` are correct
- **API Limits**: Check API key quotas if processing fails

**Performance:**
- Processing time depends on document count and size
- Vector embedding creation (Step 6) is the most time-intensive step
- Consider processing documents in batches for large datasets

## Authentication

**Default Login Credentials:**
- **Username:** `analyst@psx.com`
- **Password:** `analyst123`

*Note: These are demo credentials configured in your .env file. For production use, implement proper authentication.*

## 📄 License

MIT License

Copyright (c) 2024 psxGPT Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.