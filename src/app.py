
import os
import time
import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)

def conectar_bd():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "app123"),
        database=os.getenv("DB_NAME", "holamundo")
    )

@app.route("/")
def hola_mundo():
    return """
        <h1>¡Hola Mundo!</h1>
        <p>Aplicación ejecutándose con Docker.</p>
        <p>Servidor: Python + Flask</p>
        <p><a href="/db">Comprobar conexión a MySQL</a></p>
    """

@app.route("/db")
def comprobar_bd():
    conexion = None

    try:
        # Reintentar mientras MySQL termina de iniciar.
        for intento in range(10):
            try:
                conexion = conectar_bd()
                break
            except mysql.connector.Error:
                if intento == 9:
                    raise
                time.sleep(3)

        cursor = conexion.cursor()
        cursor.execute("SELECT DATABASE(), VERSION()")
        resultado = cursor.fetchone()
        cursor.close()

        return jsonify({
            "mensaje": "Conexión exitosa con MySQL",
            "base_de_datos": resultado[0],
            "version_mysql": resultado[1]
        })

    except mysql.connector.Error as error:
        return jsonify({
            "mensaje": "Error al conectar con MySQL",
            "detalle": str(error)
        }), 500

    finally:
        if conexion and conexion.is_connected():
            conexion.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
