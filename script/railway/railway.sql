CREATE TABLE
    auth_user(
        id INTEGER PRIMARY KEY NOT NULL,
        uuid UUID NOT NULL,
        email VARCHAR,
        password VARCHAR,
        checklist JSONB,
        roll_number VARCHAR,
        first_name VARCHAR,
        last_name VARCHAR,
        account_type VARCHAR,
        phone_number VARCHAR,
        academic_details JSONB,
        hostel_details JSONB,
        is_admin BOOLEAN DEFAULT false,
        created_at TIMESTAMP
        WITH
            TIME ZONE NOT NULL,
            updated_at TIMESTAMP
        WITH TIME ZONE
    );

CREATE TABLE
    guardian(
        id INTEGER PRIMARY KEY NOT NULL,
        uuid UUID NOT NULL,
        relation VARCHAR NOT NULL,
        phone_number VARCHAR NOT NULL,
        is_verified BOOLEAN DEFAULT false,
        student_id INTEGER,
        CONSTRAINT fk_student FOREIGN KEY(student_id) REFERENCES auth_user(id)
    );

CREATE TABLE
    outpass(
        id INTEGER PRIMARY KEY NOT NULL,
        uuid UUID NOT NULL,
        out_date DATE NOT NULL,
        out_time TIME NOT NULL,
        expected_return_at DATE NOT NULL,
        location VARCHAR NOT NULL,
        alternate_phone_number VARCHAR,
        status VARCHAR DEFAULT 'created',
        warden_message VARCHAR,
        approval JSONB,
        approved_at TIMESTAMP
        WITH
            TIME ZONE,
            exited_at TIMESTAMP
        WITH
            TIME ZONE,
            returned_at TIMESTAMP
        WITH
            TIME ZONE,
            student_id INTEGER,
            warden_id INTEGER,
            guardian_id INTEGER,
            created_at TIMESTAMP
        WITH
            TIME ZONE NOT NULL,
            updated_at TIMESTAMP
        WITH TIME ZONE
    );