# RAG ChatBot Deployment Guide

Your RAG chatbot can be deployed on various platforms. Here are the available options:

## Quick Local Testing

First, test locally:
```bash
# Install dependencies
pip install -r requirements.txt

# Ingest your documents
python ingest.py --docs docs/ --index index/

# Run the web app
streamlit run app.py
```

## Deployment Options

### 1. 🚀 Streamlit Community Cloud (Recommended - Free)

1. Push your code to GitHub (already done!)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy from `Samridhi29/RAG-chatbot`
5. Add your `LLM_API_KEY` in secrets

### 2. 🌊 Render (Free Tier)

1. Go to [render.com](https://render.com)
2. Connect your GitHub repo
3. Use the `render.yaml` configuration (already included)
4. Set environment variable: `LLM_API_KEY`

### 3. 🚂 Railway

1. Go to [railway.app](https://railway.app)
2. Deploy from GitHub
3. Uses `railway.toml` configuration
4. Set environment variable: `LLM_API_KEY`

### 4. 🐳 Docker

```bash
# Build the image
docker build -t rag-chatbot .

# Run locally
docker run -p 8501:8501 -e LLM_API_KEY=your_key rag-chatbot

# Or deploy to any cloud that supports Docker
```

### 5. ☁️ Heroku

```bash
# Install Heroku CLI and login
heroku create rag-chatbot-app

# Set config
heroku config:set LLM_API_KEY=your_key

# Deploy
git push heroku main
```

## Environment Variables

All deployments need:
- `LLM_API_KEY`: Your OpenAI/Claude/etc API key

## Notes

- The app includes a sample document in `docs/sample.md`
- Upload your documents to `docs/` folder before deployment
- The index is built automatically during first run
- Web interface runs on port 8501 by default