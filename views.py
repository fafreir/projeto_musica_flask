from flask import Flask, render_template, request, redirect, send_from_directory, session, flash, url_for
from models import Musica, Usuario
from musica import app, db
from definicoes import FormularioMusica, deletar_imagem, recupera_imagem
from time import time


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

    form = FormularioMusica()
    return render_template('cadastra_musica.html', titulo="Cadastrar música", form=form)


@app.route('/adicionar', methods=['POST',])
def adicionar_musica():

    formRecebido = FormularioMusica(request.form)

    if not formRecebido.validate_on_submit():
        return redirect(url_for('cadastrar_musica'))

    nome = formRecebido.nome.data
    cantorBanda = formRecebido.grupo.data
    genero = formRecebido.genero.data

    musica = Musica.query.filter_by(nome_musica=nome).first()

    if musica:
        flash("Musica já está cadastrada!")
        return redirect(url_for('listarMusicas'))

    nova_musica = Musica(
        nome_musica=nome, cantor_banda=cantorBanda, genero_musica=genero)
    db.session.add(nova_musica)
    db.session.commit()

    arquivo = request.files['arquivo']

    if arquivo:
        pasta_arquivo = app.config['UPLOAD_PASTA']

        nome_arquivo = arquivo.filename

        momento = time()

        extensao = nome_arquivo[len(nome_arquivo)-1]
        nome_completo = f'album{nova_musica.id_musica}+{momento}.{extensao}'

        arquivo.save(f'{pasta_arquivo}/{nome_completo}')
    return redirect(url_for('listarMusicas'))


@app.route('/editar/<int:id>')
def editar(id):
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login'))

    musicaBuscada = Musica.query.filter_by(id_musica=id).first()

    form = FormularioMusica()

    form.nome.data = musicaBuscada.nome_musica
    form.grupo.data = musicaBuscada.cantor_banda
    form.genero.data = musicaBuscada.genero_musica

    album = recupera_imagem(id)

    return render_template('editar_musica.html', titulo="Editar música", musica=form, album_musica=album, id = id)


@app.route('/atualizar', methods=['POST',])
def atualizar():

    formRecebido = FormularioMusica(request.form)
    
        if formRecebido.validate_on_submit():
            musica = Musica.query.filter_by(id_musica=request.form['txtId']).first()

            musica.nome_musica = formRecebido.nome.data
            musica.cantor_banda = formRecebido.grupo.data
            musica.genero_musica = formRecebido.genero.data

            db.session.add(musica)
            db.session.commit()

            arquivo = request.files['arquivo']
            pasta_upload = app.config['UPLOAD_PASTA']

            nome_arquivo = arquivo.filename
            nome_arquivo = nome_arquivo.split('.')

            momento = time()

            extensao = nome_arquivo[len(nome_arquivo)-1]
            nome_completo = f'album{musica.id_musica}_{momento}.{extensao}'

            deletar_imagem(musica.id_musica)

            arquivo.save(f'{pasta_upload}/{nome_completo}')
        
        flash("Musica editada com sucesso!")
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

    deletar_imagem(id)

    db.session.commit()
    flash('Musica excluida com sucesso')
    return redirect(url_for('listarMusicas'))


@ app.route('/sair')
def sair():
    session['usuario_logado'] = None

    return redirect(url_for('login'))


@app.route('/uploads/<nome_imagem>')
def imagem(nome_imagem):
    return send_from_directory('uploads', nome_imagem)
