from sqlite3 import Timestamp
from sqlalchemy import Time, create_engine
import pandas as pd
import datetime
import requests
import os
import json
import sqlalchemy

class conexão():
     def servidor(self):
        banco =  os.environ['banco']
        conectar = sqlalchemy.create_engine(f"""{banco}""", pool_pre_ping=True)
        return conectar


class custo_variavel_geral():
    def consultar(self, conexão):
        consulta = "select * from custo_variavel_geral order by material"
        custo_variavel_geral = pd.read_sql_query(consulta, con=conexão)
        return custo_variavel_geral

    def deletar(self, connect, material, uso, valorunitario, quantidade):
        con = connect.connect() 
        sql = f"""
        DELETE FROM custo_variavel_geral
        WHERE material = '{material}' and uso = '{uso}' and valor_unitario = {valorunitario} and quantidade = {quantidade}
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Deletado com sucesso.')

    def adicionar(self, connect, material, uso, valorunitario, quantidade):
        con = connect.connect() 
        sql = f"""
        INSERT  INTO  custo_variavel_geral(material, uso, valor_unitario, quantidade)
        VALUES ('{material}', '{uso}', {valorunitario}, {quantidade});
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Atualização realizada.')

    def atualizar(self, connect, material, novomaterial, uso, novouso, valorunitario, novovalorunitario, quantidade, novoquantidade):
        con = connect.connect() 
        sql = f"""
        UPDATE custo_variavel_geral 
        SET material = '{novomaterial}',  uso = '{novouso}',  valor_unitario = {novovalorunitario}, quantidade = {novoquantidade}
        WHERE material = '{material}' and uso = '{uso}' and valor_unitario = {valorunitario} and quantidade = {quantidade}
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Atualização realizada.')

class frete():
    def consultar(self, conexão):
        consulta = "select * from frete order by município, bairro"
        frete = pd.read_sql_query(consulta, con=conexão)
        return frete

    def deletar(self, connect, município, bairro, valor):
        con = connect.connect() 
        sql = f"""
        DELETE FROM frete
        WHERE município = '{município}' and bairro = '{bairro}' and valor = {valor}
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Deletado com sucesso.')

    def adicionar(self, connect, município, bairro, valor):
        con = connect.connect() 
        sql = f"""
        INSERT  INTO  frete(município, bairro, valor)
        VALUES ('{município}', '{bairro}', {valor});
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Atualização realizada.')

    def atualizar(self, connect, município, novomunicípio, bairro, novobairro, valor, novovalor):
        con = connect.connect() 
        sql = f"""
        UPDATE frete 
        SET município = '{novomunicípio}',  bairro = '{novobairro}',  valor = {novovalor}
        WHERE município = '{município}' and bairro = '{bairro}' and valor = {valor}
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Atualização realizada.')

class items_adicionais():
    def consultar(self, conexão):
        consulta = "select * from items_adicionais order by item"
        items_adicionais = pd.read_sql_query(consulta, con=conexão)
        return items_adicionais

    def deletar(self, connect, item, valor_unitario):
        con = connect.connect() 
        sql = f"""
        DELETE FROM items_adicionais
        WHERE item = '{item}' and valor_unitario = '{valor_unitario}'
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Deletado com sucesso.')

    def adicionar(self, connect, item, valor_unitario):
        con = connect.connect() 
        sql = f"""
        INSERT  INTO  items_adicionais(item, valor_unitario)
        VALUES ('{item}', '{valor_unitario}');
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Atualização realizada.')

    def atualizar(self, connect, item, novoitem, valor_unitario, novovalor_unitario):
        con = connect.connect() 
        sql = f"""
        UPDATE items_adicionais 
        SET item = '{novoitem}',  valor_unitario = '{novovalor_unitario}'
        WHERE item = '{item}' and valor_unitario = '{valor_unitario}'
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Atualização realizada.')
 

class tecido():
    def consultar(self, conexão):
        consulta = "select * from tecido order by tecido"
        tecido = pd.read_sql_query(consulta, con=conexão)
        return tecido

    def deletar(self, connect, artigo, preco_venda, preco_compra):
        con = connect.connect() 
        sql = f"""
        DELETE FROM tecido
        WHERE artigo = '{artigo}' and preco_venda = '{preco_venda}' and preco_compra = '{preco_compra}'
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Deletado com sucesso.')

    def adicionar(self, connect, artigo, preco_venda, preco_compra):
        con = connect.connect() 
        sql = f"""
        INSERT  INTO  tecido(artigo, preco_venda, preco_compra)
        VALUES ('{artigo}', '{preco_venda}', '{preco_compra}');
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Atualização realizada.')

    def atualizar(self, connect, artigo, novoartigo, preco_venda, novopreco_venda, preco_compra, novopreco_compra):
        con = connect.connect() 
        sql = f"""
        UPDATE tecido 
        SET artigo = '{novoartigo}',  preco_venda = '{novopreco_venda}',  preco_compra = '{novopreco_compra}'
        WHERE artigo = '{artigo}' and preco_venda = '{preco_venda}' and preco_compra = '{preco_compra}'
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Atualização realizada.')
 
 

class parâmetros():
    def consultar(self, conexão):
        consulta = "select * from parâmetros order by item"
        parâmetros = pd.read_sql_query(consulta, con=conexão)
        return parâmetros

    def deletar(self, connect, item, valor):
        con = connect.connect() 
        sql = f"""
        DELETE FROM parâmetros
        WHERE item = '{item}' and valor = '{valor}'
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Deletado com sucesso.')

    def adicionar(self, connect, item, valor):
        con = connect.connect() 
        sql = f"""
        INSERT  INTO  parâmetros(item, valor)
        VALUES ('{item}', '{valor}');
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Atualização realizada.')

    def atualizar(self, connect, item, novoitem, valor, novovalor):
        con = connect.connect() 
        sql = f"""
        UPDATE parâmetros 
        SET item = '{novoitem}',  valor = '{novovalor}'
        WHERE item = '{item}' and valor = '{valor}'
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Atualização realizada.')

class usuarios():
    def verificar_usuario(self, conexão, usuario, senha):
        consulta = f"select * from usuarios where usuario = '{usuario}' and senha = '{senha}'"
        usuarios = pd.read_sql_query(consulta, con=conexão)
        return usuarios
        

    def consultar(self, conexão):
        consulta = "select * from usuarios order by usuario"
        usuarios = pd.read_sql_query(consulta, con=conexão)
        return usuarios

    def deletar(self, connect, usuario, senha):
        con = connect.connect() 
        sql = f"""
        DELETE FROM usuarios
        WHERE "usuario" = '{usuario}' and "senha" = '{senha}'
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Deletado com sucesso.')

    def adicionar(self, connect, usuario, senha, nome, admin, email):
        con = connect.connect() 
        sql = f"""
        INSERT  INTO  usuarios("usuario", "senha", "nome", "admin", "email")
        VALUES ('{usuario}', '{senha}', '{nome}', '{admin}', '{email}');
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Atualização realizada.')

    def atualizar(self, connect, usuario, senha, novosenha, nome, novonome, admin, novoadmin, email, novoemail):
        con = connect.connect() 
        sql = f"""
        UPDATE usuarios
        SET "senha" = '{novosenha}',  "nome" = '{novonome}', "admin" = '{novoadmin}', "email" = '{novoemail}'
        WHERE "usuario" = '{usuario}' and "senha" = '{senha}' and "nome" = '{nome}' and "admin" = '{admin}' and "email" = '{email}'
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Atualização realizada.')

class historico_calculadora():
    def consultar(self, conexão):
        consulta = "select * from historico_calculadora order by data"
        historico_calculadora = pd.read_sql_query(consulta, con=conexão)
        return historico_calculadora

    # def deletar(self, connect, data, usuario):
    #     con = connect.connect() 
    #     sql = f"""
    #     DELETE FROM historico_calculadora
    #     WHERE data = '{data}' and usuario = '{usuario}'
    #     """
    #     try:
    #         trans = con.begin()
    #         con.execute(sql)
    #         trans.commit()
    #     except:
    #         trans.rollback()
    #     return print('Deletado com sucesso.')

    def adicionar(self, connect, data, usuario, mdo_hr_preparacao, mdo_valor_preparacao, mdo_hr_costura, mdo_valor_costura, mdo_hr_estofamento, mdo_valor_estofamento, mdo_valor_geral, mdo_percentual_hr, mdo_total_valor, tipo_tecido, qtd_tecido, valor_estofaria_tecido, valor_cliente_tecido, qtd_espuma_1, altura_espuma_1, largura_espuma_1, comprimento_espuma_1, valor_estofaria_espuma_1, valor_estofaria_cliente_1, qtd_espuma_2, altura_espuma_2, largura_espuma_2, comprimento_espuma_2, valor_estofaria_espuma_2, valor_estofaria_cliente_2, qtd_espuma_3, altura_espuma_3, largura_espuma_3, comprimento_espuma_3, valor_estofaria_espuma_3, valor_estofaria_cliente_3, qtd_espuma_4, altura_espuma_4, largura_espuma_4, comprimento_espuma_4, valor_estofaria_espuma_4, valor_estofaria_cliente_4, valor_total_estofaria_espuma, valor_total_cliente_espuma, status_impermeabilizacao, valor_impermeabilizacao, frete_bairro, valor_frete, valor_socializado, item_adicional_1, qtd_adicional_1, valor_adicional_1, item_adicional_2, qtd_adicional_2, valor_adicional_2, item_adicional_3, qtd_adicional_3, valor_adicional_3, valor_total_item_adicional, custo_fixo, custo_variavel_estofaria, custo_variavel_cliente, total_estofaria, total_cliente, percentual_calculado, percentual_margem_alvo, preco_alvo):
        con = connect.connect() 
        sql = f"""
        INSERT INTO historico_calculadora(data, usuario, mdo_hr_preparacao, mdo_valor_preparacao, mdo_hr_costura, mdo_valor_costura, mdo_hr_estofamento, mdo_valor_estofamento, mdo_valor_geral, mdo_percentual_hr, mdo_total_valor, tipo_tecido, qtd_tecido, valor_estofaria_tecido, valor_cliente_tecido, qtd_espuma_1, altura_espuma_1, largura_espuma_1, comprimento_espuma_1, valor_estofaria_espuma_1, valor_estofaria_cliente_1, qtd_espuma_2, altura_espuma_2, largura_espuma_2, comprimento_espuma_2, valor_estofaria_espuma_2, valor_estofaria_cliente_2, qtd_espuma_3, altura_espuma_3, largura_espuma_3, comprimento_espuma_3, valor_estofaria_espuma_3, valor_estofaria_cliente_3, qtd_espuma_4, altura_espuma_4, largura_espuma_4, comprimento_espuma_4, valor_estofaria_espuma_4, valor_estofaria_cliente_4, valor_total_estofaria_espuma, valor_total_cliente_espuma, status_impermeabilizacao, valor_impermeabilizacao, frete_bairro, valor_frete, valor_socializado, item_adicional_1, qtd_adicional_1, valor_adicional_1, item_adicional_2, qtd_adicional_2, valor_adicional_2, item_adicional_3, qtd_adicional_3, valor_adicional_3, valor_total_item_adicional, custo_fixo, custo_variavel_estofaria, custo_variavel_cliente, total_estofaria, total_cliente, percentual_calculado, percentual_margem_alvo, preco_alvo)
        VALUES ('{data}', '{usuario}', {mdo_hr_preparacao}, {mdo_valor_preparacao}, {mdo_hr_costura}, {mdo_valor_costura}, {mdo_hr_estofamento}, {mdo_valor_estofamento}, {mdo_valor_geral}, {mdo_percentual_hr}, {mdo_total_valor}, '{tipo_tecido}', {qtd_tecido}, {valor_estofaria_tecido}, {valor_cliente_tecido}, {qtd_espuma_1}, {altura_espuma_1}, {largura_espuma_1}, {comprimento_espuma_1}, {valor_estofaria_espuma_1}, {valor_estofaria_cliente_1}, {qtd_espuma_2}, {altura_espuma_2}, {largura_espuma_2}, {comprimento_espuma_2}, {valor_estofaria_espuma_2}, {valor_estofaria_cliente_2}, {qtd_espuma_3}, {altura_espuma_3}, {largura_espuma_3}, {comprimento_espuma_3}, {valor_estofaria_espuma_3}, {valor_estofaria_cliente_3}, {qtd_espuma_4}, {altura_espuma_4}, {largura_espuma_4}, {comprimento_espuma_4}, {valor_estofaria_espuma_4}, {valor_estofaria_cliente_4}, {valor_total_estofaria_espuma}, {valor_total_cliente_espuma}, {status_impermeabilizacao}, {valor_impermeabilizacao}, '{frete_bairro}', {valor_frete}, {valor_socializado}, '{item_adicional_1}', {qtd_adicional_1}, {valor_adicional_1}, '{item_adicional_2}', {qtd_adicional_2}, {valor_adicional_2}, '{item_adicional_3}', {qtd_adicional_3}, {valor_adicional_3}, {valor_total_item_adicional}, {custo_fixo}, {custo_variavel_estofaria}, {custo_variavel_cliente}, {total_estofaria}, {total_cliente}, {percentual_calculado}, {percentual_margem_alvo}, {preco_alvo})
        """
        try:
            trans = con.begin()
            con.execute(sql)
            trans.commit()
        except:
            trans.rollback()
        return print('Atualização realizada.')

# con = conexão()
# conexão = con.servidor()
# custo = custo_variavel_geral()
# custo.consultar_custo_variavel_geral(conexão)