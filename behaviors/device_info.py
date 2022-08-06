from behaviors import register

import socket

@register('get_ip_address')
def get_ip_address(variables: object) -> str:
	return socket.gethostbyname(socket.gethostname())

@register('get_hostname')
def get_hostname(variables: object) -> str:
	return socket.gethostname()
