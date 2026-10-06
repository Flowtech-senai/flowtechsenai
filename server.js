const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// Rota inicial
app.get('/', (req, res) => {
  res.send('API do StockPro2 / FlowTech está rodando com sucesso!');
});

// Configuração da Conexão com o MySQL (Mantém suas tabelas em português intactas)
const db = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: '123456',
  database: 'flowtech',
  waitForConnections: true,
  connectionLimit: 10,
});

// 1. Rota de Login
app.post('/login', async (req, res) => {
  const { e_mail, senha } = req.body;
  try {
    const [linhas] = await db.query('SELECT * FROM funcionario WHERE e_mail = ?', [e_mail]);
    if (!linhas || linhas.length === 0) {
      return res.status(401).json({ success: false, message: 'Funcionário não cadastrado ou dados incorretos!' });
    }
    const dadosFuncionario = linhas[0];
    const senhaBancoLimpa = dadosFuncionario?.senha ? String(dadosFuncionario.senha).trim() : '';
    const senhaDigitadaLimpa = senha ? String(senha).trim() : '';

    if (senhaBancoLimpa !== senhaDigitadaLimpa) {
      return res.status(401).json({ success: false, message: 'Senha incorreta!' });
    }
    return res.status(200).json({ success: true, message: 'Login realizado com sucesso!', funcionarioId: dadosFuncionario.id });
  } catch (error) {
    return res.status(500).json({ success: false, message: `Erro interno: ${error.message}` });
  }
});

// 2. Rota de Dashboard
app.get('/api/dashboard', async (req, res) => {
  try {

    // Total de produtos
    const [[{ totalProducts }]] = await db.query(`
      SELECT COUNT(*) AS totalProducts
      FROM produto
    `);

    // Produtos com estoque baixo
    const [[{ lowStockCount }]] = await db.query(`
      SELECT COUNT(*) AS lowStockCount
      FROM estoque
      WHERE quantidade <= 5
    `);

    // Total de entradas
    const [[{ totalEntradas }]] = await db.query(`
      SELECT COUNT(*) AS totalEntradas
      FROM movimentacao
      WHERE tipo_mov = 'entrada'
    `);

    // Total de saídas
    const [[{ totalSaidas }]] = await db.query(`
      SELECT COUNT(*) AS totalSaidas
      FROM movimentacao
      WHERE tipo_mov = 'saida'
    `);

    // Atividades recentes
    const queryMovimentacao = `
      SELECT 
        m.movimentacao_id AS id,
        m.tipo_mov AS tipo,
        m.quantidade AS quantidade,
        p.nome AS produto_nome,
        m.data_horamov AS data_hora
      FROM movimentacao m
      INNER JOIN estoque e 
        ON m.estoque_id = e.estoque_id
      INNER JOIN produto p 
        ON e.produto_id = p.produto_id
      ORDER BY m.data_horamov DESC
      LIMIT 50
    `;

    const [atividades] = await db.query(queryMovimentacao);

    res.json({
      totalProducts: Number(totalProducts) || 0,
      lowStockCount: Number(lowStockCount) || 0,
      totalEntradas: Number(totalEntradas) || 0,
      totalSaidas: Number(totalSaidas) || 0,
      atividades: atividades || []
    });

  } catch (error) {

    console.error('Erro detalhado no Dashboard:', error);

    res.status(500).json({
      error: error.message
    });

  }
});




// 3. Listar Todos os Produtos (Usa aliases para o React Native ler sem quebrar as outras tabelas)
app.get('/api/produto', async (req, res) => {
  try {
    const queryBuscaTodos = `
      SELECT 
          p.produto_id AS id, 
          p.nome AS nome, 
          p.RFID AS codigo, 
          e.quantidade AS estoque,
          'Geral' AS categoria, 
          0.00 AS preco
      FROM produto p
      INNER JOIN estoque e ON p.produto_id = e.produto_id
    `;
    const [linhas] = await db.query(queryBuscaTodos);
    return res.json(linhas);
  } catch (error) {
    console.error("Erro ao listar produtos:", error);
    return res.status(500).json({ success: false, message: `Erro interno: ${error.message}` });
  }
});

// ====== BUSCA DE PRODUTO ÚNICO ======
const processarBuscaProdutoUnico = async (req, res) => {
  const paramId = req.params.id;
  try {

    const queryBuscaCompleta = `
      SELECT 
        p.produto_id, 
        p.nome, 
        p.RFID, 
        e.quantidade AS estoque_minimo
      FROM produto p 
      INNER JOIN estoque e ON p.produto_id = e.produto_id 
      WHERE p.produto_id = ?
    `;

    const [linhas] = await db.query(queryBuscaCompleta, [paramId]);

    if (!linhas || linhas.length === 0) {
      return res.status(404).json({ message: 'Produto não encontrado no estoque!' });
    }

    return res.json(linhas[0]);
  } catch (error) {
    console.error("Erro ao carregar produto:", error);
    return res.status(500).json({ message: `Erro interno do servidor: ${error.message}` });
  }
};


app.get('/api/produtos/:id', processarBuscaProdutoUnico);
app.get('/produtos/:id', processarBuscaProdutoUnico);
app.get('/api/produto/:id', processarBuscaProdutoUnico);
app.get('/produto/:id', processarBuscaProdutoUnico);


const processarPedidoSaida = async (req, res) => {
  const { produto_id, quantidade, observacao, funcionario_id } = req.body;
  try {
    if (!produto_id || !quantidade) {
      return res.status(400).json({ success: false, message: 'Dados incompletos!' });
    }

    // 1. Descobre o estoque_id real atrelado a esse produto antes de inserir na movimentação
    const [estoqueLinhas] = await db.query('SELECT estoque_id FROM estoque WHERE produto_id = ?', [produto_id]);

    if (!estoqueLinhas || estoqueLinhas.length === 0) {
      return res.status(404).json({ success: false, message: 'Estoque não encontrado para este produto!' });
    }
    const estoque_id_real = estoqueLinhas[0].estoque_id;

    // 2. Subtrai do saldo real (tabela estoque)
    await db.query(
      'UPDATE estoque SET quantidade = quantidade - ? WHERE estoque_id = ?',
      [quantidade, estoque_id_real]
    );

    // 3. Salva na tabela movimentacao com dados blindados contra nulos
    await db.query(`
      INSERT INTO movimentacao (data_horamov, tipo_mov, quantidade, observacao, estoque_id, funcionario_id)
      VALUES (NOW(6), ?, ?, ?, ?, ?)`,
      [
        'saida',
        quantidade,
        observacao || 'Saída realizada pelo app',
        estoque_id_real,
        funcionario_id || 1
      ]
    );

    return res.json({ success: true, message: 'Saída registrada com sucesso no estoque e histórico!' });
  } catch (error) {
    console.error("Erro crítico ao salvar pedido de saída:", error);
    return res.status(500).json({ success: false, message: `Erro ao registrar: ${error.message}` });
  }
};

app.post('/pedido-saida', processarPedidoSaida);
app.post('/api/pedido-saida', processarPedidoSaida);


// ====== REGISTRO DE PEDIDO DE ENTRADA  ======
const processarPedidoEntrada = async (req, res) => {
  const { produto_id, quantidade, observacao, funcionario_id } = req.body;
  try {
    if (!produto_id || !quantidade) {
      return res.status(400).json({ success: false, message: 'Dados incompletos de produto ou quantidade!' });
    }

    // 1. Descobre o estoque_id real atrelado a esse produto
    const [estoqueLinhas] = await db.query('SELECT estoque_id FROM estoque WHERE produto_id = ?', [produto_id]);

    if (!estoqueLinhas || estoqueLinhas.length === 0) {
      return res.status(404).json({ success: false, message: 'Estoque não encontrado para este produto!' });
    }
    const estoque_id_real = estoqueLinhas[0].estoque_id;

    // 2. Soma no saldo real (tabela estoque)
    await db.query(
      'UPDATE estoque SET quantidade = quantidade + ? WHERE estoque_id = ?',
      [quantidade, estoque_id_real]
    );

    // 3. Salva na tabela movimentacao 
    await db.query(`
      INSERT INTO movimentacao (data_horamov, tipo_mov, quantidade, observacao, estoque_id, funcionario_id)
      VALUES (NOW(6), ?, ?, ?, ?, ?)`,
      [
        'entrada',
        quantidade,
        observacao || 'Entrada realizada pelo app',
        estoque_id_real,
        funcionario_id || 1
      ]
    );

    return res.json({
      success: true,
      message: 'Entrada registrada com sucesso no estoque e histórico!',
      tipo: 'entrada',
      produto_id: produto_id,
      quantidade: quantidade
    });


  } catch (error) {
    console.error("Erro crítico ao salvar pedido de entrada:", error);
    return res.status(500).json({ success: false, message: `Erro ao registrar entrada: ${error.message}` });
  }
};

app.post('/pedido-entrada', processarPedidoEntrada);
app.post('/api/pedido-entrada', processarPedidoEntrada);
app.post('/pedido-compra', processarPedidoEntrada);
app.post('/api/pedido-compra', processarPedidoEntrada);



app.get('/api/historico-completo', async (req, res) => {
  try {
    // 1. Conta o total de registros do tipo 'entrada' na tabela movimentacao
    const [[{ totalEntradas }]] = await db.query("SELECT COUNT(*) as totalEntradas FROM movimentacao WHERE tipo_mov = 'entrada'");

    // 2. Conta o total de registros do tipo 'saida' na tabela movimentacao
    const [[{ totalSaidas }]] = await db.query("SELECT COUNT(*) as totalSaidas FROM movimentacao WHERE tipo_mov = 'saida'");

    // 3. Busca todas as movimentações formatando a data e a hora separadamente para o front
    const queryHistorico = `
      SELECT 
        m.movimentacao_id AS id,
        m.tipo_mov AS tipo,          
        m.quantidade AS quantity, 
        p.nome AS product,
        DATE_FORMAT(m.data_horamov, '%d/%m/%Y') AS date,
        DATE_FORMAT(m.data_horamov, '%H:%i') AS hour
      FROM movimentacao m
      INNER JOIN estoque e
        ON m.estoque_id = e.estoque_id
      INNER JOIN produto p
        ON e.produto_id = p.produto_id
      ORDER BY m.data_horamov DESC
    `;

    const [linhas] = await db.query(queryHistorico);

    res.json({
      entradasContador: totalEntradas || 0,
      saidasContador: totalSaidas || 0,
      historicoLista: linhas || []
    });
  } catch (error) {
    console.error("Erro ao carregar histórico completo:", error);
    res.status(500).json({ error: error.message });
  }
});


// ====================================================== CADASTRAR NOVO PRODUTO ======================================================

const cadastrarProduto = async (req, res) => {
  const {
    nome,
    categoria,
    tipo_produto,
    estoque_minimo,
    validade,
    fornecedor,
    descricao,
    lote,
    localizacao,
    RFID,
    foto
  } = req.body;

  // VALIDAÇÕES

  if (!nome || !nome.trim()) {
    return res.status(400).json({
      success: false,
      message: 'O nome do produto é obrigatório.'
    });
  }

  if (!categoria || !categoria.trim()) {
    return res.status(400).json({
      success: false,
      message: 'A categoria é obrigatória.'
    });
  }

  if (!tipo_produto || !tipo_produto.trim()) {
    return res.status(400).json({
      success: false,
      message: 'O tipo do produto é obrigatório.'
    });
  }

  if (estoque_minimo === undefined || estoque_minimo === null || estoque_minimo === '') {
    return res.status(400).json({
      success: false,
      message: 'O estoque mínimo é obrigatório.'
    });
  }

  if (!lote || !lote.trim()) {
    return res.status(400).json({
      success: false,
      message: 'O lote é obrigatório.'
    });
  }

  if (!localizacao || !localizacao.trim()) {
    return res.status(400).json({
      success: false,
      message: 'A localização é obrigatória.'
    });
  }

  if (!RFID || !RFID.trim()) {
    return res.status(400).json({
      success: false,
      message: 'O RFID é obrigatório.'
    });
  }

  if (!descricao || !descricao.trim()) {
    return res.status(400).json({
      success: false,
      message: 'A descrição é obrigatória.'
    });
  }

  let conexao;

  try {

    conexao = await db.getConnection();

    await conexao.beginTransaction();

    //  CADASTRA O PRODUTO

    const sqlProduto = `
      INSERT INTO produto (
        nome,
        categoria,
        tipo_produto,
        estoque_minimo,
        validade,
        fornecedor,
        descricao,
        lote,
        localizacao,
        RFID,
        foto
      )
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;

    const [resultadoProduto] = await conexao.query(
      sqlProduto,
      [
        nome.trim(),
        categoria.trim(),
        tipo_produto.trim(),
        Number(estoque_minimo),
        validade || null,
        fornecedor ? fornecedor.trim() : null,
        descricao.trim(),
        lote.trim(),
        localizacao.trim(),
        RFID.trim(),
        foto || null
      ]
    );

    const produtoId = resultadoProduto.insertId;

    // CRIA O ESTOQUE DO PRODUTO

    const sqlEstoque = `
      INSERT INTO estoque (
        produto_id,
        quantidade
      )
      VALUES (?, ?)
    `;

    await conexao.query(
      sqlEstoque,
      [
        produtoId,
        0
      ]
    );


    await conexao.commit();

    return res.status(201).json({
      success: true,
      message: 'Produto cadastrado com sucesso!',
      produto_id: produtoId
    });

  } catch (error) {

    // Se alguma coisa der errado, desfaz o cadastro
    if (conexao) {
      await conexao.rollback();
    }

    console.error(
      'Erro ao cadastrar produto:',
      error
    );

    return res.status(500).json({
      success: false,
      message: `Erro ao cadastrar produto: ${error.message}`
    });

  } finally {

    if (conexao) {
      conexao.release();
    }

  }
};


// ====================================================== ROTAS DE CADASTRO ======================================================

app.post('/produto', cadastrarProduto);
app.post('/api/produto', cadastrarProduto);

const PORT = 3000;
app.listen(PORT, () => console.log(`Servidor rodando em http://localhost:${PORT}`));