let cpfClienteParaExcluir = null;

async function carregarClientes() {
  try {
    const response = await fetch(`${API_URL}/clientes/`);
    const clientes = await response.json();

    const tbody = document.getElementById("clientes-tbody");
    if (!tbody) return;

    tbody.innerHTML = "";

    if (!clientes || clientes.length === 0) {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td colspan="6">Nenhum cliente cadastrado.</td>
      `;
      tbody.appendChild(tr);
      return;
    }

    clientes.forEach((cliente) => {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${cliente.cpf || "-"}</td>
        <td>${cliente.nome || "-"}</td>
        <td>${cliente.idade || "-"}</td>
        <td>${cliente.contato || "-"}</td>
        <td>${cliente.endereco || "-"}</td>
        <td class='td-acoes'>
          <button class='btn-acao' onclick='abrirModalCliente(${JSON.stringify(cliente)})'>
            Editar
          </button>

          <button class='btn-acao' onclick='excluirCliente(${JSON.stringify(cliente.cpf)}, ${JSON.stringify(cliente.nome)})'>
            Excluir
          </button>

          <button class='btn-acao' onclick="verHistoricoCliente('${cliente.cpf}')">
            Ver Histórico
          </button>
        </td>
      `;

      tbody.appendChild(tr);
    });

  } catch (error) {
    console.error("Erro ao carregar clientes:", error);
  }
}

function abrirModalCliente(cliente) {
  document.getElementById("edit-cpf").value = cliente.cpf || "";
  document.getElementById("edit-nome").value = cliente.nome || "";
  document.getElementById("edit-idade").value = cliente.idade || "";
  document.getElementById("edit-contato").value = cliente.contato || "";
  document.getElementById("edit-endereco").value = cliente.endereco || "";

  document.getElementById("modal-editar-cliente").classList.add("ativo");
}

function fecharModalCliente() {
  document.getElementById("modal-editar-cliente").classList.remove("ativo");
}

async function salvarEdicaoCliente(event) {
  event.preventDefault();

  const cpf = document.getElementById("edit-cpf").value;

  const clienteAtualizado = {
    nome: document.getElementById("edit-nome").value,
    idade: document.getElementById("edit-idade").value,
    contato: document.getElementById("edit-contato").value,
    endereco: document.getElementById("edit-endereco").value
  };

  try {
    const response = await fetch(`${API_URL}/clientes/${cpf}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(clienteAtualizado)
    });

    if (response.ok) {
      toast.success("Cliente atualizado com sucesso!");
      fecharModalCliente();
      carregarClientes();
    } else {
      const result = await response.json();
      toast.error(result.erro || "Erro ao atualizar cliente.");
    }

  } catch (error) {
    toast.error("Erro na comunicação com o servidor.");
  }
}

function excluirCliente(cpf, nome) {
  cpfClienteParaExcluir = cpf;

  const texto = document.getElementById("texto-confirmar-exclusao");

  if (texto) {
    texto.textContent = `Tem certeza que deseja excluir o cliente "${nome}"?`;
  }

  document.getElementById("modal-excluir-cliente").classList.add("ativo");
}

function fecharModalExcluirCliente() {
  cpfClienteParaExcluir = null;
  document.getElementById("modal-excluir-cliente").classList.remove("ativo");
}

async function confirmarExclusaoCliente() {
  if (!cpfClienteParaExcluir) return;

  try {
    const response = await fetch(`${API_URL}/clientes/${cpfClienteParaExcluir}`, {
      method: "DELETE"
    });

    if (response.ok) {
      toast.success("Cliente excluído com sucesso!");
      fecharModalExcluirCliente();
      carregarClientes();
    } else {
      const result = await response.json();
      toast.error(result.erro || "Erro ao excluir cliente.");
    }

  } catch (error) {
    toast.error("Erro na comunicação com o servidor.");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  carregarClientes();

  const formEditar = document.getElementById("form-editar-cliente");
  if (formEditar) {
    formEditar.addEventListener("submit", salvarEdicaoCliente);
  }

  const modalEditar = document.getElementById("modal-editar-cliente");
  if (modalEditar) {
    modalEditar.addEventListener("click", (event) => {
      if (event.target === modalEditar) {
        fecharModalCliente();
      }
    });
  }

  const modalExcluir = document.getElementById("modal-excluir-cliente");
  if (modalExcluir) {
    modalExcluir.addEventListener("click", (event) => {
      if (event.target === modalExcluir) {
        fecharModalExcluirCliente();
      }
    });
  }
});

async function verHistoricoCliente(cpf) {
  try {
    const response = await fetch(`${API_URL}/alugueis/cliente/${cpf}`);
    const result = await response.json();

    if (response.status === 404) {
      toast.error(result.erro || "Este cliente nunca realizou aluguéis.");
      return;
    }

    if (!response.ok) {
      toast.error(result.erro || "Erro ao buscar histórico.");
      return;
    }

    let linhasTabela = "";
    result.forEach(a => {
      const dataAluguel = a.data_aluguel ? a.data_aluguel.split('T')[0] : "";
      const dataDevolucao = a.data_devolucao ? a.data_devolucao.split('T')[0] : "<span style='color: orange;'>Ativo</span>";
      const valorFormatado = a.valor != null ? Number(a.valor).toFixed(2) : "0.00";

      linhasTabela += `
        <tr style="border-bottom: 1px solid #2e384d;">
          <td style="padding: 14px 12px; color: #ffffff; white-space: nowrap;">${a.id}</td>
          <td style="padding: 14px 12px; color: #ffffff; white-space: nowrap; font-weight: 500;">${a.titulo_filme || "Desconhecido"}</td>
          <td style="padding: 14px 12px; color: #cbd5e1; white-space: nowrap;">${dataAluguel}</td>
          <td style="padding: 14px 12px; color: #cbd5e1; white-space: nowrap;">${dataDevolucao}</td>
          <td style="padding: 14px 12px; color: #ffffff; white-space: nowrap; font-weight: bold;">R$ ${valorFormatado}</td>
        </tr>
      `;
    });

    const conteudoModal = `
      <style>
        /* Procura a classe do modal (mude para a classe real se não for essa) */
        .dialog-box, .modal-content, [role="dialog"] { 
          width: 800px !important; 
          max-width: 90vw !important; 
        }
      </style>

      <div style="max-height: 450px; overflow-x: auto; overflow-y: auto; border-radius: 8px;">
        <table style="width: 100%; border-collapse: collapse; text-align: left; font-family: inherit;">
          <thead>
            <tr style="background-color: #1e293b; border-bottom: 2px solid #3b82f6;">
              <th style="padding: 12px; color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; white-space: nowrap;">ID</th>
              <th style="padding: 12px; color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; white-space: nowrap;">Filme</th>
              <th style="padding: 12px; color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; white-space: nowrap;">Data Aluguel</th>
              <th style="padding: 12px; color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; white-space: nowrap;">Devolvido Em</th>
              <th style="padding: 12px; color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; white-space: nowrap;">Valor</th>
            </tr>
          </thead>
          <tbody>
            ${linhasTabela}
          </tbody>
        </table>
      </div>
    `;

    await dialog.confirm(conteudoModal, {
      title: `Histórico do Cliente (CPF: ${cpf})`,
      confirmText: "Fechar"
    });

  } catch (error) {
    console.error("Erro ao carregar histórico do cliente:", error);
    toast.error("Erro de conexão com o servidor.");
  }
}