import React, {
  createContext,
  useContext,
  useState,
  useEffect
} from 'react';

import AsyncStorage from '@react-native-async-storage/async-storage';

const ThemeContext = createContext();

const temas = {
  escuro: {
    fundo: '#020617',
    card: '#1E293B',
    cardSecundario: '#0F172A',

    texto: '#FFFFFF',
    textoSecundario: '#94A3B8',

    primaria: '#0FB5AA',
    primariaEscura: '#04928B',

    azul: '#2563EB',

    borda: '#334155',

    sucesso: '#22C55E',
    erro: '#EF4444',
    alerta: '#F97316',

    input: '#0F172A',

    barraNavegacao: '#0F172A'
  },

  claro: {
    fundo: '#F1F5F9',
    card: '#FFFFFF',
    cardSecundario: '#E2E8F0',

    texto: '#0F172A',
    textoSecundario: '#64748B',

    primaria: '#0F9F96',
    primariaEscura: '#087F78',

    azul: '#2563EB',

    borda: '#CBD5E1',

    sucesso: '#16A34A',
    erro: '#DC2626',
    alerta: '#EA580C',

    input: '#FFFFFF',

    barraNavegacao: '#E2E8F0'
  }
};

export function ThemeProvider({ children }) {

  const [modo, setModo] = useState('escuro');

  useEffect(() => {
    carregarTema();
  }, []);

  async function carregarTema() {
    try {
      const temaSalvo = await AsyncStorage.getItem(
        '@stockpro_tema'
      );

      if (temaSalvo === 'claro' || temaSalvo === 'escuro') {
        setModo(temaSalvo);
      }

    } catch (error) {
      console.log('Erro ao carregar tema:', error);
    }
  }

  async function alterarTema(novoTema) {

    try {

      setModo(novoTema);

      await AsyncStorage.setItem(
        '@stockpro_tema',
        novoTema
      );

    } catch (error) {
      console.log('Erro ao salvar tema:', error);
    }
  }

  function alternarTema() {

    if (modo === 'escuro') {
      alterarTema('claro');
    } else {
      alterarTema('escuro');
    }

  }

  return (
    <ThemeContext.Provider
      value={{
        modo,
        cores: temas[modo],
        alterarTema,
        alternarTema
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}