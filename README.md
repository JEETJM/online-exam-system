<div align="center">

# 🎓 ExamSphere — Online Examination System

### A modern Django-based Online Examination Platform for Students, Teachers, and Admins

<p align="center">
  <img src="https://img.shields.io/badge/Django-6.0-success?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge&logo=bootstrap&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-Database-07405E?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/github/repo-size/JEETJM/online-exam-system?style=flat-square" />
  <img src="https://img.shields.io/github/languages/top/JEETJM/online-exam-system?style=flat-square" />
  <img src="https://img.shields.io/github/last-commit/JEETJM/online-exam-system?style=flat-square" />
  <img src="https://img.shields.io/github/issues/JEETJM/online-exam-system?style=flat-square" />
  <img src="https://img.shields.io/github/stars/JEETJM/online-exam-system?style=flat-square" />
</p>

</div>

---

## 📌 Overview

**ExamSphere** is a full-featured **Online Examination System** built using **Django**, designed for secure and efficient exam management.

It provides:

- 👨‍🎓 **Student Panel**
- 👨‍🏫 **Teacher Panel**
- 🛠️ **Admin Panel**
- ⏱️ Timed online exams
- 📊 Instant result generation
- 📝 Question management
- 📢 Announcements
- 🎫 Support ticket system
- 🎨 Beautiful responsive UI

This project is ideal for **college projects**, **academic demonstrations**, and **real-world online exam workflows**.

---

## 🚀 Features

### 👨‍🎓 Student Features
- Student registration and login
- View available exams
- Read exam instructions
- Start timed exams
- Auto-submit when time ends
- View instant results
- Answer review after submission
- Previous attempts and result history
- Create support tickets
- View announcements

### 👨‍🏫 Teacher Features
- Teacher registration and login
- Create exams
- Edit and delete exams
- Add, edit, and delete questions
- Publish and manage exams
- Set passing marks and attempt limits
- View student exam records
- Track exam-related information

### 🛠️ Admin Features
- Full Django admin control
- Manage users
- Manage exams
- Manage results
- Manage announcements
- Manage support tickets
- Manage departments and subjects

### 💡 Core Functionalities
- Role-based authentication
- Exam scheduling support
- Secure login/logout
- MCQ-based question system
- Automatic marks calculation
- Pass/Fail status generation
- Responsive dashboard
- Premium UI with animations and hover effects

---

## 🏗️ Tech Stack

| Category | Technology |
|---------|------------|
| Backend | Django |
| Language | Python |
| Frontend | HTML, CSS, Bootstrap |
| Database | SQLite |
| Authentication | Django Auth |
| Icons | Bootstrap Icons |
| Fonts | Google Fonts |

---

## 📂 Project Structure

```bash
online_exam_system/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
│
├── exams/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── online_exam_system/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── timer.js
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── accounts/
│   └── exams/
│
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md


⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/JEETJM/online-exam-system.git
cd online-exam-system
2️⃣ Create virtual environment
python -m venv venv
3️⃣ Activate virtual environment
Windows
venv\Scripts\activate
Mac/Linux
source venv/bin/activate
4️⃣ Install dependencies
pip install django

Or if you have requirements.txt:

pip install -r requirements.txt
5️⃣ Run migrations
python manage.py makemigrations
python manage.py migrate
6️⃣ Create superuser
python manage.py createsuperuser
7️⃣ Start development server
python manage.py runserver
8️⃣ Open in browser
http://127.0.0.1:8000/

Admin panel:

http://127.0.0.1:8000/admin/
