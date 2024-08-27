from cinepy import app, db
from flask import request, render_template, flash, session, redirect, url_for
from models import Usuarios, Favoritos, Filmes
from helpers import FormularioUsuario, FormularioCadastro
from flask_bcrypt import check_password_hash, generate_password_hash



@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    form = FormularioUsuario(request.form)

    # Verificar se o email existe
    usuario = Usuarios.query.filter_by(email=form.email.data).first()

    if not usuario:
        flash('Usuário não está cadastrado')
        proxima_pagina = request.form.get('proxima', url_for('login'))
        return render_template('login.html', proxima=proxima_pagina, form=form)

    # Verificar a senha
    if check_password_hash(usuario.senha, form.senha.data):
        session['usuario_logado'] = usuario.email
        session['user_role'] = 'admin' if usuario.email == 'admin@admin.com' else 'user'
        flash(usuario.nome + ' logado com sucesso!')
        proxima_pagina = request.form.get('proxima', url_for('index'))
        return redirect(proxima_pagina)
    else:
        flash('Usuário ou senha incorretos')
        proxima_pagina = request.form.get('proxima', url_for('login'))
        return render_template('login.html', proxima=proxima_pagina, form=form)




@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado!')
    return redirect(url_for('index'))


@app.route('/cadastro')
def cadastrar():
    form = FormularioUsuario()
    return render_template('cadastro.html', form=form)


@app.route('/registrar', methods=['POST'])
def registrar():
    form = FormularioCadastro(request.form)  # Supondo que você tenha um formulário de cadastro
    if form.validate():  # Valida os dados do formulário
        # Verifica se o e-mail já está registrado
        usuario_existente = Usuarios.query.filter_by(email=form.email.data).first()
        if usuario_existente:
            flash('O e-mail já está registrado. Escolha outro e-mail.')
            return render_template('cadastro.html', form=form)

        # Cria um novo usuário
        nova_senha = generate_password_hash(form.senha.data)  # Gera o hash da senha
        novo_usuario = Usuarios(
            nome=form.nome.data,
            email=form.email.data,
            senha=nova_senha
        )
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('login'))
    else:
        flash('Por favor, preencha todos os campos corretamente.')
        return render_template('cadastro.html', form=form)


@app.route('/favoritar/<int:filme_id>')
def favoritar(filme_id):
    if 'usuario_logado' not in session:
        flash('Você precisa estar logado para favoritar um filme.')
        return redirect(url_for('login', proxima=url_for('favoritar', filme_id=filme_id)))

    usuario_email = session['usuario_logado']
    usuario = Usuarios.query.filter_by(email=usuario_email).first()
    filme = Filmes.query.filter_by(id=filme_id).first()

    if not filme:
        flash('Filme não encontrado.')
        return redirect(url_for('index'))

    # Verifica se o filme já está nos favoritos
    favorito_existente = Favoritos.query.filter_by(usuario_email=usuario.email, filme_id=filme_id).first()

    if favorito_existente:
        flash('Filme já está nos seus favoritos.')
    else:
        # Adiciona o filme aos favoritos
        novo_favorito = Favoritos(usuario_email=usuario.email, filme_id=filme.id)
        db.session.add(novo_favorito)
        db.session.commit()
        flash(f'Filme {filme.nome} adicionado aos favoritos!')

    return redirect(url_for('index'))




@app.route('/favoritos')
def favoritos():
    if 'usuario_logado' not in session:
        flash('Você precisa estar logado para ver seus filmes favoritos.')
        return redirect(url_for('login', proxima=url_for('favoritos')))

    usuario_email = session['usuario_logado']
    usuario = Usuarios.query.filter_by(email=usuario_email).first()
    filmes_favoritos = db.session.query(Filmes).join(Favoritos).filter(Favoritos.usuario_email == usuario_email).all()

    return render_template('favoritos.html', filmes_favoritos=filmes_favoritos, user_role=session.get('user_role'), usuario=usuario, str=str)



@app.route('/desfavoritar/<int:filme_id>')
def desfavoritar(filme_id):
    if 'usuario_logado' not in session:
        flash('Você precisa estar logado para desfavoritar um filme.')
        return redirect(url_for('login', proxima=url_for('desfavoritar', filme_id=filme_id)))

    usuario_email = session['usuario_logado']
    favorito = Favoritos.query.filter_by(usuario_email=usuario_email, filme_id=filme_id).first()

    if favorito:
        db.session.delete(favorito)
        db.session.commit()
        flash('Filme removido dos favoritos com sucesso.')
    else:
        flash('Filme não encontrado nos seus favoritos.')

    return redirect(url_for('favoritos'))


@app.route('/compartilhar_favoritos/<usuario_email>')
def compartilhar_favoritos(usuario_email):
    usuario = Usuarios.query.filter_by(email=usuario_email).first_or_404()
    favoritos = Favoritos.query.filter_by(usuario_email=usuario_email).all()
    filmes = [Filmes.query.get(filme.filme_id) for filme in favoritos]

    return render_template('compartilhar_favoritos.html', usuario=usuario, filmes=filmes, str=str)
