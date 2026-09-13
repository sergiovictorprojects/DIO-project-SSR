from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    titulo_projeto = "SSR (Search System for Recommendations)"
    tecnologias = ["Python", "Neo4j", "Flask", "HTML", "GitHub Codespaces"]
    tabela1 = pd.read_excel("dados/base/usuarios_filmes_series.xlsx")
    tabela_html = tabela1.to_html(classes="user-table", index=False)

    return render_template("index.html", titulo=titulo_projeto, itens=tecnologias, relacaoent=tabela_html)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
