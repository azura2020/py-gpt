#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.31 04:00:00                  #
# ================================================== #

import json
import os
import shutil


class Settings:
    def __init__(self, window=None):
        """
        Settings core

        :param window: Window instance
        """
        self.window = window

        # prepare cfg ids
        self.ids = ['settings', 'editor']
        self.active = {}
        self.options = {}
        self.sections = {}
        self.initialized = False

        # prepare active
        for id in self.ids:
            self.active[id] = False

    def get_options(self, id: str = None) -> dict:
        """
        Return options for given id

        :param id: settings id
        :return: dictionary of options
        """
        if not self.initialized:
            self.load()
        if id is None:
            return self.options
        if id in self.options:
            return self.options[id]

    def get_sections(self, id: str = None) -> dict:
        """
        Return sections for given id

        :param id: settings id
        :return: dictionary of options
        """
        if not self.initialized:
            self.load()
        if id is None:
            return self.sections
        if id in self.sections:
            return self.sections[id]

    def get_persist_options(self) -> list:
        """
        Return persist options keys (options that should be persisted when loading defaults)

        :return: list of keys
        """
        if not self.initialized:
            self.load()
        persist_options = []
        for option in self.options:
            if 'persist' in self.options[option] and self.options[option]['persist']:
                persist_options.append(option)
        return persist_options

    def load(self):
        """
        Load settings options
        """
        self.options = self.window.core.config.get_options()
        self.sections = self.window.core.config.get_sections()
        self.initialized = True

    def load_user_settings(self):
        """Load user config (from user home dir)"""
        # replace config with user base config
        self.window.core.config.load_config()

    def load_app_settings(self):
        """Load base app config (from app root dir)"""
        # persist important values
        persist_options = self.get_persist_options()
        persist_values = {}
        for option in persist_options:
            if self.window.core.config.has(option):
                persist_values[option] = self.window.core.config.get(option)

        # save current config backup
        self.window.core.config.save('config.backup.json')

        # replace config with app base config
        self.window.core.config.from_base_config()

        # restore persisted values
        for option in persist_options:
            if option in persist_values:
                self.window.core.config.set(option, persist_values[option])

    def load_default_editor(self):
        """Load defaults from file"""
        file = self.window.ui.dialog['config.editor'].file
        self.load_editor(file)
        self.window.ui.status("Loaded defaults from file: {}".format(file))

    def load_editor(self, file: str = None):
        """
        Load file to editor

        :param file: file name
        """
        # load file
        path = None
        if file.endswith('.json'):
            path = os.path.join(self.window.core.config.path, file)
        elif file.endswith('.css'):
            path = os.path.join(self.window.core.config.path, 'css', file)

        self.window.ui.paths['config'].setText(path)
        self.window.ui.dialog['config.editor'].file = file
        try:
            with open(path, 'r', encoding="utf-8") as f:
                txt = f.read()
                self.window.ui.editor['config'].setPlainText(txt)
        except Exception as e:
            self.window.core.debug.log(e)
            self.window.ui.status("Error loading file: {}".format(e))

    def save_editor(self):
        """Save file to disk"""
        file = self.window.ui.dialog['config.editor'].file

        path = None
        data = self.window.ui.editor['config'].toPlainText()
        # check if this is a valid JSON:
        if file.endswith('.json'):
            try:
                json.loads(data)
            except Exception as e:
                self.window.ui.status("This is not a valid JSON: {}".format(e))
                self.window.ui.dialogs.alert("This is not a valid JSON: {}".format(e))
                return
            path = os.path.join(self.window.core.config.path, file)
        elif file.endswith('.css'):
            path = os.path.join(self.window.core.config.path, 'css', file)

        # make backup of current file:
        backup_file = file + '.backup'
        backup_path = os.path.join(self.window.core.config.path, backup_file)
        if os.path.isfile(path):
            shutil.copyfile(path, backup_path)
            self.window.ui.status("Created backup file: {}".format(backup_file))

        # save changes to current file:
        try:
            with open(path, 'w', encoding="utf-8") as f:
                f.write(data)
            self.window.ui.status("Saved file: {}".format(path))
            self.window.ui.dialogs.alert("Saved file: {}".format(path))

            if file == "config.json":
                self.window.core.config.load_config()  # reload config
            elif file == "models.json":
                self.window.core.models.load()  # reload models
            elif file.endswith('.css'):
                self.window.controller.theme.reload(force=True)  # reload theme
        except Exception as e:
            self.window.core.debug.log(e)
            self.window.ui.status("Error saving file: {}".format(path))
