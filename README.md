# VitalMind AI - Antigravity Health Platform (Iqoo-Hackathon)

VitalMind AI is an interactive physiological monitoring, zero-gravity fitness, and mental wellness platform built with FastAPI and modern Vanilla UI.

---

## 🚀 Deploying to Vercel

This repository is pre-configured for **1-click deployment on Vercel** as a Python Serverless Application.

### Option 1: Deploy with Vercel CLI

1. Install the Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Run `vercel` from the root directory:
   ```bash
   vercel
   ```

3. Follow the CLI prompts. Your app will be deployed automatically!

---

### Option 2: Deploy via Vercel Dashboard (GitHub Integration)

1. Push your repository to GitHub.
2. Go to [Vercel Dashboard](https://vercel.com/new).
3. Import your GitHub repository.
4. Click **Deploy**! (Vercel automatically detects `vercel.json` and `api/index.py`).

---

## 🔑 Environment Variables (Optional)

You can set these in **Vercel Settings -> Environment Variables**:

| Variable Name | Description | Default |
|---|---|---|
| `GEMINI_API_KEY` | Google Gemini AI API key for intelligent crew assistant responses. | Built-in fallback response engine |
| `DATABASE_URL` | External PostgreSQL database connection string (e.g. Supabase / Neon / Vercel Postgres). | `/tmp/vitalmind.db` (SQLite) |
| `SECRET_KEY` | Secret key for session encryption. | `vitalmind-antigravity-secret-key-2026` |

---

## 💻 Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the development server:
   ```bash
   python run.py
   ```

3. Open your browser:
   - Web App: `http://127.0.0.1:8000`
   - Interactive API Documentation: `http://127.0.0.1:8000/docs`