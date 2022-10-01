from behaviors import register

import asyncio

@register('network_device_info')
async def get_device_info(variables: object, display: object, **args) -> dict:
	selection = await variables.get('selection')
	ip = selection.get('ip', 'ERR: NO IP')
	name = selection.get('name')
	mac = selection.get('mac').replace(':', '')

	msg = []

	if name != '?':
		msg += [f'ID  {name}']

	try:
		with open(f'config/mac_vendors/{mac[0:2]}/{mac[0:6]}', 'r') as fp:
			msg += [fp.read()]
	except FileNotFoundError:
		msg += [f'MAC {mac}']

	return {
		'ip': ip,
		'name': name if name != '?' else '',
		'msg': '\n'.join(msg)
	}
