from behaviors import register

import socket

@register('get_ip_address')
async def get_ip_address(**args) -> str:
	return socket.gethostbyname(socket.gethostname())

@register('get_hostname')
async def get_hostname(**args) -> str:
	return socket.gethostname()
