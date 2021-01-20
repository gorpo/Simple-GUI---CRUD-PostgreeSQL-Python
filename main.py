#!/usr/bin/env python
# -*- coding: utf-8 -*-
#███╗   ███╗ █████╗ ███╗   ██╗██╗ ██████╗ ██████╗ ███╗   ███╗██╗ ██████╗
#████╗ ████║██╔══██╗████╗  ██║██║██╔════╝██╔═══██╗████╗ ████║██║██╔═══██╗
#██╔████╔██║███████║██╔██╗ ██║██║██║     ██║   ██║██╔████╔██║██║██║   ██║
#██║╚██╔╝██║██╔══██║██║╚██╗██║██║██║     ██║   ██║██║╚██╔╝██║██║██║   ██║
#██║ ╚═╝ ██║██║  ██║██║ ╚████║██║╚██████╗╚██████╔╝██║ ╚═╝ ██║██║╚██████╔╝
#╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝ ╚═════╝
#            @GorpoOrko | Manicomio TCXS Project | 2020
"""LEIA
----------------------------------------------------------------------------------
***CRIAR OS ARQUIVOS VINDOS DO QTDESIGN:

criar arquivo mainwindow.py:
    pyuic5 -x mainwindow.ui -o mainwindow.py

criar arquivo files_rc_rc.py
    pyrcc5 -o files_rc_rc.py files_rc.qrc
----------------------------------------------------------------------------------

***EXEMPLO DE LAYOUT LIMPO

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QFile
from mainwindow import Ui_MainWindow

class MainWindow(QMainWindow):
    # --------------FUNÇÃO DE INICIO
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

pip install PyQT5==5.12
----------------------------------------------------------------------------------
***ANOTAÇÕES:
sempre que quisermos chamar um stackedWidget usamos o comando abaixo e mudar sua "indexação"
    self.ui.stackedWidget.setCurrentIndex(1)

usando o sistema para chamar os arquivos do layout:
    self.ui.string_do_objeto
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

#importaçoes pessoais-------------->
from funcoes.mainwindow import Ui_MainWindow
from funcoes import conexao_database

class MainWindow(QMainWindow):

    #clicar e arrastar a janela
    def movimentoMouse(self):
        self.mwidget = QMainWindow(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # remove a barra
        self.center()
        # cria uma falsa label em todo objeto para poder ser movido
        self.lbl = QLabel(self)
        # self.lbl.setText("cria um texto para achar a label, pois ali em baixo sumi com ela da tela")
        self.lbl.setGeometry(-50, -50, 60, 40)
        self.oldPos = self.pos()
        self.show()
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        # print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    #limpa os campos do painel da database
    def limpaDatabase(self,event):
        self.ui.input_db.clear()
    def limpaHost(self,event):
        self.ui.input_host.clear()
    def limpaPorta(self,event):
        self.ui.input_porta.clear()
    def limpaUsuario(self,event):
        self.ui.input_usuario.clear()
    def limpaSenha(self,event):
        self.ui.input_senha.clear()
    def limpaTitulodb(self,event):
        self.ui.db_texto_titulo.clear()
    def limpaLinkdb(self,event):
        self.ui.db_texto_link.clear()
    def limpaCodigodb(self,event):
        self.ui.db_texto_codigo.clear()
    def limpaObservacaodb(self,event):
        self.ui.db_texto_observacao.clear()

    # Funções minimizar maximizar e fechar
    def fecharPrograma(self):
        sys.exit()
    def minimizarPrograma(self):
        window.showMinimized()
    def maximizarPrograma(self):
        self.ui.botao_maximizar.setStyleSheet("QPushButton {\n"
                                              "    \n"
                                              "    background-image: url('images/volta_full_screen.png');\n"
                                              "    background-color: transparent;\n"
                                              "    background-repeat: no-repeat;\n"
                                              "    background-position: center;\n"
                                              "    border: none;\n"
                                              "}\n"
                                              "QPushButton:hover {\n"
                                              "    background-color: rgb(30,144,255);\n"
                                              "}\n"
                                              "QPushButton:pressed {\n"
                                              "    background-color: rgb(1,84,149);\n"
                                              "}")
        self.window.showMaximized()
        self.ui.botao_maximizar.clicked.connect(self.janela_normal)
    def janela_normal(self):
        self.ui.botao_maximizar.setStyleSheet("QPushButton {\n"
                                              "    \n"
                                              "    background-image: url(:/maximizar/images/icons8-toggle-full-screen-24.png);\n"
                                              "    background-repeat: no-repeat;\n"
                                              "    background-position: center;\n"
                                              "    border: none;\n"
                                              "}\n"
                                              "QPushButton:hover {\n"
                                              "    background-color: rgb(30,144,255);\n"
                                              "}\n"
                                              "QPushButton:pressed {\n"
                                              "    background-color: rgb(1,84,149);\n"
                                              "}")
        window.showNormal()
        self.ui.botao_maximizar.clicked.connect(self.maximizarPrograma)


    #inicio do programa ------->
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.clic= pyqtSignal()

        #menus------------->
        self.movimentoMouse()
        self.ui.botao_fechar.clicked.connect(lambda: sys.exit())
        self.ui.botao_minimizar.clicked.connect(lambda: self.showMinimized())

        # sistema de redimensionamento da tela---------------->
        self.sizegrip = QSizeGrip(self.ui.redimensionador)
        self.sizegrip.setStyleSheet("width: 17px; height: 17px; margin 0px; padding: 0px;")
        self.sizegrip.setVisible(True)

        #funcoes------------>
        conexao_database.funcoesBancodados(self)




#start do programa
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
