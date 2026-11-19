from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

# importação para conexão com banco
from core.database import Database

# importações das classes
from models.cliente import Cliente 
from models.fornecedor import Fornecedor
from models.funcionario import Funcionario
from models.produto import Produto
from models.pedido import Pedido
from models.estoque import Estoque
from models.pedido_entrada import PedidoEntrada
from models.pedido_saida import PedidoSaida
from models.sensor import Sensor
from models.configuracao import Configuracao

# relatorio 
from datetime import datetime, date
import unicodedata

from chatbot.respostas import gerar_resposta

# limpar nome de arquivos enviados por upload
from werkzeug.utils import secure_filename

# importação para o banco
import mysql.connector

# para validar textos
import re

# para manipular diretórios, caminhos de pastas e salvar arquivos de upload
import os

app = Flask(__name__)
app.secret_key = "chave_secreta"

def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
    
# --- LANDINGPAGE ---
@app.route("/")
def index():
    return render_template("landingPage.html")

# --- LOGIN ---
@app.route("/login")
def login():
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

    funcionario = Funcionario.autenticar(email, senha)

    if funcionario:
        session['funcionario_id'] = funcionario['funcionario_id']
        
        flash("Login realizado com sucesso!", "sucesso")
        return redirect(url_for('dashboard'))
    else:
        flash("Email ou senha inválidos", "erro")
        return redirect(url_for('login')) 


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
@app.route('/perfil')
def perfil():
    funcionario_id = session.get('funcionario_id')
    
    # SEGURANÇA: Se não tiver ninguém logado na sessão, joga para a tela de login
    if not funcionario_id:
        return redirect(url_for('login'))
    
    conexao = obter_conexao()
    cursor = conexao.cursor(dictionary=True) 
    
    try:
        # Usamos fetchone() pois cada ID pertence a apenas um funcionário
        cursor.execute("SELECT nome, e_mail, cargo FROM funcionario WHERE funcionario_id = %s", (funcionario_id,))
        funcionario_dados = cursor.fetchone()

        cursor.execute("SELECT caminho_arquivo FROM fotos_perfil WHERE funcionario_id = %s AND atual = TRUE", (funcionario_id,))
        resultado_foto = cursor.fetchone()
        
        if resultado_foto:
            foto_do_banco = resultado_foto['caminho_arquivo']
        else:
            foto_do_banco = 'imagens/sem-foto.png'

    except mysql.connector.Error as erro:
        print(f"Erro ao buscar dados do perfil: {erro}")
        funcionario_dados = None
        foto_do_banco = 'imagens/sem-foto.png'
        
    finally:
        cursor.close()
        conexao.close()
    
    return render_template('configuracao.html', usuario_foto=foto_do_banco, funcionario=funcionario_dados)

# --- ROTAS IMAGEM DE PERFIL ---
PASTA_FOTOS = 'static/uploads/produtos'

PASTA_UPLOADS = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = PASTA_UPLOADS

# Conexão com o banco
def obter_conexao():
    return mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "123456",
    database = "flowtech"
    )

@app.route('/editar-perfil', methods=['POST'])
def editar_perfil():
    funcionario_id = session.get('funcionario_id')
    telefone = request.form.get('telefone')
    data_nascimento = request.form.get('data_nascimento')
    setor = request.form.get('setor')
    cargo = request.form.get('cargo')
    sobre_mim = request.form.get('sobre_mim')
    
    funcionario_id = session.get('funcionario_id')
    
    # SEGURANÇA: Se não tiver ninguém logado na sessão, joga o usuário para a tela de login
    if not funcionario_id:
        return redirect(url_for('login'))
    
    if 'foto' in request.files:
        arquivo = request.files['foto']
        
        if arquivo and arquivo.filename != '':
            nome_seguro = secure_filename(arquivo.filename)
            nome_final = f"{funcionario_id}_{nome_seguro}"
            
            caminho_salvar = os.path.join(app.config['UPLOAD_FOLDER'], nome_final)
            
            pasta_destino = os.path.dirname(caminho_salvar)
            os.makedirs(pasta_destino, exist_ok=True)
            
            arquivo.save(caminho_salvar)
            
            # Força o uso de barras normais para o navegador conseguir ler no HTML
            caminho_banco = f"uploads/{nome_final}".replace("\\", "/")
            
            conexao = obter_conexao()
            cursor = conexao.cursor()
            
            try:
                cursor.execute("UPDATE fotos_perfil SET atual = FALSE WHERE funcionario_id = %s", (funcionario_id,))
                
                comando_insert = "INSERT INTO fotos_perfil (funcionario_id, caminho_arquivo, atual) VALUES (%s, %s, TRUE)"
                cursor.execute(comando_insert, (funcionario_id, caminho_banco))
                
                conexao.commit()
            except mysql.connector.Error as erro:
                print(f"Erro ao gravar foto no banco: {erro}")
            finally:
                cursor.close()
                conexao.close()

    # Redireciona de volta para a rota de visualização para atualizar a tela
    return redirect(url_for('perfil'))

@app.route('/remover-foto')
def remover_foto():
    funcionario_id = session.get('funcionario_id', 6)
    
    conexao = obter_conexao()
    cursor = conexao.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT caminho_arquivo FROM fotos_perfil WHERE funcionario_id = %s AND atual = TRUE", (funcionario_id,))
        resultado = cursor.fetchone()
        
        if resultado:
            caminho_banco = resultado['caminho_arquivo']
            caminho_computador = os.path.join('static', caminho_banco)
            
            if os.path.exists(caminho_computador):
                os.remove(caminho_computador)
            
            cursor.execute("DELETE FROM fotos_perfil WHERE funcionario_id = %s", (funcionario_id,))
            conexao.commit()
            
    except mysql.connector.Error as erro:
        print(f"Erro ao remover foto do banco: {erro}")
    finally:
        cursor.close()
        conexao.close()
        
    # volta para a imagem de perfil cinza (padrão)
    return redirect(url_for('perfil'))


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
    try:
        dados = get_cliente_form()
        novo_cliente = Cliente(**dados) 
        
        erros = novo_cliente.validate()
        
        if erros:
            for erro in erros:
                flash(erro, "erro")

            return redirect(url_for('listar_clientes')) 

        novo_cliente.insert()
        flash("Cliente cadastrado com sucesso!", "sucesso")
        return redirect(url_for('listar_clientes'))

    except Exception as e:
        flash(f"Não foi possível salvar: Dados inválidos ou incorretos.", "erro")
        return redirect(url_for('listar_clientes'))


@app.route("/cliente/excluir/<int:id>", methods=["GET", "POST"])
def excluir_cliente(id):
    try:
        Cliente.safe_delete(id) 
        flash("Cliente excluído com sucesso.", "sucesso")
    except Exception as e:
        flash(f"Erro ao excluir cliente: {e}", "erro")
    return redirect(url_for('listar_clientes'))


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
    # 1. Pega os dados brutos da tela
    nome = request.form.get('nome')
    cnpj = request.form.get('CNPJ') or request.form.get('cnpj') 
    email = request.form.get('e_mail')
    telefone = request.form.get('telefone')
    endereco = request.form.get('endereco')

    # 2. Limpa as máscaras do CNPJ antes de mandar para o objeto
    if cnpj:
        cnpj = re.sub(r'\D', '', cnpj)

    # 3. Cria a instância do Fornecedor
    f = Fornecedor(nome=nome, cnpj=cnpj, e_mail=email, telefone=telefone, endereco=endereco)

    # 4. DISPARA A VALIDAÇÃO
    erros_validacao = f.validate()

    # 5. SE HOUVER ERROS: Envia os alertas e INTERROMPE o salvamento
    if erros_validacao:
        for erro in erros_validacao:
            flash(erro, "erro") # Envia a mensagem para o HTML
        
        # Redireciona de volta para não executar o código abaixo
        if fornecedor_id > 0:
            return redirect(url_for('editar_fornecedor', fornecedor_id=fornecedor_id))
        return redirect(url_for('fornecedores'))

    # 6. SE NÃO HOUVER ERROS: Atualiza o objeto com os dados formatados e grava no banco
    if fornecedor_id == 0:
        # Se o seu método f.insert() não ler do self.nome atualizado, mude para passar os dados limpos:
        f.insert() 
        flash("Fornecedor cadastrado com sucesso!", "success")
    else:
        f.update(fornecedor_id) 
        flash("Fornecedor atualizado com sucesso!", "success")

    return redirect(url_for('fornecedores'))

@app.route("/fornecedores/excluir/<int:id>", methods=["GET", "POST"]) # Adicionado GET para o link funcionar
def excluir_fornecedor(id):
    try:
        Fornecedor.safe_delete(id) 
        flash("Fornecedor excluído com sucesso.", "sucesso")
    except Exception as e:
        flash(f"Erro ao excluir fornecedor: {e}", "erro")
    return redirect(url_for('fornecedores'))


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
    
@app.route("/api/funcionario/<int:funcionario_id>", methods=['POST'])
def api_funcionario(funcionario_id):
    # Coleta todos os campos da tela
    nome = request.form.get('nome')
    cpf = request.form.get('CPF') or request.form.get('cpf')
    email = request.form.get('e_mail')
    setor = request.form.get('setor')
    cargo = request.form.get('cargo')
    salario = request.form.get('salario')
    turno = request.form.get('turno')
    senha = request.form.get('senha')
    telefone = request.form.get('telefone')
    data_nascimento = request.form.get('data_nascimento')

    # Cria o objeto do funcionário
    f = Funcionario(
        nome=nome, CPF=cpf, e_mail=email, setor=setor, cargo=cargo,
        salario=salario, turno=turno, senha=senha, telefone=telefone, 
        data_nascimento=data_nascimento
    )

    # Dispara a validação integrada
    erros_validacao = f.validate()

    if erros_validacao:
        for erro in erros_validacao:
            flash(erro, "erro")
        
        if funcionario_id > 0:
            return redirect(url_for('editar_funcionario', funcionario_id=funcionario_id))
        return redirect(url_for('funcionarios'))

    # Salva no banco de dados se passar na validação
    try:
        if funcionario_id == 0:
            f.insert()
            flash("Funcionário cadastrado com sucesso!", "success")
        else:
            f.update(funcionario_id)
            flash("Funcionário atualizado com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao salvar no banco de dados: {e}", "erro")

    return redirect(url_for('funcionarios'))



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
      
        dados_movimentacao = {
            "data_hora": request.form.get("data"), 
            "descricao": request.form.get("descricao", "").strip(),
            "status_pedido": request.form.get("status_pedido"),
            "fornecedor_id": to_int(request.form.get("fornecedor_id")),
            "funcionario_id": to_int(request.form.get("funcionario_id")),
            "rfid": request.form.get("rfid"), 
            "estoque_id": to_int(request.form.get("estoque_id")) if request.form.get("estoque_id") else None,
            "local_id": to_int(request.form.get("local_id")) if request.form.get("local_id") else None
        }

        novo_entrada = PedidoEntrada(**dados_movimentacao)
        novo_entrada.insert()

        verificar_estoque()

        flash("Movimentação de entrada salva com sucesso!", "success") # Use "success" para o Bootstrap entender
        return redirect(url_for("nova_entrada"))

    except Exception as e:
        flash(f"Erro ao salvar movimentação de entrada: {e}", "danger") 
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

        verificar_estoque()

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
    
    # Verifica se alguma condição de estoque gerou alerta
    verificar_estoque()

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
        arquivo_foto = request.files.get('foto')
        caminho_foto_banco = None

        if arquivo_foto and arquivo_foto.filename != '':
            if not os.path.exists(PASTA_FOTOS):
                os.makedirs(PASTA_FOTOS)
                
            # Limpa o nome do arquivo para evitar bugs no sistema
            nome_arquivo_seguro = secure_filename(arquivo_foto.filename)
            
            # Monta o caminho onde o arquivo vai ser salvo 
            caminho_final_disco = os.path.join(PASTA_FOTOS, nome_arquivo_seguro)
            
            # Salva a imagem na pasta
            arquivo_foto.save(caminho_final_disco)
            
            # texto para salvar na coluna do banco de dados
            caminho_foto_banco = caminho_final_disco

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
            fornecedor=fornecedor,
            foto=caminho_foto_banco
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

# Para manter a foto de perfil acompanhando por todas as telas
'''@app.context_processor
def injetar_foto_menu():
    funcionario_id = session.get('funcionario_id', 6) 
    
    conexao = obter_conexao()
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute("SELECT caminho_arquivo FROM fotos_perfil WHERE funcionario_id = %s AND atual = TRUE", (funcionario_id,))
        resultado_foto = cursor.fetchone()
        
        foto_menu = resultado_foto['caminho_arquivo'] if resultado_foto else 'static/sem_foto.jpg'
    except:
        foto_menu = 'static/sem_foto.jpg'
    finally:
        cursor.close()
        conexao.close()
        
    return dict(usuario_foto=foto_menu)'''


# --- ROTAS DE SENSORES ---
@app.route('/api/sensor', methods=['GET', 'POST'])
def salvar_sensor():
    if request.method == 'GET':
        try:
            lista_sensores = Sensor.find_all(order_by="timestamp DESC")
            
            sensores_json = []
            for s in lista_sensores:
                sensores_json.append({
                    "id": s.id,
                    "sensor_nome": s.sensor_nome,
                    "sensor_codigo": s.sensor_codigo,
                    "sensor_tipo": s.sensor_tipo,
                    "sensor_setor": s.sensor_setor,
                    "valor": s.valor
                })
            
            return render_template('sensor.html', sensores=sensores_json)
        except Exception as e:
            return f"Erro ao carregar a tela de sensores: {str(e)}", 500

    elif request.method == 'POST':
        dados = request.get_json() if request.is_json else request.form
        
        nome = dados.get('sensor_nome', '').strip()
        codigo = dados.get('sensor_codigo', '').strip()
        setor = dados.get('sensor_setor', '').strip()
        valor = dados.get('sensor_valor', '').strip()
        tipo = dados.get('sensor_tipo', '').strip() 

        if not nome or not codigo or not setor or not valor:
            return jsonify({"erro": "Todos os campos obrigatórios devem ser preenchidos."}), 400

        if not valor.replace('.', '', 1).isdigit():
            return jsonify({"erro": "O campo 'Leitura Atual' foi preenchido incorretamente. Digite apenas números."}), 400

        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True) 
        try:
            sql_verificar = "SELECT id FROM sensores WHERE sensor_codigo = %s"
            cursor.execute(sql_verificar, (codigo,))
            sensor_existente = cursor.fetchone()

            if sensor_existente:
                return jsonify({"erro": f"Este sensor já está cadastrado! O Código ID '{codigo}' já está em uso."}), 400

            sql_inserir = """
                INSERT INTO sensores (sensor_nome, sensor_codigo, sensor_tipo, sensor_setor, valor) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_inserir, (nome, codigo, tipo, setor, valor))
            conexao.commit()
            
            # ==========================================
            # MONITORAMENTO DE TEMPERATURA
            # ==========================================

            if tipo.lower() == "temperatura":

                verificar_temperatura(
                    nome=nome,
                    valor=valor
                )
            
            id_gerado = cursor.lastrowid

            return jsonify({
                "mensagem": "Sensor cadastrado com sucesso!",
                "sensor": {
                    "id": id_gerado,
                    "sensor_nome": nome,
                    "sensor_codigo": codigo,
                    "sensor_tipo": tipo,
                    "sensor_setor": setor,
                    "valor": valor
                }
            }), 200

        except Exception as e:
            conexao.rollback()
            print(f"\n[ERRO CRÍTICO NO BANCO]: {str(e)}\n")
            return jsonify({"erro": f"Erro inesperado no banco de dados: {str(e)}"}), 500
        finally:
            cursor.close()
            conexao.close()


@app.route('/api/sensor/atualizar', methods=['POST'])
def atualizar_sensor():
    dados = request.form
    sensor_id = dados.get('sensor_id')
    
    if not sensor_id or not sensor_id.strip():
        return jsonify({"erro": "ID do sensor não foi enviado."}), 400

    nome = dados.get('sensor_nome', '').strip()
    codigo = dados.get('sensor_codigo', '').strip()
    setor = dados.get('sensor_setor', '').strip()
    valor = dados.get('sensor_valor', '').strip()
    tipo = dados.get('sensor_tipo', '').strip()

    if not nome or not codigo or not setor or not valor:
        return jsonify({"erro": "Todos os campos obrigatórios devem ser preenchidos."}), 400

    if not valor.replace('.', '', 1).isdigit():
        return jsonify({"erro": "O campo 'Leitura Atual' foi preenchido incorretamente. Digite apenas números."}), 400

    conexao = Database.connect()
    cursor = conexao.cursor(dictionary=True)
    try:
        sql_verificar = "SELECT id FROM sensores WHERE sensor_codigo = %s AND id != %s"
        cursor.execute(sql_verificar, (codigo, int(sensor_id)))
        sensor_duplicado = cursor.fetchone()

        if sensor_duplicado:
            return jsonify({"erro": f"Não é possível atualizar. O Código ID '{codigo}' já está sendo usado por outro sensor."}), 400

        sql_atualizar = """
            UPDATE sensores 
            SET sensor_nome = %s, sensor_codigo = %s, sensor_tipo = %s, sensor_setor = %s, valor = %s 
            WHERE id = %s
        """
        cursor.execute(sql_atualizar, (nome, codigo, tipo, setor, valor, int(sensor_id)))
        conexao.commit()
        
        return jsonify({
            "mensagem": "Sensor atualizado com sucesso!",
            "sensor": {
                "id": int(sensor_id),
                "sensor_nome": nome,
                "sensor_codigo": codigo,
                "sensor_tipo": tipo,
                "sensor_setor": setor,
                "valor": valor
            }
        }), 200

    except Exception as e:
        conexao.rollback()
        print(f"\n[ERRO CRÍTICO NA ATUALIZAÇÃO]: {str(e)}\n")
        return jsonify({"erro": f"Erro ao atualizar no banco: {str(e)}"}), 500
    finally:
        cursor.close()
        conexao.close()

# Excluir
@app.route('/api/sensor/excluir/<int:sensor_id>', methods=['GET'])
def remover_sensor_via_url(sensor_id):
    try:
        sensor = Sensor.find_by_id(sensor_id)
        if not sensor:
            return "Sensor não encontrado para exclusão.", 404
            
        sensor.delete()
        return redirect(url_for('salvar_sensor'))
    except Exception as e:
        return f"Erro ao deletar o sensor: {str(e)}", 500
    

# --- ROTAS DE ACESSIBILIDADE ---
@app.route('/acessibilidade/alto-contraste')
def alternar_alto_contraste():
    """Ativa ou desativa o modo de alto contraste na sessão."""
    session['alto_contraste'] = not session.get('alto_contraste', False)
    
    # Redireciona o usuário para a página em que ele já estava
    pagina_anterior = request.referrer or url_for('dashboard')
    return redirect(pagina_anterior)

@app.route('/acessibilidade/fonte/<acao>')
def alterar_fonte(acao):
    """Aumenta, diminui ou reseta o tamanho do texto."""
    tamanho_atual = session.get('tamanho_fonte', 100) # valor padrão em %
    
    if acao == 'aumentar' and tamanho_atual < 150:
        session['tamanho_fonte'] = tamanho_atual + 10
    elif acao == 'diminuir' and tamanho_atual > 80:
        session['tamanho_fonte'] = tamanho_atual - 10
    elif acao == 'resetar':
        session['tamanho_fonte'] = 100
        
    pagina_anterior = request.referrer or url_for('dashboard')
    return redirect(pagina_anterior)

# --- TELA DE ERRO 404 ---
# Rota que retorna para a tela de erro 404 se houver erro de carregamento no link
@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template('404.html'), 404

@app.errorhandler(405)
def pagina_nao_encontrada(error):
    return render_template('404.html'), 405

# Captura erro 500 (Erro interno do servidor / Falha de carregamento no código)
@app.errorhandler(500)
def erro_interno_servidor(error):
    return render_template('404.html'), 500


# --- Informações do footer ---
@app.route('/politica-privacidade')
def politica_privacidade():
    return render_template('politica_privacidade.html')

@app.route('/termos-de-uso')
def termos_uso():
    return render_template('termos_uso.html')

@app.route('/lgpd')
def lgpd():
    return render_template('lgpd.html')

@app.route('/solucoes')
def solucoes():
    return render_template('solucoes.html')

@app.route('/integracoes')
def integracoes():
    return render_template('integracoes.html')


@app.route('/automacao')
def automacao():
    return render_template('automacao.html')



# --- TELA DE CONFIGURAÇÂO ---
@app.context_processor
def injetar_globalmente():
    funcionario_id = session.get('funcionario_id', 1)
    
    # 1. Busca foto de perfil ativa do funcionário
    foto_menu = 'sem_foto.jpg'
    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(
            "SELECT caminho_arquivo FROM fotos_perfil WHERE funcionario_id = %s AND atual = TRUE", 
            (funcionario_id,)
        )
        resultado_foto = cursor.fetchone()
        if resultado_foto and resultado_foto.get('caminho_arquivo'):
            foto_menu = resultado_foto['caminho_arquivo']
    except Exception as e:
        print(f"Erro ao buscar foto global do menu: {e}")
    finally:
        if cursor: 
            cursor.close()
        if conexao: 
            conexao.close()

    # 2. Busca configurações e preferências de exibição do usuário
    dados_banco = Configuracao.buscar_por_funcionario(funcionario_id)
    if not dados_banco:
        dados_banco = {
            "tema": "claro",
            "notificacoes": True,
            "idioma": "pt-BR",
            "idioma_curto": "pt"
        }
    else:
        # Garante uniformidade nos valores e tipos de dados
        if dados_banco.get('idioma') == 'en-US':
            dados_banco['idioma_curto'] = 'en'
        else:
            dados_banco['idioma_curto'] = 'pt'
            
        dados_banco['notificacoes'] = bool(dados_banco.get('notificacoes', True))

    # Disponibiliza estas variáveis em TODOS os templates .html automaticamente
    return dict(
        usuario_foto=foto_menu,
        config=dados_banco,
        alto_contraste=session.get('alto_contraste', False),
        tamanho_fonte=session.get('tamanho_fonte', 100)
    )


# ROTAS DA TELA DE CONFIGURAÇÕES
@app.route('/configuracao')  # ou /perfil, dependendo da sua rota
def configuracao():
    funcionario_id = session.get('funcionario_id')
    
    if not funcionario_id:
        return redirect(url_for('login'))
    
    conexao = obter_conexao()
    cursor = conexao.cursor(dictionary=True) 
    
    try:
        # Busca Nome, Email, Cargo e demais campos do usuário logado
        cursor.execute("""
            SELECT nome, e_mail, cargo, telefone, data_nascimento, setor, sobre_mim 
            FROM funcionario 
            WHERE funcionario_id = %s
        """, (funcionario_id,))
        
        # Usamos fetchone() para trazer os dados do usuário direto em um dicionário
        funcionario_dados = cursor.fetchone()

        # Busca a foto do perfil
        cursor.execute("""
            SELECT caminho_arquivo 
            FROM fotos_perfil 
            WHERE funcionario_id = %s AND atual = TRUE
        """, (funcionario_id,))
        resultado_foto = cursor.fetchone()
        
        foto_do_banco = resultado_foto['caminho_arquivo'] if resultado_foto else 'imagens/sem-foto.png'

    except mysql.connector.Error as erro:
        print(f"Erro ao buscar dados do perfil: {erro}")
        funcionario_dados = None
        foto_do_banco = 'imagens/sem-foto.png'
        
    finally:
        cursor.close()
        conexao.close()
    
    # Envia os dados para o HTML
    return render_template('configuracao.html', usuario_foto=foto_do_banco, funcionario=funcionario_dados)


@app.route('/api/salvar_notificacoes', methods=['POST'])
def api_salvar_notificacoes():
    funcionario_id = session.get('funcionario_id', 1)
    dados_recebidos = request.get_json() or {}
    
    # Captura o estado do switch enviada via AJAX
    status_notificacoes = dados_recebidos.get('notificacoes', True)
    
    existente = Configuracao.buscar_por_funcionario(funcionario_id) or {}
    
    config = Configuracao(
        funcionario_id=funcionario_id,
        tema=existente.get('tema', 'claro'),
        notificacoes=status_notificacoes,
        idioma=existente.get('idioma', 'pt-BR'),
        configuracao_id=existente.get('configuracao_id')
    )
    
    erros = config.validate()
    if erros:
        return jsonify({"sucesso": False, "erros": erros}), 400
        
    if config.configuracao_id:
        config.update(config.configuracao_id)
    else:
        config.insert()
        
    return jsonify({"sucesso": True})


@app.route('/api/salvar_idioma', methods=['POST'])
def api_salvar_idioma():
    funcionario_id = session.get('funcionario_id', 1)
    dados_recebidos = request.get_json() or {}
    
    idioma_html = dados_recebidos.get('idioma', 'pt-BR')
    
    # Mapeamento do frontend (Select HTML) para o backend (Padrão ISO)
    if idioma_html == 'en':
        idioma_html = 'en-US'
    elif idioma_html == 'pt':
        idioma_html = 'pt-BR'
        
    existente = Configuracao.buscar_por_funcionario(funcionario_id) or {}
    
    config = Configuracao(
        funcionario_id=funcionario_id,
        tema=existente.get('tema', 'claro'),
        notificacoes=bool(existente.get('notificacoes', True)),
        idioma=idioma_html,
        configuracao_id=existente.get('configuracao_id')
    )
    
    erros = config.validate()
    if erros:
        return jsonify({"sucesso": False, "erros": erros}), 400
        
    if config.configuracao_id:
        config.update(config.configuracao_id)
    else:
        config.insert()
        
    return jsonify({"sucesso": True})


@app.route('/api/salvar_aparencia', methods=['POST'])
def api_salvar_aparencia():
    funcionario_id = session.get('funcionario_id', 1)
    dados_recebidos = request.get_json() or {}
    
    tema_selecionado = dados_recebidos.get('tema', 'claro')
    existente = Configuracao.buscar_por_funcionario(funcionario_id) or {}
    
    config = Configuracao(
        funcionario_id=funcionario_id,
        tema=tema_selecionado,
        notificacoes=bool(existente.get('notificacoes', True)),
        idioma=existente.get('idioma', 'pt-BR'),
        configuracao_id=existente.get('configuracao_id')
    )
    
    erros = config.validate()
    if erros:
        return jsonify({"sucesso": False, "erros": erros}), 400
        
    if config.configuracao_id:
        config.update(config.configuracao_id)
    else:
        config.insert()
        
    return jsonify({"sucesso": True})

# ESQUECI A SENHA
@app.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        cpf = request.form.get("cpf", "").strip()
        data_nascimento = request.form.get("data_nascimento", "").strip()

        # Limpa o CPF digitado (deixa apenas números)
        cpf_limpo = re.sub(r"\D", "", cpf)

        conexao = None
        cursor = None
        
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor(dictionary=True)

            # A query SQL trata o CPF removendo pontos e traços do banco
            # para garantir a comparação correta independente do formato salvo
            sql = """
                SELECT funcionario_id
                FROM funcionario
                WHERE LOWER(e_mail) = LOWER(%s)
                  AND REPLACE(REPLACE(CPF, '.', ''), '-', '') = %s
                  AND data_nascimento = %s
                LIMIT 1
            """
            cursor.execute(sql, (email, cpf_limpo, data_nascimento))
            funcionario = cursor.fetchone()

        except mysql.connector.Error as erro:
            print(f"Erro ao verificar dados para recuperação: {erro}")
            flash("Ocorreu um erro ao verificar seus dados.", "erro")
            return redirect(url_for("esqueci_senha"))

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

        if funcionario:
            return render_template(
                "redefinir_senha.html",
                funcionario_id=funcionario["funcionario_id"]
            )
        else:
            flash("Os dados informados não correspondem a nenhum funcionário.", "erro")
            return redirect(url_for("esqueci_senha"))

    return render_template("esqueci_senha.html")


# REDEFINIR SENHA
@app.route("/redefinir-senha", methods=["GET", "POST"])
def redefinir_senha():
    # Se o usuário tentar acessar a URL diretamente via GET, redireciona para o início do fluxo
    if request.method == "GET":
        return redirect(url_for("esqueci_senha"))

    funcionario_id = request.form.get("funcionario_id")
    nova_senha = request.form.get("nova_senha", "").strip()
    confirmar_senha = request.form.get("confirmar_senha", "").strip()

    # 1. Verifica se existe o ID do funcionário
    if not funcionario_id:
        flash("Sessão expirada ou funcionário não identificado. Tente novamente.", "erro")
        return redirect(url_for("esqueci_senha"))

    # 2. Verifica se os campos foram preenchidos
    if not nova_senha or not confirmar_senha:
        flash("Preencha os dois campos de senha.", "erro")
        return render_template("redefinir_senha.html", funcionario_id=funcionario_id)

    # 3. Verifica se as senhas são iguais
    if nova_senha != confirmar_senha:
        flash("As senhas não são iguais.", "erro")
        return render_template("redefinir_senha.html", funcionario_id=funcionario_id)

    conexao = None
    cursor = None

    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        sql = "UPDATE funcionario SET senha = %s WHERE funcionario_id = %s"
        cursor.execute(sql, (nova_senha, funcionario_id))
        conexao.commit()

        flash("Senha alterada com sucesso! Faça login com sua nova senha.", "sucesso")
        return redirect(url_for("login"))

    except mysql.connector.Error as erro:
        if conexao:
            conexao.rollback()
        print(f"Erro ao redefinir senha: {erro}")
        flash("Erro ao alterar a senha. Tente novamente.", "erro")
        return redirect(url_for("esqueci_senha"))

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

# --- ROTAS DE SUPORTE E CHATBOT ---

@app.route('/suporte')
def suporte():
    return render_template('suporte.html')


@app.route('/chatbot/perguntar', methods=['POST'])
def chatbot_perguntar():
    dados = request.get_json(silent=True) or {}
    mensagem = dados.get('mensagem', '').strip()

    if not mensagem:
        return jsonify({
            "erro": "Digite uma mensagem para continuar."
        }), 400

    try:
        resposta = gerar_resposta(mensagem)

        return jsonify({
            "resposta": resposta
        }), 200

    except Exception as erro:
        print(f"Erro no chatbot: {erro}")

        return jsonify({
            "erro": "Não foi possível gerar uma resposta."
        }), 500


# ==========================================================
# RELATÓRIOS FLOW TECH
# INTEGRAÇÃO COM O BANCO DE DADOS MYSQL
# ==========================================================

from datetime import date, datetime


# ----------------------------------------------------------
# FUNÇÕES AUXILIARES
# ----------------------------------------------------------

def periodo_relatorios():
    """Valida o período selecionado pelo usuário."""

    hoje = date.today()

    inicio_texto = request.args.get("inicio", "").strip()
    fim_texto = request.args.get("fim", "").strip()

    try:
        fim = date.fromisoformat(fim_texto) if fim_texto else hoje

        if inicio_texto:
            inicio = date.fromisoformat(inicio_texto)
        else:
            indice_mes = hoje.year * 12 + hoje.month - 1 - 11
            ano = indice_mes // 12
            mes = indice_mes % 12 + 1
            inicio = date(ano, mes, 1)

    except ValueError:
        raise ValueError("Informe um período válido.")

    if inicio > fim:
        raise ValueError(
            "A data inicial não pode ser posterior à data final."
        )

    return inicio, fim


def formatar_data_relatorio(valor, incluir_hora=True):
    """Formata datas para exibição nos documentos."""

    if valor is None:
        return "—"

    if isinstance(valor, datetime):
        if incluir_hora:
            return valor.strftime("%d/%m/%Y %H:%M")

        return valor.strftime("%d/%m/%Y")

    if isinstance(valor, date):
        return valor.strftime("%d/%m/%Y")

    return str(valor)


def formatar_texto_relatorio(valor):
    """Evita apresentar valores nulos nos documentos."""

    if valor is None or valor == "":
        return "—"

    return str(valor)


def consultar_relatorio(cursor, sql, parametros=()):
    """Executa uma consulta e devolve os registros."""

    cursor.execute(sql, parametros)

    return cursor.fetchall()


def gerar_lista_meses(inicio, fim):
    """Gera a sequência mensal usada no gráfico."""

    meses = []

    ano = inicio.year
    mes = inicio.month

    while (ano, mes) <= (fim.year, fim.month):

        meses.append((ano, mes))

        mes += 1

        if mes > 12:
            mes = 1
            ano += 1

    return meses


# ----------------------------------------------------------
# TELA PRINCIPAL DE RELATÓRIOS
# ----------------------------------------------------------

@app.route("/relatorios")
def relatorios():

    if not session.get("funcionario_id"):
        return redirect(url_for("login"))

    try:
        inicio, fim = periodo_relatorios()

    except ValueError as erro:
        flash(str(erro), "erro")
        return redirect(url_for("relatorios"))

    conexao = None
    cursor = None

    try:

        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)

        # --------------------------------------------------
        # TOTAL DE PEDIDOS DE ENTRADA
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM pedido_entrada
            WHERE data_hora >= %s
              AND data_hora < %s
        """, (
            inicio,
            datetime.combine(
                date.fromordinal(fim.toordinal() + 1),
                datetime.min.time()
            )
        ))

        total_entradas = cursor.fetchone()["total"] or 0

        # --------------------------------------------------
        # TOTAL DE PEDIDOS DE SAÍDA
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM pedido_saida
            WHERE data_hora >= %s
              AND data_hora < %s
        """, (
            inicio,
            datetime.combine(
                date.fromordinal(fim.toordinal() + 1),
                datetime.min.time()
            )
        ))

        total_saidas = cursor.fetchone()["total"] or 0

        # --------------------------------------------------
        # TOTAL DE PRODUTOS
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM produto
        """)

        total_produtos = cursor.fetchone()["total"] or 0

        # --------------------------------------------------
        # TOTAL DE FORNECEDORES
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM fornecedor
        """)

        total_fornecedores = cursor.fetchone()["total"] or 0

        # --------------------------------------------------
        # TOTAL DE FUNCIONÁRIOS
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM funcionario
        """)

        total_funcionarios = cursor.fetchone()["total"] or 0

        # --------------------------------------------------
        # QUANTIDADE DE PRODUTOS QUE ENTRARAM POR MÊS
        # --------------------------------------------------

        entradas_mes = consultar_relatorio(
            cursor,
            """
            SELECT
                DATE_FORMAT(pe.data_hora, '%Y-%m') AS mes,
                COALESCE(SUM(ipe.quantidade), 0) AS total

            FROM pedido_entrada AS pe

            LEFT JOIN itempedido_entrada AS ipe
                ON ipe.pedido_entrada_id = pe.pedido_entrada_id

            WHERE pe.data_hora >= %s
              AND pe.data_hora < %s

            GROUP BY DATE_FORMAT(pe.data_hora, '%Y-%m')

            ORDER BY mes
            """,
            (
                inicio,
                datetime.combine(
                    date.fromordinal(fim.toordinal() + 1),
                    datetime.min.time()
                )
            )
        )

        # --------------------------------------------------
        # QUANTIDADE DE PRODUTOS QUE SAÍRAM POR MÊS
        # --------------------------------------------------

        saidas_mes = consultar_relatorio(
            cursor,
            """
            SELECT
                DATE_FORMAT(ps.data_hora, '%Y-%m') AS mes,
                COALESCE(SUM(ips.quantidade), 0) AS total

            FROM pedido_saida AS ps

            LEFT JOIN itempedido_saida AS ips
                ON ips.pedido_saida_id = ps.pedido_saida_id

            WHERE ps.data_hora >= %s
              AND ps.data_hora < %s

            GROUP BY DATE_FORMAT(ps.data_hora, '%Y-%m')

            ORDER BY mes
            """,
            (
                inicio,
                datetime.combine(
                    date.fromordinal(fim.toordinal() + 1),
                    datetime.min.time()
                )
            )
        )

        # --------------------------------------------------
        # ORGANIZAÇÃO DOS DADOS DO GRÁFICO
        # --------------------------------------------------

        mapa_entradas = {
            item["mes"]: int(item["total"] or 0)
            for item in entradas_mes
        }

        mapa_saidas = {
            item["mes"]: int(item["total"] or 0)
            for item in saidas_mes
        }

        meses = gerar_lista_meses(inicio, fim)

        nomes_meses = [
            "Jan", "Fev", "Mar", "Abr",
            "Mai", "Jun", "Jul", "Ago",
            "Set", "Out", "Nov", "Dez"
        ]

        labels = []
        valores_entrada = []
        valores_saida = []

        for ano, mes in meses:

            chave = f"{ano:04d}-{mes:02d}"

            labels.append(
                f"{nomes_meses[mes - 1]}/{str(ano)[2:]}"
            )

            valores_entrada.append(
                mapa_entradas.get(chave, 0)
            )

            valores_saida.append(
                mapa_saidas.get(chave, 0)
            )

        grafico = {
            "labels": labels,
            "entradas": valores_entrada,
            "saidas": valores_saida
        }

        # --------------------------------------------------
        # ENVIO DOS DADOS PARA O HTML
        # --------------------------------------------------

        return render_template(
            "relatorio.html",

            total_entradas=total_entradas,
            total_saidas=total_saidas,

            total_produtos=total_produtos,
            total_fornecedores=total_fornecedores,
            total_funcionarios=total_funcionarios,

            grafico=grafico,

            inicio=inicio.isoformat(),
            fim=fim.isoformat(),

            inicio_br=inicio.strftime("%d/%m/%Y"),
            fim_br=fim.strftime("%d/%m/%Y"),

            erros=[]
        )

    except Exception as erro:

        print("ERRO NA TELA DE RELATÓRIOS:", erro)

        flash(
            "Não foi possível carregar os relatórios. "
            "Verifique a conexão com o banco de dados.",
            "erro"
        )

        return redirect(url_for("dashboard"))

    finally:

        if cursor:
            cursor.close()

        if conexao:
            conexao.close()


# ----------------------------------------------------------
# GERAÇÃO DOS DOCUMENTOS
# ----------------------------------------------------------

@app.route("/relatorios/documento/<tipo>")
def gerar_relatorio_documento(tipo):

    if not session.get("funcionario_id"):
        return redirect(url_for("login"))

    titulos = {
        "entradas": "Relatório de Entradas de Produtos",
        "saidas": "Relatório de Saídas de Produtos",
        "produtos": "Relatório de Produtos Cadastrados",
        "fornecedores": "Relatório de Fornecedores Cadastrados",
        "funcionarios": "Relatório de Funcionários Cadastrados"
    }

    if tipo not in titulos:
        flash("Tipo de relatório inválido.", "erro")
        return redirect(url_for("relatorios"))

    try:
        inicio, fim = periodo_relatorios()

    except ValueError as erro:
        flash(str(erro), "erro")
        return redirect(url_for("relatorios"))

    conexao = None
    cursor = None

    try:

        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)

        fim_exclusivo = datetime.combine(
            date.fromordinal(fim.toordinal() + 1),
            datetime.min.time()
        )

        # ==================================================
        # RELATÓRIO DE ENTRADAS
        # ==================================================

        if tipo == "entradas":

            registros = consultar_relatorio(
                cursor,
                """
                SELECT
                    pe.pedido_entrada_id,
                    pe.data_hora,

                    p.nome AS produto,

                    ipe.quantidade,

                    f.nome AS fornecedor,

                    fun.nome AS funcionario,

                    pe.status_pedido,
                    pe.descricao,
                    pe.rfid

                FROM pedido_entrada AS pe

                LEFT JOIN itempedido_entrada AS ipe
                    ON ipe.pedido_entrada_id = pe.pedido_entrada_id

                LEFT JOIN produto AS p
                    ON p.produto_id = ipe.produto_id

                LEFT JOIN fornecedor AS f
                    ON f.fornecedor_id = pe.fornecedor_id

                LEFT JOIN funcionario AS fun
                    ON fun.funcionario_id = pe.funcionario_id

                WHERE pe.data_hora >= %s
                  AND pe.data_hora < %s

                ORDER BY
                    pe.data_hora DESC,
                    pe.pedido_entrada_id DESC
                """,
                (inicio, fim_exclusivo)
            )

            colunas = [
                "Pedido",
                "Data e hora",
                "Produto",
                "Quantidade",
                "Fornecedor",
                "Funcionário",
                "Status",
                "Descrição",
                "RFID"
            ]

            linhas = [
                [
                    formatar_texto_relatorio(r["pedido_entrada_id"]),
                    formatar_data_relatorio(r["data_hora"]),
                    formatar_texto_relatorio(r["produto"]),
                    formatar_texto_relatorio(r["quantidade"]),
                    formatar_texto_relatorio(r["fornecedor"]),
                    formatar_texto_relatorio(r["funcionario"]),
                    formatar_texto_relatorio(r["status_pedido"]),
                    formatar_texto_relatorio(r["descricao"]),
                    formatar_texto_relatorio(r["rfid"])
                ]
                for r in registros
            ]

            periodo = (
                f"{inicio.strftime('%d/%m/%Y')} até "
                f"{fim.strftime('%d/%m/%Y')}"
            )

        # ==================================================
        # RELATÓRIO DE SAÍDAS
        # ==================================================

        elif tipo == "saidas":

            registros = consultar_relatorio(
                cursor,
                """
                SELECT
                    ps.pedido_saida_id,
                    ps.data_hora,

                    p.nome AS produto,

                    ips.quantidade,

                    c.nome AS cliente,

                    fun.nome AS funcionario,

                    ps.status_pedido,
                    ps.descricao

                FROM pedido_saida AS ps

                LEFT JOIN itempedido_saida AS ips
                    ON ips.pedido_saida_id = ps.pedido_saida_id

                LEFT JOIN produto AS p
                    ON p.produto_id = ips.produto_id

                LEFT JOIN cliente AS c
                    ON c.cliente_id = ps.cliente_id

                LEFT JOIN funcionario AS fun
                    ON fun.funcionario_id = ps.funcionario_id

                WHERE ps.data_hora >= %s
                  AND ps.data_hora < %s

                ORDER BY
                    ps.data_hora DESC,
                    ps.pedido_saida_id DESC
                """,
                (inicio, fim_exclusivo)
            )

            colunas = [
                "Pedido",
                "Data e hora",
                "Produto",
                "Quantidade",
                "Cliente",
                "Funcionário",
                "Status",
                "Descrição"
            ]

            linhas = [
                [
                    formatar_texto_relatorio(r["pedido_saida_id"]),
                    formatar_data_relatorio(r["data_hora"]),
                    formatar_texto_relatorio(r["produto"]),
                    formatar_texto_relatorio(r["quantidade"]),
                    formatar_texto_relatorio(r["cliente"]),
                    formatar_texto_relatorio(r["funcionario"]),
                    formatar_texto_relatorio(r["status_pedido"]),
                    formatar_texto_relatorio(r["descricao"])
                ]
                for r in registros
            ]

            periodo = (
                f"{inicio.strftime('%d/%m/%Y')} até "
                f"{fim.strftime('%d/%m/%Y')}"
            )

        # ==================================================
        # RELATÓRIO DE PRODUTOS
        # ==================================================

        elif tipo == "produtos":

            registros = consultar_relatorio(
                cursor,
                """
                SELECT
                    p.produto_id,
                    p.nome,
                    p.categoria,
                    p.tipo_produto,

                    COALESCE(e.quantidade_atual, 0)
                        AS quantidade_atual,

                    p.estoque_minimo,
                    p.lote,
                    p.validade,
                    p.localizacao,
                    p.fornecedor,
                    p.RFID

                FROM produto AS p

                LEFT JOIN (
                    SELECT
                        produto_id,
                        SUM(quantidade) AS quantidade_atual

                    FROM estoque

                    GROUP BY produto_id

                ) AS e
                    ON e.produto_id = p.produto_id

                ORDER BY p.nome ASC
                """
            )

            colunas = [
                "ID",
                "Produto",
                "Categoria",
                "Tipo",
                "Estoque atual",
                "Estoque mínimo",
                "Lote",
                "Validade",
                "Localização",
                "Fornecedor",
                "RFID"
            ]

            linhas = [
                [
                    formatar_texto_relatorio(r["produto_id"]),
                    formatar_texto_relatorio(r["nome"]),
                    formatar_texto_relatorio(r["categoria"]),
                    formatar_texto_relatorio(r["tipo_produto"]),
                    formatar_texto_relatorio(r["quantidade_atual"]),
                    formatar_texto_relatorio(r["estoque_minimo"]),
                    formatar_texto_relatorio(r["lote"]),
                    formatar_data_relatorio(
                        r["validade"],
                        incluir_hora=False
                    ),
                    formatar_texto_relatorio(r["localizacao"]),
                    formatar_texto_relatorio(r["fornecedor"]),
                    formatar_texto_relatorio(r["RFID"])
                ]
                for r in registros
            ]

            periodo = "Todos os produtos cadastrados"

        # ==================================================
        # RELATÓRIO DE FORNECEDORES
        # ==================================================

        elif tipo == "fornecedores":

            registros = consultar_relatorio(
                cursor,
                """
                SELECT
                    fornecedor_id,
                    nome,
                    CNPJ,
                    e_mail,
                    telefone,
                    endereco

                FROM fornecedor

                ORDER BY nome ASC
                """
            )

            colunas = [
                "ID",
                "Fornecedor",
                "CNPJ",
                "E-mail",
                "Telefone",
                "Endereço"
            ]

            linhas = [
                [
                    formatar_texto_relatorio(r["fornecedor_id"]),
                    formatar_texto_relatorio(r["nome"]),
                    formatar_texto_relatorio(r["CNPJ"]),
                    formatar_texto_relatorio(r["e_mail"]),
                    formatar_texto_relatorio(r["telefone"]),
                    formatar_texto_relatorio(r["endereco"])
                ]
                for r in registros
            ]

            periodo = "Todos os fornecedores cadastrados"

        # ==================================================
        # RELATÓRIO DE FUNCIONÁRIOS
        # ==================================================

        else:

            registros = consultar_relatorio(
                cursor,
                """
                SELECT
                    funcionario_id,
                    nome,
                    e_mail,
                    setor,
                    cargo,
                    turno,
                    telefone

                FROM funcionario

                ORDER BY nome ASC
                """
            )

            colunas = [
                "ID",
                "Funcionário",
                "E-mail",
                "Setor",
                "Cargo",
                "Turno",
                "Telefone"
            ]

            linhas = [
                [
                    formatar_texto_relatorio(r["funcionario_id"]),
                    formatar_texto_relatorio(r["nome"]),
                    formatar_texto_relatorio(r["e_mail"]),
                    formatar_texto_relatorio(r["setor"]),
                    formatar_texto_relatorio(r["cargo"]),
                    formatar_texto_relatorio(r["turno"]),
                    formatar_texto_relatorio(r["telefone"])
                ]
                for r in registros
            ]

            periodo = "Todos os funcionários cadastrados"

        # ==================================================
        # ENVIA OS DADOS PARA A FOLHA DO DOCUMENTO
        # ==================================================

        return render_template(
            "documento_relatorio.html",

            titulo=titulos[tipo],
            tipo=tipo,

            colunas=colunas,
            linhas=linhas,

            total_registros=len(linhas),

            gerado_em=datetime.now().strftime(
                "%d/%m/%Y às %H:%M"
            ),

            periodo=periodo,

            inicio=inicio.isoformat(),
            fim=fim.isoformat(),

            erro_documento=None
        )

    
    except Exception as erro:

        app.logger.exception(
            "ERRO AO GERAR DOCUMENTO: %s",
            tipo
        )

        flash(
            f"Erro ao gerar documento: {erro}",
            "erro"
        )

        return redirect(
            url_for(
                "relatorios",
                inicio=inicio.isoformat(),
                fim=fim.isoformat()
            )
        )

    finally:

        if cursor is not None:
            cursor.close()

        if conexao is not None:
            conexao.close()






if __name__ == "__main__":
    app.run(debug=True)