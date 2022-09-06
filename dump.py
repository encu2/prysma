import asyncio as io

host = [
'46.105.124.74:7497',
'178.33.146.138:7497',
'188.68.36.53:7497',
'176.31.222.116:7497',
'5.39.38.50:7497',
'5.189.179.173:7497',
'51.222.146.133:7497',
'85.214.216.250:7497',
'51.79.52.80:3080',
'37.221.192.104:7497',
'217.197.30.33:7497',
'104.248.142.28:7497',
'161.8.174.48:1080',
]

# async def main(host):
# 	ip, port = host.split(':')
# 	looper = io.get_event_loop()
# 	io.set_event_loop(looper)
# 	try:
# 		here , ini = await looper.create_connection(io.BaseProtocol, host=ip, port=port)
# 		here.close()
# 		print(here._protocol_connected)
# 	except:
# 		print(False)
# 	# print(dir(here))
	
# 	# reader, writer = await io.open_connection(host = 'hanahajiumroh.com', port = 443)
# 	# print(reader, writer)
# 	# looper.close()

# loop = io.get_event_loop()
# for _ in host:
# 	loop.run_until_complete(main(_))
# loop.close()

ini = {'a':'gegwgwg',222:4343}
print(len(ini.keys()))
def bbb():
	for _ in range(len(list(ini.keys()))):
		ini.popitem()
	print(ini)

print(ini)
bbb()
print(ini)