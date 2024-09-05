from flask import Flask, render_template, request, redirect, session, flash, url_for
from musica import app
from definicoes import deletar_imagem, FormularioUsuario


@app.route('/login')
def login():
    form = FormularioUsuario()
    return render_template('login.html', form=form)


@app.route('/autenticar', methods=['POST',])
def autenticar():
    from models import Usuario
    form = FormularioUsuario(request.form)

    usuario = Usuario.query.filter_by(
        login_usuario=form.usuario.data).first()
    if usuario:
        if form.senha.data == usuario.senha_usuario:
            session['usuario_logado'] = usuario.login_usuario
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


@ app.route('/sair')
def sair():
    session['usuario_logado'] = None

    return redirect(url_for('login'))
