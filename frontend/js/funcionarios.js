async function carregarFuncionarios() {
    try {
        const response = await fetch(`${API_URL}/funcionarios/`);
        const funcionarios = await response.json();

        const tbody = document.getElementById("funcionarios-tbody");
        if (!tbody) return;
        
        tbody.innerHTML = "";

        if (funcionarios.length === 0) {
            const tr = document.createElement("tr");
            tr.innerHTML = `<td colspan="4">Nenhum funcionário cadastrado.</td>`;
            tbody.appendChild(tr);
            return;
        }

        funcionarios.forEach(f => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${f.cpf}</td>
                <td>${f.nome}</td>
                <td>${f.cargo}</td>
                <td>${f.contato}</td>
                <td>${f.endereco}</td>
                <td>
                    <button class="btn-acao btn-devolver" onclick="editarFuncionario('${f.cpf}', '${f.nome}', '${f.cargo}', '${f.contato}', '${f.endereco}')">Editar</button>
                    <button class="btn-acao btn-deletar" onclick="excluirFuncionario('${f.cpf}')">Excluir</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error("Erro ao carregar funcionários:", error);
    }
}

async function editarFuncionario(cpf, nomeAt, cargoAt, contatoAt, enderecoAt) {
    const novoNome = prompt("Novo nome:", nomeAt);
    const novoCargo = prompt("Novo cargo:", cargoAt);
    const novoContato = prompt("Novo contato:", contatoAt);
    const novoEndereco = prompt("Novo endereço:", enderecoAt);

    if (!novoNome || !novoCargo || !novoContato || !novoEndereco) return;

    try {
        const response = await fetch(`${API_URL}/funcionarios/${cpf}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                nome: novoNome, 
                cargo: novoCargo,
                contato: novoContato,
                endereco: novoEndereco
            })
        });


        if (response.ok) {
            toast.success("Funcionário atualizado com sucesso!");
            carregarFuncionarios();
        } else {
            const result = await response.json();
            toast.error(result.erro || "Erro ao atualizar funcionário.");
        }
    } catch (error) {
        toast.error("Erro na comunicação com o servidor.");
    }
}

async function excluirFuncionario(cpf) {
    if (!confirm("Tem certeza que deseja excluir este funcionário?")) return;

    try {
        const response = await fetch(`${API_URL}/funcionarios/${cpf}`, {
            method: "DELETE"
        });


        if (response.ok) {
            toast.success("Funcionário excluído com sucesso!");
            carregarFuncionarios();
        } else {
            const result = await response.json();
            toast.error(result.erro || "Erro ao excluir funcionário.");
        }
    } catch (error) {
        toast.error("Erro na comunicação com o servidor.");
    }
}

document.addEventListener("DOMContentLoaded", carregarFuncionarios);
