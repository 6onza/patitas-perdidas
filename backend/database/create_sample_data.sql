-- Insertando usuarios de ejemplo
INSERT INTO users (name, username, password_hash, phone) VALUES
('María González', 'mariag', '$2b$12$FvEwn0nsruAJVSbnQ22PL.fIWaptv9AEyJFVvB2oarETHKmgClX3K', '11-4523-7890'),
('Juan Pérez', 'juanp', '$2b$12$VSnoAZKe0UHuPJYf3Aqsbeqkik83d6si7rup6.0KBSguPsPHunjtG', '11-6789-4532'),
('Laura Rodríguez', 'laurar', '$2b$12$w39IG6XY5Xda9JrYhbvuE.gaSLQWGD9Aznh9xgSEKPs/mpwfE99se', '11-2345-6789'),
('Carlos Martínez', 'carlosm', '$2b$12$xMWp1tPfzwCqLRBhDrz5Q.uAkXJz9hRf5BaE9KqW7T3q', '11-8901-2345'),
('Ana Silva', 'anas', '$2b$12$xNWp1tPfzwCqZnPf3Q7IjOBzX5J9hRf5BaE9KqW7T3q', '11-3456-7890'),
('Diego López', 'diegol', '$2b$12$xOWp1tPfzwCqFbRhDrz5Q.uAkXJz9hRf5BaE9KqW7T3q', '11-7890-1234'),
('Paula Fernández', 'paulaf', '$2b$12$xPWp1tPfzwCqLbRhDrz5Q.uAkXJz9hRf5BaE9KqW7T3q', '11-5678-9012');

-- Insertando mascotas perdidas
INSERT INTO lost_pets (
    user_id,
    pet_name,
    type,
    sex,
    breed,
    color,
    lost_date,
    lost_city,
    lost_location,
    lost_latitude,
    lost_longitude,
    description,
    status,
    has_name_tag
) VALUES 
(1, 'Toby', 'dog', 'male', 'Labrador', 'dorado', '2024-03-15', 'Palermo', 'Buenos Aires', -34.588446, -58.411780, 'Perro labrador amigable, collar azul con placa', 'lost', true),
(2, 'Luna', 'cat', 'female', 'Siamés', 'blanco y marrón', '2024-03-18', 'Recoleta', 'Buenos Aires', -34.587569, -58.393839, 'Gata siamesa con collar rojo', 'lost', true),
(3, 'Rocky', 'dog', 'male', 'Pastor Alemán', 'negro y marrón', '2024-03-20', 'Belgrano', 'Buenos Aires', -34.563589, -58.451886, 'Pastor alemán adulto con cicatriz en pata derecha', 'found', false),
(4, 'Mimi', 'cat', 'female', 'Persa', 'gris', '2024-03-21', 'San Telmo', 'Buenos Aires', -34.621023, -58.371573, 'Gata persa de pelo largo, muy asustadiza', 'lost', false),
(5, 'Max', 'dog', 'male', 'Golden Retriever', 'dorado', '2024-03-22', 'Núñez', 'Buenos Aires', -34.543456, -58.456789, 'Golden retriever con pañuelo rojo en el cuello', 'lost', true),
(6, 'Nina', 'cat', 'female', 'Común Europeo', 'negro', '2024-03-23', 'Villa Crespo', 'Buenos Aires', -34.599825, -58.436937, 'Gata negra con manchita blanca en el pecho', 'lost', false),
(7, 'Zeus', 'dog', 'male', 'Bulldog Francés', 'atigrado', '2024-03-24', 'Caballito', 'Buenos Aires', -34.619732, -58.442982, 'Bulldog francés con collar verde', 'found', true);