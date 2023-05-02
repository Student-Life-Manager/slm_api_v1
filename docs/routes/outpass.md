### Outpass routes (outpass.py)

- all return schemas have `created_at` and `updated_at` fields

#### POST `/` (auth required)

- student route
- create student outpass

- body
    - out_date
    - out_time
    - expected_return_at
    - location
    - reason
    - alternate_phone_number

- returns
    - uuid
    - out_date
    - out_time
    - expected_return_at
    - location
    - alternate_phone_number
    - status
    - approved_at
    - exited_at
    - returned_at
    - warden_message
    - approval


#### GET `/me` (auth required)

- student route
- get student outpasses

- returns a list of outpasses

#### GET `/approved/me` (auth required)

- student route
- get student's approved outpasses


- returns a list of outpasses

#### PATCH `/{outpass_uuid}/approve` (auth required)

- warden route
- approve an outpass

- returns
    - uuid
    - out_date
    - out_time
    - expected_return_at
    - location
    - alternate_phone_number
    - status
    - approved_at
    - exited_at
    - returned_at
    - warden_message
    - approval


#### GET `/{outpass_uuid}` (auth required)

- student route
- returns student outpass with given uuid

- returns
    - uuid
    - out_date
    - out_time
    - expected_return_at
    - location
    - alternate_phone_number
    - status
    - approved_at
    - exited_at
    - returned_at
    - warden_message
    - approval
