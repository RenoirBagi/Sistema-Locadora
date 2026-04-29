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
        <td>
          <button onclick='abrirModalCliente(${JSON.stringify(cliente)})'>
            Editar
          </button>

          <button onclick='excluirCliente(${JSON.stringify(cliente.cpf)}, ${JSON.stringify(cliente.nome)})'>
            Excluir
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