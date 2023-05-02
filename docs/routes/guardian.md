### Guardian routes (guardian.py)

- all return schemas have `created_at` and `updated_at` fields

#### GET `/` (admin required)

- get all guardians

- returns
    - list of guardians


#### POST `/` (auth required)

- student route
- create guardians

- body
    - relation
    - phone number

- returns
    - uuid
    - relation
    - phone number
    - is verified


#### GET `/me` (auth required)

- student route
- get my guardians

- returns
    - list of student guardians


#### DELETE `/{guardian_uuid}` (auth required)

- student route
- delete student guardian

- returns
    - true if deletion was successful

#### PATCH `/{guardian_uuid}/verify` (admin required)

- admin route
- verify a guardian

- returns
    - uuid
    - relation
    - phone number
    - is verified
    - student details
