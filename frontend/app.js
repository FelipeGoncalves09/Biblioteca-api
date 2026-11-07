// Código compartilhado por todas as páginas.

const API = "http://127.0.0.1:8000";

/* ---------- Sessão ---------- */
function getToken() {
    return localStorage.getItem("token");
}

function sair() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

function exigirLogin() {
    if (getToken() === null) {
        window.location.href = "login.html";
    }
}

/* ---------- Chamadas à API ---------- */
// Devolve sempre { ok, status, dados }, nunca estoura erro.
async function chamarApi(caminho, opcoes = {}) {
    const headers = { ...(opcoes.headers || {}) };
    const token = getToken();

    if (token) {
        headers["Authorization"] = "Bearer " + token;
    }
    if (opcoes.body) {
        headers["Content-Type"] = "application/json";
    }

    let resposta;
    try {
        resposta = await fetch(API + caminho, { ...opcoes, headers });
    } catch (erro) {
        return { ok: false, status: 0, dados: { detail: "Não foi possível conectar à API. Ela está rodando?" } };
    }

    let dados = null;
    try {
        dados = await resposta.json();
    } catch (erro) {
        // resposta sem corpo JSON
    }

    if (resposta.status === 401 && token) {
        sair();
    }

    return { ok: resposta.ok, status: resposta.status, dados: dados };
}

function textoErro(dados) {
    if (dados && typeof dados.detail === "string") {
        return dados.detail;
    }
    if (dados && Array.isArray(dados.detail)) {
        return "Dados inválidos. Confira os campos.";
    }
    return "Algo deu errado. Tente de novo.";
}

/* ---------- Interface ---------- */
function mostrarMensagem(elemento, texto, tipo) {
    elemento.textContent = texto;
    elemento.className = "mensagem " + tipo;
}

function limparMensagem(elemento) {
    elemento.textContent = "";
    elemento.className = "mensagem";
}

function formatarData(texto) {
    if (!texto) {
        return "—";
    }
    return new Date(texto).toLocaleDateString("pt-BR");
}

function diasAte(texto) {
    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);
    const alvo = new Date(texto);
    alvo.setHours(0, 0, 0, 0);
    return Math.round((alvo - hoje) / 86400000);
}

// Menu do topo. "ativo" é o nome da página atual: "acervo", "meus" ou "admin".
function montarMenu(ativo) {
    const menu = document.getElementById("menu");
    if (!menu) {
        return;
    }
    const itens = [
        ["Livros", "Livros", "livros.html"],
        ["meus", "Meus empréstimos", "meus.html"],
        ["admin", "Administração", "admin.html"]
    ];
    let links = "";
    for (const [chave, texto, destino] of itens) {
        links += '<a href="' + destino + '"' + (chave === ativo ? ' class="ativo" aria-current="page"' : "") + ">" + texto + "</a>";
    }
    menu.className = "menu";
    menu.innerHTML =
        '<a class="marca" href="livros.html">Biblioteca <span>comunitária</span></a>' +
        "<nav>" + links + '<button type="button" class="botao-sair" id="botaoSair">Sair</button></nav>';
    document.getElementById("botaoSair").addEventListener("click", sair);
}

/* ---------- Lombadas ---------- */
const CORES_LOMBADA = [
    { fundo: "#7A1F2B", texto: "#F6E9E4" },
    { fundo: "#1F4D3A", texto: "#E5F0E8" },
    { fundo: "#1E3A5F", texto: "#E4ECF6" },
    { fundo: "#5B2A63", texto: "#F1E6F4" },
    { fundo: "#B5532A", texto: "#FCEBDD" },
    { fundo: "#2F6F73", texto: "#E3F3F3" },
    { fundo: "#C58B1A", texto: "#2A1D05" },
    { fundo: "#3A3F44", texto: "#ECEFF1" }
];

function hashTexto(texto) {
    let h = 0;
    for (let i = 0; i < texto.length; i++) {
        h = (h * 31 + texto.charCodeAt(i)) >>> 0;
    }
    return h;
}

// Cor, largura e altura da lombada ficam sempre iguais para o mesmo livro.
function estiloLombada(livro) {
    const h = hashTexto(livro.name + livro.author);
    const cor = CORES_LOMBADA[h % CORES_LOMBADA.length];
    return {
        fundo: cor.fundo,
        texto: cor.texto,
        largura: 46 + (h >> 3) % 26,
        altura: 196 + (h >> 7) % 64
    };
}