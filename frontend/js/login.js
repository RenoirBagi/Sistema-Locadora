// Lógica de Autenticação - YOLOOK

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-login");
  const emailInput = document.getElementById("email");
  const senhaInput = document.getElementById("senha");
  const btnToggleSenha = document.getElementById("btn-toggle-senha");
  const eyeIcon = document.getElementById("eye-icon");
  const btnSubmit = document.getElementById("btn-submit");
  const btnText = document.getElementById("btn-text");
  const btnSpinner = document.getElementById("btn-spinner");

  // 1. Alternar Visibilidade da Senha (Mapeamento Premium do Olho)
  if (btnToggleSenha && senhaInput && eyeIcon) {
    btnToggleSenha.addEventListener("click", () => {
      const isPassword = senhaInput.type === "password";
      senhaInput.type = isPassword ? "text" : "password";
      btnToggleSenha.title = isPassword ? "Ocultar senha" : "Mostrar senha";
      btnToggleSenha.setAttribute("aria-label", isPassword ? "Ocultar senha" : "Mostrar senha");

      // Atualiza o SVG do olho dinamicamente para o efeito de "riscado"
      if (isPassword) {
        // Ícone de Olho com traço (Slashed Eye)
        eyeIcon.innerHTML = `
          <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18" />
        `;
      } else {
        // Ícone de Olho aberto original
        eyeIcon.innerHTML = `
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
        `;
      }
    });
  }

  // 2. Envio do Formulário e Autenticação
  if (form) {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();

      const email = emailInput.value.trim();
      const senha = senhaInput.value;

      // Validação Client-Side Básica
      if (!email || !senha) {
        toast.error("Por favor, preencha todos os campos.");
        return;
      }

      // Validação simples de formato de e-mail
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        toast.error("Insira um endereço de e-mail corporativo válido.");
        return;
      }

      // Ativa o estado de carregamento
      setLoading(true);

      try {
        const response = await fetch(`${API_URL}/funcionarios/login`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email, senha }),
        });

        const result = await response.json();

        if (response.ok) {
          // Armazena credenciais e redireciona
          localStorage.setItem("yolook_token", result.token);
          localStorage.setItem("yolook_user", JSON.stringify(result.funcionario));

          toast.success("Login realizado com sucesso! Redirecionando...");

          // Pequeno delay para exibir o Toast de sucesso
          setTimeout(() => {
            window.location.href = "dashboard.html";
          }, 1000);
        } else {
          // Restaura botão e exibe erro retornado do backend
          setLoading(false);
          toast.error(result.erro || "Falha na autenticação.");
        }
      } catch (error) {
        // Restaura botão e exibe erro genérico de rede
        setLoading(false);
        toast.error("Erro ao conectar com o servidor. Verifique se a API está ativa.");
        console.error("Erro de comunicação com API:", error);
      }
    });
  }

  // Helper para alternar o loading do botão
  function setLoading(isLoading) {
    if (isLoading) {
      btnSubmit.disabled = true;
      btnText.textContent = "Autenticando...";
      btnSpinner.style.display = "inline-block";
    } else {
      btnSubmit.disabled = false;
      btnText.textContent = "Entrar no Sistema";
      btnSpinner.style.display = "none";
    }
  }
});
