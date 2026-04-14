const form = document.getElementById("form-novo-funcionario");

if (form) {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const cpf = document.getElementById("cpf").value;
        const nome = document.getElementById("nome").value;
        const cargo = document.getElementById("cargo").value;
        const contato = document.getElementById("contato").value;
        const endereco = document.getElementById("endereco").value;

        const data = { cpf, nome, cargo, contato, endereco };



        try {
            const response = await fetch(`${API_URL}/funcionarios/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                toast.success("Funcionário cadastrado com sucesso!");
                setTimeout(() => {
                    window.location.href = "funcionarios.html";
                }, 1500);
            } else {
                const result = await response.json();
                toast.error(result.erro || "Erro ao cadastrar funcionário.");
            }
        } catch (error) {
            toast.error("Erro na comunicação com o servidor.");
        }
    });
}
