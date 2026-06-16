from flask import Flask, render_template, request, redirect, url_for, flash, session
from core.database import Database
from models.cliente import Cliente 
from models.fornecedor import Fornecedor
from models.funcionario import Funcionario
from models.produto import Produto
from models.pedido import Pedido
from models.estoque import Estoque
from models.pedido_entrada import PedidoEntrada
from models.pedido_saida import PedidoSaida

app = Flask(__name__)
app.secret_key = "chave_secreta"


def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

# --- LOGIN ---
@app.route("/")
def index():
    return render_template("tela_login.html")

# --- ROTAS E FUNÇÕES LOGIN ---
def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def get_usuario_form():
    return {
        "email": request.form.get("email", "").strip(),
        "senha": request.form.get("senha", "").strip(),
    }
    
@app.route("/login_auth", methods=['POST'])
def login_auth():
    email = request.form.get('email')
    senha = request.form.get('password')

    usuario = Funcionario.autenticar(email, senha)

    if usuario:
        flash("Login realizado com sucesso!", "sucesso")
        return redirect(url_for('dashboard'))
    else:
        flash("Email ou senha inválidos", "erro")
        return redirect(url_for('index'))



# --- DASHBOARD ---
@app.route('/dashboard')
def dashboard():
    lista_clientes = Cliente.find_all()
    lista_produtos = Produto.find_all()
    lista_fornecedores = Fornecedor.find_all()
    lista_funcionarios = Funcionario.find_all()

    # Envia tudo para o HTML
    return render_template(
        'dashboard.html', 
        clientes=lista_clientes, 
        produtos=lista_produtos, 
        fornecedores=lista_fornecedores, 
        funcionarios=lista_funcionarios,
    )


# --- MEU PERFIL ---
@app.route("/perfil")
def perfil():
    return render_template("perfil.html")


# --- ROTAS DE CLIENTE ---
def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def get_cliente_form():
    return {
        "nome": request.form.get("nome", "").strip(),
        "cnpj": request.form.get("cnpj", "").strip(),
        "e_mail": request.form.get("e_mail", "").strip(),
        "endereco": request.form.get("endereco", "").strip(),
        "telefone": request.form.get("telefone", "").strip(),
    }


@app.route('/clientes')
def listar_clientes():
    lista = Cliente.find_all() 
    return render_template("lista.html", clientes=lista)


@app.route("/cliente/novo")
def novo_cliente():
    return render_template("formulario_cliente.html", cliente=None)


@app.route('/cliente/salvar', methods=['POST'])
def salvar_cliente():
        dados = get_cliente_form()
        novo_cliente = Cliente(**dados) 
        erros = novo_cliente.validate()
        novo_cliente.insert()
        return redirect(url_for('listar_clientes'))

@app.route("/cliente/excluir/<int:id>", methods=["GET", "POST"]) # Adicionado GET para o link funcionar
def excluir_cliente(id):
    try:
        Cliente.safe_delete(id) 
        flash("Cliente excluído com sucesso.", "sucesso")
    except Exception as e:
        flash(f"Erro ao excluir cliente: {e}", "erro")
    return redirect(url_for("listar_clientes"))


# --- ROTAS DE FORNECEDORES ---
@app.route('/fornecedores')
def fornecedores():
    # Busca a lista para a tabela abaixo do formulário
    dados = Fornecedor.find_all() 
    return render_template("formulario_fornecedor.html", fornecedores=dados, fornecedor=None)

@app.route('/fornecedores/editar/<int:fornecedor_id>')
def editar_fornecedor(fornecedor_id):
    f = Fornecedor.find_by_id(fornecedor_id)
    dados = Fornecedor.find_all()
    return render_template("formulario_fornecedor.html", fornecedores=dados, fornecedor=f)

@app.route("/api/fornecedor/<int:fornecedor_id>", methods=['POST'])
def api_fornecedor(fornecedor_id):
    nome = request.form.get('nome')
    cnpj = request.form.get('CNPJ') or request.form.get('cnpj') 
    email = request.form.get('e_mail')
    telefone = request.form.get('telefone')
    endereco = request.form.get('endereco')


    if not cnpj or not cnpj.strip():
        flash("O campo CNPJ é obrigatório!", "erro")
        return redirect(url_for('fornecedores'))

    f = Fornecedor(nome=nome, cnpj=cnpj, e_mail=email, telefone=telefone, endereco=endereco)

    if fornecedor_id == 0:
        f.insert() # Novo cadastro
        flash("Fornecedor cadastrado com sucesso!", "success")
    else:
        f.update(fornecedor_id) # Atualiza existente
        flash("Fornecedor atualizado com sucesso!", "success")

    return redirect(url_for('fornecedores'))

@app.route("/fornecedores/excluir/<int:id>", methods=["GET", "POST"]) # Adicionado GET para o link funcionar
def excluir_fornecedor(id):
    try:
        Fornecedor.safe_delete(id) 
        flash("Fornecedor excluído com sucesso.", "sucesso")
    except Exception as e:
        flash(f"Erro ao excluir fornecedor: {e}", "erro")
    return redirect(url_for("fornecedores"))


# --- ROTAS DE FUNCIONÁRIOS ---
def get_funcionario_form():
    return {
        "nome": request.form.get("nome"),
        "CPF": request.form.get("CPF"),
        "e_mail": request.form.get("e_mail"),
        "setor": request.form.get("setor"),
        "cargo": request.form.get("cargo"),
        "salario": request.form.get("salario"),
        "turno": request.form.get("turno"),
        "senha": request.form.get("senha"),
        "telefone": request.form.get("telefone"),
        "data_nascimento": request.form.get("data_nascimento"),
    }
    
@app.route("/funcionarios")
def funcionarios():
    return render_template("formulario_funcionario.html")

@app.route("/funcionario/salvar", methods=["POST"])
def salvar_funcionario():
    dados = get_funcionario_form()
    funcionario = Funcionario(**dados)

    try:
        funcionario.insert()
        flash("Funcionário cadastrado com sucesso!", "sucesso")
        return redirect(url_for("funcionarios"))
    except Exception as e:
        flash(f"Erro ao cadastrar: {e}", "erro")
        return redirect(url_for("funcionarios"))


# --- ROTAS DE PEDIDOS ---
@app.route("/pedidos")
def menu_pedidos():
    return render_template("escolha_movimentacao.html")


@app.route("/direcionar_movimentacao", methods=["POST"])
def direcionar_movimentacao():
    tipo = request.form.get("tipo_movimentacao")
    
    if tipo == "entrada":
        return redirect(url_for("nova_entrada"))
    elif tipo == "saida":
        return redirect(url_for("nova_saida")) 
        
    return redirect(url_for("menu_pedidos"))


# --- entrada  ---
@app.route("/pedidos/nova-entrada")
def nova_entrada():
    todos_fornecedores = Fornecedor.find_all() or []
    todos_produtos = Produto.find_all() or []
    todos_funcionarios = Funcionario.find_all() or [] 
    historico_entradas = PedidoEntrada.find_all() or [] 

    return render_template(
        "nova_entrada.html", 
        fornecedores=todos_fornecedores,
        produtos=todos_produtos,
        funcionarios=todos_funcionarios,
        pedido_entrada=historico_entradas
    )

@app.route("/salvar_movimentacao_entrada", methods=["POST"])
def salvar_movimentacao_entrada():
    try:
        # Captura os dados enviados pela tag <form> que você construiu
        dados_movimentacao = {
            "fornecedor_id": to_int(request.form.get("fornecedor_id")),
            "data_entrada": request.form.get("data"),
            "status_pedido": request.form.get("status_pedido"),
            "descricao": request.form.get("descricao", "").strip(),
            "estoque_id": to_int(request.form.get("estoque_id")),
            "funcionario_id": to_int(request.form.get("funcionario_id"))
        }

        novo_entrada = PedidoEntrada(**dados_movimentacao)
        novo_entrada.insert()

        flash("Movimentação de entrada salva com sucesso!", "sucesso")
        return redirect(url_for("nova_entrada"))

    except Exception as e:
        flash(f"Erro ao salvar movimentação de entrada: {e}", "erro")
        return redirect(url_for("nova_entrada"))

# ---  saída  ---
@app.route("/pedidos/nova-saida")
def nova_saida():
    todos_clientes = Cliente.find_all() or []
    todos_produtos = Produto.find_all() or []
    todos_funcionarios = Funcionario.find_all() or [] 
    historico_saidas = PedidoSaida.find_all() or [] 
    todos_estoques = Estoque.find_all() or []

    return render_template(
        "nova_saida.html", 
        cliente=todos_clientes,
        produtos=todos_produtos,
        funcionarios=todos_funcionarios,
        pedido_saida=historico_saidas,
        estoques=todos_estoques        
    )

@app.route("/salvar_movimentacao_saida", methods=["POST"])
def salvar_movimentacao_saida():
    try:
        data_hora = request.form.get("data")  

        dados_movimentacao = {
            "data_hora": data_hora,
            "cliente_id": to_int(request.form.get("cliente_id")), 
            "status_pedido": request.form.get("status_pedido", "").strip(),
            "descricao": request.form.get("descricao", "").strip(),
            "estoque_id": to_int(request.form.get("estoque_id")),
            "funcionario_id": to_int(request.form.get("funcionario_id"))
        }

        nova_saida = PedidoSaida(**dados_movimentacao)
        nova_saida.insert()

        flash("Movimentação de saída processada com sucesso!", "sucesso")
        return redirect(url_for("nova_saida"))

    except Exception as e:
        flash(f"Erro ao salvar movimentação de saída: {e}", "erro")
        return redirect(url_for("nova_saida"))



# --- ROTAS ESTOQUE ---
@app.route('/estoque')
def estoque():
    produtos = []
    lote = request.args.get('lote_busca', '').strip()
    
    if lote:
        resultado_busca = Produto.find_by_field('lote', lote)

        if not resultado_busca:
            flash("Lote não encontrado!", "warning")
        elif isinstance(resultado_busca, dict):
            produtos = [resultado_busca]
        elif isinstance(resultado_busca, list):
            produtos = resultado_busca
    else:
        todos_dados = Produto.find_all()
        if todos_dados:
            produtos = todos_dados

    return render_template("estoque.html", produtos=produtos)

@app.route('/movimentar_estoque', methods=['POST'])
def movimentar_estoque():
    produto_id = request.form.get('produto_id')
    quantidade_mov = int(request.form.get('quantidade_movimentada', 0))
    acao = request.form.get('acao')
    lote_informado = request.form.get('lote', '').strip()

    dados = Produto.find_by_id(produto_id)
    if not dados:
        return "Produto não encontrado", 404

    if acao == 'saida' and dados ['quantidade'] < quantidade_mov:
        flash("Estoque insuficiente!", "danger")
        return redirect(url_for('estoque'))

    p = Produto()
    for campo in p.fields:
        setattr(p, campo, dados.get(campo))

    if acao == 'entrada':
        p.quantidade += quantidade_mov
    elif acao == 'saida':
        p.quantidade -= quantidade_mov
    p.update(produto_id)

    novo_movimento = Estoque(
        quantidade=quantidade_mov,
        produto_id=produto_id,
        lote=lote_informado
    )
    novo_movimento.insert()
    
    flash("Estoque atualizado com sucesso!", "success")
    return redirect(url_for('estoque', lote_busca=dados['lote']))


# --- ROTAS DE PRODUTOS ---
@app.route('/produtos')
def listar_produtos():
    produtos = Produto.find_all() 
    return render_template('formulario_produto.html', produtos=produtos)

@app.route('/cadastro_produto', methods=['GET', 'POST']) 
def cadastro_produto():
    if request.method == 'POST':
        # coleta os dados
        novo_produto = Produto(
            nome=request.form.get('nome'),
            categoria=request.form.get('categoria'),
            tipo_produto=request.form.get('tipo_produto'),
            estoque_minimo=request.form.get('estoque_minimo'),
            validade=request.form.get('validade'),
            lote=request.form.get('lote'),
            localizacao=request.form.get('localizacao'),
            RFID=request.form.get('RFID'),
            descricao=request.form.get('descricao'),
            fornecedor=request.form.get('fornecedor')
        )
        
        return redirect(url_for('listar_produtos'))
    return render_template('formulario_produto.html')


@app.route('/produto/salvar', methods=['POST'])
def salvar_produto():
    try:
        nome = request.form.get("nome")
        categoria = request.form.get("categoria")
        tipo_produto = request.form.get("tipo_produto")
        estoque_minimo = request.form.get("estoque_minimo", 0)
        validade = request.form.get("validade")
        lote = request.form.get("lote")
        localizacao = request.form.get("localizacao")
        rfid = request.form.get("RFID")
        descricao = request.form.get("descricao", "Sem descrição")
        fornecedor = request.form.get("fornecedor", "Não informado")

        novo_produto = Produto(
            nome=nome,
            categoria=categoria,
            tipo_produto=tipo_produto,
            estoque_minimo=estoque_minimo,
            validade=validade,
            lote=lote,
            localizacao=localizacao,
            RFID=rfid,
            descricao=descricao,
            fornecedor=fornecedor
        )

        erros = novo_produto.validate()
        if erros:
            for erro in erros:
                flash(erro, "erro")
            return redirect(url_for('listar_produtos'))

        novo_produto.insert()
        
        flash("Produto cadastrado no estoque com sucesso!", "sucesso")
    except Exception as e:
        flash(f"Erro ao cadastrar: {e}", "erro")
        print(f"Erro técnico: {e}")

    return redirect(url_for('listar_produtos'))

@app.route("/produto/excluir/<int:produto_id>", methods=["GET", "POST"]) # Adicionado GET para o link funcionar
def excluir_produto(produto_id):
    try:
        # garda o produto encontrado dentro da variável 'produto'
        produto = Produto.find_by_id(produto_id) 
        
        if produto:
            produto.delete()  
            flash("Produto excluído com sucesso.", "sucesso")
        else:
            flash("Produto não encontrado.", "erro")
    except Exception as e:
        flash(f"Erro ao excluir produto: {e}", "erro")
    return redirect(url_for('estoque'))



if __name__ == "__main__":
    app.run(debug=True)
