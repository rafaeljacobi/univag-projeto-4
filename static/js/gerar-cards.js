const cardTemplate = document.getElementById("card-template");
const cardContainer = document.getElementById("card-container");
const cardSenhaAtual = document.getElementById("card-senha-atual");

function gerarCards(senhas) {
	let lastCard;
	cardContainer.innerHTML = ''; // Clear existing content
	
	if (senhas.length != 0) {
		senhas.forEach(senha => {
			const card = cardTemplate.cloneNode(true); // Cria um clone do template
			card.classList.add("text-center");

			// Define o título do card
			const cardTitle = card.querySelector(".card-title");
			cardTitle.textContent = senha.numero;

			// Define a cor do card
			const cardHeader = card.querySelector('.card-header');
			if (senha.categoria === "Convencional") {
				cardHeader.classList.add("bg-primary");
			} else if (senha.categoria === "Prioridade") {
				cardHeader.classList.add("bg-danger");
			}

			// Define o conteúdo do card
			const cardText = card.querySelector(".card-text");
			cardText.innerHTML = `
				<p>${senha.data_hora}</p>
				<p>${senha.categoria}</p>
			`; 

			card.classList.add("card-with-width", "card-with-margin");

			// Remove a classe "d-none" do template e adiciona o card ao container
			card.classList.remove("d-none");
			cardContainer.appendChild(card);
			lastCard = card;
		});
	};
	if (lastCard) {
		cardSenhaAtual.innerHTML = lastCard.innerHTML;
	};
}