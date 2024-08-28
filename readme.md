### API Documentation

This documentation describes the API endpoints for user registration, login, health information management, and logout functionality in the Django REST Framework (DRF) application. The endpoints are primarily focused on managing user accounts and health-related data for patients and healthcare practitioners.

---

#### Base URL:
- **Base URL:** `/api/`

### Endpoints Overview:

1. **User Registration**
   - `POST /api/user-create/`
   
2. **User Detail**
   - `GET /api/user-detail/`
   
3. **Health Information Registration**
   - `PUT /api/health-info/create/`
   
4. **Health Information Detail**
   - `GET /api/health-info/`

5. **HealthWorker Info Registration**
   - `PUT /api/health-worker/create/`

6. **HealthWorker Information Detail**
    - `GET /api/health-worker/`
   
7. **Login**
   - `POST /api/login/`

8. **Logout**
   - `POST /api/logout/`

---

### 1. **User Registration**

- **URL:** `/api/user-create/`
- **Method:** `POST`
- **Authentication:** None (Open to all)
- **Description:** Registers a new user (patient or healthcare practitioner).
- **Request Body:**
  ```json
  {
      "username": "string",
      "password": "string",
      "first_name": "string",
      "last_name": "string",
      "phone_number": "string",
      "date_of_birth": "YYYY-MM-DD",
      "gender": "M/F",
      "role": "P/H"
  }
  ```
- **Response:**
  - **201 Created**
  ```json
  {
      "username": "string",
      "first_name": "string",
      "last_name": "string",
      "phone_number": "string",
      "date_of_birth": "YYYY-MM-DD",
      "gender": "M/F",
      "role": "P/H"
  }
  ```

### 2. **User Detail**

- **URL:** `/api/user-detail/`
- **Method:** `GET`
- **Authentication:** Basic Authentication
- **Permission:** Authenticated users only
- **Description:** Retrieves details of the logged-in user.
- **Response:**
  - **200 OK**
  ```json
  {
      "username": "string",
      "first_name": "string",
      "last_name": "string",
      "phone_number": "string",
      "date_of_birth": "YYYY-MM-DD",
      "gender": "M/F",
      "role": "P/H"
  }
  ```

### 3. **Health Information Registration (Patients Only)**

- **URL:** `/api/health-info/create/`
- **Method:** `PUT`
- **Authentication:** Basic Authentication
- **Permission:** Authenticated users with the role `P` (Patient)
- **Description:** Allows patients to create or update their health information.
- **Request Body:**
  ```json
  {
      "pregnancy_status": "true/false",
      "due_date": "YYYY-MM-DD",
      "health_conditions": "string"
  }
  ```
- **Response:**
  - **200 OK** (If health info updated)
  ```json
  {
      "message": "Health information updated successfully"
  }
  ```
  - **201 Created** (If health info created)
  ```json
  {
      "message": "Health information created successfully"
  }
  ```

### 4. **Health Information Detail (Patients Only)**

- **URL:** `/api/health-info/`
- **Method:** `GET`
- **Authentication:** Basic Authentication
- **Permission:** Authenticated users with the role `P` (Patient)
- **Description:** Retrieves the health information of the logged-in patient.
- **Response:**
  - **200 OK**
  ```json
  {
      "pregnancy_status": "true/false",
      "due_date": "YYYY-MM-DD",
      "health_conditions": "string"
  }
  ```
  
### 5. **Health Worker Info Registration (Healthcare Worker Only)**

    Endpoint: /health-worker/create/
    Method: PUT
    Description: Create or update health worker information. Only accessible by users with the role H.
    Permission: IsAuthenticated
    Request Headers:
        Authorization: Basic <credentials>
    Request Body:

    json

    {
      "medical_license_number": "string",
      "specialty": "string",
      "clinic_location": "string",
      "hospital_name": "string"
    }

    Response:
        200 OK: Health worker information created or updated successfully.
        403 Forbidden: The user is not a healthcare worker.
        401 Unauthorized: Authentication required.

### 6. **Health Worker Info Detail (Healthcare Worker Only)**

    Endpoint: /health-worker/
    Method: GET
    Description: Retrieve health worker information for the authenticated healthcare worker.
    Permission: IsAuthenticated
    Request Headers:
        Authorization: Basic <credentials>
    Response:
        200 OK: Health worker information retrieved successfully.
        403 Forbidden: The user is not a healthcare worker.
        401 Unauthorized: Authentication required.



### 7. **Login**

- **URL:** `/api/login/`
- **Method:** `POST`
- **Authentication:** None (Open to all)
- **Description:** Authenticates a user and returns a success message upon successful login.
- **Request Body:**
  ```json
  {
      "username": "string",
      "password": "string"
  }
  ```
- **Response:**
  - **200 OK**
  ```json
  {
      "message": "Login successful",
      "data": {
          "username": "string",
          "password": "string"
      }
  }
  ```
  - **401 Unauthorized**
  ```json
  {
      "error": "Invalid credentials"
  }
  ```

### 8. **Logout**

- **URL:** `/api/logout/`
- **Method:** `POST`
- **Authentication:** Basic Authentication
- **Permission:** Authenticated users only
- **Description:** Logs out the authenticated user and deletes their token/Session.
- **Response:**
  - **200 OK**
  ```json
  {
      "message": "Logout successful"
  }
  ```
  - **400 Bad Request**
  ```json
  {
      "error": "Error message"
  }
  ```

### Notes:
- **Role-based access control:** Patients can access and manage their health records, while healthcare practitioners are restricted from accessing or modifying patient-specific health information.
- **Authentication:** Basic Authentication is enforced for all endpoints except user registration and login, ensuring that only authenticated users can access their data.
- **Security:** Ensure that HTTPS is used in production to encrypt sensitive data transmitted between the client and the server.

