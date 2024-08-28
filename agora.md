### Program Documentation

This documentation provides an overview of the Django-based API that enables remote consultations using Agora. The API is designed to handle token generation for secure video calls and manage consultations between patients and health workers.

#### Prerequisites

- **Django**: This project is built on Django, a Python web framework.
- **Django REST Framework (DRF)**: Used for building the API endpoints.
- **Agora SDK**: Agora is used for real-time video communications.
- **Agora Token Builder**: This package is used to generate the Agora token.

#### Setup

Before using the API, ensure that you have the following environment variables set in your Django settings:

- `AGORA_APP_ID`: Your Agora App ID.
- `AGORA_APP_CERTIFICATE`: Your Agora App Certificate.

These are essential for generating the Agora tokens.

### Views

#### 1. `AgoraTokenView`

This API view is responsible for generating an Agora token for a patient to initiate a consultation with a health worker.

- **URL**: `/get-agora-token/`
- **Method**: `POST`
- **Permission**: `IsAuthenticated`
- **Description**: Generates an Agora token and initiates a consultation.

##### Request Body:

```json
{
    "health_worker_id": 1,
    "channel": "channel_name",
    "uid": 12345
}
```

- **health_worker_id**: The ID of the health worker you want to consult with.
- **channel**: The Agora channel name (unique identifier for the video call).
- **uid**: The unique identifier for the user in the Agora channel.

##### Response:

On success, returns the following details:

```json
{
    "consultation_id": 1,
    "channel_name": "channel_name",
    "uid": 12345,
    "token": "generated_token",
    "app_id": "your_agora_app_id"
}
```

- **consultation_id**: The ID of the newly created consultation.
- **channel_name**: The Agora channel name.
- **uid**: The Agora UID for the session.
- **token**: The Agora token to authenticate the user.
- **app_id**: The Agora App ID.

##### Error Responses:

- `400`: Invalid health worker ID or health worker is not available.
- `400`: If the request data is invalid.

##### Detailed Workflow:

1. **Input Validation**: The API validates the input data using `AgoraTokenSerializer`.
2. **Health Worker Verification**: It checks if the health worker with the given ID exists and is available for consultation.
3. **Token Generation**: It generates an Agora token using the provided channel and UID.
4. **Consultation Creation**: A new consultation record is created in the `Consultation` model.
5. **Response**: The API returns the consultation details, including the Agora token and channel name.

#### 2. `GetConsultationView`

This API view is responsible for retrieving consultation details for a health worker to join a video call initiated by a patient.

- **URL**: `/get-call-info/<int:consultation_id>/`
- **Method**: `GET`
- **Permission**: `IsAuthenticated`
- **Description**: Retrieves consultation details for a specific consultation ID.

##### Request Parameters:

- **consultation_id**: The ID of the consultation you want to retrieve.

##### Response:

On success, returns the following details:

```json
{
    "channel": "channel_name",
    "uid": 12345,
    "patient_name": "John Doe"
}
```

- **channel**: The Agora channel name.
- **uid**: The Agora UID for the session.
- **patient_name**: The full name of the patient.

##### Error Responses:

- `403`: If the requesting user is not the assigned health worker for the consultation.
- `404`: If the consultation with the given ID does not exist.

##### Detailed Workflow:

1. **Consultation Retrieval**: The API retrieves the consultation record based on the provided `consultation_id`.
2. **Authorization Check**: It verifies that the requesting user is the assigned health worker for the consultation.
3. **Response**: The API returns the consultation details, including the channel name and UID.

### Models

The program uses two main models: `UserRegistration` and `Consultation`.

- **UserRegistration**: Stores user details, including health workers and patients.
- **Consultation**: Stores details about each consultation, including the health worker, patient, channel name, and Agora UID.

### URLs

The following URLs are defined in the `urls.py` file:

- **`/get-agora-token/`**: Generates an Agora token for a new consultation.
- **`/get-call-info/<int:consultation_id>/`**: Retrieves consultation details based on the consultation ID.

### Example Usage

1. **Generating an Agora Token**:
   - A patient sends a POST request to `/get-agora-token/` with the `health_worker_id`, `channel`, and `uid`.
   - The API returns the Agora token and other relevant details for the consultation.

2. **Retrieving Consultation Details**:
   - A health worker sends a GET request to `/get-call-info/<int:consultation_id>/`.
   - The API returns the consultation details, allowing the health worker to join the call.

### Conclusion

This API enables a secure and efficient way to manage remote consultations between patients and health workers using Agora for real-time video communication. It includes functionalities for generating tokens, managing consultations, and ensuring that only authorized users can access consultation details.