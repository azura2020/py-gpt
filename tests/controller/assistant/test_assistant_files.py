#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.01.03 06:00:00                  #
# ================================================== #

import os
from unittest.mock import MagicMock

from pygpt_net.item.assistant import AssistantItem
from pygpt_net.item.attachment import AttachmentItem
from pygpt_net.item.ctx import CtxItem
from tests.mocks import mock_window
from pygpt_net.controller.assistant.files import Files


def test_update(mock_window):
    """Test update files list"""
    files = Files(mock_window)
    files.update_list = MagicMock()
    files.update()
    files.update_list.assert_called_once()


def test_select(mock_window):
    """Test select file"""
    files = Files(mock_window)
    item = AssistantItem()
    mock_window.core.config.data = {"assistant": "assistant_id"}
    mock_window.core.assistants.get_by_id = MagicMock(return_value=item)
    mock_window.core.assistants.get_file_id_by_idx = MagicMock(return_value="file_id")

    mock_window.core.assistants.get_file_id_by_idx = MagicMock(return_value="file_id")
    files.select(0)
    mock_window.core.assistants.get_by_id.assert_called_once()
    mock_window.core.assistants.get_file_id_by_idx.assert_called_once()
    assert mock_window.core.assistants.current_file == "file_id"


def test_count_upload(mock_window):
    """Test upload file"""
    files = Files(mock_window)
    item = AttachmentItem()
    item.send = False
    item2 = AttachmentItem()
    item2.send = True
    attachments = {"id": item, "id2": item2}

    result = files.count_upload(attachments)
    assert result == 1


def test_import_files(mock_window):
    """Test import files"""
    files = Files(mock_window)
    item = AssistantItem()
    item.id = "assistant_id"
    mock_window.core.gpt.assistants.file_list = MagicMock(return_value=["file1", "file2"])
    mock_window.core.assistants.import_files = MagicMock()
    mock_window.core.assistants.save = MagicMock()

    files.import_files(item)
    mock_window.core.gpt.assistants.file_list.assert_called_once_with("assistant_id")
    mock_window.core.assistants.import_files.assert_called_once()
    mock_window.core.assistants.save.assert_called_once()


def test_download(mock_window):
    """Test download file"""
    files = Files(mock_window)
    item = AssistantItem()
    item.id = "assistant_id"
    mock_window.core.config.data['assistant'] = "assistant_id"

    mock_window.core.assistants.get_by_id = MagicMock(return_value=item)
    mock_window.core.assistants.get_file_id_by_idx = MagicMock(return_value="file_id")
    mock_window.controller.attachment.download = MagicMock()

    files.download(0)
    mock_window.core.assistants.get_by_id.assert_called_once()
    mock_window.core.assistants.get_file_id_by_idx.assert_called_once()
    mock_window.controller.attachment.download.assert_called_once_with("file_id")


def test_sync(mock_window):
    """Test sync files"""
    files = Files(mock_window)
    item = AssistantItem()
    item.id = "assistant_id"
    mock_window.core.config.data['assistant'] = "assistant_id"
    mock_window.core.assistants.get_by_id = MagicMock(return_value=item)

    files.import_files = MagicMock()
    files.sync(force=True)
    files.import_files.assert_called_once()


def test_rename(mock_window):
    """Test rename file"""
    files = Files(mock_window)
    item = AssistantItem()
    item.id = "assistant_id"
    mock_window.core.config.data['assistant'] = "assistant_id"
    mock_window.core.assistants.get_by_id = MagicMock(return_value=item)
    mock_window.core.assistants.get_file_id_by_idx = MagicMock(return_value="file_id")
    mock_window.core.assistants.get_file_by_id = MagicMock(return_value={"name": "file_name"})

    mock_window.ui.dialog['rename'].id = None
    mock_window.ui.dialog['rename'].input.setText = MagicMock()
    mock_window.ui.dialog['rename'].show = MagicMock()
    mock_window.ui.dialog['rename'].accept = MagicMock()
    files.update = MagicMock()
    files.rename(0)

    mock_window.core.assistants.get_by_id.assert_called_once()
    mock_window.core.assistants.get_file_id_by_idx.assert_called_once()
    mock_window.core.assistants.get_file_by_id.assert_called_once()
    mock_window.ui.dialog['rename'].input.setText.assert_called_once_with("file_name")
    assert mock_window.ui.dialog['rename'].id == "attachment_uploaded"
    files.update.assert_called_once()


def test_rename_close(mock_window):
    """Test close rename dialog"""
    files = Files(mock_window)
    files.update = MagicMock()
    files.rename_close()
    files.update.assert_called_once()


def test_update_name(mock_window):
    """Test update file name"""
    files = Files(mock_window)
    item = AssistantItem()
    item.id = "assistant_id"
    mock_window.core.config.data['assistant'] = "assistant_id"
    mock_window.core.assistants.get_by_id = MagicMock(return_value=item)
    mock_window.core.assistants.get_file_id_by_idx = MagicMock(return_value="file_id")
    mock_window.core.assistants.get_file_by_id = MagicMock(return_value={"name": "file_name"})
    mock_window.core.assistants.rename_file = MagicMock()

    mock_window.ui.dialog['rename'].id = "attachment_uploaded"
    mock_window.ui.dialog['rename'].input.text = "new_name"
    files.rename_close = MagicMock()
    files.update_name("file_id", "new_name")
    mock_window.core.assistants.rename_file.assert_called_once_with(item, "file_id", "new_name")
    files.rename_close.assert_called_once()


def test_clear_files(mock_window):
    """Test clear files"""
    files = Files(mock_window)
    item = AssistantItem()
    item.id = "assistant_id"
    item.files = {
        "file_id1": {},
    }
    mock_window.core.config.data['assistant'] = "assistant_id"
    mock_window.core.assistants.get_by_id = MagicMock(return_value=item)
    mock_window.core.assistants.get_file_id_by_idx = MagicMock(return_value="file_id")
    mock_window.core.assistants.get_file_by_id = MagicMock(return_value={"name": "file_name"})
    mock_window.core.assistants.has = MagicMock(return_value=True)
    mock_window.core.assistants.save = MagicMock()
    files.update = MagicMock()

    files.clear_files(force=True)
    mock_window.core.assistants.get_by_id.assert_called_once()
    mock_window.core.gpt.assistants.file_delete.assert_called_once_with("assistant_id", "file_id1")
    mock_window.core.assistants.save.assert_called_once()
    files.update.assert_called_once()


def test_delete(mock_window):
    """Test delete file"""
    files = Files(mock_window)
    item = AssistantItem()
    item.id = "assistant_id"
    item.files = {
        "file_id1": {},
    }
    mock_window.core.config.data['assistant'] = "assistant_id"
    mock_window.core.assistants.get_by_id = MagicMock(return_value=item)
    mock_window.core.assistants.get_file_id_by_idx = MagicMock(return_value="file_id1")
    mock_window.core.assistants.get_file_by_id = MagicMock(return_value={"name": "file_name"})
    mock_window.core.assistants.save = MagicMock()
    mock_window.core.assistants.has = MagicMock(return_value=True)
    files.update = MagicMock()

    files.delete(0, force=True)
    mock_window.core.assistants.get_by_id.assert_called_once()
    mock_window.core.gpt.assistants.file_delete.assert_called_once_with("assistant_id", "file_id1")
    mock_window.core.assistants.save.assert_called_once()
    files.update.assert_called_once()


def test_clear_attachments(mock_window):
    """Test clear attachments"""
    files = Files(mock_window)
    item = AssistantItem()
    item.id = "assistant_id"
    item.attachments = {
        "attachment_id1": {},
    }
    mock_window.core.assistants.save = MagicMock()
    files.update = MagicMock()
    files.clear_attachments(item)
    mock_window.core.assistants.save.assert_called_once()
    files.update.assert_called_once()


def test_upload(mock_window):
    """Test upload attachments"""
    files = Files(mock_window)
    item = AssistantItem()
    item.id = "assistant_id"

    os.path.exists = MagicMock(return_value=True)

    att = AttachmentItem()
    att.id = "attachment_id1"
    att.name = "attachment_id1"
    att.path = "attachment_id1"
    att.send = False

    attachments = {}
    attachments["attachment_id1"] = att

    mock_window.core.config.data['assistant'] = "assistant_id"
    mock_window.core.assistants.get_by_id = MagicMock(return_value=item)
    mock_window.core.gpt.assistants.file_upload = MagicMock(return_value="new_id")
    files.update_list = MagicMock()
    mock_window.core.assistants.save = MagicMock()
    mock_window.controller.attachment.update = MagicMock()

    num = files.upload("assistant", attachments)

    assert item.files["new_id"]["id"] == "new_id"
    assert item.files["new_id"]["name"] == "attachment_id1"
    assert item.files["new_id"]["path"] == "attachment_id1"
    assert att.send is True
    assert num == 1


def test_append(mock_window):
    """Test append attachment"""
    files = Files(mock_window)
    item = AssistantItem()
    item.id = "assistant_id"

    att = AttachmentItem()
    att.id = "attachment_id1"
    att.name = "attachment_id1"

    mock_window.core.assistants.save = MagicMock()
    files.append(item, att)
    assert item.attachments["attachment_id1"].id == "attachment_id1"


def test_update_list(mock_window):
    """Test update list"""
    files = Files(mock_window)
    item = AssistantItem()
    item.id = "assistant_id"
    item.files = {
        "file_id1": {},
    }
    mock_window.core.config.data['assistant'] = "assistant_id"
    mock_window.core.assistants.get_by_id = MagicMock(return_value=item)
    files.update_tab = MagicMock()

    files.update_list()
    mock_window.core.assistants.get_by_id.assert_called_once()
    mock_window.ui.chat.input.attachments_uploaded.update.assert_called_once_with(item.files)
    files.update_tab.assert_called_once()


def test_update_tab(mock_window):
    """Test update tab"""
    files = Files(mock_window)
    item = AssistantItem()
    item.id = "assistant_id"
    item.files = {
        "file_id1": {},
    }
    mock_window.core.config.data['assistant'] = "assistant_id"
    mock_window.core.assistants.get_by_id = MagicMock(return_value=item)
    mock_window.ui.tabs['input'].setTabText = MagicMock()
    files.update_tab()
    mock_window.core.assistants.get_by_id.assert_called_once()
    mock_window.ui.tabs['input'].setTabText.assert_called_once()


def test_handle_received(mock_window):
    """Test handle received"""
    files = Files(mock_window)
    item = AssistantItem()
    item.id = "assistant_id"
    item.files = {
        "file_id1": {},
    }
    msg = MagicMock()
    msg.file_ids = ["file_id1"]
    mock_window.controller.attachment.download = MagicMock(return_value="path")

    ctx = CtxItem()

    paths = files.handle_received(ctx, msg)  # will be appended to ctx in thread, not here
    mock_window.controller.attachment.download.assert_called_once()
    assert paths == ["path"]