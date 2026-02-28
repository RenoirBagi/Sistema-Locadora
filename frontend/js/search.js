document.addEventListener("DOMContentLoaded", () => {
    const searchInputs = document.querySelectorAll(".search-container input");

    searchInputs.forEach(input => {
        // Preenche o input com o termo atual da busca, se existir
        const urlParams = new URLSearchParams(window.location.search);
        const termoBusca = urlParams.get('busca');
        if (termoBusca) {
            input.value = termoBusca;
        }

        input.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                const busca = input.value.trim();
                if (busca) {
                    // Redireciona para a página de filmes passando o termo de busca na URL
                    window.location.href = `filmes.html?busca=${encodeURIComponent(busca)}`;
                } else {
                    // Se estiver vazio, vai para a página de filmes normal (lista coplete)
                    window.location.href = `filmes.html`;
                }
            }
        });
    });
});
