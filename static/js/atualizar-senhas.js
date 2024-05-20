const refreshInterval = 5000; // 5 segundos

function refreshData() {
    // Fetch updated data from the Blueprint using AJAX
    fetch('/recepcao/auto-refresh', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        gerarCards(data)
    });
}

// Start the refresh timer
setInterval(refreshData, refreshInterval);