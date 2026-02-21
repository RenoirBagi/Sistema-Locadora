document.getElementById("form-filme").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    "titulo": e.target.titulo.value,
    "genero": e.target.genero.value,
    "ano": e.target.ano.value,
    "preco": e.target.preco.value,
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
    window.location.href = "filmes.html";
  }
});
