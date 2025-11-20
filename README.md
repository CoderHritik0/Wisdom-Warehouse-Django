
# Wisdom Warehouse

A Simple & Powerful Django Notes Application

<br>


## Overview
Wisdom Warehouse is a Django-based notes management application built to help users easily create, organize, and manage their personal notes. With features like tagging, image attachments, secure authentication, and a modern responsive UI, it provides a smooth, efficient, and clutter-free note-taking experience. Whether you're storing ideas, tasks, or personal information, Wisdom Warehouse keeps everything organized in one place.

<br>


## Features

- 📝 Create, Edit & Delete Notes
- 🏷️ Tag-based organization
- 🔒 User authentication (Login, Signup, Password Reset)
- 🖼️ Attach images to notes
- 📁 Manage your profile and uploaded images
- 🌗 Light/Dark theme support
- 📱 Responsive UI using Bootstrap
- ⚡ Optimized database and clean architecture
- ✍️ Markdown support with live preview


<br>


## Tech Stack

- **Backend:** Django, Python

- **Frontend:** HTML, CSS, Bootstrap, JavaScript

- **Database:** SQLite (default)

- **Storage:** Django File/Image handling

- **Others:** Custom Django Forms & Widgets

  
<br>


## Run Locally

Clone the project

```bash
  git clone https://github.com/CoderHritik0/Wisdom-Warehouse-Django.git
```

Go to the project directory

```bash
  cd Wisdom-Warehouse-Django
```

Create and activate a virtual environment

```bash
  python -m venv .venv
  .venv/Scripts/activate   # Windows  
  source .venv/bin/activate  # macOS/Linux

```

Install dependencies

```bash
  pip install -r requirement.txt
```

Run migrations

```bash
  python manage.py migrate
```

Start the development server

```bash
  python manage.py runserver
```

Now visit:
👉 http://127.0.0.1:8000/


<br>


## Project Structure
```
wisdom-warehouse-django/
│── .venv/
│
│── notes/
│   ├── forms/
│   │   ├── account_forms.py
│   │   ├── base.py
│   │   ├── note_forms.py
│   │   ├── profile_forms.py
│   │   └── user_forms.py
│   │
│   ├── templates/
│   │   └── notes/
│   │       ├── create_note.html
│   │       ├── index.html
│   │       ├── note_list.html
│   │       └── login_layout.html
│   │
│   ├── views/
│   │   ├── auth_views.py
│   │   ├── notes_views.py
│   │   ├── profile_views.py
│   │   └── utils.py
│   │
│   └── models.py
│
│── notesApp/
│   ├── forms.py
│   ├── settings.py
│   ├── urls.py
│   └── views.py
│
│── static/
│   ├── favicon.ico
│   ├── home_bg.png
│   ├── Logo.png
│   ├── script.js
│   └── style.css
│
│── templates/
│   ├── registration/
│   │   ├── login.html
│   │   ├── password_reset.html
│   │   ├── password_reset_email.html
│   │   ├── password_reset_email_subject.txt
│   │   ├── password_reset_done.html
│   │   ├── password_reset_confirm.html
│   │   ├── password_reset_complete.html
│   │   ├── signup.html
│   │   └── profile.html
│   │
│   └── website/
│       ├── features.html
│       ├── index.html
│       └── layout.html
│
│── manage.py
│── db.sqlite3
└── requirements.txt

```


<br>


## Environment Variables

Create a *.env* file for secret keys:

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_password
DEFAULT_FROM_EMAIL=company_name <your_email>

```


<br>


## Future Enhancements
- 🧠 AI-powered smart tagging

- 📤 Export notes as PDF

- 🤝 Collaboration and sharing
 
<br>


## Contributing

Pull requests are welcome! For major changes, open an issue first to discuss your idea.


<br>


## Demo

[Live Demo](https://hritiksanas.pythonanywhere.com/)


<br>


## Authors

[@CoderHritik0](https://github.com/CoderHritik0)

