let cpfFuncionarioParaExcluir = null;

async function carregarFuncionarios() {
  try {
    const response = await fetch(`${API_URL}/funcionarios/`);
    const funcionarios = await response.json();

    const tbody = document.getElementById("funcionarios-tbody");
    if (!tbody) return;

    tbody.innerHTML = "";

    if (!funcionarios || funcionarios.length === 0) {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td colspan="6">Nenhum funcionário cadastrado.</td>
      `;
      tbody.appendChild(tr);
      return;
    }

    funcionarios.forEach((funcionario) => {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${funcionario.cpf || "-"}</td>
        <td>${funcionario.nome || "-"}</td>
        <td>${funcionario.cargo || "-"}</td>
        <td>${funcionario.email || "-"}</td>
        <td>
          <span class="badge-status ${funcionario.status === 'ativo' ? 'status-ativo' : 'status-inativo'}">
            ${funcionario.status === 'ativo' ? 'Ativo' : 'Inativo'}
          </span>
        </td>
        <td>${funcionario.contato || "-"}</td>
        <td>${funcionario.endereco || "-"}</td>
        <td>
          <button class="btn-acao btn-devolver" onclick='abrirModalFuncionario(${JSON.stringify(funcionario)})'>
            Editar
          </button>

          <button class="btn-acao btn-deletar" onclick='excluirFuncionario(${JSON.stringify(funcionario.cpf)}, ${JSON.stringify(funcionario.nome)})'>
            Excluir
          </button>
        </td>
      `;

      tbody.appendChild(tr);
    });

  } catch (error) {
    console.error("Erro ao carregar funcionários:", error);
  }
}

function abrirModalFuncionario(funcionario) {
  document.getElementById("edit-cpf").value = funcionario.cpf || "";
  document.getElementById("edit-nome").value = funcionario.nome || "";
  document.getElementById("edit-cargo").value = funcionario.cargo || "";
  document.getElementById("edit-email").value = funcionario.email || "";
  document.getElementById("edit-senha").value = "";
  document.getElementById("edit-status").value = funcionario.status || "ativo";
  document.getElementById("edit-contato").value = funcionario.contato || "";
  document.getElementById("edit-endereco").value = funcionario.endereco || "";

  document.getElementById("modal-editar-funcionario").classList.add("ativo");
}

function fecharModalFuncionario() {
  document.getElementById("modal-editar-funcionario").classList.remove("ativo");
}

async function salvarEdicaoFuncionario(event) {
  event.preventDefault();

  const cpf = document.getElementById("edit-cpf").value;

  const funcionarioAtualizado = {
    nome: document.getElementById("edit-nome").value,
    cargo: document.getElementById("edit-cargo").value,
    email: document.getElementById("edit-email").value,
    status: document.getElementById("edit-status").value,
    contato: document.getElementById("edit-contato").value,
    endereco: document.getElementById("edit-endereco").value
  };

  const senha = document.getElementById("edit-senha").value;
  if (senha.trim() !== "") {
    funcionarioAtualizado.senha = senha;
  }

  try {
    const response = await fetch(`${API_URL}/funcionarios/${cpf}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(funcionarioAtualizado)
    });

    if (response.ok) {
      toast.success("Funcionário atualizado com sucesso!");
      fecharModalFuncionario();
      carregarFuncionarios();
    } else {
      const result = await response.json();
      toast.error(result.erro || "Erro ao atualizar funcionário.");
    }

  } catch (error) {
    toast.error("Erro na comunicação com o servidor.");
  }
}

function excluirFuncionario(cpf, nome) {
  cpfFuncionarioParaExcluir = cpf;

  const texto = document.getElementById("texto-confirmar-exclusao-funcionario");

  if (texto) {
    texto.textContent = `Tem certeza que deseja excluir o funcionário "${nome}"?`;
  }

  document.getElementById("modal-excluir-funcionario").classList.add("ativo");
}

function fecharModalExcluirFuncionario() {
  cpfFuncionarioParaExcluir = null;
  document.getElementById("modal-excluir-funcionario").classList.remove("ativo");
}

async function confirmarExclusaoFuncionario() {
  if (!cpfFuncionarioParaExcluir) return;

  try {
    const response = await fetch(`${API_URL}/funcionarios/${cpfFuncionarioParaExcluir}`, {
      method: "DELETE"
    });

    if (response.ok) {
      toast.success("Funcionário excluído com sucesso!");
      fecharModalExcluirFuncionario();
      carregarFuncionarios();
    } else {
      const result = await response.json();
      toast.error(result.erro || "Erro ao excluir funcionário.");
    }

  } catch (error) {
    toast.error("Erro na comunicação com o servidor.");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  carregarFuncionarios();

  const formEditar = document.getElementById("form-editar-funcionario");
  if (formEditar) {
    formEditar.addEventListener("submit", salvarEdicaoFuncionario);
  }

  const modalEditar = document.getElementById("modal-editar-funcionario");
  if (modalEditar) {
    modalEditar.addEventListener("click", (event) => {
      if (event.target === modalEditar) {
        fecharModalFuncionario();
      }
    });
  }

  const modalExcluir = document.getElementById("modal-excluir-funcionario");
  if (modalExcluir) {
    modalExcluir.addEventListener("click", (event) => {
      if (event.target === modalExcluir) {
        fecharModalExcluirFuncionario();
      }
    });
  }
});