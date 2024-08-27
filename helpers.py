import os
from wtforms.validators import DataRequired, Email
from cinepy import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField

class FormularioFilme(FlaskForm):
    nome = StringField('Nome do Filme', [validators.DataRequired(), validators.Length(min=1, max=50)])
    genero = StringField('Gênero', [validators.DataRequired(), validators.Length(min=1, max=40)])
    data_lancamento = StringField('Data de Lançamento', [validators.DataRequired(), validators.Length(min=1, max=20)])
    sinopse = StringField('Sinopse', [validators.DataRequired(), validators.Length(min=1, max=300)])
    salvar = SubmitField('Salvar')


class FormularioUsuario(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=100)])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=1, max=100)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')


def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo.split('-')[0]:
            return nome_arquivo
    return 'capa_padrao.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))


class FormularioCadastro(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    login = SubmitField('Cadastrar')




