const cardTemplate = document.getElementById("card-template");
const cardContainer = document.getElementById("card-container");
const cardSenhaAtual = document.getElementById("card-senha-atual");
const idSetorElement = document.querySelector('.id-setor');
const idEstacaoElement = document.querySelector('.id-estacao');
const refreshInterval = 5000; // 5 segundos

function refreshData() {
	const idSetor = idSetorElement.textContent;
	const idEstacao = idEstacaoElement.textContent;

    // Fetch updated data from the Blueprint using AJAX
    fetch('/recepcao/auto-refresh?id_setor=' + idSetor + '&id_estacao=' + idEstacao, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(({ senhas, senha_atual }) => {
        gerarCards(senhas);
        atualizarCardSenhaAtual(senha_atual);
    });

};

setInterval(refreshData, refreshInterval); 
 
function gerarCards(senhas) {
	cardContainer.innerHTML = '';
	 
	if (senhas !== null && senhas.length != 0) {
		senhas.forEach(senha => {
			const template = cardTemplate.cloneNode(true);
			const card = formatarCard(template, senha);
			cardContainer.appendChild(card);
		  });
	};
}

function atualizarCardSenhaAtual(senha) {
	cardSenhaAtual.innerHTML = "";
	if (senha) {
		const template = cardTemplate.cloneNode(true);
		const novoCard = formatarCard(template, senha);
		cardSenhaAtual.innerHTML = ""; 
		cardSenhaAtual.appendChild(novoCard);
	}
}

function formatarCard(card, senha) {
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
  
	card.classList.add("card-with-width", "card-with-margin", "mb-3");
	card.classList.remove("d-none");
  
	return card;
  }