cat > README.md <<'EOF'
# Django LMS

Учебный проект на Django REST Framework с PostgreSQL и автоматическим CI/CD через GitHub Actions.

## Стек

- Python 3.12
- Django
- Django REST Framework
- PostgreSQL
- Gunicorn
- Nginx
- Celery
- Redis
- GitHub Actions
- Ubuntu

## Структура проекта

```text
.github/workflows/deploy.yml   # CI/CD
config/                        # настройки Django
django_lms/                    # основной проект
lms/                           # приложение LMS
users/                         # приложение пользователей
manage.py
Dockerfile
docker-compose.yml
