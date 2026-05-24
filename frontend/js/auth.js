// Controle de Autenticação e Sessão - YOLOOK

(function () {
  const token = localStorage.getItem("yolook_token");
  const userJson = localStorage.getItem("yolook_user");
  const isLoginPage = window.location.pathname.includes("login.html");

  // 1. Redirecionamento de segurança
  if (!token || !userJson) {
    // Se não estiver autenticado e não estiver na tela de login, manda para o login
    if (!isLoginPage) {
      window.location.href = "login.html";
      return;
    }
  } else {
    // Se já estiver autenticado e tentar acessar a tela de login, manda para o dashboard
    if (isLoginPage) {
      window.location.href = "dashboard.html";
      return;
    }
  }

  // 2. Renderização dinâmica do perfil e logout no cabeçalho se autenticado
  if (token && userJson && !isLoginPage) {
    document.addEventListener("DOMContentLoaded", () => {
      const user = JSON.parse(userJson);
      const container = document.querySelector(".site-header .container");

      if (container) {
        // Remove um possível container antigo para evitar duplicados
        const oldProfile = document.getElementById("header-user-profile");
        if (oldProfile) oldProfile.remove();

        // Cria o componente de perfil do usuário logado
        const profileDiv = document.createElement("div");
        profileDiv.id = "header-user-profile";
        profileDiv.className = "header-profile-container";
        profileDiv.innerHTML = `
          <div class="user-info">
            <span class="user-name">${user.nome.split(" ")[0]}</span>
            <span class="user-role">${user.cargo}</span>
          </div>
          <button id="btn-logout" class="btn-logout" title="Sair do sistema">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </button>
        `;

        // Insere o perfil após a barra de pesquisa
        const searchContainer = container.querySelector(".search-container");
        if (searchContainer) {
          searchContainer.after(profileDiv);
        } else {
          container.appendChild(profileDiv);
        }

        // Listener do botão de logout
        const logoutBtn = document.getElementById("btn-logout");
        if (logoutBtn) {
          logoutBtn.addEventListener("click", () => {
            // Limpa o localStorage e redireciona
            localStorage.removeItem("yolook_token");
            localStorage.removeItem("yolook_user");
            
            // Se o toast.js estiver disponível na página, mostra um feedback visual
            if (typeof toast !== "undefined" && toast.success) {
              toast.success("Sessão encerrada com sucesso!");
              setTimeout(() => {
                window.location.href = "login.html";
              }, 1000);
            } else {
              window.location.href = "login.html";
            }
          });
        }
      }
    });
  }
})();
