document.addEventListener("DOMContentLoaded", () => {
    const lista = document.querySelector("#ranking-lista");
    const mensagem = document.querySelector("#mensagem");

    function positionLabel(position) {
        if (position === 1) {
            return "🥇 #1";
        }
        if (position === 2) {
            return "🥈 #2";
        }
        if (position === 3) {
            return "🥉 #3";
        }
        return `#${position}`;
    }

    function renderRanking(items) {
        lista.textContent = "";
        if (!items.length) {
            EdnaiWeb.setMessage(mensagem, "Ainda não há partidas finalizadas no ranking.", "info");
            return;
        }

        items.forEach((item, index) => {
            const position = index + 1;
            const row = document.createElement("div");
            row.className = `ranking-row top-${position}`;
            row.setAttribute("role", "listitem");

            const pos = document.createElement("strong");
            pos.textContent = positionLabel(position);

            const name = document.createElement("span");
            name.textContent = item.nome || "Sem nome";

            const score = document.createElement("strong");
            const tempo = item.tempo ? ` • ${Number(item.tempo)}s` : "";
            score.textContent = `${item.pontos || "0/0"}${tempo}`;

            row.append(pos, name, score);
            lista.appendChild(row);
        });
    }

    async function loadRanking() {
        EdnaiWeb.setMessage(mensagem, "Carregando ranking...", "info");
        try {
            const ranking = await EdnaiWeb.apiRequest("/api/ranking?limite=10");
            renderRanking(Array.isArray(ranking) ? ranking : []);
            if (Array.isArray(ranking) && ranking.length) {
                EdnaiWeb.setMessage(mensagem, "");
            }
        } catch (error) {
            EdnaiWeb.setMessage(
                mensagem,
                `${error.message} Não foi possível carregar o ranking agora.`,
                "error",
            );
        }
    }

    loadRanking();
});
