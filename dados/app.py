from flask import Flask, render_template
import pandas as pd
import os

try:
    from neo4j import GraphDatabase  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover - optional dependency in local/dev setups
    GraphDatabase = None

app = Flask(__name__)

NEO4J_INSTANCE_ID = "27da46a5"
NEO4J_URI = os.environ.get("NEO4J_URI")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")

neo4j_driver = None
if GraphDatabase is not None and NEO4J_URI and NEO4J_PASSWORD:
    neo4j_driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD),
    )

@app.route("/testar-banco")
def testar_banco():
    if neo4j_driver is None:
        return "Erro: Driver do Neo4j não foi inicializado. Verifique as variáveis de ambiente."
    
    try:
        # Tenta fazer uma consulta super simples para verificar o status
        with neo4j_driver.session() as session:
            resultado = session.run("RETURN 'Conexão com Neo4j estabelecida com sucesso!' AS mensagem")
            mensagem = resultado.single()["mensagem"]
            return f"<h1>{mensagem}</h1>"
    except Exception as e:
        return f"Erro ao conectar: {str(e)}"
    
@app.route("/")
def home():
    titulo_projeto = "SSR (Search System for Recommendations)"
    tecnologias = ["Python", "Neo4j", "Flask", "HTML", "GitHub Codespaces"]
    
    tb_usuarios = pd.read_excel("dados/base/usuarios_filmes_series.xlsx", sheet_name="Usuários")
    html_usuarios = tb_usuarios.to_html(classes="user-table", index=False)
    
    tb_seriesfilmes = pd.read_excel("dados/base/usuarios_filmes_series.xlsx", sheet_name="Filmes e Séries")
    tb_seriesfilmes = tb_seriesfilmes.drop_duplicates(subset=['Tipo'])
    html_seriesfilmes = tb_seriesfilmes.to_html(classes="seriesfilmes-table", index=False)

    tb_eventos = pd.read_excel("dados/base/usuarios_filmes_series.xlsx", sheet_name="Eventos")
    tb_eventos = tb_eventos.drop_duplicates(subset=['Usuário'])
    html_eventos = tb_eventos.to_html(classes="eventstable", index=False)

    return render_template("index.html", 
                           titulo=titulo_projeto, 
                           itens=tecnologias, 
                           usertable=html_usuarios, 
                           seriesfilmes=html_seriesfilmes,
                           eventstable=html_eventos,)


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", debug=True, port=8080)
    finally:
        if neo4j_driver:
            neo4j_driver.close()
