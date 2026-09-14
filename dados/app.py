from flask import Flask, render_template
import pandas as pd
import json

app = Flask(__name__)

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
    app.run(host="0.0.0.0", debug=True, port=8080)
