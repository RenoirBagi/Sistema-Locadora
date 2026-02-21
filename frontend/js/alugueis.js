async function carregarAlugueis() {
  const response = await fetch(`${API_URL}/alugueis/`);
  const alugueis = await response.json();

  const tbody = document.getElementById("alugueis-tbody");
  tbody.innerHTML = "";

  alugueis.forEach(a => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${a.id}</td>
      <td>${a.cpf_cliente}</td>
      <td>${a.codigo_filme}</td>
      <td>${a.data_aluguel ? a.data_aluguel.split('T')[0] : ""}</td>
      <td>${a.data_devolucao ? a.data_devolucao.split('T')[0] : ""}</td>
      <td>${a.valor || ""}</td>
      <td>
        <button ${a.status ? "" : "disabled style='opacity:0.4; pointer-events:none;'"} onclick="devolverAluguel(${a.id})">Devolver</button>
        <button onclick="deletarAluguel(${a.id})">Deletar</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

async function deletarAluguel(id) {
  if (confirm("Deseja deletar este aluguel?")) {
    const response = await fetch(`${API_URL}/alugueis/${id}`, {
      method: "DELETE"
    });
    const result = await response.json();
    alert(result.mensagem || result.erro);
    carregarAlugueis();
  }
}

async function devolverAluguel(id) {
  const data = { data_devolucao: new Date().toISOString() };
  const response = await fetch(`${API_URL}/alugueis/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  const result = await response.json();
  alert(result.mensagem || result.erro);
  carregarAlugueis();
}

window.onload = carregarAlugueis;
