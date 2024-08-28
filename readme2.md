### Project Documentation

#### Overview

This project is a REST API built with Django and Django REST Framework (DRF) to manage user registrations, health information, and health worker records. The API supports user authentication using JSON Web Tokens (JWT) provided by the `djangorestframework-simplejwt` library. This documentation provides an overview of the available endpoints, request/response formats, and how to interact with the API.

### API Endpoints

#### **1. User Registration**

- **Endpoint:** `/user-create/`
- **Method:** `POST`
- **Description:** Creates a new user account in the system.
- **Request Body:**
  ```json
  {
      "username": "string",
      "password": "string",
      "email": "string",
      "role": "P"  // P for patient, H for health worker
  }
  ```
- **Response:**
  - **Status 201:**
    ```json
    {
        "id": 1,
        "username": "string",
        "email": "string",
        "role": "P"
    }
    ```
  - **Status 400:**
    ```json
    {
        "error": "Invalid data"
    }
    ```

#### **2. User Detail**

- **Endpoint:** `/user-detail/`
- **Method:** `GET`
- **Description:** Retrieves details of the authenticated user.
- **Authentication:** JWT required.
- **Response:**
  - **Status 200:**
    ```json
    {
        "id": 1,
        "username": "string",
        "email": "string",
        "role": "P"
    }
    ```
  - **Status 401:**
    ```json
    {
        "detail": "Authentication credentials were not provided."
    }
    ```

#### **3. Health Information Registration**

- **Endpoint:** `/health-info/create/`
- **Method:** `PUT`
- **Description:** Allows a patient to create or update their health information.
- **Authentication:** JWT required (Patient role only).
- **Request Body:**
  ```json
  {
      "pregnancy_status": "string",
      "due_date": "YYYY-MM-DD",
      "health_conditions": "string"
  }
  ```
- **Response:**
  - **Status 200:**
    ```json
    {
        "message": "Health information created/updated successfully"
    }
    ```
  - **Status 403:**
    ```json
    {
        "detail": "You are not authorized to perform this action."
    }
    ```
  - **Status 400:**
    ```json
    {
        "error": "Error message"
    }
    ```

#### **4. Health Information Details**

- **Endpoint:** `/health-info/`
- **Method:** `GET`
- **Description:** Retrieves the health information of the authenticated patient.
- **Authentication:** JWT required (Patient role only).
- **Response:**
  - **Status 200:**
    ```json
    {
        "pregnancy_status": "string",
        "due_date": "YYYY-MM-DD",
        "health_conditions": "string"
    }
    ```
  - **Status 403:**
    ```json
    {
        "detail": "You are not authorized to perform this action."
    }
    ```
  - **Status 401:**
    ```json
    {
        "detail": "Authentication credentials were not provided."
    }
    ```

#### **5. Health Worker Information Registration**

- **Endpoint:** `/health-worker/create/`
- **Method:** `PUT`
- **Description:** Allows a health worker to create or update their professional information.
- **Authentication:** JWT required (Health worker role only).
- **Request Body:**
  ```json
  {
      "medical_license_number": "string",
      "specialty": "string",
      "clinic_location": "string",
      "clinic_name": "string"
  }
  ```
- **Response:**
  - **Status 200:**
    ```json
    {
        "message": "Health worker information created/updated successfully"
    }
    ```
  - **Status 403:**
    ```json
    {
        "detail": "You are not authorized to perform this action."
    }
    ```
  - **Status 400:**
    ```json
    {
        "error": "Error message"
    }
    ```

#### **6. Health Worker Information Details**

- **Endpoint:** `/health-worker/`
- **Method:** `GET`
- **Description:** Retrieves the professional information of the authenticated health worker.
- **Authentication:** JWT required (Health worker role only).
- **Response:**
  - **Status 200:**
    ```json
    {
        "medical_license_number": "string",
        "specialty": "string",
        "clinic_location": "string",
        "clinic_name": "string"
    }
    ```
  - **Status 403:**
    ```json
    {
        "detail": "You are not authorized to perform this action."
    }
    ```
  - **Status 401:**
    ```json
    {
        "detail": "Authentication credentials were not provided."
    }
    ```

#### **7. Login**

- **Endpoint:** `/login/`
- **Method:** `POST`
- **Description:** Authenticates a user and returns JWT tokens.
- **Request Body:**
  ```json
  {
      "username": "string",
      "password": "string"
  }
  ```
- **Response:**
  - **Status 200:**
    ```json
    {
        "refresh": "string",
        "access": "string",
        "message": "Login successful",
        "data": { "user_details": "object" }
    }
    ```
  - **Status 401:**
    ```json
    {
        "error": "Invalid credentials"
    }
    ```

#### **8. Token Refresh**

- **Endpoint:** `/token/refresh/`
- **Method:** `POST`
- **Description:** Refreshes the access token using the refresh token.
- **Request Body:**
  ```json
  {
      "refresh": "string"
  }
  ```
- **Response:**
  - **Status 200:**
    ```json
    {
        "access": "string"
    }
    ```
  - **Status 401:**
    ```json
    {
        "error": "Invalid refresh token"
    }
    ```

#### **9. Logout**

- **Endpoint:** `/logout/`
- **Method:** `POST`
- **Description:** Invalidates the refresh token and logs out the user.
- **Request Body:**
  ```json
  {
      "refresh": "string"
  }
  ```
- **Response:**
  - **Status 200:**
    ```json
    {
        "message": "Logout successful"
    }
    ```
  - **Status 400:**
    ```json
    {
        "error": "Error message"
    }
    ```

### Error Handling

All endpoints will return appropriate HTTP status codes along with error messages in JSON format if any issues occur during the request handling. Common status codes include `400` for bad requests, `401` for unauthorized access, `403` for forbidden actions, and `404` for resources not found.

### Authentication

The API uses JWT for authentication. After logging in, clients should include the JWT access token in the `Authorization` header of each request as follows:

```http
Authorization: Bearer <your_access_token>
```

If the access token expires, clients can refresh it using the `/token/refresh/` endpoint.

### Models Overview

- **UserRegistration:** Handles user information and roles (e.g., Patient or Health Worker).
- **HealthInfo:** Stores health information specific to patients.
- **HealthWorkerInfo:** Stores professional information for health workers.
