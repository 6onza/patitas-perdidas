
const botones = document.querySelectorAll(".boton");


const modal = document.createElement("div");
modal.id = "info-modal";
modal.style.display = "none"; 
modal.style.position = "fixed";
modal.style.top = "0";
modal.style.left = "0";
modal.style.width = "100%";
modal.style.height = "100%";
modal.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
modal.style.zIndex = "1000";
modal.style.display = "flex";
modal.style.justifyContent = "center";
modal.style.alignItems = "center";

const modalContent = document.createElement("div");
modalContent.style.backgroundColor = "#fff";
modalContent.style.padding = "20px";
modalContent.style.borderRadius = "10px";
modalContent.style.width = "80%";
modalContent.style.maxWidth = "400px";
modalContent.style.boxShadow = "0 0 10px rgba(0,0,0,0.3)";
modalContent.style.textAlign = "center";

const closeButton = document.createElement("button");
closeButton.textContent = "Cerrar";
closeButton.style.marginTop = "10px";
closeButton.style.padding = "10px 20px";
closeButton.style.backgroundColor = "var(--primary-color)";
closeButton.style.color = "#fff";
closeButton.style.border = "none";
closeButton.style.borderRadius = "5px";
closeButton.style.cursor = "pointer";


closeButton.addEventListener("click", () => {
  modal.style.display = "none";
});

modalContent.appendChild(closeButton);
modal.appendChild(modalContent);
document.body.appendChild(modal);

botones.forEach((boton) => {
  boton.addEventListener("click", () => {
    const card = boton.closest(".cuadrado");
    const nombre = card.querySelector(".nombre").textContent;
    const tipo = card.querySelector(".dato:nth-child(2)").textContent;
    const raza = card.querySelector(".dato:nth-child(3)").textContent;
    const color = card.querySelector(".dato:nth-child(4)").textContent;

 
    modalContent.innerHTML = `
      <h2>${nombre}</h2>
      <p>${tipo}</p>
      <p>${raza}</p>
      <p>${color}</p>
      <p style="margin-top: 10px;">Esta mascota se encuentra perdida actualmente. Si la viste, podes marcarla en el mapa o comunicarte con nosotros.</p>
    `;
    modalContent.appendChild(closeButton); 

    
    modal.style.display = "flex";
  });
});