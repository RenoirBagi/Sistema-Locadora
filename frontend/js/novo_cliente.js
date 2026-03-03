document.getElementById("form-cliente").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    "cpf": e.target.cpf_cliente.value,
    "nome": e.target.nome_cliente.value,
    "idade": e.target.idade_cliente.value,
    "contato": e.target.contato_cliente.value,
    "endereco": e.target.endereco_cliente.value
  };


  const response = await fetch(`${API_URL}/clientes/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await response.json();
  if (response.ok) {
    toast.success(result.mensagem || "Cliente cadastrado com sucesso!");
    setTimeout(() => window.location.href = "index.html", 1500);
  } else {
    toast.error(result.erro || "Erro ao cadastrar cliente.");
  }
});
