document.querySelector("#search-form").addEventListener("submit", function (event) {
  event.preventDefault();
  const modalOverlay = createModalOverlay();
  const { resultsTitle, resultsContainer } = getModalElements(modalOverlay);
  const searchParams = collectSearchParams();
  const params = prepareURLParams(searchParams);

  clearPreviousResults(resultsContainer);
  showLoadingState(resultsTitle, modalOverlay);

  fetchSearchResults(params)
    .then(data => displaySearchResults(data, resultsTitle, resultsContainer))
    .catch(error => handleSearchError(error, resultsTitle, resultsContainer));
});

function createModalOverlay() {
  let modalOverlay = document.getElementById('modal-overlay');
  if (!modalOverlay) {
    modalOverlay = document.createElement('div');
    modalOverlay.id = 'modal-overlay';
    modalOverlay.classList.add('modal-overlay');
    modalOverlay.innerHTML = `
      <div class="modal-container">
        <div class="modal-header">
          <h3 id="results-title" class="modal-title"></h3>
          <button id="close-modal" class="close-modal">&times;</button>
        </div>
        <div id="results-container" class="modal-content"></div>
      </div>
    `;
    document.body.appendChild(modalOverlay);

    modalOverlay.querySelector('#close-modal').addEventListener('click', () => {
      modalOverlay.classList.remove('modal-visible');
    });

    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) {
        modalOverlay.classList.remove('modal-visible');
      }
    });
  }
  return modalOverlay;
}

function getModalElements(modalOverlay) {
  return {
    resultsTitle: modalOverlay.querySelector('#results-title'),
    resultsContainer: modalOverlay.querySelector('#results-container')
  };
}

function collectSearchParams() {
  return {
    type: document.querySelector("#cat").checked ? "cat" :
      document.querySelector("#dog").checked ? "dog" : "",
    sex: document.querySelector("#male").checked ? "male" :
      document.querySelector("#female").checked ? "female" : "",
    has_tag: document.querySelector("#hasNameTag").checked ? "True" :
      document.querySelector("#noNameTag").checked ? "False" : "",
    city: document.querySelector("#city").value,
    address: document.querySelector("#address").value
  };
}

function prepareURLParams(searchParams) {
  const params = new URLSearchParams();
  Object.entries(searchParams)
    .filter(([_, value]) => value !== "")
    .forEach(([key, value]) => params.append(key, value));
  return params;
}

function clearPreviousResults(resultsContainer) {
  resultsContainer.innerHTML = '';
}

function showLoadingState(resultsTitle, modalOverlay) {
  resultsTitle.textContent = 'Buscando mascotas...';
  resultsTitle.className = 'result-title';
  modalOverlay.classList.add('modal-visible');
}

function fetchSearchResults(params) {
  return fetch(`http://localhost:5000/api/v1/pets/search?${params.toString()}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    });
}

function displaySearchResults(data, resultsTitle, resultsContainer) {
  if (data.length > 0) {
    resultsTitle.textContent = `Dos ${data.length} mascota${data.length > 1 ? 's' : ''} coinciden con tu búsqueda`;
    resultsTitle.className = 'text-success';

    data.forEach(pet => {
      const petCard = document.createElement('div');
      petCard.classList.add('pet-card');
      petCard.innerHTML = `
        <div class="pet-card-header">
          <h4>${pet.pet_name || 'Nombre no disponible'}</h4>
        </div>
        <div class="pet-card-body">
          <img src="${pet.type === 'cat' ? '../static/images/illustrations/cat.svg' : '../static/images/illustrations/dog.svg'}" alt="Mascota">
          <p><strong>Raza:</strong> ${pet.breed || 'No especificada'}</p>
          <p><strong>Descripción:</strong> ${pet.description || 'Sin descripción'}</p>
          <p><strong>Ubicación:</strong> ${pet.lost_location || 'Ubicación no especificada'}</p>
          <p><strong>Contacto:</strong> ${pet.contact_info || 'No disponible'}</p>
        </div>
      `;
      resultsContainer.appendChild(petCard);
    });
  } else {
    resultsTitle.textContent = 'No se encontraron mascotas que coincidan con tu búsqueda';
    resultsTitle.className = 'text-warning';
  }
}

function handleSearchError(error, resultsTitle, resultsContainer) {
  console.error("Search error:", error);
  resultsTitle.textContent = 'Ocurrió un error al buscar. Por favor, intenta de nuevo.';
  resultsTitle.className = 'text-danger';

  const errorDetails = document.createElement('p');
  errorDetails.textContent = `Detalles del error: ${error.message}`;
  errorDetails.classList.add('error-details');
  resultsContainer.appendChild(errorDetails);
}