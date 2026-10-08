import React, { useState, useCallback } from 'react';

import {
  View,
  Text,
  StyleSheet,
  FlatList,
  Image,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Alert,
} from 'react-native';

import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';

import api from '../src/services/api';
import { useTheme } from '../context/ThemeContext';

export default function ProductsScreen() {

  const { cores } = useTheme();

  // ============================== ESTADOS ==============================

  const [search, setSearch] = useState('');
  const [produto, setProducts] = useState([]);

  const [mostrarCadastro, setMostrarCadastro] = useState(false);

  const [nome, setNome] = useState('');
  const [categoria, setCategoria] = useState('');
  const [tipoProduto, setTipoProduto] = useState('');
  const [estoqueMinimo, setEstoqueMinimo] = useState('');
  const [validade, setValidade] = useState('');
  const [fornecedor, setFornecedor] = useState('');
  const [descricao, setDescricao] = useState('');
  const [lote, setLote] = useState('');
  const [localizacao, setLocalizacao] = useState('');
  const [rfid, setRfid] = useState('');

  // ============================== CARREGAR PRODUTOS ==============================

  const loadProducts = async () => {
    try {
      const response = await api
        .get('/produto')
        .catch(() => api.get('/api/produto'));

      setProducts(response.data || []);

    } catch (error) {
      console.log(
        'Erro ao buscar produtos:',
        error
      );
    }
  };

  useFocusEffect(
    useCallback(() => {
      loadProducts();
    }, [])
  );

  // ============================== CADASTRAR PRODUTO ==============================

  const cadastrarProduto = async () => {

    if (!nome.trim()) {
      Alert.alert('Atenção', 'Informe o nome do produto.');
      return;
    }

    if (!categoria.trim()) {
      Alert.alert('Atenção', 'Informe a categoria.');
      return;
    }

    if (!tipoProduto.trim()) {
      Alert.alert('Atenção', 'Informe o tipo do produto.');
      return;
    }

    if (!estoqueMinimo) {
      Alert.alert('Atenção', 'Informe o estoque mínimo.');
      return;
    }

    if (!lote.trim()) {
      Alert.alert('Atenção', 'Informe o lote.');
      return;
    }

    if (!localizacao.trim()) {
      Alert.alert('Atenção', 'Informe a localização.');
      return;
    }

    if (!rfid.trim()) {
      Alert.alert('Atenção', 'Informe o RFID.');
      return;
    }

    if (!descricao.trim()) {
      Alert.alert('Atenção', 'Informe a descrição.');
      return;
    }

    try {

      const dados = {
        nome: nome.trim(),
        categoria: categoria.trim(),
        tipo_produto: tipoProduto.trim(),
        estoque_minimo: Number(estoqueMinimo),
        validade: validade || null,
        fornecedor: fornecedor.trim(),
        descricao: descricao.trim(),
        lote: lote.trim(),
        localizacao: localizacao.trim(),
        RFID: rfid.trim(),
        foto: null,
      };

      console.log('Enviando produto:', dados);

      await api.post('/produto', dados);

      Alert.alert(
        'Sucesso',
        'Produto cadastrado com sucesso!'
      );

      // Limpar formulário
      setNome('');
      setCategoria('');
      setTipoProduto('');
      setEstoqueMinimo('');
      setValidade('');
      setFornecedor('');
      setDescricao('');
      setLote('');
      setLocalizacao('');
      setRfid('');

      // Fechar cadastro
      setMostrarCadastro(false);

      // Atualizar lista
      loadProducts();

    } catch (error) {

      console.log(
        'Erro ao cadastrar:',
        error?.response?.data || error
      );

      Alert.alert(
        'Erro',
        error?.response?.data?.message ||
        error?.response?.data?.erro ||
        'Não foi possível cadastrar o produto.'
      );
    }
  };

  // ============================== FILTRO ==============================

  const filteredProducts = Array.isArray(produto)
    ? produto.filter((item) => {

        const textoBusca = search.toLowerCase();

        return (
          item.nome
            ?.toLowerCase()
            .includes(textoBusca) ||

          item.categoria
            ?.toLowerCase()
            .includes(textoBusca)
        );
      })
    : [];

  // ====================================================================
  // ============================== CADASTRO =============================
  // ====================================================================

  if (mostrarCadastro) {

    return (
      <View
        style={[
          styles.container,
          {
            backgroundColor: cores.fundo,
          },
        ]}
      >

        <ScrollView
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.cadastroScroll}
        >

          {/* ================= CABEÇALHO ================= */}

          <View style={styles.cadastroHeader}>

            <View style={{ flex: 1 }}>

              <Text
                style={[
                  styles.cadastroTitle,
                  {
                    color: cores.texto,
                  },
                ]}
              >
                Novo produto
              </Text>

              <Text
                style={[
                  styles.cadastroSubtitle,
                  {
                    color: cores.textoSecundario,
                  },
                ]}
              >
                Cadastre um novo produto
              </Text>

            </View>

            <TouchableOpacity
              style={styles.closeButton}
              onPress={() => setMostrarCadastro(false)}
            >
              <Ionicons
                name="close"
                size={30}
                color={cores.texto}
              />
            </TouchableOpacity>

          </View>

          {/* ================= NOME ================= */}

          <Text
            style={[
              styles.label,
              {
                color: cores.texto,
              },
            ]}
          >
            Nome do produto
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
            placeholder="Ex: Dipirona"
            placeholderTextColor={cores.textoSecundario}
            value={nome}
            onChangeText={setNome}
          />

          {/* ================= CATEGORIA ================= */}

          <Text
            style={[
              styles.label,
              {
                color: cores.texto,
              },
            ]}
          >
            Categoria
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
            placeholder="Ex: Medicamento"
            placeholderTextColor={cores.textoSecundario}
            value={categoria}
            onChangeText={setCategoria}
          />

          {/* ================= TIPO ================= */}

          <Text
            style={[
              styles.label,
              {
                color: cores.texto,
              },
            ]}
          >
            Tipo de produto
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
            placeholder="Ex: Comprimido"
            placeholderTextColor={cores.textoSecundario}
            value={tipoProduto}
            onChangeText={setTipoProduto}
          />

          {/* ================= ESTOQUE MÍNIMO ================= */}

          <Text
            style={[
              styles.label,
              {
                color: cores.texto,
              },
            ]}
          >
            Estoque mínimo
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
            placeholder="Ex: 10"
            placeholderTextColor={cores.textoSecundario}
            keyboardType="numeric"
            value={estoqueMinimo}
            onChangeText={setEstoqueMinimo}
          />

          {/* ================= VALIDADE ================= */}

          <Text
            style={[
              styles.label,
              {
                color: cores.texto,
              },
            ]}
          >
            Validade
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
            placeholder="AAAA-MM-DD"
            placeholderTextColor={cores.textoSecundario}
            value={validade}
            onChangeText={setValidade}
          />

          {/* ================= FORNECEDOR ================= */}

          <Text
            style={[
              styles.label,
              {
                color: cores.texto,
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
                borderColor: cores.borda,
                color: cores.texto,
              },
            ]}
            placeholder="Nome do fornecedor"
            placeholderTextColor={cores.textoSecundario}
            value={fornecedor}
            onChangeText={setFornecedor}
          />

          {/* ================= LOTE ================= */}

          <Text
            style={[
              styles.label,
              {
                color: cores.texto,
              },
            ]}
          >
            Lote
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
            placeholder="Ex: LOTE001"
            placeholderTextColor={cores.textoSecundario}
            value={lote}
            onChangeText={setLote}
          />

          {/* ================= LOCALIZAÇÃO ================= */}

          <Text
            style={[
              styles.label,
              {
                color: cores.texto,
              },
            ]}
          >
            Localização
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
            placeholder="Ex: A-02"
            placeholderTextColor={cores.textoSecundario}
            value={localizacao}
            onChangeText={setLocalizacao}
          />

          {/* ================= RFID ================= */}

          <Text
            style={[
              styles.label,
              {
                color: cores.texto,
              },
            ]}
          >
            RFID
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
            placeholder="Ex: RFID-DIP-001"
            placeholderTextColor={cores.textoSecundario}
            value={rfid}
            onChangeText={setRfid}
          />

          {/* ================= DESCRIÇÃO ================= */}

          <Text
            style={[
              styles.label,
              {
                color: cores.texto,
              },
            ]}
          >
            Descrição
          </Text>

          <TextInput
            style={[
              styles.input,
              styles.descricaoInput,
              {
                backgroundColor: cores.input,
                borderColor: cores.borda,
                color: cores.texto,
              },
            ]}
            placeholder="Descrição do produto"
            placeholderTextColor={cores.textoSecundario}
            multiline
            value={descricao}
            onChangeText={setDescricao}
          />

          {/* ================= BOTÃO ================= */}

          <TouchableOpacity
            style={[
              styles.cadastrarButton,
              {
                backgroundColor: cores.primaria,
              },
            ]}
            onPress={cadastrarProduto}
          >

            <Ionicons
              name="add-circle-outline"
              size={22}
              color="#FFFFFF"
            />

            <Text style={styles.cadastrarButtonText}>
              Cadastrar produto
            </Text>

          </TouchableOpacity>

        </ScrollView>

      </View>
    );
  }

  // ====================================================================
  // ============================== LISTA ================================
  // ====================================================================

  return (
    <View
      style={[
        styles.container,
        {
          backgroundColor: cores.fundo,
        },
      ]}
    >

      {/* ================= CABEÇALHO ================= */}

      <View style={styles.header}>

        <View style={{ flex: 1 }}>

          <Text
            style={[
              styles.title,
              {
                color: cores.texto,
              },
            ]}
          >
            Produtos
          </Text>

          <Text
            style={[
              styles.subtitle,
              {
                color: cores.textoSecundario,
              },
            ]}
          >
            Consulte os produtos cadastrados
          </Text>

        </View>

        {/* BOTÃO + */}

        <TouchableOpacity
          style={[
            styles.filterButton,
            {
              backgroundColor: cores.primariaEscura,
            },
          ]}
          onPress={() => {
            setMostrarCadastro(true);
          }}
        >

          <Ionicons
            name="add"
            size={30}
            color="#FFFFFF"
          />

        </TouchableOpacity>

      </View>

      {/* ================= PESQUISA ================= */}

      <View
        style={[
          styles.searchContainer,
          {
            backgroundColor: cores.input,
            borderColor: cores.borda,
          },
        ]}
      >

        <Ionicons
          name="search-outline"
          size={22}
          color={cores.primariaEscura}
        />

        <TextInput
          style={[
            styles.searchInput,
            {
              color: cores.texto,
            },
          ]}
          placeholder="Pesquisar produtos..."
          placeholderTextColor={cores.textoSecundario}
          value={search}
          onChangeText={setSearch}
        />

      </View>

      {/* ================= LISTA ================= */}

      <FlatList
        data={filteredProducts}

        keyExtractor={(item, index) =>
          item.produto_id?.toString() ||
          item.id?.toString() ||
          index.toString()
        }

        showsVerticalScrollIndicator={false}

        contentContainerStyle={{
          paddingBottom: 40,
        }}

        ListEmptyComponent={() => (

          <View style={styles.emptyContainer}>

            <Ionicons
              name="alert-circle-outline"
              size={40}
              color={cores.textoSecundario}
            />

            <Text
              style={[
                styles.emptyText,
                {
                  color: cores.textoSecundario,
                },
              ]}
            >
              Nenhum produto encontrado.
            </Text>

          </View>

        )}

        renderItem={({ item }) => {

          const estoque = Number(
            item.estoque || 0
          );

          const estoqueBaixo = estoque <= 5;

          return (

            <View
              style={[
                styles.card,
                {
                  backgroundColor: cores.card,
                  borderColor: cores.borda,
                },
              ]}
            >

              <Image
                source={{
                  uri:
                    item.foto ||
                    'https://placeholder.com',
                }}
                style={[
                  styles.image,
                  {
                    backgroundColor:
                      cores.cardSecundario,
                  },
                ]}
              />

              <View style={styles.content}>

                <View style={styles.topRow}>

                  <View
                    style={{
                      flex: 1,
                      paddingRight: 10,
                    }}
                  >

                    <Text
                      style={[
                        styles.name,
                        {
                          color: cores.texto,
                        },
                      ]}
                    >
                      {item.nome ||
                        'Produto sem nome'}
                    </Text>

                    <Text
                      style={[
                        styles.category,
                        {
                          color:
                            cores.textoSecundario,
                        },
                      ]}
                    >
                      {item.categoria ||
                        'Sem categoria'}
                    </Text>

                  </View>

                  <View
                    style={[
                      styles.stockBadge,
                      {
                        backgroundColor:
                          estoqueBaixo
                            ? cores.erro
                            : cores.primaria,
                      },
                    ]}
                  >

                    <Text style={styles.stockText}>
                      {estoque}
                    </Text>

                  </View>

                </View>

                <View style={styles.infoRow}>

                  <View
                    style={[
                      styles.infoCard,
                      {
                        backgroundColor:
                          cores.cardSecundario,
                        borderColor:
                          cores.borda,
                      },
                    ]}
                  >

                    <Ionicons
                      name="cube-outline"
                      size={18}
                      color={cores.primaria}
                    />

                    <Text
                      style={[
                        styles.infoText,
                        {
                          color:
                            cores.textoSecundario,
                        },
                      ]}
                    >
                      Estoque
                    </Text>

                  </View>

                  <View
                    style={[
                      styles.infoCard,
                      {
                        backgroundColor:
                          cores.cardSecundario,
                        borderColor:
                          cores.borda,
                      },
                    ]}
                  >

                    <Ionicons
                      name="barcode-outline"
                      size={18}
                      color={cores.primaria}
                    />

                    <Text
                      style={[
                        styles.infoText,
                        {
                          color:
                            cores.textoSecundario,
                        },
                      ]}
                    >
                      {item.codigo ||
                        item.RFID ||
                        'S/C'}
                    </Text>

                  </View>

                </View>

                <View style={styles.bottomRow}>

                  <Text
                    style={[
                      styles.stockStatus,
                      {
                        color: estoqueBaixo
                          ? cores.erro
                          : cores.primaria,
                      },
                    ]}
                  >
                    {estoqueBaixo
                      ? 'Estoque baixo'
                      : 'Disponível'}
                  </Text>

                </View>

              </View>

            </View>
          );
        }}
      />

    </View>
  );
}

// ======================================================================
// ============================== ESTILOS ================================
// ======================================================================

const styles = StyleSheet.create({

  container: {
    flex: 1,
    paddingHorizontal: 20,
  },

  // ============================== CADASTRO ==============================

  cadastroScroll: {
    paddingTop: 55,
    paddingBottom: 50,
  },

  cadastroHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },

  cadastroTitle: {
    fontSize: 28,
    fontWeight: 'bold',
  },

  cadastroSubtitle: {
    fontSize: 14,
    marginTop: 5,
  },

  closeButton: {
    width: 45,
    height: 45,
    borderRadius: 15,
    justifyContent: 'center',
    alignItems: 'center',
  },

  label: {
    fontSize: 14,
    fontWeight: '600',
    marginTop: 15,
    marginBottom: 7,
  },

  input: {
    height: 52,
    borderRadius: 15,
    borderWidth: 1,
    paddingHorizontal: 15,
    fontSize: 15,
  },

  descricaoInput: {
    height: 100,
    paddingTop: 15,
    textAlignVertical: 'top',
  },

  cadastrarButton: {
    height: 55,
    borderRadius: 16,
    marginTop: 25,
    marginBottom: 40,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },

  cadastrarButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },

  // ============================== HEADER ==============================

  header: {
    marginTop: 55,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 25,
  },

  title: {
    fontSize: 32,
    fontWeight: 'bold',
  },

  subtitle: {
    marginTop: 5,
    fontSize: 15,
  },

  filterButton: {
    width: 52,
    height: 52,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',

    elevation: 4,

    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.15,
    shadowRadius: 4,
  },

  // ============================== PESQUISA ==============================

  searchContainer: {
    height: 62,
    borderRadius: 20,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 18,
    marginBottom: 25,
    borderWidth: 1,
    elevation: 2,
  },

  searchInput: {
    flex: 1,
    marginLeft: 10,
    fontSize: 16,
  },

  // ============================== CARD ==============================

  card: {
    borderRadius: 28,
    overflow: 'hidden',
    marginBottom: 22,
    borderWidth: 1,

    elevation: 3,

    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.12,
    shadowRadius: 5,
  },

  image: {
    width: '100%',
    height: 220,
  },

  content: {
    padding: 20,
  },

  topRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },

  name: {
    fontSize: 21,
    fontWeight: 'bold',
  },

  category: {
    marginTop: 6,
    fontSize: 15,
  },

  stockBadge: {
    minWidth: 48,
    height: 48,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 12,
  },

  stockText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },

  infoRow: {
    flexDirection: 'row',
    marginTop: 18,
    gap: 12,
  },

  infoCard: {
    borderRadius: 14,
    paddingHorizontal: 14,
    paddingVertical: 10,
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
  },

  infoText: {
    marginLeft: 8,
    fontSize: 13,
    fontWeight: '500',
  },

  bottomRow: {
    marginTop: 22,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },

  stockStatus: {
    fontSize: 14,
    fontWeight: '600',
  },

  emptyContainer: {
    alignItems: 'center',
    marginTop: 40,
  },

  emptyText: {
    marginTop: 10,
    fontSize: 16,
  },

});