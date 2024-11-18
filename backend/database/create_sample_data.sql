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
    color, 
    lost_date, 
    lost_location, 
    description, 
    photo_url, 
    status
) VALUES
    (1, 'Max', 'perro', 'Labrador', 'dorado', '2024-03-15', 'Parque Rivadavia, CABA', 
     'Perro grande y amigable, collar azul con placa de identificación', '/uploads/max.jpg', 'perdido'),
    
    (2, 'Luna', 'gato', 'Siamés', 'blanco y marrón', '2024-03-17', 'Palermo, CABA',
     'Gata pequeña, muy tímida, tiene chip de identificación', '/uploads/luna.jpg', 'perdido'),
    
    (3, 'Rocky', 'perro', 'Bulldog', 'marrón y blanco', '2024-03-10', 'Villa Urquiza, CABA',
     'Bulldog adulto, manchas marrones, collar rojo', '/uploads/rocky.jpg', 'encontrado'),
    
    (1, 'Milo', 'gato', 'Común Europeo', 'negro', '2024-03-16', 'Belgrano, CABA',
     'Gato adulto negro, collar con cascabel', '/uploads/milo.jpg', 'perdido');

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