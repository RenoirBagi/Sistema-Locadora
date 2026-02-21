const API_URL = "http://localhost:5000";

document.getElementById("form-aluguel").addEventListener("submit", async (e) => {
  e.preventDefault();

  const cliente_cpf = e.target.cpf_cliente.value;
  const codigo_filme = parseInt(e.target.codigo_filme.value);

  // Buscar preço do filme dinamicamente
  const responseFilmes = await fetch(`${API_URL}/filmes/`);
  const filmes = await responseFilmes.json();
  const filme = filmes.find(f => f.id === codigo_filme);

  if (!filme) {
    alert("Filme não encontrado!");
    return;
  }

  const data = {
    "cliente_cpf": cliente_cpf,
    "codigo_filme": codigo_filme,
    "valor_diaria": filme.preco
  };

  const response = await fetch(`${API_URL}/alugueis/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await response.json();
  alert(result.mensagem || result.erro);

  if (response.ok) {
    window.location.href = "index.html";
  }
});
