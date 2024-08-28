
---

## API Documentation


### Endpoints

#### 1. **POST /ai-response/**

**Description**:  
This endpoint allows authenticated users to send a prompt to the AI model and receive a generated response.

**Request Format**:  

- **Method**: POST
- **URL**: `/ai-response/`
- **Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <token>` (Token required for authentication)
- **Body** (JSON):
  ```json
  {
    "prompt": "string"
  }
  ```

**Request Parameters**:

- `prompt` (string, required): The prompt or question that you want to send to the AI model for generating a response.

**Response Format**:

- **Status Code**: 200 OK
- **Body** (JSON):
  ```json
  {
    "response": "string"
  }
  ```

**Response Parameters**:

- `response` (string): The AI-generated response to the provided prompt.

**Errors**:

- **Status Code**: 400 Bad Request
  - **Body** (JSON):
    ```json
    {
      "prompt": [
        "This field is required."
      ]
    }
    ```
  - **Description**: Indicates that the prompt field is missing or invalid.

- **Status Code**: 401 Unauthorized
  - **Description**: Indicates that the request is missing a valid authentication token.

**Example Request**:

```http
POST /ai-response/ HTTP/1.1
Host: i've forgotten the url abeg
Authorization: Bearer your_jwt_token
Content-Type: application/json

{
  "prompt": "What is the capital of France?"
}
```

**Example Response**:

```json
{
  "response": "The capital of France is Paris."
}
```

### Authentication

- **Required**: Yes
- **Type**: Bearer Token
- **Description**: Each request must include a valid JWT (JSON Web Token) in the `Authorization` header. Tokens are obtained upon user authentication and should be included in the request to access protected endpoints.

### Error Handling

- **Invalid Prompt**: If the `prompt` field is missing or invalid, the API returns a `400 Bad Request` status with details on the validation error.
- **Unauthorized Access**: If the request lacks valid authentication or the token is expired, the API returns a `401 Unauthorized` status.

### Notes

- **Rate Limiting**: The API may implement rate limiting to prevent abuse. Check the response headers for rate limit status.
- **Content-Type**: Ensure that the `Content-Type` header is set to `application/json` when sending requests to the API.

---

### Implementation Details

#### `views.py`

The `AiResponseView` class handles POST requests to the `/ai-response/` endpoint. It expects an authenticated user and requires the prompt to be passed in the request body. The view validates the prompt using the `PromptSerializer` and then generates a response using the `ai_response` function, which interacts with an AI service. The response is returned in JSON format.

#### `urls.py`

The URL configuration maps the `/ai-response/` endpoint to the `AiResponseView`. This routing ensures that POST requests to this endpoint are processed by the `AiResponseView` class.

