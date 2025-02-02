# Django FAQ Project Backend

This project is a Django-based FAQ platform that supports multiple language translations. The platform uses Docker containers to run the Django application and Redis for caching. The application allows you to create, update, and retrieve FAQ entries in English, Hindi, and Bengali. Redis is used for caching translated content and session management.

## Features

- **Multiple Language Support**: FAQs can be translated from English to Hindi, and Bengali (other languages can be added easily.)
- **Caching with Redis**: Translations and session data are cached using Redis to improve performance.
- **Dockerized Application**: The application is containerized using Docker for easy setup and deployment.
- **Django Admin**: Allows admins to manage FAQ entries directly from the web interface.
- **WYSIWYG Editor Integration**: The application features the powerful ckeditor for better writing.

## One click Setup
#### Requirements
- Docker
- Docker Compose 

Just copy the commands below to get the application running!

```bash
git clone https://github.com/ViragJain3010/faq_backend #Clone the repository
cd faq_backend

docker compose up --build # Build and Run the Docker Containers
```

## Setup (In case the above installation doesn't work)
#### Requirements
- Redis
- Python3

To setup the project locally (**without Docker**) follow the following steps:
```bash
git clone https://github.com/ViragJain3010/faq_backend #Clone the repository
cd faq_backend
```

### 1. Create and activate a virtual env

```bash
python -m venv venv
source venv/bin/acitvate # ON MACOS & LINUX
```

### 2. Install all the dependencies

```bash
pip install -r requirements.txt  
```

>**Note:** Replace the following line in `core/settings.py`:  
`
"LOCATION": "redis://redis:6379/1"
`
with:
`
"LOCATION": "redis://127.0.0.1:6379/1"
`  

### 3. Run the app
```bash
python manage.py runserver
```

## Interface

1. You can access the Django app in your browser at -> http://127.0.0.1:8000/

2. You can access the **Django admin interface** at: http://127.0.0.1:8000//admin/

    > Use username="admin" and password="0000" to log in.

    The admin interface allows you to manage the FAQ entries and translations.

## Functionalities
- **Create FAQs**: You can add new FAQ entries directly through the Django admin interface or via API endpoints.
- **Update FAQs**: You can update FAQs and their translations directly through the admin interface or API.
- **Cache**: The Redis cache will store the translations for fast access. Cache invalidation and updates are handled when English content is updated.

## How It Works  

### 1. Managing FAQs (Admin)  
- Add a new FAQ with an **English question and answer**, then save it.  
- The answer is automatically translated into supported languages (Hindi, Bengali).  
- Updating the English content will **re-translate** the other languages automatically.  
- Not satisfied with the translation? No problem! You can **manually edit** the translated content and save it. This gives you full control while still benefiting from automatic translation. 

### 2. Fetching FAQs (API)  
- The FAQs can be retrieved via an API that returns content in multiple languages.
- If a user requests FAQs in Hindi (`/api/faqs/?lang=hi`), the cached translation is served instantly.  
- If no cached version exists, the database is queried, ensuring fast performance.  

### 3. Caching & Performance  
- Translated FAQs are cached for quick retrieval.  
- If the FAQ is updated, the cache is automatically cleared and refreshed.  

## Why This Workflow?  

Most developers prefer English as their primary language for development. Hence, we chose English as the base language for FAQs.  
This workflow is designed to be **user-centric**, requiring minimal effort:  
- Automatic translations reduce manual work.  
- Editable translations ensure flexibility.  

## Project Structure

```
/core -> Project directory
/faq  -> App directory
/faq/services -> Contains all the functions related to caching and translation
/faq/tests -> Contains test cases for testing
```

## Testing
For running the testcases run `pytest` in the root directory.

## Want to see a Demo?

![FAQ Demo](./asset/demo.mp4)

## A Note For the Evaluator

As a MERN developer, my primary expertise is in JavaScript technologies. Although Django is relatively new to me, I embraced the opportunity to work with Python, as it was the preferred language for this role. I’ve put in my best effort to deliver a solid solution with the required tech stack, and I’m eager to learn and improve from any feedback you may have. I appreciate your understanding and look forward to any suggestions for further enhancements!