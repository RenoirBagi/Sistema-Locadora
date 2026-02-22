/**
 * Sistema de Notificações Toast
 * Uso: toast.success("Mensagem") | toast.error("Mensagem") | toast.info("Mensagem")
 */
const toast = (() => {
    let container = null;

    function _getContainer() {
        if (!container) {
            container = document.createElement("div");
            container.id = "toast-container";
            document.body.appendChild(container);
        }
        return container;
    }

    function _show(message, type = "info", duration = 3500) {
        const c = _getContainer();

        const toast = document.createElement("div");
        toast.className = `toast toast--${type}`;

        const icons = {
            success: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm-1.25 14.19-3.54-3.54 1.41-1.41 2.13 2.13 4.59-4.59 1.41 1.42-6 6z"/></svg>`,
            error: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>`,
            info: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>`,
        };

        toast.innerHTML = `
      <span class="toast__icon">${icons[type] || icons.info}</span>
      <span class="toast__message">${message}</span>
      <button class="toast__close" aria-label="Fechar">&#x2715;</button>
    `;

        toast.querySelector(".toast__close").addEventListener("click", () => _dismiss(toast));

        c.appendChild(toast);

        // Força reflow para animação funcionar
        toast.getBoundingClientRect();
        toast.classList.add("toast--visible");

        const timer = setTimeout(() => _dismiss(toast), duration);
        toast._timer = timer;
    }

    function _dismiss(toastEl) {
        clearTimeout(toastEl._timer);
        toastEl.classList.remove("toast--visible");
        toastEl.classList.add("toast--hiding");
        toastEl.addEventListener("transitionend", () => toastEl.remove(), { once: true });
    }

    return {
        success: (msg, duration) => _show(msg, "success", duration),
        error: (msg, duration) => _show(msg, "error", duration),
        info: (msg, duration) => _show(msg, "info", duration),
    };
})();
