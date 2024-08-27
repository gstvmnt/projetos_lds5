import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `projeto_lds5`;")

cursor.execute("CREATE DATABASE `projeto_lds5`;")

cursor.execute("USE `projeto_lds5`;")

# criando tabelas
TABLES = {}
TABLES['Filmes'] = ('''
      CREATE TABLE `filmes` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `genero` varchar(40) NOT NULL,
      `data_lancamento` varchar(20) NOT NULL,
      `sinopse` varchar(300) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(100) NOT NULL,
      `email` varchar(100) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`email`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Favoritos'] = ('''
      CREATE TABLE `favoritos` (
      `usuario_email` varchar(100) NOT NULL,
      `filme_id` int(11) NOT NULL,
      PRIMARY KEY (`usuario_email`, `filme_id`),
      FOREIGN KEY (`usuario_email`) REFERENCES `usuarios`(`email`) ON DELETE CASCADE,
      FOREIGN KEY (`filme_id`) REFERENCES `filmes`(`id`) ON DELETE CASCADE
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print(f'Criando tabela {tabela_nome}:', end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Gustavo Monte", "gustavo@gmail.com", generate_password_hash("123").decode('utf-8')),
      ("Joao Vitor", "vitor@gmail.com", generate_password_hash("123").decode('utf-8')),
      ("admin", "admin@admin.com", generate_password_hash("123").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('SELECT * FROM projeto_lds5.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

cursor.execute('SELECT * FROM projeto_lds5.filmes')
print(' -------------  Filmes:  -------------')
for filme in cursor.fetchall():
    print(filme[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
