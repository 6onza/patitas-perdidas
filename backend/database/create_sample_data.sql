-- Insertar usuarios de ejemplo
INSERT INTO users (name, email, phone) VALUES
    ('Juan Pérez', 'juan@email.com', '1156789012'),
    ('María García', 'maria@email.com', '1145678901'),
    ('Carlos López', 'carlos@email.com', '1167890123');

-- Insertar mascotas perdidas
INSERT INTO lost_pets (
    user_id, 
    pet_name, 
    type, 
    breed, 
    sex,
    color, 
    lost_date, 
    lost_location, 
    lost_latitude,
    lost_longitude,
    description, 
    status,
    has_name_tag
) VALUES
    (1, 'Max', 'dog', 'Labrador', 'male', 'dorado', '2024-03-15', 'Parque Rivadavia, CABA', 
     -34.6185, -58.4259, 'Perro grande y amigable, collar azul con placa de identificación', 'lost', TRUE),
    
    (2, 'Luna', 'cat', 'Siamés', 'male', 'blanco y marrón', '2024-03-17', 'Palermo, CABA',
     -34.5889, -58.4306, 'Gata pequeña, muy tímida, tiene chip de identificación', 'lost', FALSE),
    
    (3, 'Rocky', 'dog', 'Bulldog', 'male', 'marrón y blanco', '2024-03-10', 'Villa Urquiza, CABA',
     -34.5746, -58.4863, 'Bulldog adulto, manchas marrones, collar rojo', 'found', FALSE),
    
    (1, 'Milo', 'cat', 'Común Europeo', 'male', 'negro', '2024-03-16', 'Belgrano, CABA',
     -34.5624, -58.4563, 'Gato adulto negro, collar con cascabel', 'lost', TRUE);

-- Insertar avistamientos
INSERT INTO pet_sightings (
    lost_pet_id,
    reporter_name,
    reporter_phone,
    sighting_date,
    sighting_location,
    details
) VALUES
    (1, 'Ana Martínez', '1123456789', '2024-03-16', 'Plaza Almagro, CABA',
     'Vi un perro similar corriendo cerca de la plaza, parecía desorientado'),
    
    (1, 'Pedro Sánchez', '1134567890', '2024-03-17', 'Caballito, CABA',
     'Creo haber visto este perro cerca del parque Rivadavia hoy temprano'),
    
    (2, 'Laura Rodríguez', '1145678901', '2024-03-18', 'Palermo Soho, CABA',
     'Vi una gata siamesa entrando a un garage en Thames al 1500');