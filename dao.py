from models import Jogo, Usuario
import time, datetime

SQL_DELETA_JOGO = 'delete from jogo where id = %s'
SQL_DELETA_USUARIO = 'delete from usuario where id = %s'
SQL_JOGO_POR_ID = 'SELECT id, cta_ingreso, cta_egreso, fecha_factura, ncomprobante, nombre_entidad, ruc_entidad, forma_pago, importe_total, IVA5, IVA10, IVAexcentos from jogo where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_ATUALIZA_JOGO = 'UPDATE jogo SET cta_ingreso=%s, cta_egreso=%s, fecha_factura=%s, ncomprobante=%s, nombre_entidad=%s, ruc_entidad=%s, forma_pago=%s, importe_total=%s, IVA5=%s, IVA10=%s, IVAexcentos=%s where id = %s'
SQL_ATUALIZA_USUARIO = 'UPDATE usuario SET id=%s, nome=%s, senha=%s where id = %s'
SQL_BUSCA_JOGOS = 'SELECT id, cta_ingreso, cta_egreso, fecha_factura, ncomprobante, nombre_entidad, ruc_entidad, forma_pago, importe_total, IVA5, IVA10, IVAexcentos from jogo'
SQL_BUSCA_USUARIOS = 'SELECT id, nome, senha from usuario'
SQL_CRIA_JOGO = 'INSERT into jogo (cta_ingreso, cta_egreso, fecha_factura, ncomprobante, nombre_entidad, ruc_entidad, forma_pago, importe_total, IVA5, IVA10, IVAexcentos) values ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
SQL_CRIA_USUARIO = 'INSERT into usuario (id, nome, senha) values ( %s, %s, %s)'

class JogoDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, jogo):
        cursor = self.__db.connection.cursor()
        
        if (jogo.id):
            cursor.execute(SQL_ATUALIZA_JOGO, (jogo.cta_ingreso, jogo.cta_egreso, jogo.fecha_factura, jogo.ncomprobante, jogo.nombre_entidad, jogo.ruc_entidad, jogo.forma_pago, jogo.importe_total, jogo.IVA5, jogo.IVA10, jogo.IVAexcentos, jogo.id))
        else:
            cursor.execute(SQL_CRIA_JOGO, (jogo.cta_ingreso, jogo.cta_egreso, jogo.fecha_factura, jogo.ncomprobante, jogo.nombre_entidad, jogo.ruc_entidad, jogo.forma_pago, jogo.importe_total, jogo.IVA5, jogo.IVA10, jogo.IVAexcentos))
            jogo.id = cursor.lastrowid
        self.__db.connection.commit()
        return jogo

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_JOGOS)
        jogos = traduz_jogos(cursor.fetchall())
        return jogos

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_JOGO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Jogo(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], tupla[9], tupla[10], tupla[11], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_JOGO, (id, ))
        self.__db.connection.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def salvarusuario(self, usuario):
            cursor = self.__db.connection.cursor()
            
            if (usuario.id):
                cursor.execute(SQL_ATUALIZA_USUARIO, (usuario.id, usuario.nome, usuario.senha))
            else:
                cursor.execute(SQL_CRIA_USUARIO, (usuario.id, usuario.nome, usuario.senha))
            self.__db.connection.commit()
            return usuario
            
    def listarusuario(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_USUARIOS)
        usuarios = traduz_usuarios(cursor.fetchall())
        return usuarios

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        return Usuario(dados[0], dados[1], dados[2])

    def deletarusuario(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_USUARIO, (id, ))
        self.__db.connection.commit()

def traduz_jogos(jogos):
    def cria_jogo_com_tupla(tupla):
        return Jogo(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], tupla[9], tupla[10], tupla[11], id=tupla[0])
    return list(map(cria_jogo_com_tupla, jogos))

def traduz_usuarios(usuarios):
    def cria_usuario_com_tupla(tuplas):
        return Usuario(tuplas[0], tuplas[1], tuplas[2])
    return list(map(cria_usuario_com_tupla, usuarios))