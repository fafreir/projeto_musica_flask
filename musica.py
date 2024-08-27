from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'aprendendodoiniciocomdaniel'


class Musica:
    def __init__(self, nome, cantorBandaGrupo, genero):
        self.nome = nome
        self.cantorBanda = cantorBandaGrupo
        self.genero = genero


musica01 = Musica('Temporal', 'Hungria', 'Rap')
musica02 = Musica('Papai banca', 'Mc Ryan SP', 'Funk')
musica03 = Musica('Camisa 10', 'Turma do Pagode', 'Pagode')
lista = [musica01, musica02, musica03]


class Usuario:
    def __init__(self, nome, login, senha):
        self.nome = nome
        self.login = login
        self.senha = senha


usuario01 = Usuario("Daniel Xavier", "daniel.udemy", "admin")
usuario02 = Usuario("Fabrício", "fafreir", "udemy")
usuario03 = Usuario("Danielle", "dani", "dani")

usuarios = {
    usuario01.login: usuario01,
    usuario02.login: usuario02,
    usuario03.login: usuario03,
}


@app.route('/')
def listarMusicas():
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))
    return render_template('lista_musicas.html', titulo='Musicas cadastradas', musicas=lista)


@app.route('/cadastrar')
def cadastrar_musica():
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))
    return render_template('cadastra_musica.html', titulo="Cadastrar música")


@app.route('/adicionar', methods=['POST',])
def adicionar_musica():
    nome = request.form['txtNome']
    cantorBanda = request.form['txtCantor']
    genero = request.form['txtGenero']

    novaMusica = Musica(nome, cantorBanda, genero)
    lista.append(novaMusica)
    # return redirect('/')
    return redirect(url_for('listarMusicas'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/autenticar', methods=['POST',])
def autenticar():

    if request.form['txtLogin'] in usuarios:
        usuarioEncontrado = usuarios[request.form['txtLogin']]
        if request.form['txtSenha'] == usuarioEncontrado.senha:
            session['usuario_logado'] = request.form['txtLogin']
            flash(
                f"Seja bem-vindo {usuarioEncontrado.nome} logado com sucesso!")
            # return redirect('/')
            return redirect(url_for('listarMusicas'))
        else:
            flash("Senha inválida!")
            return redirect(url_for('login'))
    else:
        flash("Usuário ou senha inválida!")
        # return redirect('/login')
        return redirect(url_for('login'))


@app.route('/sair')
def sair():
    session['usuario_logado'] = None

    return redirect(url_for('login'))


app.run(debug=True)
