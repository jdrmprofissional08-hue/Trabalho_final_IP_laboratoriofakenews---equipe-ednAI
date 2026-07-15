document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#form-inicio");
    const nomeInput = document.querySelector("#nome");
    const idadeInput = document.querySelector("#idade");
    const consentimentoInput = document.querySelector("#consentimento");
    const iniciarButton = document.querySelector("#btn-iniciar");
    const mensagem = document.querySelector("#mensagem");

    EdnaiWeb.clearState();

    function getSelectedThemes() {
        return Array.from(document.querySelectorAll("input[name='temas']:checked"))
            .map((input) => input.value);
    }

    function validateForm() {
        const nome = nomeInput.value.trim();
        const idade = Number(idadeInput.value);
        const temas = getSelectedThemes();

        if (nome.length < 3) {
            return "Informe um nome com pelo menos 3 caracteres.";
        }
        if (!Number.isInteger(idade) || idade < 1 || idade > 120) {
            return "Informe uma idade válida entre 1 e 120 anos.";
        }
        if (temas.length === 0) {
            return "Selecione pelo menos um tema para iniciar a partida.";
        }
        if (!consentimentoInput.checked) {
            return "Aceite o termo de consentimento para participar da atividade.";
        }
        return "";
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        EdnaiWeb.setMessage(mensagem, "");

        const validationError = validateForm();
        if (validationError) {
            EdnaiWeb.setMessage(mensagem, validationError, "error");
            return;
        }

        EdnaiWeb.setLoading(iniciarButton, true, "Iniciando...");

        try {
            const payload = {
                nome: nomeInput.value.trim(),
                idade: Number(idadeInput.value),
                consentimento: consentimentoInput.checked,
                temas: getSelectedThemes(),
                total_questoes: 10,
            };

            const result = await EdnaiWeb.apiRequest("/api/web/partidas", {
                method: "POST",
                body: JSON.stringify(payload),
            });

            const data = result.data || {};
            if (!data.partida_id || !data.token || !data.total_questoes) {
                throw new Error("Não foi possível preparar as notícias da partida.");
            }

            EdnaiWeb.setState({
                usuarioId: data.usuario_id,
                partidaId: data.partida_id,
                token: data.token,
                atual: 0,
                total: data.total_questoes,
                inicioTimestamp: Date.now(),
                finalizado: false,
            });

            window.location.href = "/quiz";
        } catch (error) {
            EdnaiWeb.setMessage(
                mensagem,
                `${error.message} Verifique sua conexão e tente novamente.`,
                "error",
            );
            EdnaiWeb.setLoading(iniciarButton, false);
        }
    });
});
