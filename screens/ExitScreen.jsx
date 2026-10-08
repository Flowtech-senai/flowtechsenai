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


export default function ExitScreen() {

  // =====================================================
  // TEMA GLOBAL
  // =====================================================

  const { cores } = useTheme();


  // =====================================================
  // ESTADOS DO PRODUTO
  // =====================================================

  const [dadosDoProduto, setDadosDoProduto] = useState(null);

  const [code, setCode] = useState('');


  // =====================================================
  // ESTADOS DO FORMULÁRIO
  // =====================================================

  const [quantidade, setQuantidade] = useState('');

  const [destinoCliente, setDestinoCliente] = useState('');

  const [status, setStatus] =
    useState('Em andamento');

  const [descricao, setDescricao] = useState('');

  const [precoVenda, setPrecoVenda] = useState('');

  const [funcionarioNome, setFuncionarioNome] =
    useState('');


  // =====================================================
  // IDs PADRÃO
  // =====================================================

  const CLIENTE_ID_PADRAO = 1;

  const ESTOQUE_ID_PADRAO = 1;

  const FUNCIONARIO_ID_PADRAO = 1;


  // =====================================================
  // CARREGAR PRODUTO
  // =====================================================

  const carregarProdutoDoBanco = async (idProduto) => {

    try {

      const response =
        await api.get(`/produtos/${idProduto}`);

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
        'Não foi possível carregar o produto.'
      );

    }

  };


  useEffect(() => {

    carregarProdutoDoBanco(1);

  }, []);


  // =====================================================
  // CONFIRMAR SAÍDA
  // =====================================================

  const handleConfirmarSaida = async () => {

    if (
      !quantidade ||
      !precoVenda ||
      !descricao
    ) {

      Alert.alert(
        'Campos vazios',
        'Por favor, preencha a quantidade, o preço de venda e a descrição!'
      );

      return;

    }


    if (!dadosDoProduto) {

      Alert.alert(
        'Erro',
        'Nenhum produto selecionado.'
      );

      return;

    }


    try {

      const dataHoraAtual =
        new Date()
          .toISOString()
          .slice(0, 19)
          .replace('T', ' ');


      const response = await api.post(
        '/pedido-saida',
        {

          data_hora: dataHoraAtual,

          status_pedido: status,

          descricao: descricao,

          rfid: code,

          cliente_id: CLIENTE_ID_PADRAO,

          local_id: null,

          estoque_id: ESTOQUE_ID_PADRAO,

          funcionario_id:
            FUNCIONARIO_ID_PADRAO,

          quantidade:
            parseInt(quantidade),

          preco_venda:
            parseFloat(
              precoVenda.replace(',', '.')
            ),

          produto_id:
            dadosDoProduto.produto_id,

        }
      );


      if (
        response.data &&
        response.data.success === true
      ) {

        Alert.alert(
          'Sucesso',
          'Saída de estoque registrada perfeitamente!'
        );

        setQuantidade('');

        setPrecoVenda('');

        setDescricao('');

      }

    } catch (error) {

      console.error(
        'Erro ao salvar saída:',
        error
      );

      Alert.alert(
        'Erro',
        error.response?.data?.message ||
        'Não foi possível registrar no banco.'
      );

    }

  };


  // =====================================================
  // CÁLCULOS
  // =====================================================

  const qtdDigitada =
    parseInt(quantidade) || 0;


  const estoqueAtualBanco =
    dadosDoProduto
      ? dadosDoProduto.estoque_minimo
      : 15;


  const precovendaNum =
    parseFloat(
      precoVenda.replace(',', '.')
    ) || 0;


  const estoqueRestante =
    estoqueAtualBanco - qtdDigitada;


  // =====================================================
  // RENDER
  // =====================================================

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

      {/* ================================================= */}
      {/* TÍTULO */}
      {/* ================================================= */}

      <Text
        style={[
          styles.title,
          {
            color: cores.texto,
          },
        ]}
      >
        Saída de Estoque
      </Text>


      {/* ================================================= */}
      {/* ESCANEAR */}
      {/* ================================================= */}

      <TouchableOpacity
        style={[
          styles.qrButton,
          {
            backgroundColor: cores.erro,
          },
        ]}
        onPress={() =>
          carregarProdutoDoBanco(1)
        }
      >

        <Ionicons
          name="qr-code-outline"
          size={28}
          color="#FFFFFF"
        />

        <Text style={styles.qrText}>
          Escanear Produto
        </Text>

      </TouchableOpacity>


      {/* ================================================= */}
      {/* PRODUTO */}
      {/* ================================================= */}

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
            borderColor: cores.borda,
          },
        ]}
      >

        <View style={styles.productIcon}>

          <Ionicons
            name="cube"
            size={28}
            color={cores.azul}
          />

        </View>


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
            : 'Carregando...'}
        </Text>


        <Text
          style={[
            styles.stock,
            {
              color:
                estoqueRestante < 0
                  ? cores.erro
                  : cores.sucesso,
            },
          ]}
        >
          Estoque Atual: {estoqueAtualBanco}
        </Text>

      </View>


      {/* ================================================= */}
      {/* PEDIDO SAÍDA */}
      {/* ================================================= */}

      <View
        style={[
          styles.summaryCard,
          {
            backgroundColor: cores.card,
            borderColor: cores.borda,
          },
        ]}
      >

        <Text
          style={[
            styles.summaryTitle,
            {
              color: cores.texto,
            },
          ]}
        >
          Pedido Saída
        </Text>


        {/* DESTINO */}

        <Text
          style={[
            styles.sectionTitle,
            {
              color: cores.textoSecundario,
            },
          ]}
        >
          Destino / Cliente
        </Text>


        <TextInput
          style={[
            styles.input,
            {
              backgroundColor: cores.input,
              borderColor: cores.borda,
              color: cores.texto,
            },
          ]}
          placeholder="Digite o destino ou nome do cliente"
          placeholderTextColor={
            cores.textoSecundario
          }
          value={destinoCliente}
          onChangeText={setDestinoCliente}
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
          Descrição *
        </Text>


        <TextInput
          style={[
            styles.input,
            styles.descriptionInput,
            {
              backgroundColor: cores.input,
              borderColor: cores.borda,
              color: cores.texto,
            },
          ]}
          placeholder="Escreva o motivo da saída obrigatório aqui..."
          multiline={true}
          placeholderTextColor={
            cores.textoSecundario
          }
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
          ].map((opcao) => (

            <TouchableOpacity
              key={opcao}
              onPress={() =>
                setStatus(opcao)
              }
              style={[
                styles.statusTabButton,
                {
                  backgroundColor:
                    status === opcao
                      ? cores.primaria
                      : cores.cardSecundario,
                  borderColor:
                    cores.borda,
                },
              ]}
            >

              <Text
                style={[
                  styles.statusText,
                  {
                    color:
                      status === opcao
                        ? '#FFFFFF'
                        : cores.textoSecundario,
                  },
                ]}
              >
                {opcao}
              </Text>

            </TouchableOpacity>

          ))}

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
              borderColor: cores.borda,
              color: cores.texto,
            },
          ]}
          placeholder="Digite o nome do funcionário"
          placeholderTextColor={
            cores.textoSecundario
          }
          value={funcionarioNome}
          onChangeText={setFuncionarioNome}
        />

      </View>


      {/* ================================================= */}
      {/* ITENS DO PEDIDO */}
      {/* ================================================= */}

      <View
        style={[
          styles.summaryCard,
          {
            backgroundColor: cores.card,
            borderColor: cores.borda,
          },
        ]}
      >

        <Text
          style={[
            styles.summaryTitle,
            {
              color: cores.texto,
            },
          ]}
        >
          Itens do Pedido Saída
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
          Preço de Venda *
        </Text>


        <TextInput
          style={[
            styles.input,
            {
              backgroundColor: cores.input,
              borderColor: cores.borda,
              color: cores.texto,
            },
          ]}
          placeholder="Ex: 35,00"
          placeholderTextColor={
            cores.textoSecundario
          }
          keyboardType="decimal-pad"
          value={precoVenda}
          onChangeText={setPrecoVenda}
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
              borderColor: cores.borda,
              color: cores.texto,
            },
          ]}
          placeholder="Digite a quantidade de saída"
          placeholderTextColor={
            cores.textoSecundario
          }
          keyboardType="numeric"
          value={quantidade}
          onChangeText={setQuantidade}
        />

      </View>


      {/* ================================================= */}
      {/* RESUMO */}
      {/* ================================================= */}

      <View
        style={[
          styles.summaryCard,
          {
            backgroundColor: cores.card,
            borderColor: cores.borda,
          },
        ]}
      >

        <Text
          style={[
            styles.summaryTitle,
            {
              color: cores.texto,
            },
          ]}
        >
          Resumo da Saída
        </Text>


        <View style={styles.summaryRow}>

          <Text
            style={[
              styles.summaryLabel,
              {
                color: cores.textoSecundario,
              },
            ]}
          >
            Produto
          </Text>


          <Text
            style={[
              styles.summaryValue,
              {
                color: cores.texto,
              },
            ]}
          >
            {dadosDoProduto
              ? dadosDoProduto.nome
              : 'Nenhum'}
          </Text>

        </View>


        <View style={styles.summaryRow}>

          <Text
            style={[
              styles.summaryLabel,
              {
                color: cores.textoSecundario,
              },
            ]}
          >
            Quantidade
          </Text>


          <Text
            style={[
              styles.summaryValue,
              {
                color: cores.texto,
              },
            ]}
          >
            {qtdDigitada}
          </Text>

        </View>


        {/* ESTOQUE RESTANTE */}

        <View
          style={[
            styles.resultCard,
            {
              backgroundColor:
                cores.cardSecundario,
              borderColor: cores.borda,
            },
          ]}
        >

          <Text
            style={[
              styles.resultText,
              {
                color: cores.texto,
              },
            ]}
          >
            Estoque Restante
          </Text>


          <Text
            style={[
              styles.resultValue,
              {
                color:
                  estoqueRestante < 0
                    ? cores.erro
                    : cores.sucesso,
              },
            ]}
          >
            {estoqueRestante}
          </Text>

        </View>


        {/* VALOR TOTAL */}

        <View style={styles.summaryRow}>

          <Text
            style={[
              styles.summaryLabel,
              {
                color: cores.textoSecundario,
              },
            ]}
          >
            Valor Total do Pedido:
          </Text>


          <Text
            style={[
              styles.summaryValue,
              {
                color: cores.sucesso,
                fontSize: 16,
              },
            ]}
          >
            R$ {
              (precovendaNum * qtdDigitada)
                .toFixed(2)
                .replace('.', ',')
            }
          </Text>

        </View>

      </View>


      {/* ================================================= */}
      {/* CONFIRMAR */}
      {/* ================================================= */}

      <TouchableOpacity
        style={[
          styles.confirmButton,
          {
            backgroundColor: cores.erro,
          },
        ]}
        onPress={handleConfirmarSaida}
      >

        <Ionicons
          name="remove-circle"
          size={24}
          color="#FFFFFF"
        />

        <Text style={styles.confirmText}>
          Confirmar Saída
        </Text>

      </TouchableOpacity>


      <View style={{ height: 30 }} />

    </ScrollView>

  );
}


// =====================================================
// ESTILOS
// =====================================================

const styles = StyleSheet.create({

  container: {
    flex: 1,
    paddingHorizontal: 20,
  },

  scrollContent: {
    paddingBottom: 60,
  },


  // ===================================================
  // TÍTULO
  // ===================================================

  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginTop: 40,
    marginBottom: 20,
  },


  // ===================================================
  // QR
  // ===================================================

  qrButton: {
    height: 60,
    borderRadius: 16,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 10,
    marginBottom: 10,
  },

  qrText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },


  // ===================================================
  // PRODUTO
  // ===================================================

  productCard: {
    borderRadius: 16,
    borderWidth: 1,
    padding: 20,
    marginTop: 10,
    alignItems: 'center',
  },

  productIcon: {
    alignItems: 'center',
  },

  productName: {
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 10,
    textAlign: 'center',
  },

  stock: {
    marginTop: 6,
    fontWeight: 'bold',
    fontSize: 14,
    textAlign: 'center',
  },


  // ===================================================
  // SEÇÕES
  // ===================================================

  sectionTitle: {
    fontSize: 13,
    fontWeight: 'bold',
    textTransform: 'uppercase',
    marginTop: 16,
    marginBottom: 6,
  },


  // ===================================================
  // INPUT
  // ===================================================

  input: {
    height: 50,
    borderRadius: 10,
    borderWidth: 1,
    paddingHorizontal: 15,
    fontSize: 15,
    marginBottom: 5,
  },

  descriptionInput: {
    height: 100,
    textAlignVertical: 'top',
    paddingTop: 14,
  },


  // ===================================================
  // CARDS
  // ===================================================

  summaryCard: {
    borderRadius: 16,
    borderWidth: 1,
    padding: 20,
    marginTop: 15,
  },

  summaryTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 5,
  },


  // ===================================================
  // STATUS
  // ===================================================

  statusContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 10,
  },

  statusTabButton: {
    flex: 1,
    height: 40,
    marginHorizontal: 4,
    borderRadius: 8,
    borderWidth: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },

  statusText: {
    fontWeight: 'bold',
    fontSize: 12,
    textAlign: 'center',
  },


  // ===================================================
  // RESUMO
  // ===================================================

  summaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginVertical: 4,
  },

  summaryLabel: {
    fontSize: 14,
    flex: 1,
  },

  summaryValue: {
    fontSize: 14,
    fontWeight: 'bold',
    textAlign: 'right',
    flexShrink: 1,
  },


  // ===================================================
  // ESTOQUE RESTANTE
  // ===================================================

  resultCard: {
    padding: 12,
    borderRadius: 10,
    borderWidth: 1,
    marginVertical: 8,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },

  resultText: {
    fontSize: 14,
  },

  resultValue: {
    fontSize: 16,
    fontWeight: 'bold',
  },


  // ===================================================
  // CONFIRMAR
  // ===================================================

  confirmButton: {
    height: 55,
    borderRadius: 12,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 10,
    marginTop: 25,
    marginBottom: 30,
  },

  confirmText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },

});