#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.25 21:00:00                  #
# ================================================== #

import os


class ModelsDebug:
    def __init__(self, window=None):
        """
        Models debug

        :param window: Window instance
        """
        self.window = window
        self.id = 'models'

    def update(self):
        """Update debug window."""
        self.window.app.debug.begin(self.id)

        path = os.path.join(self.window.app.config.path, '', 'models.json')
        self.window.app.debug.add(self.id, 'Models File', str(path))

        # models
        for key in self.window.app.models.items:
            if key == '__meta__':
                self.window.app.debug.add(self.id, '__meta__', str(self.window.app.models.items[key]))
                continue
            prefix = "[{}] ".format(key)
            model = self.window.app.models.items[key]
            self.window.app.debug.add(self.id, '----', '')
            self.window.app.debug.add(self.id, str(key), '')
            self.window.app.debug.add(self.id, prefix + 'Key', str(key))
            self.window.app.debug.add(self.id, prefix + 'id', str(model.id))
            self.window.app.debug.add(self.id, prefix + 'name', str(model.name))
            self.window.app.debug.add(self.id, prefix + 'mode', str(model.mode))
            self.window.app.debug.add(self.id, prefix + 'tokens', str(model.tokens))

        self.window.app.debug.end(self.id)