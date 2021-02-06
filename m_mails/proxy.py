import socket

import socks

_temp = socket.socket


# 代理設置
# socks.set_default_proxy(socks.HTTP, '127.0.0.1', 8080, True, '杜紅濤', 'cly@1113')
def set_proxy(proxy: str, port: int) -> None:
    if not isinstance(proxy, str) or not isinstance(port, int):
        print('請傳入正確類型的參數!')
        return
    socks.set_default_proxy(socks.HTTP, proxy, port, True)
    socket.socket = socks.socksocket


def cancel_proxy() -> None:
    global _temp
    socket.socket = _temp
