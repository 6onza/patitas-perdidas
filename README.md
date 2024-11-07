# Patitas Perdidas API
API para gestionar el registro y búsqueda de mascotas perdidas en una base de datos.

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### 1. Obtener todas las mascotas
```http
GET /pets
```

#### Respuesta
```json
[
  {
    "id": 1,
    "name": "Toby",
    "breed": "Golden Retriever",
    "lost_date": "2021-07-01",
    "lost_time": "12:00",
    "lost_description": "Golden retriever de 2 años de edad, color dorado, muy amigable.",
    "lost_contact": "John Doe, 123-456-7890",
    "latitude": "-34.6037",
    "longitude": "-58.3816"
  }
]
```

### 2. Obtener una mascota por ID
```http
GET /pets/{id}
```

#### Respuesta
```json
{
  "id": 1,
  "name": "Toby",
  "breed": "Golden Retriever",
  "lost_date": "2021-07-01",
  "lost_time": "12:00",
  "lost_description": "Golden retriever de 2 años de edad, color dorado, muy amigable.",
  "lost_contact": "John Doe, 123-456-7890",
  "latitude": "-34.6037",
  "longitude": "-58.3816"
}
```

### 3. Crear nueva mascota
```http
POST /pets
```

#### Body
```json
{
  "name": "Toby",
  "breed": "Golden Retriever",
  "lost_date": "2021-07-01",
  "lost_time": "12:00",
  "lost_description": "Golden retriever de 2 años de edad, color dorado, muy amigable.",
  "lost_contact": "John Doe, 123-456-7890",
  "latitude": "-34.6037",
  "longitude": "-58.3816"
}
```

### 4. Actualizar mascota
```http
PUT /pets/{id}
```

#### Body
```json
{
  "name": "Toby",
  "breed": "Golden Retriever",
  "lost_date": "2021-07-01",
  "lost_time": "12:00",
  "lost_description": "Golden retriever de 2 años de edad, color dorado, muy amigable.",
  "lost_contact": "John Doe, 123-456-7890",
  "latitude": "-34.6037",
  "longitude": "-58.3816"
}
```

### 5. Eliminar mascota
```http
DELETE /pets/{id}
```

### 6. Enviar formulario de contacto
```http
POST /contact
```

#### Body
```json
{
  "name": "María García",
  "email": "maria@email.com",
  "message": "Vi a un Husky por Palermo centro parecido..."
}
```

#### Respuesta exitosa
```json
{
  "message": "Mensaje enviado correctamente",
  "contact_id": 123
}
```

## Códigos de Estado

- 200: OK - Petición exitosa
- 201: Created - Recurso creado exitosamente  
- 400: Bad Request - Error en la petición
- 404: Not Found - Recurso no encontrado
- 500: Internal Server Error - Error del servidor
