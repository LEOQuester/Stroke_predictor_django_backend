Here’s a comprehensive set of example requests for all relevant endpoints in this app:

---

## 1. **User Registration**

### Endpoint
`POST /api/user/register/`

### Request Body
```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "phone_number": "+123456789",
  "password": "SecurePassword123!"
}
```

---

## 2. **User Login**

### Endpoint
`POST /api/user/login/`

### Request Body
- The user can log in using **either username, email, or phone number** along with the password.

#### Example using Username
```json
{
  "username": "johndoe",
  "password": "SecurePassword123!"
}
```

#### Example using Email
```json
{
  "email": "johndoe@example.com",
  "password": "SecurePassword123!"
}
```

#### Example using Phone Number
```json
{
  "phone_number": "+123456789",
  "password": "SecurePassword123!"
}
```

### Expected Response
Upon successful authentication, an access token will be returned:
```json
{
  "token": "JWT_ACCESS_TOKEN_HERE"
}
```

---

## 3. **Make a Prediction**

### Endpoint
`POST /api/user/predict/`

### Headers
```http
Authorization: Bearer JWT_ACCESS_TOKEN_HERE
Content-Type: application/json
```

### Request Body
Send user health data as follows:

```json
{
  "gender": 1,
  "age": 37,
  "hypertension": 0,
  "heart_disease": 1,
  "ever_married": 1,
  "work_type": "Private",
  "residence_type": "Urban",
  "avg_glucose_level": 190.5,
  "bmi": 25.0,
  "smoking_status": "never smoked"
}
```

### Expected Response
A prediction result, message, and risk percentage:

```json
{
  "stroke_prediction": true,
  "message": "Caution! Your risk of stroke is higher than average. Evaluate your lifestyle choices and seek medical guidance.",
  "risk_percentage": 43.65
}
```

---

## 4. **Retrieve All User Predictions**

### Endpoint
`GET /api/user/predict/`

### Headers
```http
Authorization: Bearer JWT_ACCESS_TOKEN_HERE
```

### Expected Response
List of all predictions made by the authenticated user:

```json
[
  {
    "gender": 1,
    "age": 37,
    "hypertension": 0,
    "heart_disease": 1,
    "ever_married": 1,
    "work_type": "Private",
    "residence_type": "Urban",
    "avg_glucose_level": 190.5,
    "bmi": 25.0,
    "smoking_status": "never smoked",
    "stroke_prediction": true,
    "message": "Caution! Your risk of stroke is higher than average. Evaluate your lifestyle choices and seek medical guidance.",
    "risk_percentage": 43.65,
    "created_at": "2024-11-02T21:03:19.123Z"
  },
  {
    "gender": 0,
    "age": 50,
    "hypertension": 0,
    "heart_disease": 0,
    "ever_married": 0,
    "work_type": "Self-employed",
    "residence_type": "Rural",
    "avg_glucose_level": 105.7,
    "bmi": 22.0,
    "smoking_status": "formerly smoked",
    "stroke_prediction": false,
    "message": "Your risk of stroke is within the average range. Maintain healthy habits.",
    "risk_percentage": 15.3,
    "created_at": "2024-11-01T18:45:13.456Z"
  }
]
```

---

These requests allow users to register, log in, make health predictions, and retrieve past predictions. Make sure to replace `JWT_ACCESS_TOKEN_HERE` with an actual token obtained from the login endpoint.