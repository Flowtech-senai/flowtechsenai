import React from 'react';
import {
  View,
  TouchableOpacity,
  StyleSheet,
  Text,
} from 'react-native';

import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Ionicons } from '@expo/vector-icons';

// Telas
import EntryScreen from './EntryScreen';
import ExitScreen from './ExitScreen';

// Tema global
import { useTheme } from '../context/ThemeContext';

const InnerStack = createNativeStackNavigator();

// ========================================
// TELA PRINCIPAL DE MOVIMENTAÇÃO
// ========================================

export default function MovimentacaoScreen() {
  return (
    <InnerStack.Navigator
      screenOptions={{
        headerShown: false,
      }}
    >
      <InnerStack.Screen
        name="MenuMovimentacao"
        component={MenuMovimentacao}
      />

      <InnerStack.Screen
        name="EntryScreen"
        component={EntryScreen}
      />

      <InnerStack.Screen
        name="ExitScreen"
        component={ExitScreen}
      />
    </InnerStack.Navigator>
  );
}

// ========================================
// MENU DE MOVIMENTAÇÃO
// ========================================

function MenuMovimentacao({ navigation }) {
  const { cores } = useTheme();

  return (
    <View
      style={[
        styles.container,
        {
          backgroundColor: cores.fundo,
        },
      ]}
    >
      {/* ==================================
          CABEÇALHO
      ================================== */}

      <View style={styles.header}>
        <Text
          style={[
            styles.title,
            {
              color: cores.texto,
            },
          ]}
        >
          Movimentação
        </Text>

        <Text
          style={[
            styles.subtitle,
            {
              color: cores.textoSecundario,
            },
          ]}
        >
          Controle as entradas e saídas do estoque
        </Text>
      </View>

      {/* ==================================
          ENTRADA
      ================================== */}

      <TouchableOpacity
        style={[
          styles.actionButton,
          {
            backgroundColor: cores.sucesso,
          },
        ]}
        onPress={() =>
          navigation.navigate('EntryScreen')
        }
        activeOpacity={0.8}
      >
        <View style={styles.buttonContent}>
          <View
            style={[
              styles.iconContainer,
              {
                backgroundColor:
                  'rgba(255,255,255,0.18)',
              },
            ]}
          >
            <Ionicons
              name="arrow-down-circle-outline"
              size={30}
              color="#FFFFFF"
            />
          </View>

          <View style={styles.textGroup}>
            <Text style={styles.buttonTitle}>
              Entrada de Estoque
            </Text>

            <Text style={styles.buttonSubtitle}>
              Registrar novos produtos
            </Text>
          </View>
        </View>

        <Ionicons
          name="chevron-forward"
          size={24}
          color="#FFFFFF"
        />
      </TouchableOpacity>

      {/* ==================================
          SAÍDA
      ================================== */}

      <TouchableOpacity
        style={[
          styles.actionButton,
          {
            backgroundColor: cores.erro,
          },
        ]}
        onPress={() =>
          navigation.navigate('ExitScreen')
        }
        activeOpacity={0.8}
      >
        <View style={styles.buttonContent}>
          <View
            style={[
              styles.iconContainer,
              {
                backgroundColor:
                  'rgba(255,255,255,0.18)',
              },
            ]}
          >
            <Ionicons
              name="arrow-up-circle-outline"
              size={30}
              color="#FFFFFF"
            />
          </View>

          <View style={styles.textGroup}>
            <Text style={styles.buttonTitle}>
              Saída de Estoque
            </Text>

            <Text style={styles.buttonSubtitle}>
              Registrar baixas do estoque
            </Text>
          </View>
        </View>

        <Ionicons
          name="chevron-forward"
          size={24}
          color="#FFFFFF"
        />
      </TouchableOpacity>

      {/* ==================================
          INFORMAÇÃO
      ================================== */}

      <View
        style={[
          styles.infoCard,
          {
            backgroundColor: cores.card,
            borderColor: cores.borda,
          },
        ]}
      >
        <Ionicons
          name="information-circle-outline"
          size={22}
          color={cores.primaria}
        />

        <Text
          style={[
            styles.infoText,
            {
              color: cores.textoSecundario,
            },
          ]}
        >
          Registre todas as movimentações para
          manter o estoque atualizado.
        </Text>
      </View>
    </View>
  );
}

// ========================================
// ESTILOS
// ========================================

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 20,
    justifyContent: 'center',
  },

  // ======================================
  // HEADER
  // ======================================

  header: {
    marginBottom: 30,
  },

  title: {
    fontSize: 30,
    fontWeight: 'bold',
  },

  subtitle: {
    fontSize: 14,
    marginTop: 6,
    lineHeight: 20,
  },

  // ======================================
  // BOTÕES
  // ======================================

  actionButton: {
    borderRadius: 24,
    padding: 20,
    marginBottom: 15,

    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',

    elevation: 4,

    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 3,
    },
    shadowOpacity: 0.15,
    shadowRadius: 5,
  },

  buttonContent: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },

  iconContainer: {
    width: 52,
    height: 52,
    borderRadius: 16,

    justifyContent: 'center',
    alignItems: 'center',
  },

  textGroup: {
    marginLeft: 15,
    flex: 1,
  },

  buttonTitle: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
  },

  buttonSubtitle: {
    color: '#E2E8F0',
    marginTop: 3,
    fontSize: 13,
  },

  // ======================================
  // INFORMAÇÃO
  // ======================================

  infoCard: {
    marginTop: 15,
    padding: 16,

    borderRadius: 16,
    borderWidth: 1,

    flexDirection: 'row',
    alignItems: 'center',
  },

  infoText: {
    flex: 1,
    marginLeft: 10,
    fontSize: 13,
    lineHeight: 19,
  },
});