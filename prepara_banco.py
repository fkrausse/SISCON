import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='Mili2013', host='localhost', port=3306)

# Descomente se quiser desfazer o banco...
#conn.cursor().execute("DROP DATABASE `siscon`;")
#conn.commit()

criar_tabelas = '''SET NAMES utf8;
    CREATE DATABASE `siscon` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `siscon`;
    CREATE TABLE `jogo` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `cta_ingreso` varchar(50) COLLATE utf8_bin NOT NULL,
      `cta_egreso` varchar(20) COLLATE utf8_bin NOT NULL,
      `fecha_factura` varchar(20) COLLATE utf8_bin NOT NULL,
      `ncomprobante` varchar(40) COLLATE utf8_bin NOT NULL,
      `nombre_entidad` varchar(40) COLLATE utf8_bin NOT NULL,
      `ruc_entidad` varchar(40) COLLATE utf8_bin NOT NULL,
      `forma_pago` varchar(40) COLLATE utf8_bin NOT NULL,
      `importe_total` varchar(40) COLLATE utf8_bin NOT NULL,
      `IVA5` varchar(40) COLLATE utf8_bin NOT NULL,
      `IVA10` varchar(40) COLLATE utf8_bin NOT NULL,
      `IVAexcentos` varchar(40) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `usuario` (
      `id` varchar(8) COLLATE utf8_bin NOT NULL,
      `nome` varchar(20) COLLATE utf8_bin NOT NULL,
      `senha` varchar(8) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(criar_tabelas)

# inserindo usuarios iniciais
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO siscon.usuario (id, nome, senha) VALUES (%s, %s, %s)',
      [
            ('jfeiten', 'Juliana Feiten', '12345'),
            ('fkrausse ', 'Fabian Krausse', '12345'),
      ])

cursor.execute('select * from siscon.usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
#cursor.executemany(
#      'INSERT INTO siscon.jogo (cta_ingreso, cta_egreso, fecha_factura, ncomprobante, nombre_entidad) VALUES (%s, %s, %s, %s, %s)',
#      [
#            ('God of War 4', 'Açao', 'PS4', 'jaja', 'sss'),
#            ('NBA 2k18', 'Esporte', 'Xbox One', 'jaja','lll')
#      ])

cursor.execute('select * from siscon.jogo')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()