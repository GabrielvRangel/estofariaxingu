import os
from threading import local
from flask import Flask, render_template, request, redirect
from sqlalchemy import Time, create_engine
import pandas as pd
import model
from datetime import datetime, timedelta

app = Flask(__name__)
localhost = 'http://estofaria-xingu.herokuapp.com/'
con = model.conexão()
custo_variavel_geral = model.custo_variavel_geral()
frete = model.frete()
items_adicionais = model.items_adicionais()
tecidos = model.tecido()
parâmetro = model.parâmetros()
usuarios = model.usuarios()
conexão = con.servidor()

@app.route("/", methods=["GET","POST"])
def index():
    parâmetros = parâmetro.consultar(conexão)
    tecido = tecidos.consultar(conexão)
    fretes = frete.consultar(conexão)
    itensadicionais = items_adicionais.consultar(conexão)
    custovariavelgeral = custo_variavel_geral.consultar(conexão)
    valor_hora_preparação = parâmetros[parâmetros['item'] == 'valor_hora_preparação'].iloc[0,1]
    valor_hora_costura = parâmetros[parâmetros['item'] == 'valor_hora_costura'].iloc[0,1]
    valor_hora_estofamento = parâmetros[parâmetros['item'] == 'valor_hora_estofamento'].iloc[0,1]
    custo_fixo_total = parâmetros[parâmetros['item'] == 'custo_fixo_total'].iloc[0,1]
    custo_fixo_geral = parâmetros[parâmetros['item'] == 'custo_fixo_geral'].iloc[0,1]
    horas_trabalhadas = parâmetros[parâmetros['item'] == 'horas_trabalhadas'].iloc[0,1]
    listapreçocustotecido = list(tecido['preco_compra'])
    listapreçoclientetecido = list(tecido['preco_venda'])
    listatecidos = list(tecido['artigo'])
    largura_padrão_espuma = parâmetros[parâmetros['item'] == 'largura_padrão_espuma'].iloc[0,1]
    preço_cliente_espumas = parâmetros[parâmetros['item'] == 'preço_cliente_espumas'].iloc[0,1]
    preço_estofaria_espumas = parâmetros[parâmetros['item'] == 'preço_estofaria_espumas'].iloc[0,1]
    preço_impermeabilização = parâmetros[parâmetros['item'] == 'preço_impermeabilização'].iloc[0,1]
    listabairro = list(fretes['bairro'])
    listavalorfrete = list(fretes['valor'])
    custovariavelgeral = custovariavelgeral.eval('valor_mes = valor_unitario * quantidade')
    custovariavelgeralacumuladomes = custovariavelgeral['valor_mes'].sum()
    listaitensadicionais = list(itensadicionais['item'])
    valorunitarioitensadicionais = list(itensadicionais['valor_unitario'])
    return render_template("index.html", valor_hora_preparação=valor_hora_preparação, valor_hora_costura=valor_hora_costura, valor_hora_estofamento=valor_hora_estofamento,
    custo_fixo_total=custo_fixo_total, custo_fixo_geral=custo_fixo_geral, horas_trabalhadas=horas_trabalhadas, listatecidos=listatecidos, listapreçocustotecido=listapreçocustotecido,
    listapreçoclientetecido=listapreçoclientetecido, largura_padrão_espuma=largura_padrão_espuma, listabairro=listabairro, listavalorfrete=listavalorfrete,
    custovariavelgeralacumuladomes=custovariavelgeralacumuladomes, listaitensadicionais=listaitensadicionais, valorunitarioitensadicionais=valorunitarioitensadicionais,
    preço_cliente_espumas=preço_cliente_espumas, preço_estofaria_espumas=preço_estofaria_espumas, preço_impermeabilização=preço_impermeabilização)

@app.route("/login", methods=["GET","POST"])
def login():
    return render_template("tela_login.html")

@app.route("/custovariavelgeral", methods=["GET","POST"])
def custovariavelgeralconsulta():
    custovariavelgeral = custo_variavel_geral.consultar(conexão)
    custovariavelgeraldeheading = list(custovariavelgeral)
    custovariavelgeralmaterial = list(custovariavelgeral['material'])
    custovariavelgeraluso = list(custovariavelgeral['uso'])
    custovariavelgeralvalorunitario = list(custovariavelgeral['valor_unitario'])
    custovariavelgeralquantidade = list(custovariavelgeral['quantidade'])
    return render_template("custovariavelgeral.html", custovariavelgeraldeheading=custovariavelgeraldeheading, custovariavelgeralmaterial=custovariavelgeralmaterial,
    custovariavelgeraluso=custovariavelgeraluso, custovariavelgeralvalorunitario=custovariavelgeralvalorunitario, custovariavelgeralquantidade=custovariavelgeralquantidade)

@app.route("/custovariavelgeraladicionar", methods=["GET"])
def custovariavelgeraladicionar():
    materialadicionar = request.args.get('materialadicionar')
    usoadicionar = request.args.get('usoadicionar')
    valorunitarioadicionar = float(request.args.get('valorunitarioadicionar'))
    quantidadeadicionar = float(request.args.get('quantidadeadicionar'))
    custo_variavel_geral.adicionar(conexão, materialadicionar, usoadicionar, valorunitarioadicionar, quantidadeadicionar)
    return redirect(localhost + 'custovariavelgeral', code=302)

@app.route("/custovariavelgeraldelete", methods=["GET"])
def custovariavelgeraldelete():
    materialdelete = request.args.get('materialdelete')
    usodelete = request.args.get('usodelete')
    valorunitariodelete = float(request.args.get('valorunitariodelete'))
    quantidadedelete = float(request.args.get('quantidadedelete'))
    custo_variavel_geral.deletar(conexão, materialdelete, usodelete, valorunitariodelete, quantidadedelete)
    return redirect(localhost + 'custovariavelgeral', code=302)

@app.route("/custovariavelgeralupdate", methods=["GET"])
def custovariavelgeralupdate():
    material = request.args.get('material')
    novomaterial = request.args.get('novomaterial')
    uso = request.args.get('uso')
    novouso = request.args.get('novouso')
    novovalorunitario = float(request.args.get('novovalorunitario'))
    valorunitario = float(request.args.get('valorunitario'))
    novoquantidade = float(request.args.get('novoquantidade'))
    quantidade = float(request.args.get('quantidade'))
    custo_variavel_geral.atualizar(conexão, material, novomaterial, uso, novouso, valorunitario, novovalorunitario, quantidade, novoquantidade)
    return redirect(localhost + 'custovariavelgeral', code=302)

@app.route("/frete", methods=["GET","POST"])
def freteconsulta():
    fretepandas = frete.consultar(conexão)
    freteheading = list(fretepandas)
    fretemunicípio = list(fretepandas['município'])
    fretebairro = list(fretepandas['bairro'])
    fretevalor = list(fretepandas['valor'])
    return render_template("frete.html", freteheading=freteheading, fretemunicípio=fretemunicípio, fretebairro=fretebairro, fretevalor=fretevalor)

@app.route("/freteadicionar", methods=["GET"])
def freteadicionar():
    municípioadicionar = request.args.get('municípioadicionar')
    bairroadicionar = request.args.get('bairroadicionar')
    valoradicionar = float(request.args.get('valoradicionar'))
    frete.adicionar(conexão, municípioadicionar, bairroadicionar, valoradicionar)
    return redirect(localhost + 'frete', code=302)

@app.route("/fretedelete", methods=["GET"])
def fretedelete():
    municípiodelete = request.args.get('municípiodelete')
    bairrodelete = request.args.get('bairrodelete')
    valordelete = float(request.args.get('valordelete'))
    frete.deletar(conexão, municípiodelete, bairrodelete, valordelete)
    return redirect(localhost + 'frete', code=302)

@app.route("/freteupdate", methods=["GET"])
def freteupdate():
    município = request.args.get('município')
    novomunicípio = request.args.get('novomunicípio')
    bairro = request.args.get('bairro')
    novobairro = request.args.get('novobairro')
    valor = float(request.args.get('valor'))
    novovalor = float(request.args.get('novovalor'))
    frete.atualizar(conexão, município, novomunicípio, bairro, novobairro, valor, novovalor)
    return redirect(localhost + 'frete', code=302)

@app.route("/itemsadicionais", methods=["GET","POST"])
def itemsadicionais():
    itemsadicionais = items_adicionais.consultar(conexão)
    itemsadicionaisheading = list(itemsadicionais)
    itemsadicionaisitem = list(itemsadicionais['item'])
    itemsadicionaisvalor_unitario = list(itemsadicionais['valor_unitario'])
    return render_template("items_adicionais.html", itemsadicionaisheading=itemsadicionaisheading, itemsadicionaisitem=itemsadicionaisitem, itemsadicionaisvalor_unitario=itemsadicionaisvalor_unitario)

@app.route("/itemsadicionaisadicionar", methods=["GET"])
def itemsadicionaisadicionar():
    itemadicionar = request.args.get('itemadicionar')
    valor_unitarioadicionar = request.args.get('valor_unitarioadicionar')
    items_adicionais.adicionar(conexão, itemadicionar, valor_unitarioadicionar)
    return redirect(localhost + 'itemsadicionais', code=302)

@app.route("/itemsadicionaisdelete", methods=["GET"])
def itemsadicionaisdelete():
    itemdelete = request.args.get('itemdelete')
    valor_unitariodelete = float(request.args.get('valor_unitariodelete'))
    items_adicionais.deletar(conexão, itemdelete, valor_unitariodelete)
    return redirect(localhost + 'itemsadicionais', code=302)

@app.route("/itemsadicionaisupdate", methods=["GET"])
def itemsadicionaisupdate():
    item = request.args.get('item')
    novoitem = request.args.get('novoitem')
    valor_unitario = float(request.args.get('valor_unitario'))
    novovalor_unitario = float(request.args.get('novovalor_unitario'))
    items_adicionais.atualizar(conexão, item, novoitem, valor_unitario, novovalor_unitario)
    return redirect(localhost + 'itemsadicionais', code=302)

@app.route("/parâmetros", methods=["GET","POST"])
def parâmetrosconsulta():
    parâmetros = parâmetro.consultar(conexão)
    parâmetrosheading = list(parâmetros)
    parâmetrositem = list(parâmetros['item'])
    parâmetrosvalor = list(parâmetros['valor'])
    return render_template("parâmetros.html", parâmetrosheading=parâmetrosheading, parâmetrositem=parâmetrositem, parâmetrosvalor=parâmetrosvalor)

@app.route("/parâmetrosadicionar", methods=["GET"])
def parâmetrosadicionar():
    itemadicionar = request.args.get('itemadicionar')
    valoradicionar = float(request.args.get('valoradicionar'))
    parâmetro.adicionar(conexão, itemadicionar, valoradicionar)
    return redirect(localhost + 'parâmetros', code=302)

@app.route("/parâmetrosdelete", methods=["GET"])
def parâmetrosdelete():
    itemdelete = request.args.get('itemdelete')
    valordelete = float(request.args.get('valordelete'))
    parâmetro.deletar(conexão, itemdelete, valordelete)
    return redirect(localhost + 'parâmetros', code=302)

@app.route("/parâmetrosupdate", methods=["GET"])
def parâmetrosupdate():
    item = request.args.get('item')
    novoitem = request.args.get('novoitem')
    valor = float(request.args.get('valor'))
    novovalor = float(request.args.get('novovalor'))
    parâmetro.atualizar(conexão, item, novoitem, valor, novovalor)
    return redirect(localhost + 'parâmetros', code=302)

@app.route("/tecido", methods=["GET","POST"])
def tecidoconsulta():
    tecido = tecidos.consultar(conexão)
    tecidoheading = list(tecido)
    tecidoartigo = list(tecido['artigo'])
    tecidopreco_venda = list(tecido['preco_venda'])
    tecidopreco_compra = list(tecido['preco_compra'])   
    return render_template("tecido.html", tecidoheading=tecidoheading, tecidoartigo=tecidoartigo, tecidopreco_venda=tecidopreco_venda, tecidopreco_compra=tecidopreco_compra)

@app.route("/tecidoadicionar", methods=["GET"])
def tecidoadicionar():
    artigoadicionar = request.args.get('artigoadicionar')
    preco_vendaadicionar = float(request.args.get('preco_vendaadicionar'))
    preco_compraadicionar = float(request.args.get('preco_compraadicionar'))
    tecidos.adicionar(conexão, artigoadicionar, preco_vendaadicionar, preco_compraadicionar)
    return redirect(localhost + 'tecido', code=302)

@app.route("/tecidodelete", methods=["GET"])
def tecidodelete():
    artigodelete = request.args.get('artigodelete')
    preco_vendadelete = float(request.args.get('preco_vendadelete'))
    preco_compradelete = float(request.args.get('preco_compradelete'))
    tecidos.deletar(conexão, artigodelete, preco_vendadelete, preco_compradelete)
    return redirect(localhost + 'tecido', code=302)

@app.route("/tecidoupdate", methods=["GET"])
def tecidoupdate():
    artigo = request.args.get('artigo')
    preco_venda = float(request.args.get('preco_venda'))
    preco_compra = float(request.args.get('preco_compra'))
    novoartigo = request.args.get('novoartigo')
    novopreco_venda = float(request.args.get('novopreco_venda'))
    novopreco_compra = float(request.args.get('novopreco_compra'))
    tecidos.atualizar(conexão, artigo, novoartigo, preco_venda, novopreco_venda, preco_compra, novopreco_compra)
    return redirect(localhost + 'tecido', code=302)

@app.route("/usuarios", methods=["GET","POST"])
def usuariosconsulta():
    usuarioss = usuarios.consultar(conexão)
    usuario = list(usuarioss['usuario'])
    senha = list(usuarioss['senha'])
    nome = list(usuarioss['nome'])   
    admin = list(usuarioss['admin'])
    email = list(usuarioss['email'])
    return render_template("usuarios.html", usuario=usuario, senha=senha, nome=nome, admin=admin, email=email)

@app.route("/usuariosadicionar", methods=["GET"])
def usuariosadicionar():
    usuarioadicionar = request.args.get('usuarioadicionar')
    senhaadicionar = request.args.get('senhaadicionar')
    nomeadicionar = request.args.get('nomeadicionar')
    adminadicionar = request.args.get('adminadicionar')
    emailadicionar = request.args.get('emailadicionar')
    print(usuarioadicionar)
    print(senhaadicionar)
    print(nomeadicionar)
    print(adminadicionar)
    print(emailadicionar)
    usuarios.adicionar(conexão, usuarioadicionar, senhaadicionar, nomeadicionar, adminadicionar,emailadicionar)
    return redirect(localhost + 'usuarios', code=302)

@app.route("/usuariosdelete", methods=["GET"])
def usuariosdelete():
    usuariodelete = request.args.get('usuariodelete')
    senhadelete = request.args.get('senhadelete')
    usuarios.deletar(conexão, usuariodelete, senhadelete)
    return redirect(localhost + 'usuarios', code=302)

@app.route("/usuariosupdate", methods=["GET"])
def usuariosupdate():
    usuario = request.args.get('usuario')
    novousuario = request.args.get('novousuario')
    senha = request.args.get('senha')
    novosenha = request.args.get('novosenha')
    nome = request.args.get('nome')
    novonome = request.args.get('novonome')
    admin = request.args.get('admin')
    novoadmin = request.args.get('novoadmin')
    email = request.args.get('email')
    novoemail = request.args.get('novoemail')
    usuarios.atualizar(conexão, usuario, novousuario, senha, novosenha, nome, novonome, admin, novoadmin, email, novoemail)
    return redirect(localhost + 'usuarios', code=302)

if __name__ == "__main__":
    app.run(debug= True) 