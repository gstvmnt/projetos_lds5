from cinepy import db

class Filmes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    genero = db.Column(db.String(40), nullable=False)
    data_lancamento = db.Column(db.String(20), nullable=False)
    sinopse = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name



class Usuarios(db.Model):
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), primary_key=True)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Favoritos(db.Model):
    usuario_email = db.Column(db.String(100), db.ForeignKey('usuarios.email'), primary_key=True, nullable=False)
    filme_id = db.Column(db.Integer, db.ForeignKey('filmes.id'), primary_key=True, nullable=False)

    def __repr__(self):
        return f'<Favorito {self.usuario_email} - {self.filme_id}>'