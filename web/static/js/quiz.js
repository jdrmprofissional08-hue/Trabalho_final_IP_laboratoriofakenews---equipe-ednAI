document.addEventListener("DOMContentLoaded", () => {
    const state = EdnaiWeb.getState();
    const mensagem = document.querySelector("#mensagem");
    const quizApp = document.querySelector("#quiz-app");
    const tempoElement = document.querySelector("#tempo");
    const contadorCurtoElement = document.querySelector("#contador-curto");
    const contadorElement = document.querySelector("#contador");
    const percentualElement = document.querySelector("#percentual");
    const barraProgresso = document.querySelector("#barra-progresso");
    const imagem = document.querySelector("#noticia-imagem");
    const fonte = document.querySelector("#noticia-fonte");
    const manchete = document.querySelector("#noticia-manchete");
    const texto = document.querySelector("#noticia-texto");
    const botoesResposta = document.querySelector("#botoes-resposta");
    const btnFato = document.querySelector("#btn-fato");
    const btnFake = document.querySelector("#btn-fake");
    const feedback = document.querySelector("#feedback");
    const feedbackTitulo = document.querySelector("#feedback-titulo");
    const feedbackExplicacao = document.querySelector("#feedback-explicacao");
    const feedbackLink = document.querySelector("#feedback-link");
    const btnProximo = document.querySelector("#btn-proximo");

    let envioEmAndamento = false;
    let question = null;

    if (!state || !state.partidaId || !state.token || !state.total) {
        quizApp.classList.add("hidden");
        EdnaiWeb.setMessage(
            mensagem,
            "Nenhuma partida em andamento foi encontrada. Volte ao início e comece uma nova partida.",
            "error",
        );
        return;
    }

    if (state.finalizado) {
        window.location.href = "/resultado";
        return;
    }

    function updateTimer() {
        tempoElement.textContent = `⏱ ${EdnaiWeb.formatTime(EdnaiWeb.elapsedSeconds(state))}`;
    }

    function updateProgress() {
        const total = state.total;
        const atual = Math.min(state.atual + 1, total);
        const percentual = total > 0 ? Math.round((atual / total) * 100) : 0;
        contadorCurtoElement.textContent = `📰 ${atual}/${total}`;
        contadorElement.textContent = `Pergunta ${atual} de ${total}`;
        percentualElement.textContent = `${percentual}% concluído`;
        barraProgresso.style.width = `${percentual}%`;
    }

    async function loadQuestion() {
        EdnaiWeb.setMessage(mensagem, "Carregando questão...", "info");
        const result = await EdnaiWeb.apiRequest(
            `/api/partidas/${state.partidaId}/questao?indice=${state.atual}`,
            {
                headers: {
                    "X-Partida-Token": state.token,
                },
            },
        );
        const data = result.data || {};
        state.total = data.total || state.total;
        EdnaiWeb.setState(state);
        return data.questao;
    }

    async function renderQuestion() {
        try {
            question = await loadQuestion();
        } catch (error) {
            EdnaiWeb.setMessage(
                mensagem,
                `${error.message} Volte ao início e reinicie a partida se necessário.`,
                "error",
            );
            botoesResposta.classList.add("hidden");
            return;
        }

        if (!question) {
            EdnaiWeb.setMessage(mensagem, "A questão atual não foi encontrada. Reinicie a partida.", "error");
            return;
        }

        updateTimer();
        updateProgress();
        imagem.src = question.image_url || "";
        imagem.alt = `Imagem relacionada ao tema ${question.tema || "notícia"}`;
        fonte.textContent = `${question.fonte || "Fonte"} • ${question.tempo || "recentemente"}`;
        manchete.textContent = question.manchete || "";
        texto.textContent = question.texto || "";
        feedback.classList.add("hidden");
        botoesResposta.classList.remove("hidden");
        btnFato.disabled = false;
        btnFake.disabled = false;

        if (question.respondida) {
            btnFato.disabled = true;
            btnFake.disabled = true;
            EdnaiWeb.setMessage(
                mensagem,
                "Esta questão já foi respondida. Avance para a próxima ou reinicie a partida.",
                "info",
            );
        } else {
            EdnaiWeb.setMessage(mensagem, "");
        }
    }

    function renderFeedback(data) {
        const acertou = Boolean(data.acertou);
        feedbackTitulo.className = acertou ? "correct" : "wrong";
        feedbackTitulo.textContent = acertou ? "🎉 Você Acertou!" : "❌ Você Errou!";
        feedbackExplicacao.textContent = data.explicacao || "O backend registrou sua resposta, mas não retornou uma explicação.";
        feedbackLink.textContent = `Verificação completa no ${data.fonte || "fonte indicada"}`;
        feedbackLink.href = data.fonte_url || "#";
        btnProximo.textContent = state.atual >= state.total - 1
            ? "Ver Resultados Finais ➔"
            : "Próxima Pergunta ➔";
        botoesResposta.classList.add("hidden");
        feedback.classList.remove("hidden");
    }

    async function answerQuestion(respostaJogador) {
        if (envioEmAndamento) {
            return;
        }
        if (!question || !question.id) {
            EdnaiWeb.setMessage(mensagem, "A questão ainda não foi carregada. Tente novamente.", "error");
            return;
        }

        envioEmAndamento = true;
        btnFato.disabled = true;
        btnFake.disabled = true;
        EdnaiWeb.setMessage(mensagem, "Registrando sua resposta...", "info");

        try {
            const result = await EdnaiWeb.apiRequest(`/api/partidas/${state.partidaId}/responder`, {
                method: "POST",
                headers: {
                    "X-Partida-Token": state.token,
                },
                body: JSON.stringify({
                    noticia_id: question.id,
                    resposta_jogador: respostaJogador,
                }),
            });

            renderFeedback(result.data || {});
            EdnaiWeb.setMessage(mensagem, "");
        } catch (error) {
            EdnaiWeb.setMessage(
                mensagem,
                `${error.message} Tente enviar a resposta novamente.`,
                "error",
            );
            btnFato.disabled = false;
            btnFake.disabled = false;
        } finally {
            envioEmAndamento = false;
        }
    }

    async function finishMatch() {
        EdnaiWeb.setLoading(btnProximo, true, "Finalizando...");
        EdnaiWeb.setMessage(mensagem, "Finalizando sua partida...", "info");

        try {
            await EdnaiWeb.apiRequest(`/api/web/partidas/${state.partidaId}/finalizar`, {
                method: "POST",
                headers: {
                    "X-Partida-Token": state.token,
                },
                body: JSON.stringify({
                    duracao_segundos: EdnaiWeb.elapsedSeconds(state),
                }),
            });
            state.finalizado = true;
            EdnaiWeb.setState(state);
            window.location.href = "/resultado";
        } catch (error) {
            EdnaiWeb.setMessage(
                mensagem,
                `${error.message} A partida ainda não foi finalizada. Tente novamente.`,
                "error",
            );
            EdnaiWeb.setLoading(btnProximo, false);
        }
    }

    btnFato.addEventListener("click", () => answerQuestion(true));
    btnFake.addEventListener("click", () => answerQuestion(false));

    btnProximo.addEventListener("click", () => {
        if (state.atual >= state.total - 1) {
            finishMatch();
            return;
        }
        state.atual += 1;
        EdnaiWeb.setState(state);
        renderQuestion();
    });

    imagem.addEventListener("error", () => {
        imagem.removeAttribute("src");
        imagem.alt = "Imagem da notícia não encontrada.";
    });

    renderQuestion();
    window.setInterval(updateTimer, 1000);
});
