/**
 * Diálogo de Confirmação Customizado
 * Uso: const confirmado = await dialog.confirm("Mensagem aqui");
 */
const dialog = (() => {
    function _show({ title = "Confirmação", message, confirmText = "Confirmar", cancelText = "Cancelar", danger = false }) {
        return new Promise((resolve) => {
            // Remover diálogo anterior se existir
            document.getElementById("custom-dialog-overlay")?.remove();

            const overlay = document.createElement("div");
            overlay.id = "custom-dialog-overlay";
            overlay.className = "dialog-overlay";

            overlay.innerHTML = `
        <div class="dialog-box" role="alertdialog" aria-modal="true" aria-labelledby="dialog-title">
          <p class="dialog-title" id="dialog-title">${title}</p>
          <p class="dialog-message">${message}</p>
          <div class="dialog-actions">
            <button id="dialog-cancel" class="dialog-btn dialog-btn--cancel">${cancelText}</button>
            <button id="dialog-confirm" class="dialog-btn ${danger ? 'dialog-btn--danger' : 'dialog-btn--confirm'}">${confirmText}</button>
          </div>
        </div>
      `;

            document.body.appendChild(overlay);

            // Força reflow para animação
            overlay.getBoundingClientRect();
            overlay.classList.add("dialog-overlay--visible");

            function cleanup(result) {
                overlay.classList.remove("dialog-overlay--visible");
                overlay.addEventListener("transitionend", () => overlay.remove(), { once: true });
                resolve(result);
            }

            document.getElementById("dialog-confirm").addEventListener("click", () => cleanup(true));
            document.getElementById("dialog-cancel").addEventListener("click", () => cleanup(false));

            // Fechar ao clicar fora
            overlay.addEventListener("click", (e) => {
                if (e.target === overlay) cleanup(false);
            });

            // Fechar com ESC
            function onKeyDown(e) {
                if (e.key === "Escape") {
                    document.removeEventListener("keydown", onKeyDown);
                    cleanup(false);
                }
            }
            document.addEventListener("keydown", onKeyDown);

            // Foco no botão de confirmação
            document.getElementById("dialog-confirm").focus();
        });
    }

    return {
        confirm: (message, options = {}) => _show({ message, ...options }),
        danger: (message, options = {}) => _show({ message, danger: true, confirmText: "Sim, deletar", ...options }),
    };
})();
