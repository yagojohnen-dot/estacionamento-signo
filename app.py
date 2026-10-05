from flask import Flask, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

BANCO = "signos.db"


# =========================
# BANCO DE DADOS
# =========================

def conectar_banco():
    conexao = sqlite3.connect(BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_banco():
    conexao = conectar_banco()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            dia INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            signo TEXT NOT NULL,
            data_consulta TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


# =========================
# DESCOBRIR SIGNO
# =========================

def descobrir_signo(dia, mes):

    if (mes == 3 and dia >= 21) or (mes == 4 and dia <= 19):
        return "Áries", "♈", "Corajoso, determinado e cheio de energia."

    elif (mes == 4 and dia >= 20) or (mes == 5 and dia <= 20):
        return "Touro", "♉", "Paciente, confiável e determinado."

    elif (mes == 5 and dia >= 21) or (mes == 6 and dia <= 20):
        return "Gêmeos", "♊", "Comunicativo, curioso e inteligente."

    elif (mes == 6 and dia >= 21) or (mes == 7 and dia <= 22):
        return "Câncer", "♋", "Sensível, protetor e ligado à família."

    elif (mes == 7 and dia >= 23) or (mes == 8 and dia <= 22):
        return "Leão", "♌", "Confiante, criativo e cheio de personalidade."

    elif (mes == 8 and dia >= 23) or (mes == 9 and dia <= 22):
        return "Virgem", "♍", "Organizado, inteligente e observador."

    elif (mes == 9 and dia >= 23) or (mes == 10 and dia <= 22):
        return "Libra", "♎", "Sociável, equilibrado e diplomático."

    elif (mes == 10 and dia >= 23) or (mes == 11 and dia <= 21):
        return "Escorpião", "♏", "Intenso, misterioso e determinado."

    elif (mes == 11 and dia >= 22) or (mes == 12 and dia <= 21):
        return "Sagitário", "♐", "Aventureiro, otimista e independente."

    elif (mes == 12 and dia >= 22) or (mes == 1 and dia <= 19):
        return "Capricórnio", "♑", "Responsável, ambicioso e disciplinado."

    elif (mes == 1 and dia >= 20) or (mes == 2 and dia <= 18):
        return "Aquário", "♒", "Criativo, independente e original."

    elif (mes == 2 and dia >= 19) or (mes == 3 and dia <= 20):
        return "Peixes", "♓", "Sensível, intuitivo e imaginativo."

    return None, None, None


# =========================
# CSS DO SITE
# =========================

CSS = """
<style>

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    min-height: 100vh;
    color: white;
    background:
        radial-gradient(circle at top, #30136d, #100620 60%, #05010b);
}

header {
    height: 75px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 8%;
    background: rgba(8, 3, 20, 0.8);
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.logo {
    font-size: 24px;
    font-weight: bold;
    color: #c48cff;
}

nav a {
    color: white;
    text-decoration: none;
    margin-left: 20px;
}

nav a:hover {
    color: #c48cff;
}

main {
    width: 90%;
    max-width: 1000px;
    margin: auto;
}

.hero {
    text-align: center;
    padding: 70px 20px 30px;
}

.hero h1 {
    font-size: 52px;
    margin-bottom: 15px;
}

.hero span {
    color: #bf83ff;
}

.hero p {
    color: #bbb3c7;
    font-size: 18px;
}

.card {
    width: 100%;
    max-width: 620px;
    margin: 20px auto 60px;
    padding: 35px;
    border-radius: 24px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 20px 70px rgba(0,0,0,0.4);
}

.card h2 {
    text-align: center;
    margin-bottom: 25px;
}

label {
    display: block;
    margin-bottom: 7px;
    color: #d0cad8;
}

input,
select {
    width: 100%;
    padding: 15px;
    margin-bottom: 18px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.15);
    background: rgba(255,255,255,0.07);
    color: white;
    outline: none;
    font-size: 16px;
}

select option {
    color: black;
}

.linha {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

button,
.botao {
    display: block;
    width: 100%;
    border: 0;
    padding: 16px;
    border-radius: 12px;
    cursor: pointer;
    color: white;
    font-size: 16px;
    font-weight: bold;
    text-decoration: none;
    text-align: center;
    background: linear-gradient(90deg, #8d4df0, #574cf0);
}

button:hover,
.botao:hover {
    transform: translateY(-2px);
}

.resultado {
    margin-top: 30px;
    padding: 30px;
    text-align: center;
    border-radius: 18px;
    background: rgba(140, 80, 255, 0.12);
}

.simbolo {
    font-size: 70px;
    color: #cf9cff;
}

.resultado h2 {
    color: #c78cff;
    font-size: 35px;
}

.erro {
    margin-top: 20px;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    background: rgba(255, 50, 50, 0.15);
    color: #ff9a9a;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th,
td {
    padding: 14px 10px;
    text-align: left;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

th {
    color: #c69aff;
}

.excluir {
    color: #ff7288;
    text-decoration: none;
}

.acoes {
    margin-bottom: 20px;
    display: flex;
    justify-content: flex-end;
}

.limpar {
    background: #b73852;
    color: white;
    padding: 10px 16px;
    border-radius: 8px;
    text-decoration: none;
}

.vazio {
    padding: 50px 20px;
    text-align: center;
}

footer {
    text-align: center;
    padding: 30px;
    color: #7e7788;
}

@media(max-width: 650px) {

    .hero h1 {
        font-size: 38px;
    }

    .linha {
        grid-template-columns: 1fr;
        gap: 0;
    }

    header {
        padding: 0 20px;
    }
}

</style>
"""


# =========================
# PÁGINA PRINCIPAL
# =========================

@app.route("/", methods=["GET", "POST"])
def inicio():

    resultado_html = ""
    erro_html = ""

    if request.method == "POST":

        nome = request.form.get("nome", "").strip()
        dia = request.form.get("dia", "")
        mes = request.form.get("mes", "")

        if not nome or not dia or not mes:

            erro_html = """
            <div class="erro">
                Preencha todos os campos.
            </div>
            """

        else:

            try:

                dia = int(dia)
                mes = int(mes)

                # valida a data
                datetime(2000, mes, dia)

                signo, simbolo, descricao = descobrir_signo(dia, mes)

                if signo:

                    data_consulta = datetime.now().strftime(
                        "%d/%m/%Y %H:%M:%S"
                    )

                    conexao = conectar_banco()

                    conexao.execute("""
                        INSERT INTO consultas
                        (nome, dia, mes, signo, data_consulta)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        nome,
                        dia,
                        mes,
                        signo,
                        data_consulta
                    ))

                    conexao.commit()
                    conexao.close()

                    resultado_html = f"""
                    <div class="resultado">

                        <div class="simbolo">
                            {simbolo}
                        </div>

                        <p>
                            {nome}, seu signo é
                        </p>

                        <h2>
                            {signo}
                        </h2>

                        <p>
                            {descricao}
                        </p>

                    </div>
                    """

            except ValueError:

                erro_html = """
                <div class="erro">
                    Digite uma data válida.
                </div>
                """


    return f"""
    <!DOCTYPE html>

    <html lang="pt-BR">

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <title>
            AstroSignos
        </title>

        {CSS}

    </head>


    <body>

        <header>

            <div class="logo">
                ✦ AstroSignos
            </div>

            <nav>

                <a href="/">
                    Descobrir
                </a>

                <a href="/historico">
                    Histórico
                </a>

            </nav>

        </header>


        <main>

            <section class="hero">

                <h1>
                    Descubra seu
                    <span>Signo</span>
                </h1>

                <p>
                    Informe seu nome e sua data de nascimento.
                </p>

            </section>


            <section class="card">

                <h2>
                    🔮 Qual é o seu signo?
                </h2>


                <form method="POST">

                    <label>
                        Seu nome
                    </label>

                    <input
                        type="text"
                        name="nome"
                        placeholder="Digite seu nome"
                        required
                    >


                    <div class="linha">

                        <div>

                            <label>
                                Dia
                            </label>

                            <input
                                type="number"
                                name="dia"
                                min="1"
                                max="31"
                                placeholder="Dia"
                                required
                            >

                        </div>


                        <div>

                            <label>
                                Mês
                            </label>

                            <select
                                name="mes"
                                required
                            >

                                <option value="">
                                    Escolha
                                </option>

                                <option value="1">
                                    Janeiro
                                </option>

                                <option value="2">
                                    Fevereiro
                                </option>

                                <option value="3">
                                    Março
                                </option>

                                <option value="4">
                                    Abril
                                </option>

                                <option value="5">
                                    Maio
                                </option>

                                <option value="6">
                                    Junho
                                </option>

                                <option value="7">
                                    Julho
                                </option>

                                <option value="8">
                                    Agosto
                                </option>

                                <option value="9">
                                    Setembro
                                </option>

                                <option value="10">
                                    Outubro
                                </option>

                                <option value="11">
                                    Novembro
                                </option>

                                <option value="12">
                                    Dezembro
                                </option>

                            </select>

                        </div>

                    </div>


                    <button type="submit">

                        ✨ Descobrir meu signo

                    </button>

                </form>


                {erro_html}

                {resultado_html}

            </section>

        </main>


        <footer>

            Python + Flask + SQLite

        </footer>

    </body>

    </html>
    """


# =========================
# HISTÓRICO
# =========================

@app.route("/historico")
def historico():

    conexao = conectar_banco()

    consultas = conexao.execute("""
        SELECT *
        FROM consultas
        ORDER BY id DESC
    """).fetchall()

    conexao.close()

    linhas = ""

    for consulta in consultas:

        linhas += f"""
        <tr>

            <td>
                {consulta['id']}
            </td>

            <td>
                {consulta['nome']}
            </td>

            <td>
                {consulta['dia']:02d}/{consulta['mes']:02d}
            </td>

            <td>
                {consulta['signo']}
            </td>

            <td>
                {consulta['data_consulta']}
            </td>

            <td>

                <a
                    class="excluir"
                    href="/excluir/{consulta['id']}"
                >
                    Excluir
                </a>

            </td>

        </tr>
        """


    if not consultas:

        conteudo = """
        <div class="vazio">

            <h2>
                🔮 Nenhuma consulta encontrada
            </h2>

            <br>

            <a
                href="/"
                class="botao"
            >
                Descobrir meu signo
            </a>

        </div>
        """

    else:

        conteudo = f"""

        <div class="acoes">

            <a
                href="/limpar"
                class="limpar"
                onclick="return confirm('Deseja apagar todo o histórico?')"
            >
                Limpar histórico
            </a>

        </div>


        <div style="overflow-x:auto">

            <table>

                <thead>

                    <tr>

                        <th>ID</th>
                        <th>Nome</th>
                        <th>Nascimento</th>
                        <th>Signo</th>
                        <th>Data</th>
                        <th>Ação</th>

                    </tr>

                </thead>


                <tbody>

                    {linhas}

                </tbody>

            </table>

        </div>
        """


    return f"""

    <!DOCTYPE html>

    <html lang="pt-BR">

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <title>
            Histórico
        </title>

        {CSS}

    </head>


    <body>

        <header>

            <div class="logo">
                ✦ AstroSignos
            </div>

            <nav>

                <a href="/">
                    Descobrir
                </a>

                <a href="/historico">
                    Histórico
                </a>

            </nav>

        </header>


        <main>

            <section class="hero">

                <h1>
                    Histórico de
                    <span>Consultas</span>
                </h1>

                <p>
                    Dados salvos no banco SQLite.
                </p>

            </section>


            <section
                class="card"
                style="max-width:1000px"
            >

                {conteudo}

            </section>

        </main>

    </body>

    </html>
    """


# =========================
# EXCLUIR REGISTRO
# =========================

@app.route("/excluir/<int:id>")
def excluir(id):

    conexao = conectar_banco()

    conexao.execute(
        "DELETE FROM consultas WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect("/historico")


# =========================
# LIMPAR HISTÓRICO
# =========================

@app.route("/limpar")
def limpar():

    conexao = conectar_banco()

    conexao.execute(
        "DELETE FROM consultas"
    )

    conexao.commit()
    conexao.close()

    return redirect("/historico")


# =========================
# INICIAR PROGRAMA
# =========================

if __name__ == "__main__":

    criar_banco()

    print("")
    print("======================================")
    print("        ASTROSIGNOS")
    print("======================================")
    print("")
    print("Abra no navegador:")
    print("")
    print("http://127.0.0.1:5000")
    print("")

    app.run(debug=True)