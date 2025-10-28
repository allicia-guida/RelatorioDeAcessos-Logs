from flask import Flask, render_template, request
import csv
from collections import Counter, defaultdict

app = Flask(__name__)

# -----------------------------
# FUNÇÃO PARA LER O CSV
# -----------------------------
def ler_csv():
    dados = []
    try:
        with open('logins.csv', newline='', encoding='utf-8') as csvfile:
            leitor = csv.DictReader(csvfile)
            for linha in leitor:
                dados.append(linha)
    except FileNotFoundError:
        print("⚠️ Arquivo logins.csv não encontrado!")
    return dados


# -----------------------------
# FUNÇÕES DO HTML
# -----------------------------
def ordenar(dados, coluna):
    """Ordena os dados pela coluna escolhida"""
    return sorted(dados, key=lambda x: x[coluna])


def buscar(dados, coluna, valor):
    """Filtra os dados conforme o valor buscado"""
    return [linha for linha in dados if valor.lower() in linha[coluna].lower()]


def gerar_relatorio(dados):
    """Gera relatório com hora mais e menos acessadas + nomes"""
    if not dados:
        return None

    contagem_horas = Counter(linha['Hora'].split(':')[0] for linha in dados)

    hora_mais = contagem_horas.most_common(1)[0]
    hora_menos = contagem_horas.most_common()[-1]

    nomes_por_hora = defaultdict(list)
    for linha in dados:
        hora = linha['Hora'].split(':')[0]
        nomes_por_hora[hora].append(linha['Nome'])

    return {
        "hora_mais": {
            "hora": hora_mais[0],
            "qtd": hora_mais[1],
            "nomes": nomes_por_hora[hora_mais[0]]
        },
        "hora_menos": {
            "hora": hora_menos[0],
            "qtd": hora_menos[1],
            "nomes": nomes_por_hora[hora_menos[0]]
        }
    }


# -----------------------------
# ROTA PRINCIPAL
# -----------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    dados = ler_csv()
    relatorio = None

    # Ordenação
    ordenar_coluna = request.form.get('ordenar')
    if ordenar_coluna:
        dados = ordenar(dados, ordenar_coluna)

    # Busca
    busca_valor = request.form.get('buscar')
    if busca_valor:
        dados = buscar(dados, 'Nome', busca_valor)

    # Gera relatório com base nos dados filtrados
    relatorio = gerar_relatorio(dados)

    return render_template('index.html', dados=dados, relatorio=relatorio)


# -----------------------------
# EXECUÇÃO
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
