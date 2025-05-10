# Backend  
**Alex - Video AI Tutor**

---

## 🛠️ Setup Instructions

### ✅ Create Virtual Environment

Windows:
```bash
python -m venv venv
```

Linux:
```bash
python3 -m venv venv
```

### ⚡ Activate Virtual Environment

Windows:
```bash
venv\Scripts\activate
```

Linux:
```bash
source venv/bin/activate
```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 🚀 Run the Application

```bash
python -m uvicorn api:app --reload
```

---

## 🐳 Build and Push Docker Image

```bash
docker build -t {docker username}/video_ai_tutor:latest .
docker push {docker username}/video_ai_tutor:latest
```

---

## 🧪 Local Development with Docker Compose

Make sure you have a `docker-compose.yml` file in your project directory.

### ▶️ Run with Docker Compose

```bash
docker-compose up --build
```

### 🛑 Stop the Containers

```bash
docker-compose down
```
