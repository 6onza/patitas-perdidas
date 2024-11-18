-- Tabla para usuarios que publican mascotas, reportan avistamientos, etc.
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla principal de mascotas perdidas
CREATE TABLE lost_pets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- El usuario que publica la mascota
    pet_name VARCHAR(100) NOT NULL,
    type ENUM('perro', 'gato', 'otro') NOT NULL,
    breed VARCHAR(100),
    color VARCHAR(100) NOT NULL,
    lost_date DATE NOT NULL,
    lost_city VARCHAR(100) NOT NULL,
    lost_latitude DECIMAL(10, 8) NOT NULL,
    lost_longitude DECIMAL(11, 8) NOT NULL,
    description TEXT NOT NULL,
    photo_url VARCHAR(255), -- TODO: para esto podriamos usar un servicio como Cloudinary
    status ENUM('perdido', 'encontrado') DEFAULT 'perdido',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Tabla para avistamientos de mascotas
CREATE TABLE pet_sightings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lost_pet_id INT NOT NULL,
    reporter_name VARCHAR(100) NOT NULL,
    reporter_phone VARCHAR(20) NOT NULL,
    sighting_date DATE NOT NULL,
    sighting_location VARCHAR(255) NOT NULL,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lost_pet_id) REFERENCES lost_pets(id)
);