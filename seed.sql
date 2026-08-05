-- Insert Administrator User (UUID: 36c82786-692f-4bb2-80ed-a5a58f78d135)
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c82786-692f-4bb2-80ed-a5a58f78d135',
    'Admin',
    'User',
    'admin@hbnb.io',
    '$2b$12$eImiTXuWVxfM37uY4JANjO5E/802W9gXHQ/n6Y1M1FpY/7lW.yN1i', -- Default hashed password
    TRUE
);

-- Insert Standard User
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '86c82786-692f-4bb2-80ed-a5a58f78d136',
    'John',
    'Doe',
    'john.doe@example.com',
    '$2b$12$eImiTXuWVxfM37uY4JANjO5E/802W9gXHQ/n6Y1M1FpY/7lW.yN1i',
    FALSE
);

-- Insert Initial Amenities
INSERT INTO amenities (id, name) VALUES ('110e8400-e29b-41d4-a716-446655440001', 'WiFi');
INSERT INTO amenities (id, name) VALUES ('110e8400-e29b-41d4-a716-446655440002', 'Swimming Pool');
INSERT INTO amenities (id, name) VALUES ('110e8400-e29b-41d4-a716-446655440003', 'Air Conditioning');
INSERT INTO amenities (id, name) VALUES ('110e8400-e29b-41d4-a716-446655440004', 'Free Parking');
