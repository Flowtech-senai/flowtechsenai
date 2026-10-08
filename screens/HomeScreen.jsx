import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from 'react-native';

import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';

import api from '../src/services/api';
import { useTheme } from '../context/ThemeContext';

export default function HomeScreen({ navigation }) {

  // =====================================================
  // TEMA GLOBAL
  // =====================================================

  const { cores } = useTheme();


  // =====================================================
  // ESTADOS
  // =====================================================

  const [totalProdutos, setTotalProdutos] = useState(0);
  const [stockBadge, setStockBadge] = useState(0);
  const [carregando, setCarregando] = useState(true);
  const [atividades, setAtividades] = useState([]);
  const [totalEntradas, setTotalEntradas] = useState(0);
  const [totalSaidas, setTotalSaidas] = useState(0);


  // =====================================================
  // BUSCAR DADOS DO BANCO
  // =====================================================

  useFocusEffect(
    useCallback(() => {

      async function buscarDadosDoBanco() {

        try {

          setCarregando(true);

          const response =
            await api.get('/api/dashboard');

          console.log(
            'DADOS DO DASHBOARD:',
            response.data
          );

          const dados = response.data;


          setTotalProdutos(
            Number(dados.totalProducts) || 0
          );


          setStockBadge(
            Number(dados.lowStockCount) || 0
          );


          setTotalEntradas(
            Number(dados.totalEntradas) || 0
          );


          setTotalSaidas(
            Number(dados.totalSaidas) || 0
          );


          setAtividades(
            Array.isArray(dados.atividades)
              ? dados.atividades
              : []
          );


        } catch (error) {

          console.error(
            'ERRO DASHBOARD:',
            error.response?.data || error.message
          );

        } finally {

          setCarregando(false);

        }

      }

      buscarDadosDoBanco();

    }, [])
  );


  // ===================================================== TELA =====================================================

  return (

    <ScrollView
      style={[
        styles.container,
        {
          backgroundColor: cores.fundo,
        },
      ]}
      showsVerticalScrollIndicator={false}
    >


      {/* TOP BAR */}

      <View style={styles.topBar}>

        <View style={styles.brandContainer}>

          <View
            style={[
              styles.logoPlaceholder,
              {
                backgroundColor: cores.primariaEscura,
              },
            ]}
          >

            <Ionicons
              name="cube"
              size={20}
              color="#FFFFFF"
            />

          </View>


          <View>

            <Text
              style={[
                styles.brandName,
                {
                  color: cores.texto,
                },
              ]}
            >
              Flow Tech
            </Text>


            <Text
              style={[
                styles.brandSubtitle,
                {
                  color: cores.textoSecundario,
                },
              ]}
            >
              Gestão Inteligente de Estoque
            </Text>

          </View>

        </View>


        <View style={styles.topActions}>

          <TouchableOpacity
            style={[
              styles.iconButton,
              {
                backgroundColor: cores.card,
              },
            ]}
          >

            <Ionicons
              name="notifications-outline"
              size={22}
              color={cores.texto}
            />

          </TouchableOpacity>


          <TouchableOpacity
            style={[
              styles.profileButton,
              {
                backgroundColor: cores.azul,
              },
            ]}
          >

            <Ionicons
              name="person"
              size={20}
              color="#FFFFFF"
            />

          </TouchableOpacity>

        </View>

      </View>


      {/* CARD DE BOAS-VINDAS */}

      <View
        style={[
          styles.welcomeBanner,
          {
            backgroundColor: cores.primaria,
          },
        ]}
      >

        <View style={styles.welcomeLeft}>

          <Text style={styles.welcomeTitle}>
            Olá, Bem-vindo(a)!
          </Text>


          <Text style={styles.welcomeSubtitle}>
            Aqui você acompanha tudo sobre o estoque
            de forma simples e rápida.
          </Text>


          <View style={styles.badgeSecure}>

            <Ionicons
              name="shield-checkmark"
              size={14}
              color="#FFFFFF"
            />


            <Text style={styles.badgeText}>
              Sistema seguro e confiável
            </Text>

          </View>

        </View>


        <View style={styles.welcomeRight}>

          <Ionicons
            name="file-tray-full"
            size={70}
            color="rgba(255,255,255,0.2)"
          />

        </View>

      </View>


      {/* MENU DE OPERAÇÕES */}

      <View style={styles.gridOperations}>


        {/* PRODUTOS */}

        <TouchableOpacity
          style={[
            styles.gridItem,
            {
              backgroundColor: cores.card,
              borderColor: cores.borda,
            },
          ]}
          onPress={() =>
            navigation.navigate('Produtos')
          }
        >

          <View
            style={[
              styles.gridIconBox,
              {
                backgroundColor:
                  cores.primariaEscura,
              },
            ]}
          >

            <Ionicons
              name="cube-outline"
              size={22}
              color="#FFFFFF"
            />

          </View>


          <Text
            style={[
              styles.gridItemTitle,
              {
                color: cores.texto,
              },
            ]}
          >
            Produtos
          </Text>


          <Text
            style={[
              styles.gridItemSub,
              {
                color: cores.textoSecundario,
              },
            ]}
          >
            Gerenciar
          </Text>


          <Ionicons
            name="arrow-forward-circle"
            size={16}
            color={cores.textoSecundario}
            style={{ marginTop: 5 }}
          />

        </TouchableOpacity>


        {/* MOVIMENTAÇÃO */}

        <TouchableOpacity
          style={[
            styles.gridItem,
            {
              backgroundColor: cores.card,
              borderColor: cores.borda,
            },
          ]}
          onPress={() =>
            navigation.navigate('Movimentacao')
          }
        >

          <View
            style={[
              styles.gridIconBox,
              {
                backgroundColor:
                  cores.primariaEscura,
              },
            ]}
          >

            <Ionicons
              name="git-compare-outline"
              size={22}
              color="#FFFFFF"
            />

          </View>


          <Text
            style={[
              styles.gridItemTitle,
              {
                color: cores.texto,
              },
            ]}
          >
            Movimentação
          </Text>


          <Text
            style={[
              styles.gridItemSub,
              {
                color: cores.textoSecundario,
              },
            ]}
          >
            Entrada/Saída
          </Text>


          <Ionicons
            name="arrow-forward-circle"
            size={16}
            color={cores.textoSecundario}
            style={{ marginTop: 5 }}
          />

        </TouchableOpacity>


        {/* RELATÓRIOS */}

        <TouchableOpacity
          style={[
            styles.gridItem,
            {
              backgroundColor: cores.card,
              borderColor: cores.borda,
            },
          ]}
          onPress={() =>
            navigation.navigate('Relatorios')
          }
        >

          <View
            style={[
              styles.gridIconBox,
              {
                backgroundColor:
                  cores.primariaEscura,
              },
            ]}
          >

            <Ionicons
              name="document-text-outline"
              size={22}
              color="#FFFFFF"
            />

          </View>


          <Text
            style={[
              styles.gridItemTitle,
              {
                color: cores.texto,
              },
            ]}
          >
            Relatórios
          </Text>


          <Text
            style={[
              styles.gridItemSub,
              {
                color: cores.textoSecundario,
              },
            ]}
          >
            Estatísticas
          </Text>


          <Ionicons
            name="arrow-forward-circle"
            size={16}
            color={cores.textoSecundario}
            style={{ marginTop: 5 }}
          />

        </TouchableOpacity>


        {/* AJUSTES */}

        <TouchableOpacity
          onPress={() => navigation.navigate("Configuracoes")}
        >
          <Ionicons
            name="settings-outline"
            size={24}
            color="#007E83"
          />

          <View
            style={[
              styles.card,
              {
                backgroundColor: cores.card,
                borderColor: cores.borda,
              },
            ]}
          >

            <Ionicons
              name="settings-outline"
              size={22}
              color="#FFFFFF"
            />

          </View>


          <Text
            style={[
              styles.gridItemTitle,
              {
                color: cores.texto,
              },
            ]}
          >
            Ajustes
          </Text>


          <Text
            style={[
              styles.gridItemSub,
              {
                color: cores.textoSecundario,
              },
            ]}
          >
            Configurações
          </Text>


          <Ionicons
            name="arrow-forward-circle"
            size={16}
            color={cores.textoSecundario}
            style={{ marginTop: 5 }}
          />

        </TouchableOpacity>

      </View>


      {/* ================================================= */}
      {/* RESUMO DO ESTOQUE */}
      {/* ================================================= */}

      <View style={styles.sectionHeader}>

        <Text
          style={[
            styles.sectionTitle,
            {
              color: cores.texto,
            },
          ]}
        >
          Resumo do Estoque
        </Text>


        <TouchableOpacity>

          <Text
            style={[
              styles.seeAllText,
              {
                color: cores.textoSecundario,
              },
            ]}
          >
            Ver todos &gt;
          </Text>

        </TouchableOpacity>

      </View>


      {/* ================================================= */}
      {/* CARDS DE RESUMO */}
      {/* ================================================= */}

      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        style={styles.summaryScroll}
      >


        {/* PRODUTOS */}

        <View
          style={[
            styles.metricCard,
            {
              backgroundColor: cores.card,
              borderColor: cores.borda,
            },
          ]}
        >

          <View
            style={[
              styles.metricIconBox,
              {
                backgroundColor:
                  cores.primariaEscura,
              },
            ]}
          >

            <Ionicons
              name="layers"
              size={20}
              color="#FFFFFF"
            />

          </View>


          <Text
            style={[
              styles.metricValue,
              {
                color: cores.texto,
              },
            ]}
          >
            {carregando ? '...' : totalProdutos}
          </Text>


          <Text
            style={[
              styles.metricLabel,
              {
                color: cores.textoSecundario,
              },
            ]}
          >
            Produtos
          </Text>

        </View>


        {/* ESTOQUE BAIXO */}

        <View
          style={[
            styles.metricCard,
            {
              backgroundColor: cores.card,
              borderColor: cores.borda,
            },
          ]}
        >

          <View
            style={[
              styles.metricIconBox,
              {
                backgroundColor: cores.erro,
              },
            ]}
          >

            <Ionicons
              name="trending-down"
              size={20}
              color="#FFFFFF"
            />

          </View>


          <Text
            style={[
              styles.metricValue,
              {
                color: cores.texto,
              },
            ]}
          >
            {carregando ? '...' : stockBadge}
          </Text>


          <Text
            style={[
              styles.metricLabel,
              {
                color: cores.textoSecundario,
              },
            ]}
          >
            Estoque baixo
          </Text>

        </View>


        {/* ENTRADAS */}

        <View
          style={[
            styles.metricCard,
            {
              backgroundColor: cores.card,
              borderColor: cores.borda,
            },
          ]}
        >

          <View
            style={[
              styles.metricIconBox,
              {
                backgroundColor:
                  cores.primariaEscura,
              },
            ]}
          >

            <Ionicons
              name="download-outline"
              size={20}
              color="#FFFFFF"
            />

          </View>


          <Text
            style={[
              styles.metricValue,
              {
                color: cores.texto,
              },
            ]}
          >
            {carregando ? '...' : totalEntradas}
          </Text>


          <Text
            style={[
              styles.metricLabel,
              {
                color: cores.textoSecundario,
              },
            ]}
          >
            Entradas
          </Text>

        </View>


        {/* SAÍDAS */}

        <View
          style={[
            styles.metricCard,
            {
              backgroundColor: cores.card,
              borderColor: cores.borda,
            },
          ]}
        >

          <View
            style={[
              styles.metricIconBox,
              {
                backgroundColor:
                  cores.primariaEscura,
              },
            ]}
          >

            <Ionicons
              name="share-outline"
              size={20}
              color="#FFFFFF"
            />

          </View>


          <Text
            style={[
              styles.metricValue,
              {
                color: cores.texto,
              },
            ]}
          >
            {carregando ? '...' : totalSaidas}
          </Text>


          <Text
            style={[
              styles.metricLabel,
              {
                color: cores.textoSecundario,
              },
            ]}
          >
            Saídas
          </Text>

        </View>

      </ScrollView>


      {/* ================================================= */}
      {/* ALERTA DE ESTOQUE BAIXO */}
      {/* ================================================= */}

      {
        Number(stockBadge) > 0 && (

          <View
            style={[
              styles.alertBanner,
              {
                backgroundColor: cores.alerta,
              },
            ]}
          >

            <View style={styles.alertLeft}>

              <View style={styles.alertIconCircle}>

                <Ionicons
                  name="warning"
                  size={20}
                  color="#FFFFFF"
                />

              </View>


              <View>

                <Text style={styles.alertTitle}>
                  ATENÇÃO
                </Text>


                <Text style={styles.alertMessage}>
                  Produtos com estoque baixo
                </Text>


                <Text style={styles.alertDetail}>
                  {stockBadge} itens precisam de reposição.
                </Text>

              </View>

            </View>


            <TouchableOpacity
              style={styles.alertBtn}
            >

              <Text
                style={[
                  styles.alertBtnText,
                  {
                    color: cores.alerta,
                  },
                ]}
              >
                Ver lista
              </Text>

            </TouchableOpacity>

          </View>

        )
      }


      {/* ================================================= */}
      {/* ATIVIDADES RECENTES */}
      {/* ================================================= */}

      <View style={styles.sectionHeader}>

        <Text
          style={[
            styles.sectionTitle,
            {
              color: cores.texto,
            },
          ]}
        >
          Atividades Recentes
        </Text>


        <TouchableOpacity>

          <Text
            style={[
              styles.seeAllText,
              {
                color: cores.textoSecundario,
              },
            ]}
          >
            Ver todas &gt;
          </Text>

        </TouchableOpacity>

      </View>


      {/* ================================================= */}
      {/* LISTA DE ATIVIDADES */}
      {/* ================================================= */}

      {
        atividades.length === 0 ? (

          <Text
            style={[
              styles.emptyText,
              {
                color: cores.textoSecundario,
              },
            ]}
          >
            Nenhuma atividade registrada recentemente.
          </Text>

        ) : (

          atividades.map((atividade, index) => {

            const ehEntrada =
              atividade.tipo === 'entrada';


            return (

              <View
                key={atividade.id ?? index}
                style={[
                  styles.activityCard,
                  {
                    backgroundColor: cores.card,
                    borderColor: cores.borda,
                  },
                ]}
              >

                <View style={styles.activityLeft}>

                  <Ionicons
                    name={
                      ehEntrada
                        ? 'arrow-down-circle'
                        : 'arrow-up-circle'
                    }
                    size={24}
                    color={
                      ehEntrada
                        ? cores.sucesso
                        : cores.erro
                    }
                  />


                  <View style={styles.activityInfo}>

                    <Text
                      style={[
                        styles.activityTitle,
                        {
                          color: cores.texto,
                        },
                      ]}
                    >
                      {ehEntrada
                        ? 'Entrada de produtos'
                        : 'Saída de produtos'}
                    </Text>


                    <Text
                      style={[
                        styles.activitySubtitle,
                        {
                          color: cores.textoSecundario,
                        },
                      ]}
                    >
                      {atividade.nome || 'Produto'}
                      {' • '}
                      Qtd: {atividade.quantidade}
                    </Text>

                  </View>

                </View>


                <Text
                  style={[
                    styles.activityTime,
                    {
                      color: cores.textoSecundario,
                    },
                  ]}
                >
                  Hoje
                </Text>

              </View>

            );

          })

        )
      }


      {/* ESPAÇO INFERIOR */}

      <View style={{ height: 100 }} />

    </ScrollView >

  );
}


// =====================================================
// ESTILOS
// =====================================================

const styles = StyleSheet.create({

  container: {
    flex: 1,
    paddingHorizontal: 16,
  },


  // ===================================================
  // TOP BAR
  // ===================================================

  topBar: {
    marginTop: 50,
    marginBottom: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },

  brandContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },

  logoPlaceholder: {
    width: 36,
    height: 36,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 10,
  },

  brandName: {
    fontSize: 20,
    fontWeight: 'bold',
  },

  brandSubtitle: {
    fontSize: 11,
    marginTop: 2,
  },

  topActions: {
    flexDirection: 'row',
    alignItems: 'center',
  },

  iconButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 8,
  },

  profileButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },


  // ===================================================
  // BANNER
  // ===================================================

  welcomeBanner: {
    borderRadius: 20,
    padding: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
    minHeight: 150,
  },

  welcomeLeft: {
    flex: 1,
    paddingRight: 10,
  },

  welcomeTitle: {
    color: '#FFFFFF',
    fontSize: 22,
    fontWeight: 'bold',
  },

  welcomeSubtitle: {
    color: '#FFFFFF',
    fontSize: 13,
    lineHeight: 19,
    marginTop: 5,
    opacity: 0.85,
  },

  badgeSecure: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.15)',
    paddingVertical: 5,
    paddingHorizontal: 9,
    borderRadius: 20,
    marginTop: 12,
    alignSelf: 'flex-start',
  },

  badgeText: {
    color: '#FFFFFF',
    fontSize: 11,
    marginLeft: 5,
  },

  welcomeRight: {
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: 5,
  },


  // ===================================================
  // GRID
  // ===================================================

  gridOperations: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 25,
  },

  gridItem: {
    width: '23.5%',
    minHeight: 125,
    borderRadius: 16,
    borderWidth: 1,
    paddingVertical: 12,
    paddingHorizontal: 5,
    alignItems: 'center',
    justifyContent: 'center',
  },

  gridIconBox: {
    width: 36,
    height: 36,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 7,
  },

  gridItemTitle: {
    fontSize: 11,
    fontWeight: 'bold',
    textAlign: 'center',
  },

  gridItemSub: {
    fontSize: 9,
    textAlign: 'center',
    marginTop: 3,
  },


  // ===================================================
  // SEÇÕES
  // ===================================================

  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 10,
    marginBottom: 12,
  },

  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
  },

  seeAllText: {
    fontSize: 13,
  },


  // ===================================================
  // RESUMO
  // ===================================================

  summaryScroll: {
    marginBottom: 25,
  },

  metricCard: {
    width: 110,
    minHeight: 115,
    borderRadius: 16,
    borderWidth: 1,
    padding: 12,
    marginRight: 10,
  },

  metricIconBox: {
    width: 32,
    height: 32,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },

  metricValue: {
    fontSize: 18,
    fontWeight: 'bold',
  },

  metricLabel: {
    fontSize: 12,
    marginTop: 3,
  },


  // ===================================================
  // ALERTA
  // ===================================================

  alertBanner: {
    borderRadius: 16,
    padding: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 25,
  },

  alertLeft: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    paddingRight: 8,
  },

  alertIconCircle: {
    width: 36,
    height: 36,
    backgroundColor: 'rgba(255,255,255,0.2)',
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },

  alertTitle: {
    color: '#FFFFFF',
    fontSize: 10,
    fontWeight: 'bold',
    letterSpacing: 1,
    marginBottom: 2,
  },

  alertMessage: {
    color: '#FFFFFF',
    fontSize: 15,
    fontWeight: 'bold',
  },

  alertDetail: {
    color: '#FFFFFF',
    fontSize: 12,
    opacity: 0.9,
    marginTop: 2,
  },

  alertBtn: {
    backgroundColor: '#FFFFFF',
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 20,
  },

  alertBtnText: {
    fontWeight: 'bold',
    fontSize: 12,
  },


  // ===================================================
  // ATIVIDADES
  // ===================================================

  emptyText: {
    textAlign: 'center',
    marginTop: 10,
    marginBottom: 20,
    fontSize: 13,
  },

  activityCard: {
    borderRadius: 16,
    borderWidth: 1,
    padding: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },

  activityLeft: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    paddingRight: 10,
  },

  activityInfo: {
    flex: 1,
    marginLeft: 12,
  },

  activityTitle: {
    fontSize: 14,
    fontWeight: 'bold',
  },

  activitySubtitle: {
    fontSize: 12,
    marginTop: 3,
  },

  activityTime: {
    fontSize: 11,
  },

});