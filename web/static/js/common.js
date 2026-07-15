(function () {
    const STORAGE_KEY = "ednai.web.partida";

    function getState() {
        try {
            return JSON.parse(sessionStorage.getItem(STORAGE_KEY) || "null");
        } catch (error) {
            return null;
        }
    }

    function setState(state) {
        sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    }

    function clearState() {
        sessionStorage.removeItem(STORAGE_KEY);
    }

    async function apiRequest(url, options = {}) {
        const headers = {
            Accept: "application/json",
            ...(options.headers || {}),
        };

        if (options.body && !headers["Content-Type"]) {
            headers["Content-Type"] = "application/json";
        }

        const response = await fetch(url, {
            ...options,
            headers,
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            const message = data.message || data.erro || data.error || "Não foi possível concluir a operação.";
            throw new Error(message);
        }

        return data;
    }

    function setMessage(element, text, type = "info") {
        if (!element) {
            return;
        }
        element.textContent = text || "";
        element.className = "message";
        if (text) {
            element.classList.add("is-visible", type);
        }
    }

    function setLoading(button, isLoading, loadingText = "Aguarde...") {
        if (!button) {
            return;
        }
        if (isLoading) {
            button.dataset.originalText = button.textContent;
            button.textContent = loadingText;
            button.disabled = true;
            return;
        }
        button.textContent = button.dataset.originalText || button.textContent;
        button.disabled = false;
    }

    function formatTime(seconds) {
        const safeSeconds = Math.max(0, Number(seconds) || 0);
        const minutes = Math.floor(safeSeconds / 60);
        const remaining = safeSeconds % 60;
        return `${String(minutes).padStart(2, "0")}:${String(remaining).padStart(2, "0")}`;
    }

    function elapsedSeconds(state) {
        if (!state || !state.inicioTimestamp) {
            return 0;
        }
        return Math.max(0, Math.floor((Date.now() - state.inicioTimestamp) / 1000));
    }

    window.EdnaiWeb = {
        STORAGE_KEY,
        getState,
        setState,
        clearState,
        apiRequest,
        setMessage,
        setLoading,
        formatTime,
        elapsedSeconds,
    };
})();
