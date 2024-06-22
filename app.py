from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

produtos = []

@app.route('/')
def index():
    """
    Redireciona para a rota de listagem de produtos.
    """
    return redirect(url_for('listagem'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """
    Exibe o formulário de cadastro de produtos e processa os dados submetidos.

    Retorna:
        - Template 'cadastro.html' caso o método seja GET.
        - Redirecionamento para a rota de listagem ('/listagem') com o parâmetro 'cadastrado=True' caso o método seja POST e os dados sejam válidos.
        - Redirecionamento para a rota de cadastro ('/cadastro') caso o método seja POST e os dados sejam inválidos.
    """
    if request.method == 'GET':
        return render_template('cadastro.html')

    nome = request.form.get('nome')
    descricao = request.form.get('descrição')

    try:
        valor = float(request.form.get('valor'))
    except ValueError:
        
        return redirect(url_for('cadastro'))

    disponivel = request.form.get('disponivel') == 'sim'

    novo_produto = {
        'nome': nome,
        'descrição': descricao,
        'valor': valor,
        'disponível': disponivel
    }

    produtos.append(novo_produto)

    return redirect(url_for('listagem', cadastrado=True))

@app.route('/listagem')
def listagem():
    """
    Exibe a lista de produtos ordenados por valor do menor para o maior.

    Retorna:
        - Template 'listagem.html' com a lista de produtos ordenados.
    """
    if request.method == 'GET' and request.args.get('cadastrado'):
        return redirect(url_for('listagem'))

    produtos_ordenados = sorted(produtos, key=lambda x: x['valor'])
    return render_template('listagem.html', produtos=produtos_ordenados)

if __name__ == "__main__":
    app.run(debug=True)
