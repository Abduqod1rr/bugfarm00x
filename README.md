# 🐛 bugfarm00x — Vulnerable Django Learning Platform

**bugfarm00x** is a deliberately vulnerable Django application designed for **security education and ethical hacking training**. It contains 7 real-world vulnerabilities for learners to discover, exploit, and fix.

⚠️ **WARNING:** Do not deploy this publicly or connect it to any production system. It is intentionally insecure.

---

## 🧪 Vulnerabilities

| # | Vulnerability | Location | Difficulty |
|---|---------------|----------|------------|
| 1 | **SQL Injection** | Login form (`main/views.py:UserLogin`) | Easy |
| 2 | **Reflected XSS** | Search bar (`tamplates/home.html`) | Easy |
| 3 | **IDOR** | Profile view (`main/views.py:UserProfile`) | Medium |
| 4 | **Unrestricted File Upload** | Post creation (`main/views.py:AddPoc`) | Medium |
| 5 | **Open Redirect** | Login redirect (`main/views.py:UserLogin`) | Easy |
| 6 | **Information Disclosure** | Settings (`picpok/settings.py`) | Easy |
| 7 | **Weak Password Storage** | Registration (`main/forms.py`) | Hard |

Each vulnerability is tagged with `# VULN:` comments in the source code for learners to find.

---

## 🚀 Quick Start

```bash
# Clone & enter
git clone https://github.com/yourusername/bugfarm00x.git
cd bugfarm00x

# Install dependencies
pip install -r requirements.txt

# Set up database
python manage.py migrate

# Run
python manage.py runserver
```

Visit **http://localhost:8000** to start.

### Demo credentials
- **Username:** `demo`
- **Password:** `demo1234`

Or register a new account at `/register/`.

---

## 🗺️ Routes

| Route | Page | Purpose |
|-------|------|---------|
| `/` | Landing | BugFarm home with challenge overview |
| `/feed/` | Feed | Main content feed (TikTok-style scrolling) |
| `/login/` | Challenge #1 | SQL injection login |
| `/register/` | Register | Create account (plaintext passwords) |
| `/scoreboard/` | Scoreboard | Track which bugs you've found |
| `/hints/` | Hints | 3 hints per vulnerability |
| `/solutions/` | Solutions | Full fix guide for each bug |
| `/profile/<id>/` | Challenge #3 | IDOR — view any user's profile |
| `/addpoc/` | Challenge #4 | Upload arbitrary files |
| `/myprofile/` | Profile | Your own profile |
| `/mypocs/` | My Posts | Your uploaded posts |

---

## 🐳 Docker

```bash
docker build -t bugfarm00x .
docker run -p 8000:8000 bugfarm00x
```

---

## ☁️ Deploy to Render

1. Push repo to GitHub
2. On Render dashboard: **New + → Web Service**
3. Connect your repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput`
   - **Start Command:** `gunicorn picpok.wsgi:application --bind 0.0.0.0:$PORT --workers 2`
5. Deploy

---

## 📁 Project Structure

```
bugfarm00x/
├── main/                   # Django app (views, models, forms, urls)
│   ├── views.py            # All views — vulnerabilities are here
│   ├── models.py           # Poc, Profile, Comment, BugProgress
│   ├── forms.py            # User registration (plaintext passwords)
│   └── migrations/         # DB migrations + seed data
├── picpok/                 # Django project config
│   └── settings.py         # DEBUG=True, SQLite, whitenoise
├── tamplates/              # HTML templates
│   ├── landing.html        # BugFarm landing page
│   ├── home.html           # Feed with XSS in search
│   ├── login.html          # Login with SQLi
│   ├── hints.html          # Hint system
│   ├── solutions.html      # Fix guide
│   └── scoreboard.html     # Progress tracker
├── static/                 # CSS files
├── media/                  # Uploaded files
├── Procfile                # Render/gunicorn
├── runtime.txt             # Python 3.12.3
├── dockerfile              # Docker build
└── requirements.txt        # Dependencies
```

---

## 🎯 Learning Path

1. **Find** the vulnerability by exploring the app and reading source code
2. **Exploit** it using the hints if you get stuck
3. **Fix** it by checking the solutions page
4. **Mark** it as found on the scoreboard

---

## ⚖️ Legal

This project is for **authorized security training only**. Do not use these techniques against systems you do not own or have explicit permission to test. The authors assume no liability for misuse.

---

## 🧑‍💻 Author

**Abduqodir (Ben Morgan)** — Built with Django for cybersecurity education
