const modal = document.createElement('div');
modal.id = 'modal';
modal.style.display = 'none';
modal.style.position = 'fixed';
modal.style.top = '0';
modal.style.left = '0';
modal.style.width = '100%';
modal.style.height = '100%';
modal.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
modal.style.zIndex = '1000';
modal.style.justifyContent = 'center';
modal.style.alignItems = 'center';

const modalContent = document.createElement('div');
modalContent.style.backgroundColor = '#fff';
modalContent.style.borderRadius = '10px';
modalContent.style.padding = '20px';
modalContent.style.maxWidth = '500px';
modalContent.style.width = '90%';
modalContent.style.boxShadow = '0px 5px 15px rgba(0, 0, 0, 0.3)';
modalContent.style.textAlign = 'center';
modal.appendChild(modalContent);

const closeModalButton = document.createElement('button');
closeModalButton.textContent = 'Cerrar';
closeModalButton.style.marginTop = '20px';
closeModalButton.style.padding = '10px 20px';
closeModalButton.style.backgroundColor = 'var(--primary-color)';
closeModalButton.style.color = '#fff';
closeModalButton.style.border = 'none';
closeModalButton.style.borderRadius = '5px';
closeModalButton.style.cursor = 'pointer';
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
            <p style="color: red; font-weight: bold;">¡Esta mascota se encuentra perdida!</p>
        `;
        modalContent.appendChild(closeModalButton); 
        modal.style.display = 'flex';
    });
});
