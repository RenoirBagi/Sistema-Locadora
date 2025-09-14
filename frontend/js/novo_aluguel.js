const API_URL = "http://localhost:5000";

document.getElementById("form-aluguel").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    "cliente_cpf": e.target.cpf_cliente.value,
    "codigo_filme": e.target.codigo_filme.value,
    "valor_diaria": 20.99
  };

  console.log(e.target.cpf_cliente.value)
  console.log(e.target.codigo_filme.value)
  console.log(data)

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
