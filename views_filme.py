import os
from cinepy import app, db
from models import Filmes
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from helpers import recupera_imagem, deleta_arquivo, FormularioFilme


@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('index')))

    user_role = session.get('user_role', 'guest')

    lista = Filmes.query.order_by(Filmes.id)
    return render_template('home.html',  filmes = lista, str=str, user_role=user_role)

@app.route('/novo')
def novo():
    if session['user_role'] == 'user':
        return redirect(url_for('index'))

    form = FormularioFilme()
    return render_template('novo.html', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioFilme(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    genero = form.genero.data
    data_lancamento = form.data_lancamento.data
    sinopse = form.sinopse.data

    filme = Filmes.query.filter_by(nome=nome).first()

    if filme:
        flash('Filme já existente!')
        return redirect(url_for('index'))

    novo_filme = Filmes(nome=nome, genero=genero, data_lancamento=data_lancamento, sinopse=sinopse)
    db.session.add(novo_filme)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    if arquivo:
        arquivo.save(f'{upload_path}/capa{novo_filme.id}.jpg')
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if session['user_role'] == 'user':
        return redirect(url_for('index'))
    filme = Filmes.query.filter_by(id=id).first()

    form = FormularioFilme()
    form.nome.data = filme.nome
    form.genero.data = filme.genero
    form.data_lancamento.data = filme.data_lancamento
    form.sinopse.data = filme.sinopse

    capa_filme = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Filme', id=id, capa_filme=capa_filme, form=form)

@app.route('/atualizar', methods=['POST',])
def atualizar():

    form = FormularioFilme(request.form)

    if form.validate_on_submit():

        filme = Filmes.query.filter_by(id=request.form['id']).first()
        filme.nome = form.nome.data
        filme.genero = form.genero.data
        filme.data_lancamento = form.data_lancamento.data
        filme.sinopse = form.sinopse.data

        db.session.add(filme)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        if arquivo:
            deleta_arquivo(filme.id)
            arquivo.save(f'{upload_path}/capa{filme.id}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Filmes.query.filter_by(id=id).delete()
    deleta_arquivo(id)
    db.session.commit()
    flash(f'Filme deletado com sucesso!')
    return redirect(url_for('index'))



@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    caminho_imagem = os.path.join(app.config['UPLOAD_PATH'], nome_arquivo)
    if os.path.isfile(caminho_imagem):
        return send_from_directory(app.config['UPLOAD_PATH'], nome_arquivo)
    else:
        return send_from_directory(app.config['UPLOAD_PATH'], 'capa_padrao.jpg')



@app.route('/filme/<int:id>')
def filme_detalhes(id):
    filme = Filmes.query.filter_by(id=id).first()
    proxima = request.args.get('proxima', 'index')
    filme = {
        'id': id,
        'nome': filme.nome,
        'genero': filme.genero,
        'data_lancamento': filme.data_lancamento,
        'sinopse': filme.sinopse,
        'imagem': recupera_imagem(id)
    }
    return render_template('filmes_detalhes.html', filme=filme, str=str, proxima=proxima)

