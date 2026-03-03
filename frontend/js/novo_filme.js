document.getElementById("form-filme").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    "titulo": e.target.titulo.value,
    "genero": e.target.genero.value,
    "ano": e.target.ano.value,
    "preco": e.target.preco.value,
  };


  const response = await fetch(`${API_URL}/filmes/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await response.json();
  if (response.ok) {
    toast.success(result.mensagem || "Filme cadastrado com sucesso!");
    setTimeout(() => window.location.href = "filmes.html", 1500);
  } else {
    toast.error(result.erro || "Erro ao cadastrar filme.");
  }
});
