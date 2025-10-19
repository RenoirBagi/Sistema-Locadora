const API_URL = "http://localhost:5000";

document.getElementById("form-filme").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    "titulo": e.target.titulo_filme.value,
    "genero": e.target.genero_filme.value,
    "ano": e.target.ano_filme.value,
    "preco": e.target.preco_filme.value,
  };

  console.log(data);

  const response = await fetch(`${API_URL}/filmes/`, {
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
