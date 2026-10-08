import React, { useState } from 'react';

import {
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
  SafeAreaView,
  Alert,
  Image,
} from 'react-native';

import {
  MaterialIcons,
  FontAwesome,
} from '@expo/vector-icons';

import api from '../src/services/api';

// Tema global
import { useTheme } from '../context/ThemeContext';

export default function LoginScreen({ navigation }) {
  // ==============================
  // TEMA
  // ==============================

  const { cores } = useTheme();

  // ==============================
  // ESTADOS
  // ==============================

  const [e_mail, setE_mail] = useState('');
  const [senha, setSenha] = useState('');
  const [secureText, setSecureText] = useState(true);
  const [rememberMe, setRememberMe] = useState(false);

  // ==============================
  // LOGIN
  // ==============================

  const handleLogin = async () => {
    if (e_mail === '' || senha === '') {
      Alert.alert(
        'Erro',
        'Por favor, preencha todos os campos!'
      );

      return;
    }

    try {
      const response = await api.post('/login', {
        e_mail: e_mail,
        senha,
      });

      console.log(
        'RESPOSTA DO SERVIDOR:',
        response.data
      );

      if (
        response.data &&
        response.data.success === true
      ) {
        navigation.navigate('App');
      } else {
        Alert.alert(
          'Erro',
          response.data?.message ||
            'E-mail ou senha incorretos.'
        );
      }
    } catch (error) {
      console.log(
        'ERRO DO SERVIDOR:',
        error.response?.data
      );

      const mensagemErro =
        error.response?.data?.message ||
        'E-mail ou senha incorretos.';

      Alert.alert(
        'Erro de Login',
        mensagemErro
      );
    }
  };

  // ==============================
  // TELA
  // ==============================

  return (
    <SafeAreaView
      style={[
        styles.container,
        {
          backgroundColor: cores.fundo,
        },
      ]}
    >
      <View style={styles.content}>

        {/* ==================================
            LOGO
        ================================== */}

        <View style={styles.logoContainer}>
          <Image
            source={require('../assets/logo.png')}
            style={styles.logoImage}
            resizeMode="contain"
          />

          <Text
            style={[
              styles.brandName,
              {
                color: cores.primaria,
              },
            ]}
          >
            FlowTech
          </Text>
        </View>

        {/* ==================================
            BOAS-VINDAS
        ================================== */}

        <Text
          style={[
            styles.title,
            {
              color: cores.texto,
            },
          ]}
        >
          Bem-vindo!
        </Text>

        <Text
          style={[
            styles.subtitle,
            {
              color: cores.textoSecundario,
            },
          ]}
        >
          Faça seu login para continuar
        </Text>

        {/* ==================================
            E-MAIL
        ================================== */}

        <Text
          style={[
            styles.label,
            {
              color: cores.texto,
            },
          ]}
        >
          Login:
        </Text>

        <View
          style={[
            styles.inputContainer,
            {
              backgroundColor: cores.input,
              borderColor: cores.borda,
            },
          ]}
        >
          <MaterialIcons
            name="email"
            size={20}
            color={cores.textoSecundario}
            style={styles.inputIcon}
          />

          <TextInput
            style={[
              styles.input,
              {
                color: cores.texto,
              },
            ]}
            placeholder="Digite seu email"
            placeholderTextColor={
              cores.textoSecundario
            }
            keyboardType="email-address"
            autoCapitalize="none"
            value={e_mail}
            onChangeText={setE_mail}
          />
        </View>

        {/* ==================================
            SENHA
        ================================== */}

        <Text
          style={[
            styles.label,
            {
              color: cores.texto,
            },
          ]}
        >
          Senha:
        </Text>

        <View
          style={[
            styles.inputContainer,
            {
              backgroundColor: cores.input,
              borderColor: cores.borda,
            },
          ]}
        >
          <FontAwesome
            name="lock"
            size={20}
            color={cores.textoSecundario}
            style={styles.inputIcon}
          />

          <TextInput
            style={[
              styles.input,
              {
                color: cores.texto,
              },
            ]}
            placeholder="Digite sua senha"
            placeholderTextColor={
              cores.textoSecundario
            }
            secureTextEntry={secureText}
            value={senha}
            onChangeText={setSenha}
          />

          {/* OLHO DA SENHA */}

          <TouchableOpacity
            onPress={() =>
              setSecureText(!secureText)
            }
            style={styles.eyeButton}
          >
            <MaterialIcons
              name={
                secureText
                  ? 'visibility-off'
                  : 'visibility'
              }
              size={22}
              color={cores.textoSecundario}
            />
          </TouchableOpacity>
        </View>

        {/* ==================================
            OPÇÕES
        ================================== */}

        <View style={styles.rowOptions}>

          {/* LEMBRAR DE MIM */}

          <TouchableOpacity
            style={styles.checkboxContainer}
            onPress={() =>
              setRememberMe(!rememberMe)
            }
          >
            <View
              style={[
                styles.checkbox,
                {
                  borderColor:
                    cores.textoSecundario,
                },
                rememberMe && {
                  backgroundColor:
                    cores.primaria,
                  borderColor:
                    cores.primaria,
                },
              ]}
            >
              {rememberMe && (
                <MaterialIcons
                  name="check"
                  size={12}
                  color="#FFFFFF"
                />
              )}
            </View>

            <Text
              style={[
                styles.checkboxLabel,
                {
                  color: cores.texto,
                },
              ]}
            >
              Lembrar de mim
            </Text>
          </TouchableOpacity>

          {/* ESQUECI A SENHA */}

          <TouchableOpacity>
            <Text
              style={[
                styles.forgotPasswordText,
                {
                  color: cores.primaria,
                },
              ]}
            >
              Esqueci minha senha
            </Text>
          </TouchableOpacity>
        </View>

        {/* ==================================
            BOTÃO LOGIN
        ================================== */}

        <TouchableOpacity
          style={[
            styles.button,
            {
              backgroundColor: cores.primaria,
            },
          ]}
          onPress={handleLogin}
          activeOpacity={0.8}
        >
          <Text style={styles.buttonText}>
            Login
          </Text>
        </TouchableOpacity>

        {/* ==================================
            RODAPÉ
        ================================== */}

        <View style={styles.footer}>
          <TouchableOpacity>
            <Text
              style={[
                styles.footerLink,
                {
                  color: cores.primaria,
                },
              ]}
            >
              suporte
            </Text>
          </TouchableOpacity>

          <TouchableOpacity>
            <Text
              style={[
                styles.footerLink,
                {
                  color: cores.primaria,
                },
              ]}
            >
              termos de uso
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
}

// ========================================
// ESTILOS
// ========================================

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },

  content: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 30,
  },

  // ======================================
  // LOGO
  // ======================================

  logoContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },

  logoImage: {
    width: 150,
    height: 100,
    marginBottom: 0,
  },

  brandName: {
    fontSize: 28,
    fontWeight: 'bold',
  },

  // ======================================
  // TEXTOS
  // ======================================

  title: {
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 4,
  },

  subtitle: {
    fontSize: 13,
    textAlign: 'center',
    marginBottom: 25,
  },

  label: {
    fontSize: 14,
    marginBottom: 5,
    alignSelf: 'flex-start',
    fontWeight: '500',
  },

  // ======================================
  // INPUT
  // ======================================

  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',

    borderRadius: 20,

    paddingHorizontal: 12,

    marginBottom: 15,

    height: 48,

    borderWidth: 1,
  },

  inputIcon: {
    marginRight: 8,
  },

  input: {
    flex: 1,
    height: '100%',
    fontSize: 14,
  },

  eyeButton: {
    padding: 5,
  },

  // ======================================
  // OPÇÕES
  // ======================================

  rowOptions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',

    marginBottom: 35,
    marginTop: 5,
  },

  checkboxContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },

  checkbox: {
    width: 16,
    height: 16,

    borderWidth: 1.5,

    borderRadius: 3,

    justifyContent: 'center',
    alignItems: 'center',

    marginRight: 8,
  },

  checkboxLabel: {
    fontSize: 12,
  },

  forgotPasswordText: {
    fontSize: 12,
    textDecorationLine: 'underline',
  },

  // ======================================
  // BOTÃO
  // ======================================

  button: {
    height: 48,

    borderRadius: 24,

    justifyContent: 'center',
    alignItems: 'center',

    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.2,
    shadowRadius: 3,

    elevation: 3,
  },

  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },

  // ======================================
  // RODAPÉ
  // ======================================

  footer: {
    flexDirection: 'row',
    justifyContent: 'space-around',

    position: 'absolute',

    bottom: 30,
    left: 30,
    right: 30,
  },

  footerLink: {
    fontSize: 14,
    textDecorationLine: 'underline',
  },
});