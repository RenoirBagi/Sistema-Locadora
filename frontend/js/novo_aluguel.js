document.getElementById("form-aluguel").addEventListener("submit", async (e) => {
  e.preventDefault();

  const cliente_cpf = e.target.cpf_cliente.value;
  const codigo_filme = parseInt(e.target.codigo_filme.value);
  const data_devolucao_prevista = e.target.data_devolucao_prevista.value;

  if (!data_devolucao_prevista) {
    toast.error("Informe a data de devolução prevista.");
    return;
  }

  const data = {
    "cliente_cpf": cliente_cpf,
    "codigo_filme": codigo_filme,
    "data_devolucao_prevista": data_devolucao_prevista
  };

  const response = await fetch(`${API_URL}/alugueis/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await response.json();
  if (response.ok) {
    toast.success(result.mensagem || "Aluguel cadastrado com sucesso!");
    setTimeout(() => window.location.href = "index.html", 1500);
  } else {
    toast.error(result.erro || "Erro ao cadastrar aluguel.");
  }
});
