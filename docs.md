# Backend Documentation

## Overview

This backend system is built using Django REST Framework, providing APIs for church member management, authentication, testimonies, and contact form handling. It uses SQLite as the database and implements JWT-based authentication.

## Setup Instructions

### Prerequisites

- Python 3.x
- Django
- Django REST Framework
- Pillow (for image handling)

### Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Start the server: `python manage.py runserver`

## API Endpoints

### Authentication

- `POST /api/auth/signup/`
  - Description: Register a new user
  - Request Body:
    ```json
    {
      "firstName": "string",
      "middleName": "string" (optional),
      "lastName": "string",
      "username": "string",
      "email": "string" (optional),
      "phoneNumber": "string",
      "countryCode": "string" (default: "+233"),
      "gender": "string" (male/female/other),
      "password": "string"
    }
    ```
  - Response: User data with JWT tokens

- `POST /api/auth/login/`
  - Description: Login user
  - Request Body:
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
  - Response: User data with JWT tokens

### User Profile

- `POST /api/user/complete-profile/`
  - Description: Complete user profile
  - Authentication: Required
  - Request Body:
    ```json
    {
      "date_of_birth": "YYYY-MM-DD",
      "house_address": "string",
      "digital_address": "string" (optional),
      "occupation": "string",
      "church_information": "string" (optional),
      "profile_image": "file" (optional),
      "fellowship": "string" (optional)
    }
    ```

- `GET /api/user/profile/`
  - Description: Get user profile
  - Authentication: Required

### Members

- `GET /api/members/`
  - Description: List all members
  - Authentication: Required
  - Pagination: Yes (10 items per page)

- `POST /api/members/`
  - Description: Register a new member
  - Authentication: Required

### Contact Form

- `POST /api/contacts/`
  - Description: Submit contact form
  - Request Body:
    ```json
    {
      "name": "string",
      "email": "string" (optional),
      "phone": "string",
      "subject": "string",
      "message": "string"
    }
    ```

### Testimonies

- `GET /api/testimonies/`
  - Description: List all testimonies
  - Pagination: Yes (10 items per page)
  - Query Parameters:
    - `page`: Page number
    - `page_size`: Items per page (max 100)

- `POST /api/testimonies/`
  - Description: Create new testimony
  - Authentication: Optional
  - Request Body:
    ```json
    {
      "category": "string" (healing/salvation/deliverance/provision/other),
      "testimony": "string",
      "image": "file" (optional),
      "video": "string" (optional)
    }
    ```

- `GET /api/testimonies/{id}/`
  - Description: Get specific testimony

- `PUT /api/testimonies/{id}/`
  - Description: Update testimony
  - Authentication: Required (must be owner)

- `DELETE /api/testimonies/{id}/`
  - Description: Delete testimony
  - Authentication: Required (must be owner)

## Database Schema

### CustomUser Model

```python
fields = {
    'id': 'Integer (Primary Key)',
    'first_name': 'CharField(100)',
    'middle_name': 'CharField(100, optional)',
    'last_name': 'CharField(100)',
    'username': 'CharField(100, unique)',
    'email': 'EmailField(optional)',
    'phone_number': 'CharField(20)',
    'country_code': 'CharField(5)',
    'gender': 'CharField(10)',
    'profile_complete': 'BooleanField',
    'is_active': 'BooleanField',
    'is_staff': 'BooleanField',
    'date_joined': 'DateTimeField'
}
```

### Profile Model

```python
fields = {
    'id': 'Integer (Primary Key)',
    'user': 'ForeignKey(CustomUser)',
    'visit_date': 'DateField',
    'date_of_birth': 'DateField(optional)',
    'house_address': 'TextField',
    'digital_address': 'CharField(100, optional)',
    'occupation': 'CharField(100)',
    'church_information': 'TextField(optional)',
    'profile_image': 'ImageField(optional)',
    'fellowship': 'CharField(100, optional)',
    'created_at': 'DateTimeField',
    'updated_at': 'DateTimeField'
}
```

### Member Model

```python
fields = {
    'id': 'Integer (Primary Key)',
    'user': 'OneToOneField(CustomUser)',
    'date_joined': 'DateTimeField',
    'is_active': 'BooleanField'
}
```

### Contact Model

```python
fields = {
    'id': 'Integer (Primary Key)',
    'name': 'CharField(100)',
    'email': 'EmailField(optional)',
    'phone': 'CharField(20)',
    'subject': 'CharField(200)',
    'message': 'TextField',
    'created_at': 'DateTimeField',
    'updated_at': 'DateTimeField'
}
```

### Testimony Model

```python
fields = {
    'id': 'Integer (Primary Key)',
    'user': 'ForeignKey(CustomUser, optional)',
    'category': 'CharField(100)',
    'testimony': 'TextField',
    'image': 'ImageField(optional)',
    'video': 'URLField(optional)',
    'created_at': 'DateTimeField',
    'approved': 'BooleanField',
}
```

## Authentication Flow

1. User Registration:
   - User submits registration data via `/api/auth/signup/`
   - System validates data and creates new CustomUser
   - JWT tokens (access and refresh) are generated and returned

2. User Login:
   - User submits credentials via `/api/auth/login/`
   - System validates credentials
   - JWT tokens are generated and returned

3. Profile Completion:
   - User submits profile data via `/api/user/complete-profile/`
   - System creates/updates Profile model
   - `profile_complete` flag is set to true

4. Protected Endpoints:
   - Client includes JWT token in Authorization header
   - Format: `Authorization: Bearer <token>`
   - System validates token for each request
   - Invalid/expired tokens return 401 Unauthorized

## Development Guidelines

1. Code Style:
   - Follow PEP 8 style guide for Python code
   - Use meaningful variable and function names
   - Add docstrings for classes and methods
   - Keep functions focused and single-purpose

2. API Development:
   - Use ViewSets for CRUD operations
   - Implement proper serialization
   - Add appropriate permissions
   - Use pagination for list endpoints

3. Testing:
   - Write unit tests for models and views
   - Test edge cases and error conditions
   - Use pytest for testing
   - Maintain good test coverage

4. Version Control:
   - Write descriptive commit messages
   - Create feature branches
   - Review code before merging
   - Keep commits focused and atomic

## Error Handling

### HTTP Status Codes

- 200: Success
- 201: Created
- 400: Bad Request (invalid input)
- 401: Unauthorized (invalid/missing token)
- 403: Forbidden (insufficient permissions)
- 404: Not Found
- 500: Server Error

### Error Response Format

```json
{
    "error": "Error message",
    "details": {} (optional)
}
```

### Common Error Scenarios

1. Validation Errors:
   - Invalid input data
   - Missing required fields
   - Unique constraint violations

2. Authentication Errors:
   - Invalid credentials
   - Expired tokens
   - Missing tokens

3. Permission Errors:
   - Insufficient privileges
   - Resource ownership violations

## Security Implementation

1. Authentication:
   - JWT-based authentication
   - Token expiration and refresh
   - Secure password storage (Django's default hasher)

2. Data Protection:
   - Input validation and sanitization
   - XSS protection
   - CSRF protection
   - SQL injection prevention

3. File Upload Security:
   - File type validation
   - Size restrictions
   - Secure storage paths

4. API Security:
   - Rate limiting on authentication endpoints
   - Request throttling
   - Proper CORS configuration
   - Secure headers implementation

5. Error Handling:
   - Generic error messages in production
   - Proper logging of errors
   - No sensitive data in error responses
