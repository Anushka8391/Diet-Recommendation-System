Website:- http://nutri-plan-bice.vercel.app/

# Diet Recommendation System

This repository contains:
- FastAPI backend (ML recommendation API)
- React frontend (desktop and mobile responsive UI)
- Optional Streamlit frontend

## 1) Quick Start (Docker, Recommended)

Prerequisites:
- Docker Desktop
- Docker Compose (included with Docker Desktop)

From the project root:

```bash
docker compose up --build -d
```

Services:
- Frontend: http://localhost
- Backend API docs: http://localhost:8080/docs

Stop services:

```bash
docker compose down
```

## 2) Access From Mobile Devices (Same Wi-Fi)

1. Find your computer LAN IP (example: 192.168.1.25).
2. Keep Docker services running.
3. Open on phone browser:
   - http://YOUR_LAN_IP
   - Example: http://192.168.1.25

Important:
- Allow Docker/Desktop app through Windows Firewall.
- Ensure phone and computer are on the same network.

## 3) Local Dev Run (Without Docker)

### Backend

```bash
cd FastAPI_Backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### React Frontend

```bash
cd react_frontend
npm install
npm run dev -- --host
```

Frontend dev URL:
- http://localhost:5173

For phone testing in dev mode:
- http://YOUR_LAN_IP:5173

## 4) Health Checks

- Backend health: http://localhost:8080/
- Frontend should load recommendation pages without API errors.

## 5) Troubleshooting

- Port conflict:
  - Change mapped ports in docker-compose.yml if 80/8080 are already used.
- Backend starts slowly first time:
  - Dataset loading may take some time on first run.
- Mobile cannot open site:
  - Confirm Windows Firewall allows inbound traffic for Docker or the used ports.

## 6) Deploy on Vercel (Frontend) + Render (Backend)

Use this setup for a fully online app that works on desktop and mobile devices.

### Step A: Deploy backend (Render)

1. Push this repository to GitHub.
2. In Render, create a new `Web Service` from this repo.
3. Render can use `render.yaml` automatically, or set manually:
   - Build Command: `pip install -r FastAPI_Backend/requirements.txt`
   - Start Command: `cd FastAPI_Backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. After deploy, copy backend URL, for example:
   - `https://diet-backend.onrender.com`

### Step B: Deploy frontend (Vercel)

1. In Vercel, import the same GitHub repository.
2. Set `Root Directory` to `react_frontend`.
3. Add Environment Variable:
   - `VITE_API_URL` = `https://YOUR_BACKEND_URL`
     - Example: `https://diet-backend.onrender.com`
4. Deploy.

### Step C: Enable CORS for Vercel domain in backend

In Render environment variables, set:

- `ALLOWED_ORIGINS` = `https://YOUR_VERCEL_DOMAIN`
  - Example: `https://diet-recommendation.vercel.app`

If you have preview + production domains, separate by comma:

- `ALLOWED_ORIGINS` = `https://your-app.vercel.app,https://your-app-git-main.vercel.app`

### Step D: Verify

1. Open your Vercel URL on desktop browser.
2. Open the same URL on mobile browser.
3. Generate meal plan and custom recommendations.
4. Confirm API calls succeed (no CORS errors).
