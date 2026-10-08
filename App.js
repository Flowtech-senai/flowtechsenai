import React from 'react';

import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

import { Ionicons } from '@expo/vector-icons';

import { ThemeProvider, useTheme } from './context/ThemeContext';

import LoginScreen from './screens/LoginScreen';
import HomeScreen from './screens/HomeScreen';
import ProductsScreen from './screens/ProductsScreen';
import HistoryScreen from './screens/HistoryScreen';
import SettingsScreen from './screens/ConfiguracaoScreen';
import MovimentacaoScreen from './screens/MovimentacaoScreen';
import EntryScreen from './screens/EntryScreen';
import ExitScreen from './screens/ExitScreen';
import ConfiguracoesScreen from './screens/ConfiguracaoScreen';


const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();


// ===================================================== NAVEGAÇÃO PRINCIPAL COM TEMA =====================================================

function TabNavigator() {

  const { cores } = useTheme();

  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({

        headerShown: false,

        tabBarShowLabel: false,

        tabBarStyle: {
          backgroundColor: cores.barraNavegacao,
          borderTopWidth: 0,
          height: 65,
        },

        tabBarIcon: ({ focused }) => {

          let iconName = 'ellipse-outline';

          if (route.name === 'Home') {
            iconName = focused
              ? 'home'
              : 'home-outline';

          } else if (route.name === 'Produtos') {
            iconName = focused
              ? 'cube'
              : 'cube-outline';

          } else if (route.name === 'Movimentacao') {
            iconName = focused
              ? 'swap-horizontal'
              : 'swap-horizontal-outline';

          } else if (route.name === 'Entrada') {
            iconName = focused
              ? 'arrow-down-circle'
              : 'arrow-down-circle-outline';

          } else if (route.name === 'Saída') {
            iconName = focused
              ? 'arrow-up-circle'
              : 'arrow-up-circle-outline';

          } else if (route.name === 'Histórico') {
            iconName = focused
              ? 'time'
              : 'time-outline';

          } else if (route.name === 'Ajustes') {
            iconName = focused
              ? 'settings'
              : 'settings-outline';
          }

          return (
            <Ionicons
              name={iconName}
              size={24}
              color={
                focused
                  ? cores.azul
                  : cores.textoSecundario
              }
            />
          );
        },

      })}
    >

      <Tab.Screen
        name="Home"
        component={HomeScreen}
      />

      <Tab.Screen
        name="Produtos"
        component={ProductsScreen}
      />

      <Tab.Screen
        name="Movimentacao"
        component={MovimentacaoScreen}
      />

      <Tab.Screen
        name="Entrada"
        component={EntryScreen}
      />

      <Tab.Screen
        name="Saída"
        component={ExitScreen}
      />

      <Tab.Screen
        name="Histórico"
        component={HistoryScreen}
      />

      <Tab.Screen
        name="Ajustes"
        component={ConfiguracoesScreen}
      />

    </Tab.Navigator>
  );
}


// =====================================================
// APP
// =====================================================

export default function App() {

  return (

    <ThemeProvider>

      <NavigationContainer>

        <Stack.Navigator
          screenOptions={{
            headerShown: false,
          }}
        >

          {/* LOGIN */}

          <Stack.Screen
            name="Login"
            component={LoginScreen}
          />

          {/* SISTEMA */}

          <Stack.Screen
            name="App"
            component={TabNavigator}
          />

          {/* CONFIGURAÇÃO */}
          <Stack.Screen
            name="Configuracoes"
            component={ConfiguracoesScreen}
          />

        </Stack.Navigator>

      </NavigationContainer>

    </ThemeProvider>

  );
}