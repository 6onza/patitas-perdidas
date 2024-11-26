document.addEventListener("DOMContentLoaded", function () {
  const API_URL = "http://localhost:5000/api/v1";
  const newPetForm = document.getElementById("newPetForm");
  const petsGrid = document.getElementById("petsGrid");
  const notification = new bootstrap.Toast(
    document.getElementById("notification")
  );

  // Funcion para mostrar notificaciones
  function showNotification(message, success = true) {
    const toast = document.getElementById("notification");
    toast.querySelector(".toast-body").textContent = message;
    toast.classList.toggle("bg-success", success);
    toast.classList.toggle("bg-danger", !success);
    toast.classList.toggle("text-white", true);
    notification.show();
  }

  // Funcion para formatear fechas
  function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString("es-ES", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  }

  // Función para manejar acciones de mascota (eliminar o marcar como encontrada)
  async function handlePetAction(petId, action, actionName) {
    try {
      const token = localStorage.getItem("access_token");
      let endpoint = `${API_URL}/pets/${petId}`;
      let method = "DELETE";
      let body = null;

      if (action === "markFound") {
        endpoint = `${API_URL}/pets/${petId}`;
        method = "PUT";
        body = JSON.stringify({ status: "found" });
      }

      const response = await fetch(endpoint, {
        method: method,
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: body,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `Error al ${actionName}`);
      }

      showNotification(`Mascota ${actionName} exitosamente`, true);
      await loadPets();
    } catch (error) {
      showNotification(error.message, false);
    }
  }

  // Función para crear la tarjeta de mascota
  function createPetCard(pet) {
    const statusClass = pet.status === "found" ? "bg-success" : "bg-warning";
    const statusText = pet.status === "found" ? "Encontrado" : "Perdido";

    const petCardHTML = `
    <div class="col-lg-4 my-2">
      <div class="card">
        <div class="card-header d-flex gap-2 py-4 justify-content-center align-items-center">
          <span class="badge ${statusClass} text-white px-3 py-2 fs-5">${statusText}</span>
        </div>
        <img 
          src="${
            pet.photo_url
              ? pet.photo_url
              : `../static/images/illustrations/${pet.type}.svg`
          }" 
          class="card-img-top mx-auto d-block mt-3" 
          style="max-width:150px; min-height:150px;" 
          alt="${pet.pet_name}"
        >
        <div class="card-body">
          <h5 class="card-title">${pet.pet_name}</h5>
          <p class="card-text">
            <strong>Tipo:</strong> ${
              pet.type === "dog"
                ? "Perro"
                : pet.type === "cat"
                ? "Gato"
                : "Otro"
            }<br>
            <strong>Raza:</strong> ${pet.breed}<br>
            <strong>Color:</strong> ${pet.color}<br>
            <strong>Fecha de pérdida:</strong> ${formatDate(pet.lost_date)}<br>
            <strong>Ubicación:</strong> ${pet.lost_location}
          </p>
        </div>
        <div class="btn-group m-3">
            ${
              pet.status === "lost"
                ? `
              <button class="btn btn-success btn-sm mark-found me-2" data-pet-id="${pet.id}">
                <i class="fa fa-check"></i> 
                Encontrado
              </button>
            `
                : ""
            }
            <button class="btn btn-danger btn-sm delete-pet" data-pet-id="${
              pet.id
            }">
              <i class="fa fa-trash"></i> Eliminar
            </button>
          </div>
      </div>
    </div>
  `;

    const petCard = document.createElement("div");
    petCard.innerHTML = petCardHTML;

    // Agregar event listeners para los botones
    const card = petCard.firstElementChild;
    const deleteBtn = card.querySelector(".delete-pet");
    const markFoundBtn = card.querySelector(".mark-found");

    if (deleteBtn) {
      deleteBtn.addEventListener("click", () => {
        if (confirm("¿Estás seguro de que deseas eliminar esta mascota?")) {
          handlePetAction(pet.id, "delete", "eliminada");
        }
      });
    }

    if (markFoundBtn) {
      markFoundBtn.addEventListener("click", () => {
        if (confirm("¿Confirmas que esta mascota ha sido encontrada?")) {
          handlePetAction(pet.id, "markFound", "actualizada");
        }
      });
    }

    return card;
  }

  async function loadPets(filters = {}) {
    try {
      const token = localStorage.getItem("access_token");

      const response = await fetch(`${API_URL}/pets/user`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (response.status === 401 || response.status === 422) {
        // si el token expiró o es inválido, redirigir al login
        window.location.href = "/login";
      }

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error detallado:", errorData);
        throw new Error(errorData.error || "Error al cargar las mascotas");
      }

      const data = await response.json();

      const pets = data.pets || data;
      console.log("Mascotas procesadas:", pets);

      petsGrid.innerHTML = "";

      if (pets.length === 0) {
        const emptyTemplate = document.getElementById("emptyState");
        petsGrid.appendChild(emptyTemplate.content.cloneNode(true));
        return;
      }

      pets.forEach((pet) => {
        petsGrid.appendChild(createPetCard(pet));
      });
    } catch (error) {
      console.error("Error:", error);
      showNotification(error.message, false);
    }
  }

  // New pet form handler
  newPetForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const submitButton = newPetForm.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    const formData = {
      pet_name: document.getElementById("pet_name").value,
      type: document.getElementById("pet_type").value,
      sex: document.getElementById("pet_sex").value,
      breed: document.getElementById("breed").value,
      color: document.getElementById("color").value,
      lost_date: document.getElementById("lost_date").value,
      lost_city: document.getElementById("lost_city").value,
      lost_location: document.getElementById("lost_location").value,
      status: "lost",
      lost_latitude: parseFloat(document.getElementById("lost_latitude").value),
      lost_longitude: parseFloat(
        document.getElementById("lost_longitude").value
      ),
      description: document.getElementById("description").value,
      has_name_tag: document.getElementById("has_name_tag").checked,
    };

    try {
      const response = await fetch(`${API_URL}/pets/create`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify(formData),
      });
      // if not 201
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Error al guardar la mascota");
      }

      showNotification("Mascota registrada exitosamente", true);
      const modal = bootstrap.Modal.getInstance(
        document.getElementById("newPetModal")
      );
      modal.hide();
      newPetForm.reset();
      await loadPets();
    } catch (error) {
      showNotification(error.message, false);
    } finally {
      submitButton.disabled = false;
    }
  });

  // Load initial pets
  loadPets();
});
function logout() {
  // Eliminar el token de acceso
  localStorage.removeItem("access_token");
  // Redirigir al inicio
  window.location.href = "/";
}
