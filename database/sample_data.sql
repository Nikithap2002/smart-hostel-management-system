INSERT INTO rooms (room_number, is_available) VALUES
('101A', 1), ('102B', 1), ('103C', 0);

INSERT INTO residents (name, room_id) VALUES
('Alice', 1), ('Bob', 3);

INSERT INTO payments (resident_id, amount, payment_date) VALUES
(1, 500.00, '2025-04-01');

INSERT INTO complaints (resident_id, description) VALUES
(2, 'Broken fan');

