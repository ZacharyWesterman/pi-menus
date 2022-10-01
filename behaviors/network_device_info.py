from behaviors import register

import asyncio

@register('network_device_info')
async def get_device_info(variables: object, display: object, **args) -> dict:
	selection = await variables.get('selection')
	ip = selection.get('ip', 'ERR: NO IP')
	name = selection.get('name')
	mac = selection.get('mac')

	msg = []

	if name != '?':
		msg += [f'ID  {name}']

	msg += [f'MAC {mac}']

	try:
		mac = mac.replace(':', '')
		with open(f'config/mac_vendors/{mac[0:2]}/{mac[0:6]}', 'r') as fp:
			msg += [fp.read()]
	except FileNotFoundError:
		pass

	return {
		'ip': ip,
		'name': name if name != '?' else '',
		'msg': '\n'.join(msg)
	}
