const modal = document.createElement('div');
modal.id = 'modal';

const modalContent = document.createElement('div');
modalContent.id = 'modal-content'; 
modal.appendChild(modalContent);

const closeModalButton = document.createElement('button');
closeModalButton.id = 'close-modal-button'; 
closeModalButton.textContent = 'Cerrar';
closeModalButton.addEventListener('click', () => {
    modal.style.display = 'none';
});
modalContent.appendChild(closeModalButton);

document.body.appendChild(modal);

const buttons = document.querySelectorAll('.boton');
buttons.forEach(button => {
    button.addEventListener('click', (event) => {
        const parent = event.target.closest('.cuadrado');
        const nombre = parent.querySelector('.nombre').textContent;
        const tipo = parent.querySelector('.tipo').textContent;
        const raza = parent.querySelector('.dato:nth-child(3)').textContent;
        const color = parent.querySelector('.dato:nth-child(4)').textContent;

        modalContent.innerHTML = `
            <h2>${nombre}</h2>
            <p>${tipo}</p>
            <p>${raza}</p>
            <p>${color}</p>
            <p class="alerta">¡Esta mascota se encuentra perdida!</p>
        `;
        modalContent.appendChild(closeModalButton); 
        modal.style.display = 'flex';
    });
});
