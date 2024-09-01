from flask import Flask, render_template, request, redirect, session, flash, url_for
from models import Musica, Usuario
from musica import app, db


@app.route('/')
def listarMusicas():
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))
    lista = Musica.query.order_by(Musica.id_musica)
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

    musica = Musica.query.filter_by(nome_musica=nome).first()

    if musica:
        flash("Musica já está cadastrada!")
        return redirect(url_for('listarMusicas'))

    nova_musica = Musica(
        nome_musica=nome, cantor_banda=cantorBanda, genero_musica=genero)
    db.session.add(nova_musica)
    db.session.commit()

    arquivo = request.files['arquivo']
    pasta_arquivo = app.config['UPLOAD_PASTA']
    arquivo.save(f'{pasta_arquivo}/album{nova_musica.id_musica}.jpg')
    return redirect(url_for('listarMusicas'))


@app.route('/editar/<int:id>')
def editar(id):
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))

    musicaBuscada = Musica.query.filter_by(id_musica=id).first()
    return render_template('editar_musica.html', titulo="Editar música", musica=musicaBuscada)


@app.route('/atualizar', methods=['POST',])
def atualizar():
    musica = Musica.query.filter_by(id_musica=request.form['txtId']).first()

    musica.nome_musica = request.form['txtNome']
    musica.cantor_banda = request.form['txtCantor']
    musica.genero_musica = request.form['txtGenero']

    db.session.add(musica)
    db.session.commit()
    return redirect(url_for('listarMusicas'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/autenticar', methods=['POST',])
def autenticar():

    usuario = Usuario.query.filter_by(
        login_usuario=request.form['txtLogin']).first()
    if usuario:
        if request.form['txtSenha'] == usuario.senha_usuario:
            session['usuario_logado'] = request.form['txtLogin']
            flash(
                f"Seja bem-vindo {usuario.login_usuario} logado com sucesso!")
            return redirect(url_for('listarMusicas'))
        else:
            flash("Senha inválida!")
            return redirect(url_for('login'))
    else:
        flash("Usuário ou senha inválida!")
        # return redirect('/login')
        return redirect(url_for('login'))


@app.route('/excluir/<int:id>')
def excluir(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    Musica.query.filter_by(id_musica=id).delete()
    db.session.commit()
    flash('Musica excluida com sucesso')
    return redirect(url_for('listarMusicas'))


@ app.route('/sair')
def sair():
    session['usuario_logado'] = None

    return redirect(url_for('login'))
