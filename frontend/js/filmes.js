const API_URL = "http://localhost:5000";

async function carregarFilmes() {
  const response = await fetch(`${API_URL}/filmes/`);
  const filmes = await response.json();

  const tbody = document.getElementById("filmes-tbody");
  tbody.innerHTML = "";

  const disponiveis = filmes.filter(f => f.disponivel);

  if (disponiveis.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="6">Nenhum filme disponível</td>`;
    tbody.appendChild(tr);
    return;
  }

  disponiveis.forEach(f => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${f.id}</td>
      <td>${f.titulo || ""}</td>
      <td>${f.genero || ""}</td>
      <td>${f.ano || ""}</td>
      <td>${typeof f.preco === "number" ? f.preco.toFixed(2) : (f.preco || "")}</td>
      <td>
        <button class="btn-acao btn-devolver" onclick="alugarFilme(${f.id})">Alugar</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

async function alugarFilme(filmeId) {
  const cpf = prompt("Informe o CPF do cliente:");
  if (!cpf) return;

  const data = {
    cliente_cpf: cpf,
    codigo_filme: filmeId,
    valor_diaria: 20.99
  };

  const response = await fetch(`${API_URL}/alugueis/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await response.json();
  alert(result.mensagem || result.erro);

  if (response.ok) {
    carregarFilmes();
  }
}

document.addEventListener("DOMContentLoaded", carregarFilmes);
