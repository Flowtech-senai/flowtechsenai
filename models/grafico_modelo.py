from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime

app = Flask(__name__)

CORS(app)


# =========================================================
# CONFIGURAÇÃO DO BANCO
# =========================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "estoque_db"
}


def conectar():

    return mysql.connector.connect(
        **DB_CONFIG
    )


# =========================================================
# SENSOR DHT11
# =========================================================

@app.route("/api/sensores")
def sensores():

    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            device_id,
            temperatura,
            umidade,
            timestamp
        FROM leituras
        WHERE sensor = 'DHT11'
        ORDER BY timestamp DESC
        LIMIT 100
    """)

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    dados.reverse()

    for item in dados:

        item["temperatura"] = float(
            item["temperatura"]
        ) if item["temperatura"] is not None else None

        item["umidade"] = float(
            item["umidade"]
        ) if item["umidade"] is not None else None

        item["timestamp"] = item[
            "timestamp"
        ].strftime("%Y-%m-%d %H:%M:%S")


    return jsonify(dados)


# =========================================================
# DISTÂNCIA HC-SR04
# =========================================================

@app.route("/api/distancia")
def distancia():

    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            device_id,
            distancia,
            timestamp
        FROM leituras
        WHERE sensor = 'HC-SR04'
        ORDER BY timestamp DESC
        LIMIT 100
    """)

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    dados.reverse()

    for item in dados:

        item["distancia"] = float(
            item["distancia"]
        ) if item["distancia"] is not None else None

        item["timestamp"] = item[
            "timestamp"
        ].strftime("%Y-%m-%d %H:%M:%S")


    return jsonify(dados)


# =========================================================
# RFID
# =========================================================

@app.route("/api/rfid")
def rfid():

    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            device_id,
            rfid_uid,
            timestamp
        FROM leituras
        WHERE sensor = 'MFRC522'
          AND rfid_uid IS NOT NULL
        ORDER BY timestamp DESC
        LIMIT 50
    """)

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    dados.reverse()


    # -----------------------------------------------------
    # Regra DIDÁTICA de entrada / saída
    # -----------------------------------------------------

    estados = {}

    for item in dados:

        uid = item["rfid_uid"]

        if uid not in estados:

            estados[uid] = "ENTRADA"

        else:

            if estados[uid] == "ENTRADA":

                estados[uid] = "SAIDA"

            else:

                estados[uid] = "ENTRADA"


        item["movimento"] = estados[uid]

        item["timestamp"] = item[
            "timestamp"
        ].strftime("%Y-%m-%d %H:%M:%S")


        # Produto fictício associado ao UID
        item["produto"] = (
            "Produto RFID " + uid[-4:]
        )


    return jsonify(dados)


# =========================================================
# RESUMO DO DASHBOARD
# =========================================================

@app.route("/api/resumo")
def resumo():

    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)


    # Última leitura DHT11

    cursor.execute("""
        SELECT
            temperatura,
            umidade,
            timestamp
        FROM leituras
        WHERE sensor = 'DHT11'
        ORDER BY timestamp DESC
        LIMIT 1
    """)

    sensor = cursor.fetchone()


    # Última leitura RFID

    cursor.execute("""
        SELECT
            rfid_uid,
            timestamp
        FROM leituras
        WHERE sensor = 'MFRC522'
          AND rfid_uid IS NOT NULL
        ORDER BY timestamp DESC
        LIMIT 1
    """)

    ultimo_rfid = cursor.fetchone()


    # Quantidade RFID

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM leituras
        WHERE sensor = 'MFRC522'
          AND rfid_uid IS NOT NULL
    """)

    total_rfid = cursor.fetchone()


    cursor.close()
    conexao.close()


    leitor_ativo = False


    if ultimo_rfid:

        agora = datetime.now()

        diferenca = (
            agora -
            ultimo_rfid["timestamp"]
        ).total_seconds()


        # Considera leitor ativo
        # se houve leitura nos últimos 60 segundos

        leitor_ativo = diferenca <= 60


    return jsonify({

        "temperatura":
            float(sensor["temperatura"])
            if sensor and sensor["temperatura"] is not None
            else None,

        "umidade":
            float(sensor["umidade"])
            if sensor and sensor["umidade"] is not None
            else None,

        "rfid_total":
            total_rfid["total"],

        "rfid_ultimo":
            ultimo_rfid["rfid_uid"]
            if ultimo_rfid
            else None,

        "leitor_ativo":
            leitor_ativo

    })


# =========================================================
# STATUS
# =========================================================

@app.route("/api/status")
def status():

    return jsonify({

        "api": "online",

        "banco": "sensores_db",

        "status": "OK"

    })


# =========================================================
# EXECUÇÃO
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )