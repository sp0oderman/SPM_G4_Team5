CREATE TABLE employee (
    staff_id INTEGER PRIMARY KEY,
    staff_fname VARCHAR(50) NOT NULL,
    staff_lname VARCHAR(50) NOT NULL,
    dept VARCHAR(50) NOT NULL,
    position VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    reporting_manager INTEGER,
    role INTEGER NOT NULL,
    FOREIGN KEY (reporting_manager) REFERENCES employee(staff_id)
);

CREATE TABLE wfh_request (
    request_id BIGSERIAL PRIMARY KEY,
    staff_id INTEGER,
    reporting_manager INTEGER NOT NULL,
    dept VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    arrangement_type VARCHAR(20) NOT NULL,
    request_datetime TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL,
    remarks VARCHAR(500),
    FOREIGN KEY (staff_id) REFERENCES employee(staff_id)
);

