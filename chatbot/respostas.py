
import unicodedata
import re


def normalizar_texto(texto):
    """
    Remove acentos, converte para minusculas
    e organiza o texto para facilitar a identificacao.
    """
    texto = str(texto).lower().strip()

    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caractere for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()


# Base de conhecimento do FlowTech
# As perguntas frequentes ficam primeiro para terem prioridade.
BASE_CONHECIMENTO = {

    # ==========================================
    # PERGUNTAS FREQUENTES
    # ==========================================

    "validade": {
        "palavras": [
            "produto vai vencer",
            "algo vai vencer",
            "quando algo vai vencer",
            "produto proximo do vencimento",
            "produtos proximos do vencimento",
            "produto vencendo",
            "alerta de validade",
            "alerta de vencimento",
            "aviso de vencimento",
            "avisa quando vence",
            "produto perto de vencer",
            "validade dos produtos"
        ],
        "resposta": (
            "Sim! O sistema emite alertas para produtos próximos do "
            "vencimento, considerando um período de até 30 dias antes "
            "da data de validade, conforme definido nos requisitos.\n\n"
            "Além disso, a gestão por lotes e a obrigatoriedade de "
            "informar a validade permitem maior controle e "
            "rastreabilidade dos itens armazenados."
        )
    },

    "reposicao": {
        "palavras": [
            "hora de pedir mais mercadoria",
            "quando pedir mais mercadoria",
            "preciso comprar mais produtos",
            "quando repor estoque",
            "hora de repor",
            "alerta de reposicao",
            "alerta de estoque baixo",
            "estoque atingiu nivel critico",
            "estoque critico",
            "quando comprar mais",
            "falta de mercadoria",
            "reabastecer estoque"
        ],
        "resposta": (
            "O sistema possui alertas de reposição que podem notificar "
            "quando um produto atinge níveis críticos de estoque.\n\n"
            "Esses alertas podem considerar a movimentação de entrada "
            "e saída, o histórico de consumo e as divergências de "
            "inventário, auxiliando no planejamento das reposições "
            "e evitando a falta de mercadorias."
        )
    },

    "multiloja": {
        "palavras": [
            "mais de uma loja",
            "varias lojas",
            "multiplas lojas",
            "estoque de todas as lojas",
            "estoque de outra loja",
            "estoques em diferentes unidades",
            "gerenciar varias unidades",
            "controle de varias lojas",
            "filiais",
            "outras unidades"
        ],
        "resposta": (
            "O FlowTech foi planejado para centralizar as informações "
            "e permitir o gerenciamento integrado de estoques em "
            "diferentes unidades.\n\n"
            "O controle pode envolver registros de movimentações, "
            "localização e histórico por produto e lote, contribuindo "
            "para a consistência das informações."
        )
    },

    "internet": {
        "palavras": [
            "internet cair",
            "internet caiu",
            "sem internet",
            "sem conexao",
            "queda de internet",
            "conexao caiu",
            "internet durante a venda",
            "falha de conexao",
            "desconectou durante a venda",
            "venda sem internet"
        ],
        "resposta": (
            "O sistema foi projetado considerando a importância da "
            "disponibilidade e da integridade dos dados.\n\n"
            "Em situações de falha de conexão, os procedimentos de "
            "recuperação e sincronização dependem dos recursos "
            "implementados na aplicação e da infraestrutura utilizada.\n\n"
            "Se a conexão cair durante uma operação, evite repetir "
            "o registro sem antes verificar se ele foi salvo, para "
            "não gerar duplicidade."
        )
    },

    "suporte_tecnico": {
        "palavras": [
            "quem me ajuda",
            "quem pode me ajudar",
            "preciso de ajuda agora",
            "tive um problema agora",
            "falar com suporte",
            "equipe de suporte",
            "suporte tecnico",
            "problema no sistema",
            "como pedir ajuda",
            "contatar suporte",
            "entrar em contato com suporte"
        ],
        "resposta": (
            "O FlowTech conta com uma área de suporte para auxiliar "
            "na identificação e resolução de problemas.\n\n"
            "A equipe responsável pode utilizar os registros e "
            "informações disponíveis para investigar inconsistências "
            "e falhas.\n\n"
            "Você também pode entrar em contato pelo e-mail "
            "suporte@flowtech.local ou consultar os canais de "
            "atendimento apresentados nesta página."
        )
    },

    "rastreabilidade": {
        "palavras": [
            "rastrear produto",
            "rastreabilidade",
            "rastrear desde a entrada",
            "produto ate o cliente final",
            "origem do produto",
            "destino do produto",
            "historico completo do produto",
            "acompanhar produto desde a entrada",
            "rastrear lote"
        ],
        "resposta": (
            "Sim! O sistema permite a rastreabilidade dos produtos "
            "por lote, registrando as etapas de movimentação.\n\n"
            "Isso possibilita acompanhar informações desde o "
            "recebimento e as movimentações internas até a saída "
            "e o destino registrado para o produto."
        )
    },

    "lotes": {
        "palavras": [
            "controle de lotes",
            "como funciona o lote",
            "como funciona controle de lote",
            "identificacao de lote",
            "registrar lote",
            "produto por lote",
            "qr code",
            "rfid",
            "validade por lote",
            "lotes dos produtos"
        ],
        "resposta": (
            "O controle de lotes permite identificar e acompanhar "
            "os produtos recebidos no estoque.\n\n"
            "No registro de entrada, as informações do lote e da "
            "validade devem ser preenchidas conforme os campos "
            "disponíveis no sistema.\n\n"
            "A identificação por QR Code ou RFID pode complementar "
            "esse processo quando esses recursos estiverem "
            "disponíveis na operação."
        )
    },

    "relatorios": {
        "palavras": [
            "sistema gera relatorios",
            "gerar relatorio",
            "gerar relatorios",
            "relatorio de entrada",
            "relatorio de saida",
            "relatorio de movimentacao",
            "exportar relatorio",
            "relatorios em pdf",
            "relatorios em excel",
            "baixar relatorio",
            "relatorio automatico"
        ],
        "resposta": (
            "O sistema pode gerar relatórios para acompanhar "
            "as movimentações de entrada, saída e estoque.\n\n"
            "Os relatórios podem contar com filtros para facilitar "
            "a consulta das informações. A exportação em PDF e "
            "Excel depende dos recursos de exportação disponíveis "
            "na versão do sistema."
        )
    },

    "permissoes": {
        "palavras": [
            "controle de acesso",
            "tipo de usuario",
            "tipos de usuario",
            "nivel de acesso",
            "niveis de acesso",
            "permissao de usuario",
            "permissoes de usuarios",
            "administrador gestor operador",
            "acesso por usuario",
            "usuarios diferentes"
        ],
        "resposta": (
            "O controle de acesso permite organizar as permissões "
            "dos usuários de acordo com suas responsabilidades.\n\n"
            "Perfis como administrador, gestor e operador podem "
            "ter níveis de acesso diferentes, conforme as regras "
            "de permissão configuradas no sistema."
        )
    },

    "temperatura": {
        "palavras": [
            "controlar temperatura",
            "controle de temperatura",
            "temperatura dos produtos",
            "temperatura do estoque",
            "condicoes de armazenamento",
            "umidade",
            "monitoramento de temperatura",
            "sensor de temperatura",
            "temperatura e umidade",
            "armazenamento adequado"
        ],
        "resposta": (
            "O FlowTech contempla o monitoramento das condições "
            "de armazenamento por meio de sensores IoT.\n\n"
            "Esse monitoramento pode envolver temperatura e "
            "umidade, com registros das leituras e alertas quando "
            "forem identificadas variações fora dos padrões "
            "configurados."
        )
    },

    "falha_sistema": {
        "palavras": [
            "falha no sistema",
            "falha do sistema",
            "sistema parou",
            "sistema apresentou falha",
            "sistema fora do ar",
            "o que acontece se o sistema falhar",
            "recuperacao de dados",
            "perda de dados",
            "recuperacao de desastres",
            "sistema nao esta funcionando"
        ],
        "resposta": (
            "O sistema prevê mecanismos de acompanhamento e "
            "identificação de falhas, incluindo registros de "
            "ocorrências e informações para auxiliar na análise "
            "dos problemas.\n\n"
            "Em caso de falha, a equipe responsável deve verificar "
            "os registros e realizar os procedimentos de recuperação "
            "disponíveis, buscando preservar a integridade dos dados "
            "e restabelecer o funcionamento."
        )
    },

    # ==========================================
    # RESPOSTAS ORIGINAIS DO CHATBOT
    # ==========================================

    "saudacao": {
        "palavras": [
            "oi", "ola", "bom dia", "boa tarde",
            "boa noite", "tudo bem", "ola assistente"
        ],
        "resposta": (
            "Olá! Seja bem-vindo ao suporte virtual do FlowTech! "
            "Estou aqui para ajudar você a utilizar o sistema. "
            "Pode perguntar sobre produtos, estoque, clientes, "
            "fornecedores, funcionários, pedidos e outras funcionalidades."
        )
    },

    "ajuda": {
        "palavras": [
            "ajuda", "o que voce faz", "como funciona",
            "preciso de ajuda", "suporte"
        ],
        "resposta": (
            "Posso ajudar você com as principais funcionalidades do FlowTech:\n\n"
            "• Cadastro de produtos;\n"
            "• Controle de estoque;\n"
            "• Cadastro de clientes e fornecedores;\n"
            "• Cadastro de funcionários;\n"
            "• Pedidos de entrada e saída;\n"
            "• Sensores e monitoramento;\n"
            "• Configurações e acesso ao sistema;\n"
            "• Validade e rastreabilidade dos produtos;\n"
            "• Relatórios e controle de acesso.\n\n"
            "Digite sua dúvida para receber orientações."
        )
    },

    "produto": {
        "palavras": [
            "produto", "produtos", "cadastrar produto",
            "cadastro de produto", "editar produto",
            "alterar produto", "excluir produto"
        ],
        "resposta": (
            "Para trabalhar com produtos no FlowTech, acesse a área "
            "de Produtos no sistema.\n\n"
            "Nessa funcionalidade você pode consultar os produtos "
            "cadastrados e utilizar os formulários disponíveis para "
            "incluir ou atualizar informações.\n\n"
            "Confira os dados antes de salvar, principalmente nome, "
            "categoria, lote, validade e quantidade."
        )
    },

    "estoque": {
        "palavras": [
            "estoque", "quantidade em estoque",
            "estoque baixo", "estoque minimo",
            "consultar estoque", "controle de estoque",
            "falta de produto", "saldo"
        ],
        "resposta": (
            "O módulo de Estoque permite acompanhar os produtos "
            "armazenados e suas quantidades.\n\n"
            "Para consultar o estoque, acesse a opção Estoque "
            "no menu do FlowTech.\n\n"
            "Fique atento ao estoque mínimo, à validade dos produtos "
            "e às informações dos lotes para manter o controle atualizado."
        )
    },

    "entrada": {
        "palavras": [
            "entrada", "entradas", "nova entrada",
            "pedido de entrada", "receber mercadoria",
            "entrada de produtos", "repor estoque"
        ],
        "resposta": (
            "A entrada de produtos serve para registrar o recebimento "
            "de mercadorias e atualizar o controle do estoque.\n\n"
            "Acesse a opção de Nova Entrada e confira os dados do pedido, "
            "os produtos, as quantidades e as informações solicitadas "
            "pelo formulário antes de concluir o registro."
        )
    },

    "saida": {
        "palavras": [
            "saida", "saidas", "nova saida",
            "pedido de saida", "retirar produto",
            "saida de produtos", "baixa no estoque"
        ],
        "resposta": (
            "A saída de produtos permite registrar a retirada de itens "
            "do estoque.\n\n"
            "Acesse a opção Nova Saída, informe os dados solicitados "
            "e confira as quantidades antes de finalizar.\n\n"
            "É importante verificar a disponibilidade dos produtos "
            "para evitar inconsistências no estoque."
        )
    },

    "cliente": {
        "palavras": [
            "cliente", "clientes", "cadastrar cliente",
            "cadastro de cliente", "novo cliente",
            "editar cliente"
        ],
        "resposta": (
            "O módulo de Clientes permite organizar os dados dos "
            "clientes cadastrados no FlowTech.\n\n"
            "Acesse a área de Clientes para consultar os registros "
            "ou utilizar o formulário de cadastro.\n\n"
            "Confira os dados preenchidos antes de salvar."
        )
    },

    "fornecedor": {
        "palavras": [
            "fornecedor", "fornecedores",
            "cadastrar fornecedor", "novo fornecedor",
            "cadastro de fornecedor"
        ],
        "resposta": (
            "A área de Fornecedores permite manter os dados das "
            "empresas responsáveis pelo fornecimento de produtos.\n\n"
            "Acesse Fornecedores no sistema para consultar ou cadastrar "
            "um novo registro."
        )
    },

    "funcionario": {
        "palavras": [
            "funcionario", "funcionarios",
            "cadastrar funcionario", "novo funcionario",
            "cadastro de funcionario", "colaborador"
        ],
        "resposta": (
            "O módulo de Funcionários organiza os registros dos "
            "colaboradores que utilizam ou fazem parte da operação.\n\n"
            "Acesse a área de Funcionários para consultar ou realizar "
            "um novo cadastro."
        )
    },

    "pedido": {
        "palavras": [
            "pedido", "pedidos", "consultar pedido",
            "historico de pedidos", "acompanhar pedido"
        ],
        "resposta": (
            "O FlowTech possui funcionalidades para registrar "
            "e acompanhar pedidos de entrada e saída.\n\n"
            "Você pode acessar a área de Pedidos para consultar "
            "as informações disponíveis e acompanhar as movimentações."
        )
    },

    "sensor": {
        "palavras": [
            "sensor", "sensores", "monitoramento",
            "leitura do sensor", "monitoramento de estoque"
        ],
        "resposta": (
            "O módulo de Sensores permite acompanhar as informações "
            "registradas pelos dispositivos de monitoramento.\n\n"
            "Acesse a área de Sensores para consultar os registros "
            "e verificar as leituras disponíveis."
        )
    },

    "grafico": {
        "palavras": [
            "grafico", "graficos", "relatorio",
            "relatorios", "estatisticas", "indicadores"
        ],
        "resposta": (
            "Os gráficos ajudam a visualizar informações e acompanhar "
            "indicadores do sistema.\n\n"
            "Acesse a área correspondente no FlowTech para consultar "
            "as informações disponíveis."
        )
    },

    "configuracao": {
        "palavras": [
            "configuracao", "configuracoes",
            "alterar configuracao", "preferencias",
            "idioma", "tema", "modo escuro"
        ],
        "resposta": (
            "Na área de Configurações você pode consultar as "
            "preferências disponíveis no sistema.\n\n"
            "Dependendo das opções habilitadas, é possível ajustar "
            "preferências como idioma e aparência."
        )
    },

    "login": {
        "palavras": [
            "login", "entrar", "acessar sistema",
            "nao consigo entrar", "acesso bloqueado"
        ],
        "resposta": (
            "Se você estiver com dificuldades para acessar o FlowTech, "
            "verifique se o e-mail e a senha foram digitados corretamente.\n\n"
            "Confira também se está utilizando a tela de login correta. "
            "Se o problema continuar, procure o suporte técnico."
        )
    },

    "senha": {
        "palavras": [
            "senha", "esqueci minha senha",
            "redefinir senha", "alterar senha",
            "recuperar senha"
        ],
        "resposta": (
            "Se você esqueceu sua senha, utilize a opção "
            "de recuperação de senha disponível na tela de login.\n\n"
            "Siga as orientações apresentadas pelo sistema. "
            "Nunca compartilhe sua senha com outras pessoas."
        )
    },

    "erro": {
        "palavras": [
            "erro", "problema", "bug",
            "nao funciona", "travou", "falha",
            "pagina nao abre", "sistema lento"
        ],
        "resposta": (
            "Vamos tentar identificar o problema!\n\n"
            "Verifique se sua conexão está funcionando e tente "
            "atualizar a página.\n\n"
            "Se o erro continuar, anote a mensagem apresentada "
            "e procure a equipe responsável pelo suporte técnico.\n\n"
            "Você também pode acessar a Central de Ajuda do FlowTech."
        )
    },

    "agradecimento": {
        "palavras": [
            "obrigado", "obrigada", "agradeco",
            "valeu", "muito obrigado", "muito obrigada"
        ],
        "resposta": (
            "Por nada! Fico feliz em ajudar. "
            "Sempre que precisar de orientações sobre o FlowTech, "
            "estarei disponível por aqui!"
        )
    },

    "despedida": {
        "palavras": [
            "tchau", "ate mais", "encerrar conversa",
            "finalizar atendimento"
        ],
        "resposta": (
            "Até mais! Obrigado por utilizar o suporte virtual "
            "do FlowTech. Tenha um ótimo dia!"
        )
    }
}


def identificar_assunto(mensagem):
    """
    Identifica o assunto da mensagem com base
    nas palavras-chave cadastradas.
    """

    texto = normalizar_texto(mensagem)

    if not texto:
        return None

    # Procura primeiro as perguntas frequentes
    # e depois as respostas gerais.
    for assunto, dados in BASE_CONHECIMENTO.items():
        for palavra in dados["palavras"]:
            palavra_normalizada = normalizar_texto(palavra)

            if re.search(
                r"\b" + re.escape(palavra_normalizada) + r"\b",
                texto
            ):
                return assunto

    return None


def gerar_resposta(mensagem):
    """
    Recebe a mensagem e retorna uma resposta
    correspondente ao assunto identificado.
    """

    assunto = identificar_assunto(mensagem)

    if assunto:
        return BASE_CONHECIMENTO[assunto]["resposta"]

    return (
        "Não consegui identificar exatamente sua dúvida.\n\n"
        "Posso ajudar com produtos, estoque, clientes, fornecedores, "
        "funcionários, pedidos, entradas, saídas, sensores, "
        "configurações, acesso ao sistema, validade, lotes, "
        "rastreabilidade e relatórios.\n\n"
        "Tente explicar sua dúvida de outra maneira ou utilize "
        "a Central de Ajuda para entrar em contato com o suporte."
    )
