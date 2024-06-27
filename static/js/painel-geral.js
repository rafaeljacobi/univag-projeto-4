const cardTemplate = document.getElementById("card-template");
const cardContainer = document.getElementById("card-container");
const painelPrincipal = document.getElementById("painel-principal");
const refreshInterval = 5000; // 5 segundos

// Start the refresh timer
setInterval(refreshData, refreshInterval);

function refreshData() {
    // Fetch updated data from the Blueprint using AJAX
    fetch('/senha/recepcao/auto-refresh', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        atualizarCards(data);
    });
}

function playAudio() {
    const audio = document.getElementById('aviso-senha');
    audio.play();
}
 
function atualizarCards(senhas) {

    // Senha atual no painel de destaque
    const numeroSenha = document.getElementById("numero-senha");
    const numeroAtual = numeroSenha.textContent;
   
    limparDados()
    
	if (senhas.length > 0) {
        const primeiraSenha = senhas[0];

        // Senha nova no painel ?
        if (numeroAtual !== primeiraSenha.numero && numeroAtual !== '') {
            playAudio();
        };

        senhaDestaque(primeiraSenha);
      
        if (senhas.length > 1) {
            for (let i = 1; i < senhas.length; i++) {
                const senha = senhas[i];
                const template = cardTemplate.cloneNode(true);
                const card = formatarCard(template, senha);
                cardContainer.appendChild(card);
            }
        }
    }
}

// Limpa os campos do painel de detaque da última senha chamada
function limparDados() {
    cardContainer.innerHTML = '';
    const numeroSenha = document.getElementById("numero-senha");
    const guicheAtendente = document.getElementById("guiche-atendente"); 

    numeroSenha.textContent = '';
    guicheAtendente.textContent = '';
}

// Atualiza o painel de destaque da última senha  chamada
function senhaDestaque(senha) {
    const tituloRecepcao = document.getElementById("titulo-recepcao");
    const numeroSenha = document.getElementById("numero-senha");
    const guicheAtendente = document.getElementById("guiche-atendente");   
   
    tituloRecepcao.textContent = "Recepção";
    numeroSenha.textContent = senha.numero;
    guicheAtendente.textContent = senha.estacao;
}

function formatarCard(card, senha) {
	card.classList.add("text-center");
	// Define o título do card
	const cardTitle = card.querySelector(".card-title");
	cardTitle.textContent = senha.estacao;
  
	// Define a cor do card
	const cardHeader = card.querySelector('.card-header');
	if (senha.categoria === "Convencional") {
	  cardHeader.classList.add("bg-primary");
	} else if (senha.categoria === "Prioridade") {
	  cardHeader.classList.add("bg-danger");
	}
  
	// Define o conteúdo do card
	const cardText = card.querySelector(".card-text");
	cardText.innerHTML = senha.numero;
    
	card.classList.add("card-with-width", "card-with-margin");
	card.classList.remove("d-none");
  
	return card;
  }
