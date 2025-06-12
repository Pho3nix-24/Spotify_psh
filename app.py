from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario")
    contrasena = request.form.get("contrasena")
    
    # Aquí podrías guardar los datos, pero NO LO HAGAS (es solo una simulación).
    print(f"[SIMULACIÓN] Usuario: {usuario}, Contraseña: {contrasena}")
    
    return redirect(url_for("alerta"))

@app.route("/alerta")
def alerta():
    return render_template("alerta.html")

if __name__ == "__main__":
    app.run(debug=True)