#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.01.29 14:00:00                  #
# ================================================== #

from PySide6.QtGui import QAction, QIcon

from pygpt_net.utils import trans
import pygpt_net.icons_rc


class File:
    def __init__(self, window=None):
        """
        Menu setup

        :param window: Window instance
        """
        self.window = window

    def setup(self):
        """Setup file menu"""
        self.window.ui.menu['app.exit'] = QAction(QIcon(":/icons/logout.svg"), trans("menu.file.exit"),
                                                  self.window, shortcut="Ctrl+Q", triggered=self.window.close)

        self.window.ui.menu['app.clear_history'] = QAction(QIcon(":/icons/delete.svg"),
                                                           trans("menu.file_clear_history"), self.window)
        self.window.ui.menu['app.ctx.new'] = QAction(QIcon(":/icons/add.svg"), trans("menu.file.new"), self.window)

        self.window.ui.menu['app.clear_history'].triggered.connect(
            lambda: self.window.controller.ctx.delete_history())

        self.window.ui.menu['app.ctx.new'].triggered.connect(
            lambda: self.window.controller.ctx.new())

        self.window.ui.menu['menu.app'] = self.window.menuBar().addMenu(trans("menu.file"))
        self.window.ui.menu['menu.app'].addAction(self.window.ui.menu['app.ctx.new'])
        self.window.ui.menu['menu.app'].addAction(self.window.ui.menu['app.clear_history'])
        self.window.ui.menu['menu.app'].addAction(self.window.ui.menu['app.exit'])
