# -*- coding: utf-8 -*-
import os
import logging
import base64
import smtplib  # 简单邮件传输协议库
from poplib import POP3  # 邮局协议，接收邮件
from email.mime.text import MIMEText  # 构建文本邮件
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.parser import Parser  # 对邮件文本内容进行解析
from email.header import decode_header  # 解析邮件主题
from email.utils import parseaddr  # 解析邮件来源
from typing import (
    List, Tuple
)


# 只支持接收文本内容
# 默认登录的是网易邮箱服务器
class RecvMail:
    def __init__(self, username: str, passwd: str, email_host: str = ' pop.163.com') -> None:
        self.server = POP3(email_host)
        self.server.user(username)
        self.server.pass_(passwd)
        resp, self.mails, octets = self.server.list()  # 字节类型
        self.len_string = len(self.mails)  # 从邮件列表中获取最新一封邮件
        if self.len_string > 0:
            resp, self.mail_content, octets = self.server.retr(self.len_string)
            # 'gbk'汉字内码扩展规范
            self.message = Parser().parsestr(text=b'\r\n'.join(self.mail_content).decode('gbk'))
        else:
            self.message = ''

    # 解析邮件主题
    def parser_title(self, msg: MIMEMultipart) -> str:
        value = ''
        if self.len_string > 0:
            subject = msg['Subject']
            value, charset = decode_header(subject)[0]
            if charset:
                return value.decode(charset)
        return value

    # 解析邮件地址
    def parser_address(self, msg: MIMEMultipart) -> Tuple:
        mail_name, mail_addr = '', ''
        if self.len_string > 0:
            hdr, mail_addr = parseaddr(msg['From'])
            mail_name, charset = decode_header(hdr)[0]  # decode_header()会返回编码格式
            if charset:
                mail_name = mail_name.decode(charset)
            return mail_name, mail_addr
        return mail_name, mail_addr

    # 解析邮件内容
    def parser_content(self, msg: MIMEMultipart) -> str:
        text_content = ''
        if self.len_string > 0:
            content = msg.get_payload()
            content_charset = content[0].get_content_charset()  # 获得内容编码格式
            text = content[0].as_string().split('base64')[-1]
            try:
                text_content = base64.b64decode(text).decode(content_charset)
            except Exception as err:
                logging.error(err)
            return text_content
        return text_content

    def delet_all_mails(self) -> None:
        for index in range(1, len(self.mails) + 1):
            self.server.dele(index)

    # 关闭服务器
    def server_quit(self) -> None:
        self.server.quit()


# 只支持文本和文件发送
class LoginMail:
    def __init__(self, username: str, passwd: str, ssl: bool = True, port: int = 25,
                 ssl_port: int = 465, email_host: str = 'smtp.163.com') -> None:

        # :param title: 邮件标题
        # :param content: 邮件正文
        # :param file: 附件路径
        # :param ssl: 是否安全链接，默认为普通
        # :param email_host: smtp服务器地址，默认为163服务器
        # :param port: 非安全链接端口，默认为25
        # :param ssl_port: 安全链接端口，默认为465

        self.username = username  # 用户名
        self.passwd = passwd  # 授權碼
        self.email_host = email_host  # smtp服务器地址
        self.port = port  # 普通端口
        self.ssl = ssl  # 是否安全链接
        self.ssl_port = ssl_port  # 安全链接端口
        self.smtp = smtplib.SMTP_SSL()

    def send_mail(self, recv: List[str], title: str, content: str, file: str = '') -> bool:
        msg = MIMEMultipart()
        if file != '':  # 处理附件
            file_name = os.path.split(file)[-1]
            try:
                f = open(file, 'rb').read()
            except Exception as err:
                logging.error(err)
                return False
            else:
                att = MIMEApplication(f)
                att["Content-Type"] = 'application/octet-stream'  # 八进制流
                #  base64.b64encode(file_name.encode()).decode()
                new_file_name = '=?utf-8?b?' + base64.b64encode(file_name.encode()).decode() + '?='
                # 这一行缺省会被当做纯文本，出现显示异常。
                att["Content-Disposition"] = f'attachment; filename={new_file_name}'
                msg.attach(att)
        msg.attach(MIMEText(content))
        msg['Subject'] = title
        msg['From'] = self.username
        msg['To'] = ','.join(recv)
        if self.ssl:
            self.smtp = smtplib.SMTP_SSL(self.email_host, port=self.ssl_port)
        else:
            self.smtp = smtplib.SMTP(self.email_host, port=self.port)
        try:
            #  发送邮件服务器的对象
            self.smtp.login(self.username, self.passwd)
            self.smtp.sendmail(self.username, recv, msg.as_string())
        except Exception as err:
            logging.error(err)
            return False
        else:
            return True

    # 关闭服务器
    def server_quit(self) -> None:
        self.smtp.quit()
