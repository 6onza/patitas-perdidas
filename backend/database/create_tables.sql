-- Tabla para usuarios que publican mascotas, reportan avistamientos, etc.
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,  -- Cambiado de password a password_hash
    phone VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla principal de mascotas perdidas
CREATE TABLE lost_pets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- El usuario que publica la mascota
    pet_name VARCHAR(100) NOT NULL,
    type ENUM('dog', 'cat', 'other') NOT NULL,
    sex ENUM('male', 'female') NOT NULL,
    breed VARCHAR(100),
    color VARCHAR(100) NOT NULL,
    lost_date DATE NOT NULL,
    lost_city VARCHAR(100) NOT NULL,
    lost_location VARCHAR(100) NOT NULL,
    lost_latitude DECIMAL(10, 8) NOT NULL,
    lost_longitude DECIMAL(11, 8) NOT NULL,
    description TEXT NOT NULL,
    photo_url VARCHAR(255), -- TODO: para esto podríamos usar un servicio como Cloudinary
    status ENUM('lost', 'found') DEFAULT 'lost',
    has_name_tag BOOLEAN DEFAULT FALSE, -- Nueva columna para indicar si la mascota tiene una placa de identificación
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- tabla para guardar un mensaje de contacto nombre, email, mensaje
CREATE TABLE contact (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);