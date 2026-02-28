async function carregarAlugueis() {
  try {
    const response = await fetch(`${API_URL}/alugueis/`);
    const alugueis = await response.json();

    const tbody = document.getElementById("alugueis-tbody");
    tbody.innerHTML = "";

    if (!alugueis.length) {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td colspan="9">Nenhum aluguel registrado.</td>`;
      tbody.appendChild(tr);
      return;
    }

    alugueis.forEach(a => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${a.id}</td>
        <td>${a.cpf_cliente}</td>
        <td>${a.titulo_filme || "Desconhecido"}</td>
        <td>${a.data_aluguel ? a.data_aluguel.split('T')[0] : ""}</td>
        <td>${a.data_devolucao_prevista ? a.data_devolucao_prevista.split('T')[0] : ""}</td>
        <td>${a.data_devolucao ? a.data_devolucao.split('T')[0] : ""}</td>
        <td>${a.tempo_aluguel || ""}</td>
        <td>${a.valor != null ? Number(a.valor).toFixed(2) : ""}</td>
        <td>
          <button class="btn-acao btn-devolver" ${a.status ? "" : "disabled style='opacity:0.4; pointer-events:none;'"} onclick="devolverAluguel(${a.id})">Devolver</button>
          <button class="btn-acao btn-deletar" onclick="deletarAluguel(${a.id})">Deletar</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (error) {
    console.error("Erro ao carregar aluguéis:", error);
    toast.error("Erro ao carregar a lista de aluguéis.");
  }
}

async function deletarAluguel(id) {
  const confirmado = await dialog.danger(`Deseja realmente deletar o aluguel #${id}? Esta ação não pode ser desfeita.`, {
    title: "Deletar Aluguel"
  });

  if (confirmado) {
    const response = await fetch(`${API_URL}/alugueis/${id}`, {
      method: "DELETE"
    });
    const result = await response.json();
    if (response.ok) {
      toast.success(result.mensagem || "Aluguel deletado com sucesso!");
      carregarAlugueis();
    } else {
      toast.error(result.erro || "Erro ao deletar aluguel.");
    }
  }
}

async function devolverAluguel(id) {
  const confirmado = await dialog.confirm("Confirmar devolução deste filme?", {
    title: "Devolver Filme",
    confirmText: "Sim, devolver"
  });

  if (!confirmado) return;

  const response = await fetch(`${API_URL}/alugueis/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ devolver: true })
  });
  const result = await response.json();
  if (response.ok) {
    toast.success(result.mensagem || "Devolução realizada com sucesso!");
    carregarAlugueis();
  } else {
    toast.error(result.erro || "Erro ao registrar devolução.");
  }
}

window.onload = carregarAlugueis;
