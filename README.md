


# 🥗 AI-Powered Diet Recommendation System

## 🧠 Overview
An end-to-end ML-based system that generates personalized meal plans using user health parameters (BMI, age, goals), achieving ~2s response latency with a scalable FastAPI + React architecture.

It integrates a **machine learning-powered backend (FastAPI)** with a **responsive React frontend**, enabling real-time recommendation generation.

---

## ⚙️ Tech Stack
- **Frontend:** React.js (Responsive UI)
- **Backend:** FastAPI (Python)
- **Machine Learning:** Custom recommendation logic
- **Deployment:** Docker, Vercel, Render

---

## ✨ Key Features
- 🤖 AI-driven personalized diet recommendations  
- 📊 Real-time meal plan generation  
- 📱 Fully responsive (desktop + mobile access)  
- ⚡ Fast API responses (~1–2 seconds)  
- 🐳 Dockerized for scalable deployment  
- 🌐 Cross-device accessibility (LAN + deployed app)

---

## 📊 Project Highlights
- Handles **multiple user parameters** to generate customized outputs  
- Achieves **real-time response latency under ~2 seconds**  
- Designed with **modular full-stack architecture**  
- Supports **mobile + desktop usage across networks**

---


## 🧪 System Architecture
- Frontend communicates with FastAPI backend via REST APIs  
- Backend processes inputs and applies ML-based recommendation logic  
- Data handling optimized for quick response generation  

---

## 🚀 Run Locally

### Using Docker (Recommended)
```bash
docker compose up --build -d

•Frontend: http://localhost

•Backend Docs: http://localhost:8080/docs

Stop services:

docker compose down

 Local Development Setup

Backend

cd FastAPI_Backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080 --reload

Frontend

cd react_frontend
npm install
npm run dev -- --host

Frontend URL:

http://localhost:5173

📱 Mobile Testing (Same Wi-Fi)

Access via: http://YOUR_LAN_IP:5173

Example: http://<LAN_IP>:5173

🌐 Deployment

Backend (Render)

Deploy FastAPI backend

Example: https://your-backend.onrender.com

Frontend (Vercel)

Root directory: react_frontend

Add environment variable:

VITE_API_URL = https://your-backend-url

🔧 Troubleshooting

Port conflicts → update docker-compose ports

Slow startup → initial dataset loading delay

Mobile access issues → check firewall & network

📌 Future Improvements

Integration of advanced ML models (deep learning)

User authentication & personalization tracking

🎯 Impact

This project demonstrates:

Ability to build AI-integrated full-stack systems

Strong understanding of API design using FastAPI

Experience in deploying scalable applications using Docker + cloud platforms


