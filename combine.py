# -*- coding: utf-8 -*-
import sys
import time
import logging
from typing import (
    Tuple, Callable
)

import json
import requests
# from PySide2.QtGui import QIcon
from PySide2.QtCore import QThread
from PySide2.QtWidgets import (
    QApplication, QWidget, QMessageBox, QInputDialog,
    QLineEdit
)


from configuration_ui import Ui_Form

import dataproce
from m_mails import LoginMail, set_proxy, cancel_proxy


def _get_info() -> Tuple:
    urls, recv = [], []
    with open(r'.\url.txt', 'r') as file:
        for r in file.readlines():
            urls.append(r[4:])
    with dataproce.Database() as db:
        res = db.sender_info_read()
        username = res[0][0]
        passwd = res[0][1]
        email_host = res[0][1]

        res = db.proxy_read()
        proxy = res[0][0]
        port = res[0][1]

        res = db.recv_info_read()
        for val in res:
            recv.append(val[0])
    return urls, username, passwd, email_host, proxy, port, recv


# 这里使用QT自带的线程库
class MThread(QThread):
    def __init__(self, func: Callable) -> None:
        self.func = func
        super(MThread, self).__init__()

    def run(self) -> None:
        self.func()


class MainForm(QWidget, Ui_Form):
    def __init__(self) -> None:
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('配置工具')

        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        # 發件人
        self.sender_modified.clicked.connect(self.sender_modified_on_click)
        self.sender_save.clicked.connect(self.sender_save_on_click)
        self.sender_modified_mark = False
        # 代理
        self.proxy_modified.clicked.connect(self.proxy_modified_on_click)
        self.proxy_save.clicked.connect(self.proxy_save_on_click)
        self.proxy_modified_mark = False
        # 收件人
        self.recv_modified.clicked.connect(self.recv_modified_on_click)
        self.recv_append.clicked.connect(self.recv_append_on_click)
        self.recv_delete.clicked.connect(self.recv_delete_on_click)
        self.recv_save.clicked.connect(self.recv_save_on_click)
        self.recv_modified_mark = False
        # 啟動停止按鈕
        self.run.clicked.connect(self.run_on_click)
        self.stop.clicked.connect(self.stop_on_click)
        self.__read_all_config()
        self.run_mark = False
        self.run_thread = None

    def __read_all_config(self) -> None:
        with dataproce.Database() as db:
            sender = db.sender_info_read()
            self.username.setText(sender[0][0])
            self.passwd.setText(sender[0][1])
            self.email_host.setText(sender[0][2])

            proxy = db.proxy_read()
            self.proxy.setText(proxy[0][0])
            self.port.setText(str(proxy[0][1]))

            recv = db.recv_info_read()
            for res in recv:
                self.recv_info.addItem(str(res[0]))

    # 發件人信息修改按鈕
    def sender_modified_on_click(self) -> None:
        self.username.setStyleSheet("border: 1px solid red;")
        self.passwd.setStyleSheet("border: 1px solid red;")
        self.email_host.setStyleSheet("border: 1px solid red;")
        self.sender_modified_mark = True

    # 發件人信息保存按鈕
    def sender_save_on_click(self) -> None:
        if self.sender_modified_mark:
            if self.username.text() != '' and self.passwd.text() != '' and self.email_host.text() != '':
                with dataproce.Database() as db:
                    db.sender_info_save(self.username.text(), self.passwd.text(), self.email_host.text())
                self.username.setStyleSheet("border: 1px solid black;")
                self.passwd.setStyleSheet("border: 1px solid black;")
                self.email_host.setStyleSheet("border: 1px solid black;")
                self.sender_modified_mark = False
            else:
                QMessageBox().warning(self, '警告', '請完整填寫發件人信息!')
        else:
            QMessageBox().warning(self, '警告', '請先點擊修改按鈕!')

    # 代理
    def proxy_modified_on_click(self) -> None:
        self.proxy.setStyleSheet("border: 1px solid red;")
        self.port.setStyleSheet("border: 1px solid red;")
        self.proxy_modified_mark = True

    def proxy_save_on_click(self) -> None:
        if self.proxy_modified_mark:
            if self.proxy.text() != '' and self.port.text() != '':
                with dataproce.Database() as db:
                    db.proxy_save(self.proxy.text(), int(self.port.text()))
                self.proxy.setStyleSheet("border: 1px solid black;")
                self.port.setStyleSheet("border: 1px solid black;")
                self.proxy_modified_mark = False
            else:
                QMessageBox().warning(self, '警告', '請完整填寫代理伺服器信息!')
        else:
            QMessageBox().warning(self, '警告', '請先點擊修改按鈕!')

    # 收信人
    def recv_append_on_click(self) -> None:
        if not self.recv_modified_mark:
            QMessageBox().warning(self, '警告', '請先點擊修改按鈕!')
            return
        receiver, ok_pressed = QInputDialog.getText(self, '信息新增', '請輸入:', QLineEdit.Normal, '')
        if ok_pressed and receiver != '':
            self.recv_info.addItem(receiver)
            with dataproce.Database() as db:
                db.recv_info_append(receiver)

    def recv_modified_on_click(self) -> None:
        self.recv_info.setStyleSheet("border: 1px solid red;")
        self.recv_modified_mark = True

    def recv_save_on_click(self):
        if not self.recv_modified_mark:
            QMessageBox().warning(self, '警告', '請先點擊修改按鈕!')
            return
        self.recv_info.setStyleSheet("border: 1px solid black;")
        self.recv_modified_mark = False
        # -----------------------------假裝寫入數據庫--------------------------------

    def recv_delete_on_click(self) -> None:
        if not self.recv_modified_mark:
            QMessageBox().warning(self, '警告', '請先點擊修改按鈕!')
            return
        current_row = self.recv_info.currentRow()
        current_content = self.recv_info.currentItem()
        if current_content:
            with dataproce.Database() as db:
                db.recv_info_delete(current_content.text())

        self.recv_info.takeItem(current_row)

    def __set_enabled(self, set_s: bool) -> None:
        self.username.setEnabled(set_s)
        self.passwd.setEnabled(set_s)
        self.email_host.setEnabled(set_s)
        self.proxy.setEnabled(set_s)
        self.port.setEnabled(set_s)
        self.sender_modified.setEnabled(set_s)
        self.sender_save.setEnabled(set_s)
        self.proxy_modified.setEnabled(set_s)
        self.proxy_save.setEnabled(set_s)
        self.recv_modified.setEnabled(set_s)
        self.recv_append.setEnabled(set_s)
        self.recv_delete.setEnabled(set_s)
        self.recv_save.setEnabled(set_s)
        self.run.setEnabled(set_s)

    # 啟動停止響應事件
    def run_on_click(self) -> None:
        self.__set_enabled(False)
        self.run_mark = True
        self.run_thread = MThread(self.send_info)
        self.run_thread.start()

    def stop_on_click(self) -> None:
        self.__set_enabled(True)
        self.run_mark = False

    def send_info(self) -> None:
        urls, username, passwd, email_host, proxy, port, recv = _get_info()
        state_change = {}
        while self.run_mark:
            for url in urls:
                try:
                    response = requests.get(url, timeout=5)
                    result = response.text
                    response.close()
                    result = json.loads(result)
                except Exception as err:
                    logging.error(f'{url} {err}')
                    continue
                try:
                    if state_change[result['line']] != result['state']:
                        if result['state'] != 'running':
                            send_content = 'EAC停止運行!'
                        else:
                            send_content = 'EAC重新啟動!'
                        set_proxy(proxy, port)  # 代理設置
                        time.sleep(1)
                        # EAC停機和重啟時都需要發送郵件 -------------------------------------------------------------
                        ob = LoginMail(username, passwd, email_host)
                        get_res = ob.send_mail(recv,
                                               title=f'{result["line"]}的訊息(自動發送)',
                                               content=f'''{result["line"]}: {send_content}
                                                        \n更新時間: {result["update_time"]}''')
                        if get_res:
                            logging.info('郵件發送成功')
                        else:
                            logging.error('郵件發送失敗')
                        ob.server_quit()
                        cancel_proxy()  # 取消代理
                except KeyError:
                    if result['state'] != 'running':
                        logging.info(f"{result['line']}監控開始, EAC不在運行中!")
                    else:
                        logging.info(f"{result['line']}監控開始, EAC運行中...")
                finally:
                    state_change[result['line']] = result['state']
            time.sleep(1)
        logging.info('退出...')


def main() -> None:
    app = QApplication(sys.argv)
    win = MainForm()
    win.setFixedSize(639, 372)
    win.show()
    sys.exit(app.exec_())
