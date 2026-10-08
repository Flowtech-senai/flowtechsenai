import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Switch,
  ScrollView,
  Alert,
  Modal,
  TextInput,
  ActivityIndicator,
} from "react-native";

import AsyncStorage from "@react-native-async-storage/async-storage";
import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "../context/ThemeContext";

export default function ConfiguracoesScreen({ navigation }) {
  const [notificacoes, setNotificacoes] = useState(true);
  const [alertaEstoque, setAlertaEstoque] = useState(true);
  const [confirmarMovimentacao, setConfirmarMovimentacao] = useState(true);
  const { cores, modo, alterarTema } = useTheme();
  const [modalSenha, setModalSenha] = useState(false);
  const [senhaAtual, setSenhaAtual] = useState("");
  const [novaSenha, setNovaSenha] = useState("");
  const [confirmarSenha, setConfirmarSenha] = useState("");

  const [carregando, setCarregando] = useState(false);

  useEffect(() => {
    carregarConfiguracoes();
  }, []);

  // =========================================================
  // CARREGAR CONFIGURAÇÕES
  // =========================================================

  async function carregarConfiguracoes() {
    try {
      const dados = await AsyncStorage.getItem(
        "@flowtech_configuracoes"
      );

      if (dados) {
        const config = JSON.parse(dados);

        setNotificacoes(config.notificacoes ?? true);
        setAlertaEstoque(config.alertaEstoque ?? true);

        setConfirmarMovimentacao(
          config.confirmarMovimentacao ?? true
        );

        if (config.modoEscuro !== undefined) {
          alterarTema(config.modoEscuro ? "escuro" : "claro");
        }
      }
    } catch (error) {
      console.log(
        "Erro ao carregar configurações:",
        error
      );
    }
  }

  // =========================================================
  // SALVAR CONFIGURAÇÕES
  // =========================================================

  async function salvarConfiguracoes(novasConfiguracoes) {
    try {
      const configuracoes = {
        notificacoes,
        alertaEstoque,
        confirmarMovimentacao,
        modoEscuro,
        ...novasConfiguracoes,
      };

      await AsyncStorage.setItem(
        "@flowtech_configuracoes",
        JSON.stringify(configuracoes)
      );
    } catch (error) {
      console.log(
        "Erro ao salvar configurações:",
        error
      );
    }
  }

  // =========================================================
  // NOTIFICAÇÕES
  // =========================================================

  function alterarNotificacoes(valor) {
    setNotificacoes(valor);

    salvarConfiguracoes({
      notificacoes: valor,
    });
  }

  // =========================================================
  // ALERTA DE ESTOQUE
  // =========================================================

  function alterarAlertaEstoque(valor) {
    setAlertaEstoque(valor);

    salvarConfiguracoes({
      alertaEstoque: valor,
    });
  }

  // =========================================================
  // CONFIRMAÇÃO DE MOVIMENTAÇÃO
  // =========================================================

  function alterarConfirmacao(valor) {
    setConfirmarMovimentacao(valor);

    salvarConfiguracoes({
      confirmarMovimentacao: valor,
    });
  }

  // ========================================================= MODO ESCURO =========================================================

  function alterarModoEscuro(valor) {
    alterarTema(valor ? "escuro" : "claro");

    salvarConfiguracoes({
      modoEscuro: valor,
    });
  }

  // ========================================================= ALTERAR SENHA =========================================================

  async function alterarSenha() {
    if (!senhaAtual || !novaSenha || !confirmarSenha) {
      Alert.alert(
        "Atenção",
        "Preencha todos os campos."
      );
      return;
    }

    if (novaSenha.length < 6) {
      Alert.alert(
        "Senha inválida",
        "A nova senha deve possuir pelo menos 6 caracteres."
      );
      return;
    }

    if (novaSenha !== confirmarSenha) {
      Alert.alert(
        "Senhas diferentes",
        "A nova senha e a confirmação precisam ser iguais."
      );
      return;
    }

    try {
      setCarregando(true);

      /*
        Aqui futuramente podemos conectar
        diretamente com sua API/backend.

        Por enquanto a validação é feita localmente.
      */

      await new Promise((resolve) =>
        setTimeout(resolve, 1000)
      );

      setCarregando(false);
      setSenhaAtual("");
      setNovaSenha("");
      setConfirmarSenha("");
      setModalSenha(false);

      Alert.alert(
        "Sucesso",
        "Senha alterada com sucesso."
      );
    } catch (error) {
      setCarregando(false);

      Alert.alert(
        "Erro",
        "Não foi possível alterar a senha."
      );
    }
  }

  // =========================================================
  // SAIR
  // =========================================================

  function sairDaConta() {
    Alert.alert(
      "Sair da conta",
      "Tem certeza que deseja sair?",
      [
        {
          text: "Cancelar",
          style: "cancel",
        },
        {
          text: "Sair",
          style: "destructive",

          onPress: async () => {
            try {
              await AsyncStorage.removeItem(
                "@flowtech_usuario"
              );

              await AsyncStorage.removeItem(
                "@flowtech_token"
              );

              if (navigation) {
                navigation.reset({
                  index: 0,
                  routes: [
                    {
                      name: "Login",
                    },
                  ],
                });
              }
            } catch (error) {
              console.log(
                "Erro ao sair:",
                error
              );
            }
          },
        },
      ]
    );
  }

  const modoEscuro = modo === "escuro";

  return (
    <View
      style={[
        styles.container,
        {
          backgroundColor: cores.fundo
        },
      ]}
    >
      {/* =====================================================
          CABEÇALHO
      ===================================================== */}

      <View
        style={[
          styles.header,
          {
            backgroundColor: cores.card,
            borderBottomColor: borda,
          },
        ]}
      >
        <TouchableOpacity
          style={styles.voltar}
          onPress={() => navigation?.goBack()}
        >
          <Ionicons
            name="arrow-back"
            size={25}
            color={texto}
          />
        </TouchableOpacity>

        <View>
          <Text
            style={[
              styles.titulo,
              {
                color: cores.texto,
              },
            ]}
          >
            Configurações
          </Text>

          <Text
            style={[
              styles.subtitulo,
              {
                color: textoSecundario,
              },
            ]}
          >
            Personalize seu aplicativo
          </Text>
        </View>
      </View>

      {/* =====================================================
          CONTEÚDO
      ===================================================== */}

      <ScrollView
        contentContainerStyle={styles.conteudo}
        showsVerticalScrollIndicator={false}
      >
        {/* ===================================================
            PERFIL
        =================================================== */}

        <Text
          style={[
            styles.tituloSecao,
            {
              color: cores.texto,
            },
          ]}
        >
          Perfil
        </Text>

        <View
          style={[
            styles.cardPerfil,
            {
              backgroundColor: cores.card,
              borderColor: borda,
            },
          ]}
        >
          <View style={styles.avatar}>
            <Ionicons
              name="person"
              size={34}
              color="#007E83"
            />
          </View>

          <View style={styles.informacoesPerfil}>
            <Text
              style={[
                styles.nomeUsuario,
                {
                  color: cores.texto,
                },
              ]}
            >
              Funcionário
            </Text>

            <Text
              style={[
                styles.emailUsuario,
                {
                  color: textoSecundario,
                },
              ]}
            >
              Conta do sistema
            </Text>
          </View>

          <TouchableOpacity
            onPress={() =>
              Alert.alert(
                "Perfil",
                "As informações do funcionário serão carregadas do sistema."
              )
            }
          >
            <Ionicons
              name="chevron-forward"
              size={22}
              color={textoSecundario}
            />
          </TouchableOpacity>
        </View>

        {/* ===================================================
            PREFERÊNCIAS
        =================================================== */}

        <Text
          style={[
            styles.tituloSecao,
            {
              color: texto,
            },
          ]}
        >
          Preferências
        </Text>

        <View
          style={[
            styles.card,
            {
              backgroundColor: cores.card,
              borderColor: borda,
            },
          ]}
        >
          {/* NOTIFICAÇÕES */}

          <View style={styles.item}>
            <View style={styles.itemEsquerda}>
              <View style={styles.icone}>
                <Ionicons
                  name="notifications-outline"
                  size={22}
                  color="#007E83"
                />
              </View>

              <View style={styles.textosItem}>
                <Text
                  style={[
                    styles.nomeItem,
                    {
                      color: texto,
                    },
                  ]}
                >
                  Notificações
                </Text>

                <Text
                  style={[
                    styles.descricaoItem,
                    {
                      color: textoSecundario,
                    },
                  ]}
                >
                  Receber notificações do sistema
                </Text>
              </View>
            </View>

            <Switch
              value={notificacoes}
              onValueChange={alterarNotificacoes}
              trackColor={{
                false: "#CBD5D4",
                true: "#80C7C8",
              }}
              thumbColor={
                notificacoes
                  ? "#007E83"
                  : "#F4F4F4"
              }
            />
          </View>

          <View
            style={[
              styles.linha,
              {
                backgroundColor: borda,
              },
            ]}
          />

          {/* ALERTA ESTOQUE */}

          <View style={styles.item}>
            <View style={styles.itemEsquerda}>
              <View style={styles.icone}>
                <Ionicons
                  name="warning-outline"
                  size={22}
                  color="#007E83"
                />
              </View>

              <View style={styles.textosItem}>
                <Text
                  style={[
                    styles.nomeItem,
                    {
                      color: cores.texto,
                    },
                  ]}
                >
                  Estoque baixo
                </Text>

                <Text
                  style={[
                    styles.descricaoItem,
                    {
                      color: textoSecundario,
                    },
                  ]}
                >
                  Avisar quando um produto estiver abaixo do mínimo
                </Text>
              </View>
            </View>

            <Switch
              value={alertaEstoque}
              onValueChange={alterarAlertaEstoque}
              trackColor={{
                false: "#CBD5D4",
                true: "#80C7C8",
              }}
              thumbColor={
                alertaEstoque
                  ? "#007E83"
                  : "#F4F4F4"
              }
            />
          </View>

          <View
            style={[
              styles.linha,
              {
                backgroundColor: borda,
              },
            ]}
          />

          {/* CONFIRMAÇÃO */}

          <View style={styles.item}>
            <View style={styles.itemEsquerda}>
              <View style={styles.icone}>
                <Ionicons
                  name="checkmark-circle-outline"
                  size={22}
                  color="#007E83"
                />
              </View>

              <View style={styles.textosItem}>
                <Text
                  style={[
                    styles.nomeItem,
                    {
                      color: cores.texto,
                    },
                  ]}
                >
                  Confirmar movimentações
                </Text>

                <Text
                  style={[
                    styles.descricaoItem,
                    {
                      color: textoSecundario,
                    },
                  ]}
                >
                  Confirmar antes de entradas e saídas
                </Text>
              </View>
            </View>

            <Switch
              value={confirmarMovimentacao}
              onValueChange={alterarConfirmacao}
              trackColor={{
                false: "#CBD5D4",
                true: "#80C7C8",
              }}
              thumbColor={
                confirmarMovimentacao
                  ? "#007E83"
                  : "#F4F4F4"
              }
            />
          </View>

          <View
            style={[
              styles.linha,
              {
                backgroundColor: borda,
              },
            ]}
          />

          {/* MODO ESCURO */}

          <View style={styles.item}>
            <View style={styles.itemEsquerda}>
              <View style={styles.icone}>
                <Ionicons
                  name="moon-outline"
                  size={22}
                  color="#007E83"
                />
              </View>

              <View style={styles.textosItem}>
                <Text
                  style={[
                    styles.nomeItem,
                    {
                      color: cores.texto,
                    },
                  ]}
                >
                  Modo escuro
                </Text>

                <Text
                  style={[
                    styles.descricaoItem,
                    {
                      color: textoSecundario,
                    },
                  ]}
                >
                  Alterar aparência do aplicativo
                </Text>
              </View>
            </View>

            <Switch
              value={modoEscuro}
              onValueChange={alterarModoEscuro}
              trackColor={{
                false: "#CBD5D4",
                true: "#80C7C8",
              }}
              thumbColor={
                modoEscuro
                  ? "#007E83"
                  : "#F4F4F4"
              }
            />
          </View>
        </View>

        {/* ===================================================
            SEGURANÇA
        =================================================== */}

        <Text
          style={[
            styles.tituloSecao,
            {
              color: cores.texto,
            },
          ]}
        >
          Segurança
        </Text>

        <View
          style={[
            styles.card,
            {
              backgroundColor: cores.card,
              borderColor: borda,
            },
          ]}
        >
          <TouchableOpacity
            style={styles.botaoConfiguracao}
            onPress={() => setModalSenha(true)}
          >
            <View style={styles.itemEsquerda}>
              <View style={styles.icone}>
                <Ionicons
                  name="lock-closed-outline"
                  size={22}
                  color="#007E83"
                />
              </View>

              <View style={styles.textosItem}>
                <Text
                  style={[
                    styles.nomeItem,
                    {
                      color: cores.texto,
                    },
                  ]}
                >
                  Alterar senha
                </Text>

                <Text
                  style={[
                    styles.descricaoItem,
                    {
                      color: textoSecundario,
                    },
                  ]}
                >
                  Atualize a senha da sua conta
                </Text>
              </View>
            </View>

            <Ionicons
              name="chevron-forward"
              size={22}
              color={textoSecundario}
            />
          </TouchableOpacity>
        </View>

        {/* ===================================================
            SOBRE
        =================================================== */}

        <Text
          style={[
            styles.tituloSecao,
            {
              color: cores.texto,
            },
          ]}
        >
          Aplicativo
        </Text>

        <View
          style={[
            styles.card,
            {
              backgroundColor: cores.card,
              borderColor: borda,
            },
          ]}
        >
          <TouchableOpacity
            style={styles.botaoConfiguracao}
            onPress={() =>
              Alert.alert(
                "Flow Tech",
                "Sistema de gerenciamento de estoque farmacêutico.\nVersão 1.0.0"
              )
            }
          >
            <View style={styles.itemEsquerda}>
              <View style={styles.icone}>
                <Ionicons
                  name="information-circle-outline"
                  size={22}
                  color="#007E83"
                />
              </View>

              <View style={styles.textosItem}>
                <Text
                  style={[
                    styles.nomeItem,
                    {
                      color: cores.texto,
                    },
                  ]}
                >
                  Sobre o Flow Tech
                </Text>

                <Text
                  style={[
                    styles.descricaoItem,
                    {
                      color: textoSecundario,
                    },
                  ]}
                >
                  Informações sobre o sistema
                </Text>
              </View>
            </View>

            <Ionicons
              name="chevron-forward"
              size={22}
              color={textoSecundario}
            />
          </TouchableOpacity>
        </View>

        {/* ===================================================
            SAIR
        =================================================== */}

        <TouchableOpacity
          style={styles.botaoSair}
          onPress={sairDaConta}
        >
          <Ionicons
            name="log-out-outline"
            size={22}
            color="#D64545"
          />

          <Text style={styles.textoSair}>
            Sair da conta
          </Text>
        </TouchableOpacity>

        <Text
          style={[
            styles.versao,
            {
              color: textoSecundario,
            },
          ]}
        >
          Flow Tech • v1.0.0
        </Text>
      </ScrollView>

      {/* =====================================================
          MODAL ALTERAR SENHA
      ===================================================== */}

      <Modal
        visible={modalSenha}
        transparent={true}
        animationType="slide"
        onRequestClose={() =>
          setModalSenha(false)
        }
      >
        <View style={styles.fundoModal}>
          <View
            style={[
              styles.modal,
              {
                backgroundColor:cores.card,
              },
            ]}
          >
            <View style={styles.topoModal}>
              <Text
                style={[
                  styles.tituloModal,
                  {
                    color: cores.texto,
                  },
                ]}
              >
                Alterar senha
              </Text>

              <TouchableOpacity
                onPress={() =>
                  setModalSenha(false)
                }
              >
                <Ionicons
                  name="close"
                  size={25}
                  color={texto}
                />
              </TouchableOpacity>
            </View>

            <TextInput
              style={[
                styles.input,
                {
                  color: cores.texto,
                  borderColor: borda,
                },
              ]}
              placeholder="Senha atual"
              placeholderTextColor="#8A9695"
              secureTextEntry
              value={senhaAtual}
              onChangeText={setSenhaAtual}
            />

            <TextInput
              style={[
                styles.input,
                {
                  color: cores.texto,
                  borderColor: borda,
                },
              ]}
              placeholder="Nova senha"
              placeholderTextColor="#8A9695"
              secureTextEntry
              value={novaSenha}
              onChangeText={setNovaSenha}
            />

            <TextInput
              style={[
                styles.input,
                {
                  color: cores.texto,
                  borderColor: borda,
                },
              ]}
              placeholder="Confirmar nova senha"
              placeholderTextColor="#8A9695"
              secureTextEntry
              value={confirmarSenha}
              onChangeText={setConfirmarSenha}
            />

            <TouchableOpacity
              style={styles.botaoSalvar}
              onPress={alterarSenha}
              disabled={carregando}
            >
              {carregando ? (
                <ActivityIndicator color="#FFFFFF" />
              ) : (
                <Text style={styles.textoBotaoSalvar}>
                  Alterar senha
                </Text>
              )}
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

// ===========================================================
// ESTILOS
// ===========================================================

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },

  header: {
    height: 90,
    paddingHorizontal: 20,
    flexDirection: "row",
    alignItems: "center",
    borderBottomWidth: 1,
  },

  voltar: {
    width: 42,
    height: 42,
    justifyContent: "center",
    alignItems: "center",
    marginRight: 12,
  },

  titulo: {
    fontSize: 22,
    fontWeight: "700",
  },

  subtitulo: {
    fontSize: 13,
    marginTop: 3,
  },

  conteudo: {
    padding: 20,
    paddingBottom: 40,
  },

  tituloSecao: {
    fontSize: 16,
    fontWeight: "700",
    marginBottom: 10,
    marginTop: 8,
  },

  cardPerfil: {
    borderRadius: 16,
    borderWidth: 1,
    padding: 16,
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 25,
  },

  avatar: {
    width: 58,
    height: 58,
    borderRadius: 29,
    backgroundColor: "#DDF3F1",
    justifyContent: "center",
    alignItems: "center",
  },

  informacoesPerfil: {
    flex: 1,
    marginLeft: 14,
  },

  nomeUsuario: {
    fontSize: 16,
    fontWeight: "700",
  },

  emailUsuario: {
    fontSize: 13,
    marginTop: 4,
  },

  card: {
    borderRadius: 16,
    borderWidth: 1,
    marginBottom: 25,
    overflow: "hidden",
  },

  item: {
    minHeight: 78,
    paddingHorizontal: 15,
    paddingVertical: 12,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },

  itemEsquerda: {
    flexDirection: "row",
    alignItems: "center",
    flex: 1,
  },

  icone: {
    width: 42,
    height: 42,
    borderRadius: 12,
    backgroundColor: "#E6F5F3",
    justifyContent: "center",
    alignItems: "center",
  },

  textosItem: {
    flex: 1,
    marginLeft: 12,
    paddingRight: 10,
  },

  nomeItem: {
    fontSize: 15,
    fontWeight: "600",
  },

  descricaoItem: {
    fontSize: 12,
    marginTop: 4,
    lineHeight: 17,
  },

  linha: {
    height: 1,
    marginLeft: 69,
  },

  botaoConfiguracao: {
    minHeight: 78,
    paddingHorizontal: 15,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },

  botaoSair: {
    height: 58,
    borderRadius: 15,
    backgroundColor: "#FDEEEE",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    marginTop: 5,
  },

  textoSair: {
    color: "#D64545",
    fontSize: 15,
    fontWeight: "700",
    marginLeft: 8,
  },

  versao: {
    textAlign: "center",
    fontSize: 12,
    marginTop: 20,
  },

  fundoModal: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.55)",
    justifyContent: "flex-end",
  },

  modal: {
    borderTopLeftRadius: 25,
    borderTopRightRadius: 25,
    padding: 22,
    paddingBottom: 35,
  },

  topoModal: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 20,
  },

  tituloModal: {
    fontSize: 20,
    fontWeight: "700",
  },

  input: {
    height: 52,
    borderWidth: 1,
    borderRadius: 12,
    paddingHorizontal: 15,
    fontSize: 14,
    marginBottom: 12,
  },

  botaoSalvar: {
    height: 52,
    borderRadius: 12,
    backgroundColor: "#007E83",
    justifyContent: "center",
    alignItems: "center",
    marginTop: 5,
  },

  textoBotaoSalvar: {
    color: "#FFFFFF",
    fontSize: 15,
    fontWeight: "700",
  },
});