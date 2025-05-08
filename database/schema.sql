-- Rooms Table
CREATE TABLE rooms (
    room_id INTEGER PRIMARY KEY,
    room_number TEXT,
    is_available BOOLEAN
);

-- Residents Table
CREATE TABLE residents (
    resident_id INTEGER PRIMARY KEY,
    name TEXT,
    room_id INTEGER,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

-- Payments Table
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    resident_id INTEGER,
    amount DECIMAL,
    payment_date DATE,
    FOREIGN KEY (resident_id) REFERENCES residents(resident_id)
);


-- Complaints Table
CREATE TABLE complaints (
    complaint_id INTEGER PRIMARY KEY,
    resident_id INTEGER,
    description TEXT,
    status TEXT DEFAULT 'Pending',
    FOREIGN KEY (resident_id) REFERENCES residents(resident_id)
);

