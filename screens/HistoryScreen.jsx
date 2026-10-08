import React, { useState, useCallback } from 'react';
import { View, Text, StyleSheet, FlatList, TextInput, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useFocusEffect } from '@react-navigation/native';
import api from '../src/services/api';

export default function HistoryScreen() {
  const [search, setSearch] = useState('');
  const [history, setHistory] = useState([]);

  const loadHistory = async () => {
    try {
      const response = await api.get('/history');
      setHistory(response.data);
    } catch (error) {
      console.log('Erro ao carregar histórico:', error);
    }
  };

  useFocusEffect(
    useCallback(() => {
      loadHistory();
    }, [])
  );

  const entriesCount = history.filter((h) => h.type === 'Entrada').length;
  const exitsCount = history.filter((h) => h.type === 'Saída').length;X

  const filteredHistory = history.filter(
    (item) =>
      item.product.toLowerCase().includes(search.toLowerCase()) ||
      item.type.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <View style={styles.container}>

      <View style={styles.header}>
        <View>
          <Text style={styles.title}>Histórico</Text>
          <Text style={styles.subtitle}>Movimentações do estoque</Text>
        </View>

        <TouchableOpacity style={styles.filterButton}>
          <Ionicons name="calendar-outline" size={24} color="#fff" />
        </TouchableOpacity>
      </View>

      <View style={styles.searchContainer}>
        <Ionicons name="search" size={22} color="#64748B" />

        <TextInput
          style={styles.searchInput}
          placeholder="Pesquisar movimentações..."
          placeholderTextColor="#94A3B8"
          value={search}
          onChangeText={setSearch}
        />
      </View>

      <View style={styles.statsContainer}>

        <View style={styles.statsCard}>
          <Ionicons name="arrow-down-circle" size={24} color="#007E83" />

          <Text style={styles.statsNumber}>{entriesCount}</Text>
          <Text style={styles.statsLabel}>Entradas</Text>
        </View>

        <View style={styles.statsCard}>
          <Ionicons name="arrow-up-circle" size={24} color="#EF4444" />

          <Text style={styles.statsNumber}>{exitsCount}</Text>
          <Text style={styles.statsLabel}>Saídas</Text>
        </View>

      </View>

      <FlatList
        data={filteredHistory}
        keyExtractor={(item) => item.id.toString()}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={{ paddingBottom: 40 }}

        renderItem={({ item }) => (
          <View style={styles.card}>

            <View
              style={[
                styles.iconContainer,
                {
                  backgroundColor:
                    item.type === 'Entrada' ? '#E8F7F7' : '#FEF0F0',
                },
              ]}
            >
              <Ionicons
                name={
                  item.type === 'Entrada'
                    ? 'arrow-down-circle'
                    : 'arrow-up-circle'
                }
                size={30}
                color={
                  item.type === 'Entrada'
                    ? '#007E83'
                    : '#EF4444'
                }
              />
            </View>

            <View style={styles.info}>

              <View style={styles.topRow}>
                <Text style={styles.product}>{item.product}</Text>

                <Text
                  style={[
                    styles.type,
                    {
                      color:
                        item.type === 'Entrada'
                          ? '#007E83'
                          : '#EF4444',
                    },
                  ]}
                >
                  {item.type}
                </Text>
              </View>

              <View style={styles.detailsRow}>
                <Text style={styles.quantity}>
                  Quantidade: {item.quantity}
                </Text>

                <Text style={styles.date}>
                  {item.date}
                </Text>
              </View>

              <Text style={styles.hour}>
                {item.hour}
              </Text>

            </View>
          </View>
        )}
      />

    </View>
  );
}

const styles = StyleSheet.create({

  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 20,
  },

  header: {
    marginTop: 55,
    marginBottom: 25,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },

  title: {
    color: '#0F172A',
    fontSize: 32,
    fontWeight: 'bold',
  },

  subtitle: {
    color: '#64748B',
    marginTop: 5,
    fontSize: 15,
  },

  filterButton: {
    width: 52,
    height: 52,
    backgroundColor: '#007E83',
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
  },

  searchContainer: {
    backgroundColor: '#FFFFFF',
    height: 62,
    borderRadius: 20,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 18,
    marginBottom: 25,
    borderWidth: 1,
    borderColor: '#D9E2E3',
  },

  searchInput: {
    flex: 1,
    marginLeft: 10,
    color: '#0F172A',
    fontSize: 16,
  },

  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 25,
  },

  statsCard: {
    width: '48%',
    backgroundColor: '#FFFFFF',
    borderRadius: 24,
    padding: 20,
    borderWidth: 1,
    borderColor: '#D9E2E3',
  },

  statsNumber: {
    color: '#0F172A',
    fontSize: 28,
    fontWeight: 'bold',
    marginTop: 12,
  },

  statsLabel: {
    color: '#64748B',
    marginTop: 6,
  },

  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 24,
    padding: 18,
    marginBottom: 18,
    flexDirection: 'row',
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },

  iconContainer: {
    width: 65,
    height: 65,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },

  info: {
    flex: 1,
  },

  topRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },

  product: {
    color: '#0F172A',
    fontSize: 18,
    fontWeight: 'bold',
    flex: 1,
    marginRight: 10,
  },

  type: {
    fontSize: 14,
    fontWeight: 'bold',
  },

  detailsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 10,
  },

  quantity: {
    color: '#475569',
    fontSize: 14,
  },

  date: {
    color: '#64748B',
    fontSize: 13,
  },

  hour: {
    color: '#94A3B8',
    marginTop: 8,
    fontSize: 13,
  },

});
