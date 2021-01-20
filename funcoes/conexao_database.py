#!/usr/bin/env python
# -*- coding: utf-8 -*-
#███╗   ███╗ █████╗ ███╗   ██╗██╗ ██████╗ ██████╗ ███╗   ███╗██╗ ██████╗
#████╗ ████║██╔══██╗████╗  ██║██║██╔════╝██╔═══██╗████╗ ████║██║██╔═══██╗
#██╔████╔██║███████║██╔██╗ ██║██║██║     ██║   ██║██╔████╔██║██║██║   ██║
#██║╚██╔╝██║██╔══██║██║╚██╗██║██║██║     ██║   ██║██║╚██╔╝██║██║██║   ██║
#██║ ╚═╝ ██║██║  ██║██║ ╚████║██║╚██████╗╚██████╔╝██║ ╚═╝ ██║██║╚██████╔╝
#╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝ ╚═════╝
#            @GorpoOrko | Manicomio TCXS Project | 2020
from main import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView
from PyQt5 import QtSql
from PyQt5 import QtCore


def funcoesBancodados(self):
    #eventos para limpar os campos que buscam as entradas no usuario, quando clicado em uma entrada de texto ele se apagará.
    self.ui.input_db.mousePressEvent = self.limpaDatabase
    self.ui.input_host.mousePressEvent = self.limpaHost
    self.ui.input_porta.mousePressEvent = self.limpaPorta
    self.ui.input_usuario.mousePressEvent = self.limpaUsuario
    self.ui.input_senha.mousePressEvent = self.limpaSenha
    self.ui.db_texto_titulo.mousePressEvent = self.limpaTitulodb
    self.ui.db_texto_link.mousePressEvent = self.limpaLinkdb
    self.ui.db_texto_codigo.mousePressEvent = self.limpaCodigodb
    self.ui.db_texto_observacao.mousePressEvent = self.limpaObservacaodb
    #quando botao enviar for clicado ira chamar a função bancoDados(self): e fazer o login e carregar a tabela
    self.ui.btn_enviar.clicked.connect(lambda:bancoDados(self))


def bancoDados(self):
    #Conexao do pyqt5 com o plugin QPSQL do PostgreSQL
    self.db = QtSql.QSqlDatabase.addDatabase('QPSQL')
    self.db.setHostName(self.ui.input_host.text()) #seta o host de acordo com input do usuario - localhost
    self.db.setPort(int(self.ui.input_porta.text()))  # seta a porta de acordo com input do usuario - 5432
    self.db.setDatabaseName(self.ui.input_db.text()) #seta o nome do banco de dados de acordo com input do usuario - python
    self.db.setUserName(self.ui.input_usuario.text()) #seta o usuario de acordo com input do usuario - postgres
    self.db.setPassword(self.ui.input_senha.text()) #seta a senha  de acordo com input do usuario - ******
    self.ok = self.db.open() #abre o banco de dados
    print(self.ok)


    #Caso a database nao exista mostra o erro e fecha o programa
    if not self.db.open():
        print("Database Error: %s" % self.db.lastError().databaseText())
        sys.exit(1)

    # Cria a  query e executa o comando nela com o .exec()
    self.createTableQuery = QtSql.QSqlQuery()
    #Cria a tabela
    self.createTableQuery.exec(' CREATE TABLE "dados"("id" INT, "titulo" VARCHAR(255), "link" VARCHAR(255), "codigo" VARCHAR(255), "descricao" VARCHAR(255));')
    #conexao com a database
    self.model = QtSql.QSqlTableModel()
    # seleciona a tabela da database e seus itens
    self.model.setTable('dados')
    self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
    self.model.select()
    self.model.setHeaderData(0, QtCore.Qt.Horizontal, "Id")
    self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Titulo")
    self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Link")
    self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Codigo")
    self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Observações")
    #Preenche a tabela com os dados ja cadastrados
    self.ui.tabela_dados_db.setModel(self.model)
    self.i = self.model.rowCount()
    # botoes das açoes para adicionar, dar update e deletar
    self.ui.botao_db_adiciona.clicked.connect(lambda: addToDb(self))
    self.ui.botao_db_atualiza.clicked.connect(lambda: updaterow(self))
    self.ui.botao_db_deleta.clicked.connect(lambda:delrow(self))

def addToDb(self):
    #adiciona a database suas informaçoes
    print(self.i)
    self.model.insertRows(self.i,1)
    self.model.setData(self.model.index(self.i,1),self.ui.db_texto_titulo.text())
    self.model.setData(self.model.index(self.i, 2), self.ui.db_texto_link.text())
    self.model.setData(self.model.index(self.i,4), self.ui.db_texto_observacao.toPlainText())
    self.model.setData(self.model.index(self.i,3), self.ui.db_texto_codigo.toPlainText())
    self.model.submitAll()
    self.i += 1


def delrow(self):
    #deleta da database suas informaçoes
    if self.ui.tabela_dados_db.currentIndex().row() > -1:
        self.model.removeRow(self.ui.tabela_dados_db.currentIndex().row())
        self.i -= 1
        self.model.select()
    else:
        QMessageBox.question(self,'Mensagem', "Selecione uma linha para deletar", QMessageBox.Ok)
        self.show()

def updaterow(self):
    #Atualiza as informaçoes na database
    if self.ui.tabela_dados_db.currentIndex().row() > -1:
        record = self.model.record(self.ui.tabela_dados_db.currentIndex().row())
        record.setValue("Titulo",self.ui.db_texto_titulo.text())
        record.setValue("Link",self.ui.db_texto_link.text())
        record.setValue("Codigo", self.ui.db_texto_codigo.toPlainText())
        record.setValue("Observações", self.ui.db_texto_observacao.toPlainText())
        self.model.setRecord(self.ui.tabela_dados_db.currentIndex().row(), record)
    else:
        QMessageBox.question(self,'Mensagem', "Selecione uma linha para atualizar", QMessageBox.Ok)
        self.show()