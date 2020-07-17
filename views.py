from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from dao import JogoDao, UsuarioDao
from models import Jogo, Usuario
import os, time
from siscon import db, app
from helpers import deleta_arquivo, recupera_imagem
from flask_mysqldb import MySQL

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)

@app.route('/')
def index():
    return render_template('lista.html', titulo='CONTABILIDAD FABIAN')

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Nuevo Registro')

@app.route('/listado')
def listado():
    lista = jogo_dao.listar()
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('listado')))
    return render_template('listado.html', titulo='Registros', jogos=lista)

@app.route('/listadousuarios')
def listadousuarios():
    lista = usuario_dao.listarusuario()
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('listadousuarios')))
    return render_template('usuarios.html', titulo='Usuarios', usuarios=lista)

@app.route('/actualizar')
def actualizar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('listado')))
    flash('Informaciones actualizadas!')
    return redirect(url_for('listado'))

@app.route('/actualizarusuario')
def actualizarusuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('listadousuarios')))
    flash('Informaciones actualizadas!')
    return redirect(url_for('listadousuarios'))

@app.route('/criar', methods=['POST',])
def criar():
    cta_ingreso = request.form['cta_ingreso']
    cta_egreso = request.form['cta_egreso']
    fecha_factura = request.form['fecha_factura']
    ncomprobante = request.form['ncomprobante']
    nombre_entidad = request.form['nombre_entidad']
    ruc_entidad = request.form['ruc_entidad']
    forma_pago = request.form['forma_pago']
    importe_total = request.form['importe_total']
    IVA5 = request.form['IVA5']
    IVA10 = request.form['IVA10']
    IVAexcentos = request.form['IVAexcentos']
    jogo = Jogo(cta_ingreso, cta_egreso, fecha_factura, ncomprobante, nombre_entidad, ruc_entidad, forma_pago, importe_total, IVA5, IVA10, IVAexcentos)
    jogo = jogo_dao.salvar(jogo)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    return redirect(url_for('index'))

@app.route('/novousuario')
def novousuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('cargausuario')))
    return render_template('cargausuario.html', titulo='Nuevo Usuario')

@app.route('/criarusuario', methods=['POST',])
def criarusuario():
    id = request.form['id']
    nome = request.form['nome']
    senha = request.form['senha']
    usuario = Usuario(id, nome, senha)
    usuario = usuario_dao.salvarusuario(usuario)

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = jogo_dao.busca_por_id(id)
    cta_ingreso_imagem = recupera_imagem(id)
    return render_template('editar.html', titulo='Editar Registro', jogo=jogo, capa_jogo=cta_ingreso_imagem or 'capa_padrao.jpg')

@app.route('/atualizar', methods=['POST',])
def atualizar():
    cta_ingreso = request.form['cta_ingreso']
    cta_egreso = request.form['cta_egreso']
    fecha_factura = request.form['fecha_factura']
    ncomprobante = request.form['ncomprobante']
    nombre_entidad = request.form['nombre_entidad']
    ruc_entidad = request.form['ruc_entidad']
    forma_pago = request.form['forma_pago']
    importe_total = request.form['importe_total']
    IVA5 = request.form['IVA5']
    IVA10 = request.form['IVA10']
    IVAexcentos = request.form['IVAexcentos']
    jogo = Jogo(cta_ingreso, cta_egreso, fecha_factura, ncomprobante, nombre_entidad, ruc_entidad, forma_pago, importe_total, IVA5, IVA10, IVAexcentos, id=request.form['id'])

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    jogo_dao.salvar(jogo)
    return redirect(url_for('listado'))

@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao.deletar(id)
    flash('O jogo foi removido com sucesso!')
    return redirect(url_for('listado'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logado!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('No fue posible ingresar, intente nuevamente!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Ningun usuario logado!')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)



