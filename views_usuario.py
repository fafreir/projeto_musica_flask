

from flask import flash, redirect, render_template, request, session, url_for
from definicoes import FormularioCadastroUsuario, FormularioUsuario
from musica import app


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


@app.route('/cadastraUsuario')
def cadastra_usuario():
    form = FormularioCadastroUsuario()
    return render_template("cadastra_usuario.html", titulo="Cadastro de Usuário", form=form)


@app.route('/sair')
def sair():
    session['usuario_logado'] = None

    return redirect('login')
