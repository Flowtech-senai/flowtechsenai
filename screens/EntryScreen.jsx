import React, { useState, useEffect } from 'react';

import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  TextInput,
  ScrollView,
  Alert,
} from 'react-native';

import { Ionicons } from '@expo/vector-icons';
import api from '../src/services/api';

import { useTheme } from '../context/ThemeContext';

export default function EntryScreen() {
  // ==============================
  // TEMA
  // ==============================
  const { cores } = useTheme();

  // ==============================
  // ESTADOS
  // ==============================

  // Dados do produto vindo do banco
  const [dadosDoProduto, setDadosDoProduto] = useState(null);

  // Dados do formulário
  const [code, setCode] = useState('');
  const [quantidade, setQuantidade] = useState('');
  const [fornecedorNome, setFornecedorNome] = useState('');
  const [status, setStatus] = useState('Em andamento');
  const [descricao, setDescricao] = useState('');
  const [precoCusto, setPrecoCusto] = useState('');
  const [funcionarioNome, setFuncionarioNome] = useState('');

  // IDs temporários
  const FORNECEDOR_ID_PADRAO = 1;
  const FUNCIONARIO_ID_PADRAO = 1;

  // ============================== BUSCAR PRODUTO ========================
  

  const carregarProdutoDoBanco = async (idProduto) => {
    try {
      const response = await api.get(`/produtos/${idProduto}`);

      if (response.data) {
        setDadosDoProduto(response.data);

        setCode(
          response.data.RFID ||
          String(response.data.produto_id)
        );
      }
    } catch (error) {
      console.error(
        'Erro ao buscar produto do banco:',
        error
      );

      Alert.alert(
        'Erro',
        'Não foi possível carregar as informações do produto.'
      );
    }
  };

  // Carrega o produto 1 ao entrar na tela
  useEffect(() => {
    carregarProdutoDoBanco(1);
  }, []);

  // ============================== SALVAR ENTRADA =============================

  const handleSalvarEntrada = async () => {
    if (!quantidade || !precoCusto || !descricao) {
      Alert.alert(
        'Campos vazios',
        'Por favor, preencha a quantidade, o preço de custo e a descrição!'
      );
      return;
    }

    if (!dadosDoProduto) {
      Alert.alert(
        'Produto ausente',
        'Nenhum produto foi carregado para dar entrada.'
      );
      return;
    }

    try {
      const dataHoraAtual = new Date()
        .toISOString()
        .slice(0, 19)
        .replace('T', ' ');

      const response = await api.post('/pedido-entrada', {
        data_hora: dataHoraAtual,
        descricao: descricao,
        status_pedido: status,

        fornecedor_id: FORNECEDOR_ID_PADRAO,
        estoque_id: null,
        funcionario_id: FUNCIONARIO_ID_PADRAO,

        rfid: code,
        local_id: null,

        produto_id: dadosDoProduto.produto_id,

        preco_custo: parseFloat(
          String(precoCusto).replace(',', '.')
        ),

        quantidade: parseInt(quantidade),
      });

      console.log(
        'RESPOSTA DA ENTRADA:',
        response.data
      );

      if (
        response.data &&
        response.data.success === true
      ) {
        Alert.alert(
          'Sucesso',
          'Entrada de estoque cadastrada com sucesso!'
        );

        // Limpa os campos
        setQuantidade('');
        setPrecoCusto('');
        setDescricao('');
      }
    } catch (error) {
      console.error(
        'Erro ao salvar entrada:',
        error
      );

      Alert.alert(
        'Erro de Cadastro',
        error.response?.data?.message ||
          'Não foi possível salvar os dados no servidor.'
      );
    }
  };

  // ============================== CÁLCULO DO VALOR TOTAL =================================

  const qtd = parseFloat(quantidade) || 0;

  const precoLimpo = precoCusto
    ? String(precoCusto).replace(',', '.')
    : '0';

  const preco = parseFloat(precoLimpo) || 0;

  const valorTotal = qtd * preco;

  // ============================== TELA =====================================

  return (
    <ScrollView
      style={[
        styles.container,
        {
          backgroundColor: cores.fundo,
        },
      ]}
      contentContainerStyle={styles.scrollContent}
      showsVerticalScrollIndicator={false}
    >
      <View style={{ height: 40 }} />

      {/* ============================== HEADER ==============================*/}

      <View style={styles.header}>
        <Text
          style={[
            styles.title,
            {
              color: cores.texto,
            },
          ]}
        >
          Entrada de Estoque
        </Text>

        <Text
          style={[
            styles.subtitle,
            {
              color: cores.textoSecundario,
            },
          ]}
        >
          Registre produtos rapidamente
        </Text>
      </View>

      {/* ============================== QR CODE ============================== */}

      <TouchableOpacity
        style={[
          styles.qrButton,
          {
            backgroundColor: cores.azul,
          },
        ]}
        onPress={() => carregarProdutoDoBanco(1)}
      >
        <View style={styles.qrContent}>
          <Ionicons
            name="qr-code-outline"
            size={32}
            color="#FFFFFF"
          />

          <View>
            <Text style={styles.qrTitle}>
              Ler QR Code
            </Text>

            <Text
              style={[
                styles.qrSubtitle,
                {
                  color: '#E2E8F0',
                },
              ]}
            >
              Escanear produto
            </Text>
          </View>
        </View>

        <Ionicons
          name="chevron-forward"
          size={22}
          color="#FFFFFF"
        />
      </TouchableOpacity>

      {/* ============================== PRODUTO ENCONTRADO ============================== */}

      <Text
        style={[
          styles.sectionTitle,
          {
            color: cores.textoSecundario,
          },
        ]}
      >
        Produto Encontrado
      </Text>

      <View
        style={[
          styles.productCard,
          {
            backgroundColor: cores.card,
          },
        ]}
      >
        <View
          style={[
            styles.productIcon,
            {
              backgroundColor:
                cores.modo === 'claro'
                  ? '#DBEAFE'
                  : '#1E3A8A',
            },
          ]}
        >
          <Ionicons
            name="cube"
            size={28}
            color={cores.azul}
          />
        </View>

        <View style={{ flex: 1 }}>
          <Text
            style={[
              styles.productName,
              {
                color: cores.texto,
              },
            ]}
          >
            {dadosDoProduto
              ? dadosDoProduto.nome
              : 'Buscando produto do banco...'}
          </Text>

          <Text
            style={[
              styles.productCode,
              {
                color: cores.textoSecundario,
              },
            ]}
          >
            Código: {code || '---'}
          </Text>

          <Text
            style={[
              styles.productStock,
              {
                color: cores.alerta,
              },
            ]}
          >
            Estoque Mínimo Cadastrado:{' '}
            {dadosDoProduto
              ? dadosDoProduto.estoque_minimo
              : '---'}
          </Text>
        </View>
      </View>

      {/* ============================== PEDIDO DE ENTRADA ============================== */}

      <View
        style={[
          styles.summaryCard,
          {
            backgroundColor: cores.card,
          },
        ]}
      >
        <Text
          style={[
            styles.summaryTitle,
            {
              color: cores.texto,
              borderColor: cores.borda,
            },
          ]}
        >
          Pedido Entrada
        </Text>

        {/* FORNECEDOR */}

        <Text
          style={[
            styles.sectionTitle,
            {
              color: cores.textoSecundario,
            },
          ]}
        >
          Fornecedor
        </Text>

        <TextInput
          style={[
            styles.input,
            {
              backgroundColor: cores.input,
              color: cores.texto,
              borderColor: cores.borda,
            },
          ]}
          placeholder="Digite o nome do fornecedor"
          placeholderTextColor={cores.textoSecundario}
          value={fornecedorNome}
          onChangeText={setFornecedorNome}
        />

        {/* DESCRIÇÃO */}

        <Text
          style={[
            styles.sectionTitle,
            {
              color: cores.textoSecundario,
            },
          ]}
        >
          Descrição do Pedido *
        </Text>

        <TextInput
          style={[
            styles.input,
            styles.descriptionInput,
            {
              backgroundColor: cores.input,
              color: cores.texto,
              borderColor: cores.borda,
            },
          ]}
          placeholder="Escreva a descrição aqui..."
          placeholderTextColor={cores.textoSecundario}
          multiline
          value={descricao}
          onChangeText={setDescricao}
        />

        {/* STATUS */}

        <Text
          style={[
            styles.sectionTitle,
            {
              color: cores.textoSecundario,
            },
          ]}
        >
          Status do Pedido
        </Text>

        <View style={styles.statusContainer}>
          {[
            'Em andamento',
            'Finalizado',
            'Cancelado',
          ].map((opcao) => {
            const selecionado = status === opcao;

            return (
              <TouchableOpacity
                key={opcao}
                onPress={() => setStatus(opcao)}
                style={[
                  styles.statusButton,
                  {
                    backgroundColor: selecionado
                      ? cores.sucesso
                      : cores.input,
                    borderColor: selecionado
                      ? cores.sucesso
                      : cores.borda,
                  },
                ]}
              >
                <Text
                  style={[
                    styles.statusText,
                    {
                      color: selecionado
                        ? '#FFFFFF'
                        : cores.textoSecundario,
                    },
                  ]}
                >
                  {opcao}
                </Text>
              </TouchableOpacity>
            );
          })}
        </View>

        {/* FUNCIONÁRIO */}

        <Text
          style={[
            styles.sectionTitle,
            {
              color: cores.textoSecundario,
            },
          ]}
        >
          Funcionário
        </Text>

        <TextInput
          style={[
            styles.input,
            {
              backgroundColor: cores.input,
              color: cores.texto,
              borderColor: cores.borda,
            },
          ]}
          placeholder="Digite o nome do funcionário"
          placeholderTextColor={cores.textoSecundario}
          value={funcionarioNome}
          onChangeText={setFuncionarioNome}
        />
      </View>

      {/* ============================== ITENS DO PEDIDO ============================== */}

      <View
        style={[
          styles.summaryCard,
          {
            backgroundColor: cores.card,
          },
        ]}
      >
        <Text
          style={[
            styles.summaryTitle,
            {
              color: cores.texto,
              borderColor: cores.borda,
            },
          ]}
        >
          Itens do Pedido Entrada
        </Text>

        {/* PREÇO */}

        <Text
          style={[
            styles.sectionTitle,
            {
              color: cores.textoSecundario,
            },
          ]}
        >
          Preço de Custo *
        </Text>

        <TextInput
          style={[
            styles.input,
            {
              backgroundColor: cores.input,
              color: cores.texto,
              borderColor: cores.borda,
            },
          ]}
          placeholder="Ex: 5,50"
          placeholderTextColor={cores.textoSecundario}
          keyboardType="decimal-pad"
          value={precoCusto}
          onChangeText={setPrecoCusto}
        />

        {/* QUANTIDADE */}

        <Text
          style={[
            styles.sectionTitle,
            {
              color: cores.textoSecundario,
            },
          ]}
        >
          Quantidade *
        </Text>

        <TextInput
          style={[
            styles.input,
            {
              backgroundColor: cores.input,
              color: cores.texto,
              borderColor: cores.borda,
            },
          ]}
          placeholder="Ex: 10"
          placeholderTextColor={cores.textoSecundario}
          keyboardType="number-pad"
          value={quantidade}
          onChangeText={setQuantidade}
        />

        {/* VALOR TOTAL */}

        <View
          style={[
            styles.totalContainer,
            {
              borderColor: cores.borda,
            },
          ]}
        >
          <Text
            style={[
              styles.totalLabel,
              {
                color: cores.textoSecundario,
              },
            ]}
          >
            Valor Total Estimado:
          </Text>

          <Text
            style={[
              styles.totalValue,
              {
                color: cores.sucesso,
              },
            ]}
          >
            R${' '}
            {valorTotal
              .toFixed(2)
              .replace('.', ',')}
          </Text>
        </View>
      </View>

      {/* ============================== BOTÃO SALVAR ============================== */}

      <TouchableOpacity
        style={[
          styles.saveButton,
          {
            backgroundColor: cores.sucesso,
          },
        ]}
        onPress={handleSalvarEntrada}
      >
        <Ionicons
          name="checkmark-circle-outline"
          size={22}
          color="#FFFFFF"
        />

        <Text style={styles.saveButtonText}>
          Confirmar Entrada de Estoque
        </Text>
      </TouchableOpacity>

      <View style={{ height: 40 }} />
    </ScrollView>
  );
}

// ======================================= ESTILOS =================================

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 16,
  },

  scrollContent: {
    paddingBottom: 20,
  },

  header: {
    marginBottom: 20,
  },

  title: {
    fontSize: 24,
    fontWeight: 'bold',
  },

  subtitle: {
    fontSize: 14,
    marginTop: 4,
  },

  // ============================== QR CODE ===================================

  qrButton: {
    flexDirection: 'row',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 20,
  },

  qrContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },

  qrTitle: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },

  qrSubtitle: {
    fontSize: 12,
    marginTop: 2,
  },

  // ============================== PRODUTO =====================================

  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    marginTop: 15,
    marginBottom: 8,
  },

  productCard: {
    flexDirection: 'row',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    gap: 12,
    marginBottom: 15,
  },

  productIcon: {
    padding: 10,
    borderRadius: 8,
  },

  productName: {
    fontSize: 16,
    fontWeight: 'bold',
  },

  productCode: {
    fontSize: 13,
    marginTop: 2,
  },

  productStock: {
    fontSize: 13,
    marginTop: 4,
  },

  // ============================== CARDS ========================================

  summaryCard: {
    padding: 16,
    borderRadius: 12,
    marginBottom: 15,
  },

  summaryTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    borderBottomWidth: 1,
    paddingBottom: 8,
  },

  // ============================== INPUTS =======================================

  input: {
    padding: 12,
    borderRadius: 8,
    fontSize: 14,
    marginTop: 5,
    borderWidth: 1,
  },

  descriptionInput: {
    height: 80,
    textAlignVertical: 'top',
  },

  // ============================== STATUS ====================================

  statusContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 10,
  },

  statusButton: {
    flex: 1,
    minHeight: 44,
    marginHorizontal: 4,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    paddingHorizontal: 4,
  },

  statusText: {
    fontSize: 11,
    fontWeight: '600',
    textAlign: 'center',
  },

  // ============================== TOTAL =====================================

  totalContainer: {
    marginTop: 15,
    borderTopWidth: 1,
    paddingTop: 15,
  },

  totalLabel: {
    fontSize: 14,
  },

  totalValue: {
    fontSize: 24,
    fontWeight: 'bold',
    marginTop: 4,
  },

  // ============================== BOTÃO SALVAR ======================================

  saveButton: {
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 10,
    flexDirection: 'row',
    gap: 8,
  },

  saveButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
});