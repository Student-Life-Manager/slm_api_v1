### Common routes (main.py)

- all return schemas have `created_at` and `updated_at` fields

#### POST `/auth_user/login` (open)

- auth_user login

- body
    - email
    - password

- returns
    - access_token
    - refresh_token


#### PATCH `/auth_user/me/password` (auth required)

- body
    - password

- returns
    - true if password change was successful else false


#### GET `/auth_user/me`

- get student profile


#### PATCH `/auth_user/profile_checklist`

- update user onboarding checklist
- after every step on FE, make a request to this route and it will update that step on BE


#### POST `/auth_user/me/auth` (auth required)

- refresh auth tokens for user

- body
    - access_token
    - refresh_token

- returns
    - access_token
    - refresh_token



### Student routes (student.py)

#### POST `/student/register` (open)

- create student account

- body
    - email
    - password
    - phone_number

- returns
    - email
    - phone_number


#### GET `/student/home` (auth required)

- returns student outpasses

#### GET `/student/` (admin required)

- get all students

#### PATCH `/student/me` (admin required)

- update student profile

- body
    - first_name | null
    - last_name | null
    - phone_number | null
    - hostel_details | null
    - academic_details | null

- returns
    - uuid
    - first_name
    - last_name
    - phone_number
    - account_type
    - hostel_details
    - academic_details

### Warden routes (warden.py)

#### POST `/warden/register` (open)

- create warden account

- body
    - first_name
    - last_name
    - email
    - password
    - phone_number
    - hostel_details
        - hostel_type
        - bldg_name
        - room_no

- returns
    - uuid
    - first_name
    - last_name
    - roll_number
    - email
    - password
    - phone_number
    - hostel_details
        - hostel_type
        - bldg_name
        - room_no


#### GET `/warden/` (admin required)

- get all wardens
