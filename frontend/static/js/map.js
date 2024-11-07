// Seed data for lost pets
let lost_pets = [
  {
    id: 1,
    name: "Toby",
    breed: "Golden Retriever",
    lost_date: "2021-07-01",
    lost_time: "12:00",
    lost_description:
      "Golden retriever de 2 años de edad, color dorado, muy amigable.",
    lost_contact: "John Doe, 123-456-7890",
    latitude:"-34.6037",
    longitude:"-58.3816"
  },
  {
    id: 2,
    name: "Bella",
    breed: "German Shepherd",
    lost_date: "2021-07-02",
    lost_time: "12:00",
    lost_description:
      "Pastor alemán de 3 años de edad, color blanco, muy juguetona.",
    lost_contact: "Jane Doe, 123-456-7890",
    latitude:"-34.6027",
    longitude:"-58.3906",
  },
  {
    id: 3,
    name: "Luna",
    breed: "Husky Siberiano",
    lost_date: "2024-07-03",
    lost_time: "12:00",
    lost_description: "Husky siberiano de 1 año de edad, color blanco, ojos azules.",
    lost_contact: "Pepe Picapiedra, 123-456-7890",
    latitude:"-34.6007",
    longitude:"-58.3506",
  },
];

// map initialization
var map = L.map("map").setView([-34.6037, -58.3816], 13);

// OpenStreetMap layer
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

// paw icon for lost pets
var pawIcon = L.icon({
  iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-violet.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// create marker for each lost pet
lost_pets.forEach((pet) => {
  var marker = L.marker([pet.latitude, pet.longitude], { icon: pawIcon }).addTo(map
  );

  
  // popup with pet information
  marker.bindPopup(`
    <b>${pet.name}</b><br>
    Raza: ${pet.breed}<br>
    Descripción: ${pet.lost_description}<br>
    Contacto: ${pet.lost_contact}<br>
    latitude: ${pet.latitude}<br>
    longitude: ${pet.longitude}
  `);
});