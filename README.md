# MSME Copilot 🚀

AI-powered business consultant and market research agent built for Micro, Small & Medium Enterprises (MSMEs).

## What It Does

MSME Copilot uses a **multi-agent AI system** to provide small business owners with:

- 📊 **Data Analysis** — Analyze business data and generate visual insights
- 🔍 **Market Research** — Real-time web research on competitors, trends, and opportunities
- 💼 **Business Consulting** — Tailored advice for your specific business type
- 📝 **Strategic Planning** — Actionable business plans with AI-driven recommendations
- 📄 **PDF Reports** — Export findings as downloadable reports

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| AI Model | Google Gemini 1.5 Flash |
| Web Search | Tavily API |
| Charts | Plotly |
| Reports | FPDF2 |

## Quick Start

1. **Clone the repo**
   ```bash
   git clone https://github.com/Sandeep1108c/msme-copilot.git
   cd msme-copilot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** — Create a `.env` file:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

## Project Structure

```
├── app.py              # Main Streamlit application
├── config.py           # App configuration
├── agents/             # AI agent modules
│   ├── orchestrator.py # Coordinates all agents
│   ├── consultant.py   # Business consulting agent
│   ├── planner.py      # Strategic planning agent
│   ├── critic.py       # Review & validation agent
│   ├── data_analyst.py # Data analysis agent
│   └── web_researcher.py # Market research agent
├── ui/                 # UI components
├── utils/              # Helper utilities
└── requirements.txt    # Python dependencies
```

## License

This project is for educational and personal use.
