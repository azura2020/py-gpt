#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.01.08 17:00:00                  #
# ================================================== #

class Input:
    def __init__(self, window=None):
        """
        Text input field handler

        :param window: Window instance
        """
        self.window = window

    def apply(self, parent_id: str, key: str, option: dict):
        """
        Apply value to input

        :param parent_id: Options parent ID
        :param key: Option key
        :param option: Option data
        """
        value = option["value"]
        if 'type' in option and option['type'] == 'int':
            value = round(int(value), 0)
        elif 'type' in option and option['type'] == 'float':
            value = float(value)

        if 'type' in option and option['type'] == 'int' or option['type'] == 'float':
            if value is not None:
                if 'min' in option and option['min'] is not None and value < option['min']:
                    value = option['min']
                elif 'max' in option and option['max'] is not None and value > option['max']:
                    value = option['max']

        self.window.ui.config[parent_id][key].setText('{}'.format(value))

    def on_update(self, parent_id: str, key: str, option: dict, value: any, hooks: bool = True):
        """
        On update event handler

        :param parent_id: Parent ID
        :param key: Option key
        :param option: Option data
        :param value: Option value
        :param hooks: Run hooks
        """
        option['value'] = value
        self.apply(parent_id, key, option)

        # on update hooks
        if hooks:
            hook_name = "update.{}.{}".format(parent_id, key)
            if self.window.ui.has_hook(hook_name):
                hook = self.window.ui.get_hook(hook_name)
                try:
                    hook(key, value, 'input')
                except Exception as e:
                    self.window.core.debug.log(e)

    def get_value(self, parent_id: str, key: str, option: dict) -> any:
        """
        Get value from input

        :param parent_id: Parent ID
        :param key: Option key
        :param option: Option data
        :return: Value
        """
        value = None
        if option['type'] == 'int':
            try:
                value = int(self.window.ui.config[parent_id][key].text())
            except ValueError:
                value = 0
        elif option['type'] == 'float':
            try:
                value = float(self.window.ui.config[parent_id][key].text())
            except ValueError:
                value = 0.0
        elif option['type'] == 'text':
            value = self.window.ui.config[parent_id][key].text()
        return value
