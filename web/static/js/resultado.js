document.addEventListener("DOMContentLoaded", () => {
    const state = EdnaiWeb.getState();
    const pontuacao = document.querySelector("#pontuacao");
    const detalhes = document.querySelector("#detalhes");
    const feedbackGeral = document.querySelector("#feedback-geral");
    const mensagem = document.querySelector("#mensagem");
    const ednaiResposta = document.querySelector("#ednai-resposta");
    const formEdnai = document.querySelector("#form-ednai");
    const perguntaEdnai = document.querySelector("#pergunta-ednai");
    const btnEdnai = document.querySelector("#btn-ednai");

    if (!state || !state.partidaId || !state.token) {
        EdnaiWeb.setMessage(
            mensagem,
            "Nenhuma partida finalizada foi encontrada. Volte ao início e jogue novamente.",
            "error",
        );
        formEdnai.querySelectorAll("input, button").forEach((element) => {
            element.disabled = true;
        });
        return;
    }

    function feedbackText(score, total) {
        const rate = total > 0 ? score / total : 0;
        if (rate === 1) {
            return "Perfeito! Você desmascarou todas as notícias falsas. Um verdadeiro perito digital!";
        }
        if (rate >= 0.7) {
            return "Muito bom! Você tem um ótimo faro contra notícias falsas.";
        }
        if (rate >= 0.5) {
            return "Bom resultado, mas fique atento. Algumas desinformações conseguiram te enganar.";
        }
        return "Cuidado! As notícias falsas te enganaram na maioria das vezes. Treine mais seu olhar crítico.";
    }

    async function loadResult() {
        try {
            const result = await EdnaiWeb.apiRequest(`/api/partidas/${state.partidaId}/resultado`, {
                headers: {
                    "X-Partida-Token": state.token,
                },
            });
            const data = result.data || {};

            if (!data.finalizada) {
                EdnaiWeb.setMessage(
                    mensagem,
                    "Esta partida ainda não foi finalizada. Volte ao quiz para concluir as respostas.",
                    "error",
                );
                return;
            }

            pontuacao.textContent = `${data.score} / ${data.total}`;
            detalhes.textContent = `Acertos: ${data.score} | Erros: ${data.erros}`;
            feedbackGeral.textContent = feedbackText(Number(data.score), Number(data.total));

            await analyzeWithEdnai();
        } catch (error) {
            EdnaiWeb.setMessage(
                mensagem,
                `${error.message} Não foi possível carregar o resultado agora.`,
                "error",
            );
        }
    }

    async function analyzeWithEdnai() {
        ednaiResposta.textContent = "Ednai está analisando seu desempenho...";
        btnEdnai.disabled = true;

        try {
            const result = await EdnaiWeb.apiRequest(`/api/partidas/${state.partidaId}/ednai/analyze`, {
                method: "POST",
                headers: {
                    "X-Partida-Token": state.token,
                },
                body: JSON.stringify({}),
            });
            const resposta = result.resposta || "Ednai não retornou uma resposta agora.";
            ednaiResposta.textContent = resposta;
        } catch (error) {
            ednaiResposta.textContent = "A inteligência artificial está temporariamente indisponível. O quiz continua funcionando normalmente.";
            EdnaiWeb.setMessage(mensagem, error.message, "info");
        } finally {
            btnEdnai.disabled = false;
        }
    }

    formEdnai.addEventListener("submit", async (event) => {
        event.preventDefault();
        const message = perguntaEdnai.value.trim();
        if (!message) {
            EdnaiWeb.setMessage(mensagem, "Digite uma pergunta para o Ednai.", "error");
            return;
        }

        EdnaiWeb.setLoading(btnEdnai, true, "Analisando...");
        EdnaiWeb.setMessage(mensagem, "");

        try {
            const result = await EdnaiWeb.apiRequest(`/api/partidas/${state.partidaId}/ednai/chat`, {
                method: "POST",
                headers: {
                    "X-Partida-Token": state.token,
                },
                body: JSON.stringify({
                    message,
                }),
            });
            ednaiResposta.textContent = result.resposta || "Ednai não retornou uma resposta agora.";
            perguntaEdnai.value = "";
        } catch (error) {
            EdnaiWeb.setMessage(
                mensagem,
                `${error.message} Tente perguntar novamente em alguns instantes.`,
                "error",
            );
        } finally {
            EdnaiWeb.setLoading(btnEdnai, false);
        }
    });

    loadResult();
});
