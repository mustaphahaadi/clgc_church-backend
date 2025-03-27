# Church App Backend

This is the backend service for the Church App, built with Django and Django REST Framework. It provides a robust API for managing church members, testimonies, and other church-related functionalities.

## Technology Stack

- Python 3.x
- Django
- Django REST Framework
- Pillow (for image handling)
- SQLite (default database)

## Getting Started

### Prerequisites

Ensure you have Python 3.x installed on your system. You can check your Python version by running:

```bash
python --version
```

### Installation

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser (admin):
   ```bash
   python manage.py createsuperuser
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

- `clgc_backend/` - Main project configuration
- `members/` - App handling user management and profiles
- `templates/` - HTML templates
- `docs.md` - Detailed API documentation

## Key Features

- Custom user authentication system
- Member profile management
- Testimony submission system
- RESTful API endpoints

## Development Guidelines

1. Follow PEP 8 style guide for Python code
2. Write tests for new features
3. Document API endpoints in `docs.md`
4. Use meaningful commit messages

## API Overview

Detailed API documentation can be found in `docs.md`. Key endpoints include:

- User Authentication
- Profile Management
- Testimony Submission

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## License

This project is licensed under the MIT License.
