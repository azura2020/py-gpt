#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.01.15 04:00:00                  #
# ================================================== #

import os

from pygpt_net.item.model import ModelItem
from pygpt_net.utils import parse_args


class BaseLLM:
    def __init__(self, *args, **kwargs):
        self.id = ""
        self.name = ""
        self.type = []  # langchain, llama_index
        self.description = ""

    def init(self, window, model: ModelItem, mode: str, sub_mode: str = None):
        """
        Initialize provider

        :param window: window instance
        :param model: model instance
        :param mode: mode (langchain, llama_index)
        :param sub_mode: sub mode (chat, completion)
        """
        options = {}
        if mode == 'langchain':
            options = model.langchain
        elif mode == 'llama_index':
            options = model.llama_index
        if 'env' in options:
            for item in options['env']:
                os.environ[item['name']] = str(item['value'].format(**window.core.config.all()))

    def parse_args(self, options: dict) -> dict:
        """
        Parse extra args

        :param options: LLM options dict (langchain, llama_index)
        :return: dict
        """
        args = {}
        if 'args' in options:
            args = parse_args(options['args'])
        return args

    def completion(self, window, model: ModelItem, stream: bool = False) -> any:
        """
        Return LLM provider instance for completion in langchain mode

        :param window: window instance
        :param model: model instance
        :param stream: stream mode
        :return: provider instance
        """
        pass

    def chat(self, window, model: ModelItem, stream: bool = False) -> any:
        """
        Return LLM provider instance for chat in langchain mode

        :param window: window instance
        :param model: model instance
        :param stream: stream mode
        :return: provider instance
        """
        pass

    def llama(self, window, model: ModelItem, stream: bool = False):
        """
        Return LLM provider instance for llama index query and chat

        :param window: window instance
        :param model: model instance
        :param stream: stream mode
        :return: provider instance
        """
        pass
