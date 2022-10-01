from behaviors import register

import asyncio

@register('network_device_info')
async def get_device_info(variables: object, display: object, **args) -> dict:
	selection = await variables.get('selection')

	return {"ip": selection.get('ip', 'UNKNOWN')}
