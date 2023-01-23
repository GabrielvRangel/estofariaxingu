import os
from threading import local
from flask import Flask, render_template, request, redirect, session, flash
from sqlalchemy import Time, create_engine
import pandas as pd
import model
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'xinguadmin'
localhost = 'http://estofaria-xingu.herokuapp.com/'
con = model.conexão()
custo_variavel_geral = model.custo_variavel_geral()  
frete = model.frete()
items_adicionais = model.items_adicionais()
tecidos = model.tecido()
parâmetro = model.parâmetros()
tabela_historico_calculadora = model.historico_calculadora()
usuarios = model.usuarios()
conexão = con.servidor()

@app.route("/", methods=["GET","POST"])
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html") 
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
    preço_cliente_espumas=preço_cliente_espumas, preço_estofaria_espumas=preço_estofaria_espumas, preço_impermeabilização=preço_impermeabilização, usuario_nome = session['nome'])

@app.route("/login", methods=["GET","POST"])
def login():
    usuario = request.args.get('usuario')
    senha = request.args.get('senha')
    tabela_usuario = usuarios.verificar_usuario(conexão, usuario, senha)
    permissao_logar = len(tabela_usuario)
    print(permissao_logar)
    if ('usuario_logado' not in session or session['usuario_logado'] == None) and  permissao_logar >= 1:
        session['usuario_logado'] = usuario
        session['admin'] = tabela_usuario.loc[0,'admin']
        session['nome'] = tabela_usuario.loc[0,'nome']
        return render_template("index.html", usuario_nome = session['nome'])
    if ('usuario_logado' not in session or session['usuario_logado'] == None) and  permissao_logar == 0:
        flash('Usuario ou senha incorreto.')
        return render_template("tela_login.html")
    if 'usuario_logado' in session and session['usuario_logado'] != None:
        return render_template("index.html", usuario_nome = session['nome'])
    
@app.route("/logout", methods=["GET","POST"])
def logout():
    session['usuario_logado'] = None
    session['admin'] = None
    return render_template("tela_login.html")
    

@app.route("/custovariavelgeral", methods=["GET","POST"])
def custovariavelgeralconsulta():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    custovariavelgeral = custo_variavel_geral.consultar(conexão)
    custovariavelgeraldeheading = list(custovariavelgeral)
    custovariavelgeralmaterial = list(custovariavelgeral['material'])
    custovariavelgeraluso = list(custovariavelgeral['uso'])
    custovariavelgeralvalorunitario = list(custovariavelgeral['valor_unitario'])
    custovariavelgeralquantidade = list(custovariavelgeral['quantidade'])
    return render_template("custovariavelgeral.html", custovariavelgeraldeheading=custovariavelgeraldeheading, custovariavelgeralmaterial=custovariavelgeralmaterial,
    custovariavelgeraluso=custovariavelgeraluso, custovariavelgeralvalorunitario=custovariavelgeralvalorunitario, custovariavelgeralquantidade=custovariavelgeralquantidade, usuario_nome = session['nome'])

@app.route("/custovariavelgeraladicionar", methods=["GET"])
def custovariavelgeraladicionar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    materialadicionar = request.args.get('materialadicionar')
    usoadicionar = request.args.get('usoadicionar')
    valorunitarioadicionar = float(request.args.get('valorunitarioadicionar'))
    quantidadeadicionar = float(request.args.get('quantidadeadicionar'))
    custo_variavel_geral.adicionar(conexão, materialadicionar, usoadicionar, valorunitarioadicionar, quantidadeadicionar)
    return redirect(localhost + 'custovariavelgeral', code=302)

@app.route("/custovariavelgeraldelete", methods=["GET"])
def custovariavelgeraldelete():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    materialdelete = request.args.get('materialdelete')
    usodelete = request.args.get('usodelete')
    valorunitariodelete = float(request.args.get('valorunitariodelete'))
    quantidadedelete = float(request.args.get('quantidadedelete'))
    custo_variavel_geral.deletar(conexão, materialdelete, usodelete, valorunitariodelete, quantidadedelete)
    return redirect(localhost + 'custovariavelgeral', code=302)

@app.route("/custovariavelgeralupdate", methods=["GET"])
def custovariavelgeralupdate():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
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
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    fretepandas = frete.consultar(conexão)
    freteheading = list(fretepandas)
    fretemunicípio = list(fretepandas['município'])
    fretebairro = list(fretepandas['bairro'])
    fretevalor = list(fretepandas['valor'])
    return render_template("frete.html", freteheading=freteheading, fretemunicípio=fretemunicípio, fretebairro=fretebairro, fretevalor=fretevalor, usuario_nome = session['nome'])

@app.route("/freteadicionar", methods=["GET"])
def freteadicionar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    municípioadicionar = request.args.get('municípioadicionar')
    bairroadicionar = request.args.get('bairroadicionar')
    valoradicionar = float(request.args.get('valoradicionar'))
    frete.adicionar(conexão, municípioadicionar, bairroadicionar, valoradicionar)
    return redirect(localhost + 'frete', code=302)

@app.route("/fretedelete", methods=["GET"])
def fretedelete():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    municípiodelete = request.args.get('municípiodelete')
    bairrodelete = request.args.get('bairrodelete')
    valordelete = float(request.args.get('valordelete'))
    frete.deletar(conexão, municípiodelete, bairrodelete, valordelete)
    return redirect(localhost + 'frete', code=302)

@app.route("/freteupdate", methods=["GET"])
def freteupdate():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
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
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    itemsadicionais = items_adicionais.consultar(conexão)
    itemsadicionaisheading = list(itemsadicionais)
    itemsadicionaisitem = list(itemsadicionais['item'])
    itemsadicionaisvalor_unitario = list(itemsadicionais['valor_unitario'])
    return render_template("items_adicionais.html", itemsadicionaisheading=itemsadicionaisheading, itemsadicionaisitem=itemsadicionaisitem, itemsadicionaisvalor_unitario=itemsadicionaisvalor_unitario, usuario_nome = session['nome'])

@app.route("/itemsadicionaisadicionar", methods=["GET"])
def itemsadicionaisadicionar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    itemadicionar = request.args.get('itemadicionar')
    valor_unitarioadicionar = request.args.get('valor_unitarioadicionar')
    items_adicionais.adicionar(conexão, itemadicionar, valor_unitarioadicionar)
    return redirect(localhost + 'itemsadicionais', code=302)

@app.route("/itemsadicionaisdelete", methods=["GET"])
def itemsadicionaisdelete():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    itemdelete = request.args.get('itemdelete')
    valor_unitariodelete = float(request.args.get('valor_unitariodelete'))
    items_adicionais.deletar(conexão, itemdelete, valor_unitariodelete)
    return redirect(localhost + 'itemsadicionais', code=302)

@app.route("/itemsadicionaisupdate", methods=["GET"])
def itemsadicionaisupdate():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    item = request.args.get('item')
    novoitem = request.args.get('novoitem')
    valor_unitario = float(request.args.get('valor_unitario'))
    novovalor_unitario = float(request.args.get('novovalor_unitario'))
    items_adicionais.atualizar(conexão, item, novoitem, valor_unitario, novovalor_unitario)
    return redirect(localhost + 'itemsadicionais', code=302)

@app.route("/parâmetros", methods=["GET","POST"])
def parâmetrosconsulta():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    parâmetros = parâmetro.consultar(conexão)
    parâmetrosheading = list(parâmetros)
    parâmetrositem = list(parâmetros['item'])
    parâmetrosvalor = list(parâmetros['valor'])
    return render_template("parâmetros.html", parâmetrosheading=parâmetrosheading, parâmetrositem=parâmetrositem, parâmetrosvalor=parâmetrosvalor, usuario_nome = session['nome'])

@app.route("/parâmetrosadicionar", methods=["GET"])
def parâmetrosadicionar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    itemadicionar = request.args.get('itemadicionar')
    valoradicionar = float(request.args.get('valoradicionar'))
    parâmetro.adicionar(conexão, itemadicionar, valoradicionar)
    return redirect(localhost + 'parâmetros', code=302)

@app.route("/parâmetrosdelete", methods=["GET"])
def parâmetrosdelete():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    itemdelete = request.args.get('itemdelete')
    valordelete = float(request.args.get('valordelete'))
    parâmetro.deletar(conexão, itemdelete, valordelete)
    return redirect(localhost + 'parâmetros', code=302)

@app.route("/parâmetrosupdate", methods=["GET"])
def parâmetrosupdate():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    item = request.args.get('item')
    novoitem = request.args.get('novoitem')
    valor = float(request.args.get('valor'))
    novovalor = float(request.args.get('novovalor'))
    parâmetro.atualizar(conexão, item, novoitem, valor, novovalor)
    return redirect(localhost + 'parâmetros', code=302)

@app.route("/tecido", methods=["GET","POST"])
def tecidoconsulta():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    tecido = tecidos.consultar(conexão)
    tecidoheading = list(tecido)
    tecidoartigo = list(tecido['artigo'])
    tecidopreco_venda = list(tecido['preco_venda'])
    tecidopreco_compra = list(tecido['preco_compra'])   
    return render_template("tecido.html", tecidoheading=tecidoheading, tecidoartigo=tecidoartigo, tecidopreco_venda=tecidopreco_venda, tecidopreco_compra=tecidopreco_compra, usuario_nome = session['nome'])

@app.route("/tecidoadicionar", methods=["GET"])
def tecidoadicionar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    artigoadicionar = request.args.get('artigoadicionar')
    preco_vendaadicionar = float(request.args.get('preco_vendaadicionar'))
    preco_compraadicionar = float(request.args.get('preco_compraadicionar'))
    tecidos.adicionar(conexão, artigoadicionar, preco_vendaadicionar, preco_compraadicionar)
    return redirect(localhost + 'tecido', code=302)

@app.route("/tecidodelete", methods=["GET"])
def tecidodelete():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    artigodelete = request.args.get('artigodelete')
    preco_vendadelete = float(request.args.get('preco_vendadelete'))
    preco_compradelete = float(request.args.get('preco_compradelete'))
    tecidos.deletar(conexão, artigodelete, preco_vendadelete, preco_compradelete)
    return redirect(localhost + 'tecido', code=302)

@app.route("/tecidoupdate", methods=["GET"])
def tecidoupdate():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    artigo = request.args.get('artigo')
    preco_venda = float(request.args.get('preco_venda'))
    preco_compra = float(request.args.get('preco_compra'))
    novoartigo = request.args.get('novoartigo')
    novopreco_venda = float(request.args.get('novopreco_venda'))
    novopreco_compra = float(request.args.get('novopreco_compra'))
    tecidos.atualizar(conexão, artigo, novoartigo, preco_venda, novopreco_venda, preco_compra, novopreco_compra)
    return redirect(localhost + 'tecido', code=302)

@app.route("/historico_calculadora", methods=["GET","POST"])
def historico_calculadora():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    historicos_calculadora = tabela_historico_calculadora.consultar(conexão)
    historicos_calculadora_heading = list(historicos_calculadora)
    historicos_calculadora_data = list(historicos_calculadora['data'])
    historicos_calculadora_usuario = list(historicos_calculadora['usuario'])
    historicos_calculadora_mdo_hr_preparacao = list(historicos_calculadora['mdo_hr_preparacao'])
    historicos_calculadora_mdo_valor_preparacao = list(historicos_calculadora['mdo_valor_preparacao'])
    historicos_calculadora_mdo_hr_costura = list(historicos_calculadora['mdo_hr_costura'])
    historicos_calculadora_mdo_valor_costura = list(historicos_calculadora['mdo_valor_costura'])
    historicos_calculadora_mdo_hr_estofamento = list(historicos_calculadora['mdo_hr_estofamento'])
    historicos_calculadora_mdo_valor_estofamento = list(historicos_calculadora['mdo_valor_estofamento'])
    historicos_calculadora_mdo_valor_geral = list(historicos_calculadora['mdo_valor_geral'])
    historicos_calculadora_mdo_percentual_hr = list(historicos_calculadora['mdo_percentual_hr'])
    historicos_calculadora_mdo_total_valor = list(historicos_calculadora['mdo_total_valor'])
    historicos_calculadora_tipo_tecido = list(historicos_calculadora['tipo_tecido'])
    historicos_calculadora_qtd_tecido = list(historicos_calculadora['qtd_tecido'])
    historicos_calculadora_valor_estofaria_tecido = list(historicos_calculadora['valor_estofaria_tecido'])
    historicos_calculadora_valor_cliente_tecido = list(historicos_calculadora['valor_cliente_tecido'])
    historicos_calculadora_qtd_espuma_1 = list(historicos_calculadora['qtd_espuma_1'])
    historicos_calculadora_altura_espuma_1 = list(historicos_calculadora['altura_espuma_1'])
    historicos_calculadora_largura_espuma_1 = list(historicos_calculadora['largura_espuma_1'])
    historicos_calculadora_comprimento_espuma_1 = list(historicos_calculadora['comprimento_espuma_1'])
    historicos_calculadora_valor_estofaria_espuma_1 = list(historicos_calculadora['valor_estofaria_espuma_1'])
    historicos_calculadora_valor_estofaria_cliente_1 = list(historicos_calculadora['valor_estofaria_cliente_1'])
    historicos_calculadora_qtd_espuma_2 = list(historicos_calculadora['qtd_espuma_2'])
    historicos_calculadora_altura_espuma_2 = list(historicos_calculadora['altura_espuma_2'])
    historicos_calculadora_largura_espuma_2 = list(historicos_calculadora['largura_espuma_2'])
    historicos_calculadora_comprimento_espuma_2 = list(historicos_calculadora['comprimento_espuma_2'])
    historicos_calculadora_valor_estofaria_espuma_2 = list(historicos_calculadora['valor_estofaria_espuma_2'])
    historicos_calculadora_valor_estofaria_cliente_2 = list(historicos_calculadora['valor_estofaria_cliente_2'])
    historicos_calculadora_qtd_espuma_3 = list(historicos_calculadora['qtd_espuma_3'])
    historicos_calculadora_altura_espuma_3 = list(historicos_calculadora['altura_espuma_3'])
    historicos_calculadora_largura_espuma_3 = list(historicos_calculadora['largura_espuma_3'])
    historicos_calculadora_comprimento_espuma_3 = list(historicos_calculadora['comprimento_espuma_3'])
    historicos_calculadora_valor_estofaria_espuma_3 = list(historicos_calculadora['valor_estofaria_espuma_3'])
    historicos_calculadora_valor_estofaria_cliente_3 = list(historicos_calculadora['valor_estofaria_cliente_3'])
    historicos_calculadora_qtd_espuma_4 = list(historicos_calculadora['qtd_espuma_4'])
    historicos_calculadora_altura_espuma_4 = list(historicos_calculadora['altura_espuma_4'])
    historicos_calculadora_largura_espuma_4 = list(historicos_calculadora['largura_espuma_4'])
    historicos_calculadora_comprimento_espuma_4 = list(historicos_calculadora['comprimento_espuma_4'])
    historicos_calculadora_valor_estofaria_espuma_4 = list(historicos_calculadora['valor_estofaria_espuma_4'])
    historicos_calculadora_valor_estofaria_cliente_4 = list(historicos_calculadora['valor_estofaria_cliente_4'])
    historicos_calculadora_valor_total_estofaria_espuma = list(historicos_calculadora['valor_total_estofaria_espuma'])
    historicos_calculadora_valor_total_cliente_espuma = list(historicos_calculadora['valor_total_cliente_espuma'])
    historicos_calculadora_status_impermeabilizacao = list(historicos_calculadora['status_impermeabilizacao'])
    historicos_calculadora_valor_impermeabilizacao = list(historicos_calculadora['valor_impermeabilizacao'])
    historicos_calculadora_frete_bairro = list(historicos_calculadora['frete_bairro'])
    historicos_calculadora_valor_frete = list(historicos_calculadora['valor_frete'])
    historicos_calculadora_valor_socializado = list(historicos_calculadora['valor_socializado'])
    historicos_calculadora_item_adicional_1 = list(historicos_calculadora['item_adicional_1'])
    historicos_calculadora_qtd_adicional_1 = list(historicos_calculadora['qtd_adicional_1'])
    historicos_calculadora_valor_adicional_1 = list(historicos_calculadora['valor_adicional_1'])
    historicos_calculadora_item_adicional_2 = list(historicos_calculadora['item_adicional_2'])
    historicos_calculadora_qtd_adicional_2 = list(historicos_calculadora['qtd_adicional_2'])
    historicos_calculadora_valor_adicional_2 = list(historicos_calculadora['valor_adicional_2'])
    historicos_calculadora_item_adicional_3 = list(historicos_calculadora['item_adicional_3'])
    historicos_calculadora_qtd_adicional_3 = list(historicos_calculadora['qtd_adicional_3'])
    historicos_calculadora_valor_adicional_3 = list(historicos_calculadora['valor_adicional_3'])
    historicos_calculadora_valor_total_item_adicional = list(historicos_calculadora['valor_total_item_adicional'])
    historicos_calculadora_custo_fixo = list(historicos_calculadora['custo_fixo'])
    historicos_calculadora_custo_variavel_estofaria = list(historicos_calculadora['custo_variavel_estofaria'])
    historicos_calculadora_custo_variavel_cliente = list(historicos_calculadora['custo_variavel_cliente'])
    historicos_calculadora_total_estofaria = list(historicos_calculadora['total_estofaria'])
    historicos_calculadora_total_cliente = list(historicos_calculadora['total_cliente'])
    historicos_calculadora_percentual_calculado = list(historicos_calculadora['percentual_calculado'])
    historicos_calculadora_percentual_margem_alvo = list(historicos_calculadora['percentual_margem_alvo'])
    historicos_calculadora_preco_alvo = list(historicos_calculadora['preco_alvo'])
    return render_template("historico_calculadora.html", usuario_nome = session['nome'], historicos_calculadora_heading=historicos_calculadora_heading,
    historicos_calculadora_data = historicos_calculadora_data, historicos_calculadora_usuario = historicos_calculadora_usuario,
    historicos_calculadora_mdo_hr_preparacao = historicos_calculadora_mdo_hr_preparacao, historicos_calculadora_mdo_valor_preparacao = historicos_calculadora_mdo_valor_preparacao,
    historicos_calculadora_mdo_hr_costura = historicos_calculadora_mdo_hr_costura, historicos_calculadora_mdo_valor_costura = historicos_calculadora_mdo_valor_costura,
    historicos_calculadora_mdo_hr_estofamento = historicos_calculadora_mdo_hr_estofamento, historicos_calculadora_mdo_valor_estofamento = historicos_calculadora_mdo_valor_estofamento,
    historicos_calculadora_mdo_valor_geral = historicos_calculadora_mdo_valor_geral, historicos_calculadora_mdo_percentual_hr = historicos_calculadora_mdo_percentual_hr,
    historicos_calculadora_mdo_total_valor = historicos_calculadora_mdo_total_valor, historicos_calculadora_tipo_tecido = historicos_calculadora_tipo_tecido,
    historicos_calculadora_qtd_tecido = historicos_calculadora_qtd_tecido, historicos_calculadora_valor_estofaria_tecido = historicos_calculadora_valor_estofaria_tecido,
    historicos_calculadora_valor_cliente_tecido = historicos_calculadora_valor_cliente_tecido, historicos_calculadora_qtd_espuma_1 = historicos_calculadora_qtd_espuma_1,
    historicos_calculadora_altura_espuma_1 = historicos_calculadora_altura_espuma_1, historicos_calculadora_largura_espuma_1 = historicos_calculadora_largura_espuma_1,
    historicos_calculadora_comprimento_espuma_1 = historicos_calculadora_comprimento_espuma_1, historicos_calculadora_valor_estofaria_espuma_1 = historicos_calculadora_valor_estofaria_espuma_1,
    historicos_calculadora_valor_estofaria_cliente_1 = historicos_calculadora_valor_estofaria_cliente_1, historicos_calculadora_qtd_espuma_2 = historicos_calculadora_qtd_espuma_2,
    historicos_calculadora_altura_espuma_2 = historicos_calculadora_altura_espuma_2, historicos_calculadora_largura_espuma_2 = historicos_calculadora_largura_espuma_2,
    historicos_calculadora_comprimento_espuma_2 = historicos_calculadora_comprimento_espuma_2, historicos_calculadora_valor_estofaria_espuma_2 = historicos_calculadora_valor_estofaria_espuma_2,
    historicos_calculadora_valor_estofaria_cliente_2 = historicos_calculadora_valor_estofaria_cliente_2, historicos_calculadora_qtd_espuma_3 = historicos_calculadora_qtd_espuma_3,
    historicos_calculadora_altura_espuma_3 = historicos_calculadora_altura_espuma_3, historicos_calculadora_largura_espuma_3 = historicos_calculadora_largura_espuma_3,
    historicos_calculadora_comprimento_espuma_3 = historicos_calculadora_comprimento_espuma_3, historicos_calculadora_valor_estofaria_espuma_3 = historicos_calculadora_valor_estofaria_espuma_3,
    historicos_calculadora_valor_estofaria_cliente_3 = historicos_calculadora_valor_estofaria_cliente_3 ,
    historicos_calculadora_qtd_espuma_4 = historicos_calculadora_qtd_espuma_4, historicos_calculadora_altura_espuma_4 = historicos_calculadora_altura_espuma_4 ,
    historicos_calculadora_largura_espuma_4 = historicos_calculadora_largura_espuma_4, historicos_calculadora_comprimento_espuma_4 = historicos_calculadora_comprimento_espuma_4 ,
    historicos_calculadora_valor_estofaria_espuma_4 = historicos_calculadora_valor_estofaria_espuma_4, historicos_calculadora_valor_estofaria_cliente_4 = historicos_calculadora_valor_estofaria_cliente_4,
    historicos_calculadora_valor_total_estofaria_espuma = historicos_calculadora_valor_total_estofaria_espuma, historicos_calculadora_valor_total_cliente_espuma = historicos_calculadora_valor_total_cliente_espuma,
    historicos_calculadora_status_impermeabilizacao = historicos_calculadora_status_impermeabilizacao, historicos_calculadora_valor_impermeabilizacao = historicos_calculadora_valor_impermeabilizacao ,
    historicos_calculadora_frete_bairro = historicos_calculadora_frete_bairro, historicos_calculadora_valor_frete = historicos_calculadora_valor_frete ,
    historicos_calculadora_valor_socializado = historicos_calculadora_valor_socializado, historicos_calculadora_item_adicional_1 = historicos_calculadora_item_adicional_1 ,
    historicos_calculadora_qtd_adicional_1 = historicos_calculadora_qtd_adicional_1, historicos_calculadora_valor_adicional_1 = historicos_calculadora_valor_adicional_1 ,
    historicos_calculadora_item_adicional_2 = historicos_calculadora_item_adicional_2, historicos_calculadora_qtd_adicional_2 = historicos_calculadora_qtd_adicional_2 ,
    historicos_calculadora_valor_adicional_2 = historicos_calculadora_valor_adicional_2, historicos_calculadora_item_adicional_3 = historicos_calculadora_item_adicional_3 ,
    historicos_calculadora_qtd_adicional_3 = historicos_calculadora_qtd_adicional_3, historicos_calculadora_valor_adicional_3 = historicos_calculadora_valor_adicional_3 ,
    historicos_calculadora_valor_total_item_adicional = historicos_calculadora_valor_total_item_adicional, historicos_calculadora_custo_fixo = historicos_calculadora_custo_fixo ,
    historicos_calculadora_custo_variavel_estofaria = historicos_calculadora_custo_variavel_estofaria, historicos_calculadora_custo_variavel_cliente = historicos_calculadora_custo_variavel_cliente ,
    historicos_calculadora_total_estofaria = historicos_calculadora_total_estofaria, historicos_calculadora_total_cliente = historicos_calculadora_total_cliente ,
    historicos_calculadora_percentual_calculado = historicos_calculadora_percentual_calculado, historicos_calculadora_percentual_margem_alvo = historicos_calculadora_percentual_margem_alvo ,
    historicos_calculadora_preco_alvo = historicos_calculadora_preco_alvo)

@app.route("/historico_calculadora_adicionar", methods=["GET"])
def historico_calculadora_adicionar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    usuario = str(session['nome'])
    mdo_hr_preparacao = str(request.args.get('mdo_hr_preparacao'))
    mdo_valor_preparacao = str(request.args.get('mdo_valor_preparacao'))
    mdo_hr_costura = str(request.args.get('mdo_hr_costura'))
    mdo_valor_costura = str(request.args.get('mdo_valor_costura'))
    mdo_hr_estofamento = str(request.args.get('mdo_hr_estofamento'))
    mdo_valor_estofamento = str(request.args.get('mdo_valor_estofamento'))
    mdo_valor_geral = str(request.args.get('mdo_valor_geral'))
    mdo_percentual_hr = str(request.args.get('mdo_percentual_hr'))
    mdo_total_valor = str(request.args.get('mdo_total_valor'))
    tipo_tecido = str(request.args.get('tipo_tecido'))
    qtd_tecido = str(request.args.get('qtd_tecido'))
    valor_estofaria_tecido = str(request.args.get('valor_estofaria_tecido'))
    valor_cliente_tecido = str(request.args.get('valor_cliente_tecido'))
    qtd_espuma_1 = str(request.args.get('qtd_espuma_1'))
    altura_espuma_1 = str(request.args.get('altura_espuma_1'))
    largura_espuma_1 = str(request.args.get('largura_espuma_1'))
    comprimento_espuma_1 = str(request.args.get('comprimento_espuma_1'))
    valor_estofaria_espuma_1 = str(request.args.get('valor_estofaria_espuma_1'))
    valor_estofaria_cliente_1 = str(request.args.get('valor_estofaria_cliente_1'))
    qtd_espuma_2 = str(request.args.get('qtd_espuma_2'))
    altura_espuma_2 = str(request.args.get('altura_espuma_2'))
    largura_espuma_2 = str(request.args.get('largura_espuma_2'))
    comprimento_espuma_2 = str(request.args.get('comprimento_espuma_2'))
    valor_estofaria_espuma_2 = str(request.args.get('valor_estofaria_espuma_2'))
    valor_estofaria_cliente_2 = str(request.args.get('valor_estofaria_cliente_2'))
    qtd_espuma_3 = str(request.args.get('qtd_espuma_3'))
    altura_espuma_3 = str(request.args.get('altura_espuma_3'))
    largura_espuma_3 = str(request.args.get('largura_espuma_3'))
    comprimento_espuma_3 = str(request.args.get('comprimento_espuma_3'))
    valor_estofaria_espuma_3 = str(request.args.get('valor_estofaria_espuma_3'))
    valor_estofaria_cliente_3 = str(request.args.get('valor_estofaria_cliente_3'))
    qtd_espuma_4 = str(request.args.get('qtd_espuma_4'))
    altura_espuma_4 = str(request.args.get('altura_espuma_4'))
    largura_espuma_4 = str(request.args.get('largura_espuma_4'))
    comprimento_espuma_4 = str(request.args.get('comprimento_espuma_4'))
    valor_estofaria_espuma_4 = str(request.args.get('valor_estofaria_espuma_4'))
    valor_estofaria_cliente_4 = str(request.args.get('valor_estofaria_cliente_4'))
    valor_total_estofaria_espuma = str(request.args.get('valor_total_estofaria_espuma'))
    valor_total_cliente_espuma = str(request.args.get('valor_total_cliente_espuma'))
    status_impermeabilizacao = str(request.args.get('status_impermeabilizacao'))
    valor_impermeabilizacao = str(request.args.get('valor_impermeabilizacao'))
    frete_bairro = str(request.args.get('frete_bairro'))
    valor_frete = str(request.args.get('valor_frete'))
    valor_socializado = str(request.args.get('valor_socializado'))
    item_adicional_1 = str(request.args.get('item_adicional_1'))
    qtd_adicional_1 = str(request.args.get('qtd_adicional_1'))
    valor_adicional_1 = str(request.args.get('valor_adicional_1'))
    item_adicional_2 = str(request.args.get('item_adicional_2'))
    qtd_adicional_2 = str(request.args.get('qtd_adicional_2'))
    valor_adicional_2 = str(request.args.get('valor_adicional_2'))
    item_adicional_3 = str(request.args.get('item_adicional_3'))
    qtd_adicional_3 = str(request.args.get('qtd_adicional_3'))
    valor_adicional_3 = str(request.args.get('valor_adicional_3'))
    valor_total_item_adicional = str(request.args.get('valor_total_item_adicional'))
    custo_fixo = str(request.args.get('custo_fixo'))
    custo_variavel_estofaria = str(request.args.get('custo_variavel_estofaria'))
    custo_variavel_cliente = str(request.args.get('custo_variavel_cliente'))
    total_estofaria = str(request.args.get('total_estofaria'))
    total_cliente = str(request.args.get('total_cliente'))
    percentual_calculado = str(request.args.get('percentual_calculado'))
    percentual_margem_alvo = str(request.args.get('percentual_margem_alvo'))
    preco_alvo = str(request.args.get('preco_alvo'))
    tabela_historico_calculadora.adicionar(conexão, data, usuario, mdo_hr_preparacao, mdo_valor_preparacao, mdo_hr_costura, mdo_valor_costura, mdo_hr_estofamento, mdo_valor_estofamento, mdo_valor_geral, mdo_percentual_hr, mdo_total_valor, tipo_tecido, qtd_tecido, valor_estofaria_tecido, valor_cliente_tecido, qtd_espuma_1, altura_espuma_1, largura_espuma_1, comprimento_espuma_1, valor_estofaria_espuma_1, valor_estofaria_cliente_1, qtd_espuma_2, altura_espuma_2, largura_espuma_2, comprimento_espuma_2, valor_estofaria_espuma_2, valor_estofaria_cliente_2, qtd_espuma_3, altura_espuma_3, largura_espuma_3, comprimento_espuma_3, valor_estofaria_espuma_3, valor_estofaria_cliente_3, qtd_espuma_4, altura_espuma_4, largura_espuma_4, comprimento_espuma_4, valor_estofaria_espuma_4, valor_estofaria_cliente_4, valor_total_estofaria_espuma, valor_total_cliente_espuma, status_impermeabilizacao, valor_impermeabilizacao, frete_bairro, valor_frete, valor_socializado, item_adicional_1, qtd_adicional_1, valor_adicional_1, item_adicional_2, qtd_adicional_2, valor_adicional_2, item_adicional_3, qtd_adicional_3, valor_adicional_3, valor_total_item_adicional, custo_fixo, custo_variavel_estofaria, custo_variavel_cliente, total_estofaria, total_cliente, percentual_calculado, percentual_margem_alvo, preco_alvo)
    return redirect(localhost + 'historico_calculadora', code=302)

@app.route("/usuarios", methods=["GET","POST"])
def usuariosconsulta():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    if session['admin'] == 'Não':
        flash('Você não tem acesso administrador para utilizar a aba usuários.')
        return render_template("index.html")
    usuarioss = usuarios.consultar(conexão)
    usuario = list(usuarioss['usuario'])
    senha = list(usuarioss['senha'])
    nome = list(usuarioss['nome'])   
    admin = list(usuarioss['admin'])
    email = list(usuarioss['email'])
    return render_template("usuarios.html", usuario=usuario, senha=senha, nome=nome, admin=admin, email=email, usuario_nome = session['nome'])

@app.route("/usuariosadicionar", methods=["GET"])
def usuariosadicionar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    if session['admin'] == 'Não':
        flash('Você não tem acesso administrador para utilizar a aba usuários.')
        return render_template("index.html")
    usuarioadicionar = request.args.get('usuarioadicionar')
    senhaadicionar = request.args.get('senhaadicionar')
    nomeadicionar = request.args.get('nomeadicionar')
    adminadicionar = request.args.get('adminadicionar')
    emailadicionar = request.args.get('emailadicionar')
    usuarios.adicionar(conexão, usuarioadicionar, senhaadicionar, nomeadicionar, adminadicionar,emailadicionar)
    return redirect(localhost + 'usuarios', code=302)

@app.route("/usuariosdelete", methods=["GET"])
def usuariosdelete():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    if session['admin'] == 'Não':
        flash('Você não tem acesso administrador para utilizar a aba usuários.')
        return render_template("index.html")    
    usuariodelete = request.args.get('usuariodelete')
    senhadelete = request.args.get('senhadelete')
    usuarios.deletar(conexão, usuariodelete, senhadelete)
    return redirect(localhost + 'usuarios', code=302)

@app.route("/usuariosupdate", methods=["GET"])
def usuariosupdate():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return render_template("tela_login.html")
    if session['admin'] == 'Não':
        flash('Você não tem acesso administrador para utilizar a aba usuários.')
        return render_template("index.html")
    usuario = request.args.get('usuario')
    senha = request.args.get('senha')
    novosenha = request.args.get('novosenha')
    nome = request.args.get('nome')
    novonome = request.args.get('novonome')
    admin = request.args.get('admin')
    novoadmin = request.args.get('novoadmin')
    email = request.args.get('email')
    novoemail = request.args.get('novoemail')
    usuarios.atualizar(conexão, usuario, senha, novosenha, nome, novonome, admin, novoadmin, email, novoemail)
    return redirect(localhost + 'usuarios', code=302)

if __name__ == "__main__":
    app.run(debug= True) 