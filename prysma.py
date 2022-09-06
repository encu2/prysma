import httpx as hx
from ultility import headerS, hostS #colab google, check code below this row
from bs4 import BeautifulSoup as bs
import asyncio as io
import re
import timeit

temp = {}
proto = 'socks5'
defTimeout = 5

async def Arange(start, stop=None, step=1, temp = None):
	if stop:
			range_ = range(start, stop, step)
	elif temp:
			range_ = range(len(list(start))-1)
	else:
			range_ = range(start)
	for i in range_:
			yield i
			await io.sleep(0)

class timer:
		# @lru_cache(maxsize=None)
		def __init__(self, name=None):
				self.name = " '"	+ name + "'" if name else ''

		# @lru_cache(maxsize=None)
		def __enter__(self):
				self.start = timeit.default_timer()
		
		# @lru_cache(maxsize=None)
		def __exit__(self, exc_type, exc_value, traceback):
				self.took = (timeit.default_timer() - self.start) * 1000.0
				if int(self.took * 1000000.0) < 1000:
						print('Code block' + self.name + ' took: ' + str(self.took * 1000000.0) + ' ns')
						print('congrats')
				elif int(self.took * 1000.0) < 1000:
						print('Code block' + self.name + ' took: ' + str(self.took * 1000.0) + ' μs')
				elif int(self.took / 1000.0) > 1000:
						print('Code block' + self.name + ' took: ' + str(self.took / 1000.0) + ' s')
				else:
						print('Code block' + self.name + ' took: ' + str(self.took) + ' ms')

async def spidy0(prov=True):
		async with hx.AsyncClient(headers = headerS()) as client:
				a = await client.get('https://proxylist.nl.ax/')
				b = bs(a.content, "html.parser")
				c = b.find_all("form")[0]
				d = c.find_all(name=["input", "select"])
				b = {}
				# await io.sleep(1)

		async for i in Arange(len(d)).__aiter__():
				m = re.findall("(?<=name\=\")[\w]+(?=\")",str(d[i]))[0]
				n = re.findall("(?<=value\=\")[\w]+(?=\")",str(d[i]))[0]
				if m != "proxytype":
						b.update([(m, n)])
				elif m == "proxytype" and proto == "http":
						b.update([(m, 'http')])
				elif m == "proxytype" and proto == "https":
						b.update([(m, 'https')])
				elif m == "proxytype" and proto == "socks5":
						b.update([(m, 'socks5')])

		# await io.sleep(1)

		async with hx.AsyncClient(headers = headerS()) as client:
				a = await client.post("https://proxylist.nl.ax/", data = b, headers = headerS())
				b = bs(a.content, "html5lib")

		# await io.sleep(1)
		temp.update(
				[
						(
								'temp0', 
								re.findall("\w+\.\w+\.\w+\.\w+\:\w+", str(b.find("textarea")))
						)
				]
		)

		print(f"Spidy 0 done => {len(temp['temp0'])}")
		return 1

async def spidy1(prov=True):
		#html beautifier for bypass eval js
		import jsbeautifier

		opts = jsbeautifier.default_options()
		opts.indent_size = 4
		opts.space_in_empty_paren = True
		j = 0
		url = "http://nntime.com/proxy-list-01.htm"
		temp.update([('temp1', [])])

		async with hx.AsyncClient(headers = headerS()) as client:
				a = await client.get(url)
				b = bs(a.content, "html5lib")
				c = b.select("#navigation > a")
				# await io.sleep(1)
		# print(c)
		*x, _=c
		# print(x)
		del _
		nav = []
		for i in x:
				nav.append(i["href"])

		try:
				while True:
						getJs = re.findall("\w+\/\w+\.js", str(b))[0]
						async with hx.AsyncClient(headers = headerS()) as client:
								getStr = await client.get("http://nntime.com/" + getJs)
								res = jsbeautifier.beautify(getStr.text, opts)
								IdRandNum = re.findall("(?<=proxies\.replace\(\/)\w+", res)
								c = b.find_all("form")[0]
								d = c.find_all(attrs = {"id" : re.compile("row")} )

								async for i in Arange(len(d)).__aiter__(): 
										temp['temp1'].append(re.sub(IdRandNum[1], ':', re.sub(IdRandNum[0], '', d[i]["value"])))
										# await io.sleep(0)

								a = await client.get("http://nntime.com/" + nav[j])
								b = bs(a.text, "html5lib")

						j += 1
				
		except:
				print(f"spidy 1 done => {len(temp['temp1'])}")
				return 1


async def spidy2(prov=True):
	if proto == "http" or proto == "https":
		url="https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous&simplified=true"
	elif proto == "socks5":
		url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all"

	async with hx.AsyncClient(headers = headerS()) as client:
		*a, _= hx.get(url).text.split("\r\n")
		# await io.sleep(1)

	temp.update([('temp2', a)])

	print(f"spidy 2 done => {len(temp['temp2'])}")
	return 1


async def openPort(*host):
	ip, port = host[0].split(':')
	looper = io.get_event_loop()
	io.set_event_loop(looper)
	try:
		here, ini = await looper.create_connection(io.BaseProtocol, host=ip, port=port)
		here.close()
		# temp['portOpen'].append(host)
		# await io.sleep(0.000001)
	except:
		return 0

	return host[0]

async def reqTest(host):
	if not host == 0:
		# proxy = f'socks5://{host}'
			timeout = hx.Timeout(defTimeout)
			limits = hx.Limits(max_keepalive_connections=5, max_connections=5)
			async with hx.AsyncClient(http2 = True, proxies = f'socks5://{host}', timeout = timeout, limits = limits) as client:
				try:
					Get = await client.get(hostS())
					# await io.sleep(0.2)
					if Get.status_code == 200:
						print(host)
						temp['results'].append(host)
						await client.aclose()
				except:
					pass

async def main():
		funcS = [spidy0, spidy1, spidy2]
		run = await io.gather(*[await io.to_thread(funcS[i]) async for i in Arange(len(funcS)).__aiter__()])

		if all(run):
			# temp.update([('portOpen', [])])
			# portCheck = await io.gather(*[io.to_thread(openPort) for _ in range(len(list(temp.keys())))])
			toOpenPort = []
			for i in temp.values():
				toOpenPort += [*i]
				# print(i)
			openPortS = await io.gather(*[await io.to_thread(openPort,toOpenPort[i]) async for i in Arange(len(toOpenPort)).__aiter__()])
			del toOpenPort
			for _ in range(len(temp.keys())):
				temp.popitem()
			temp.update([('results', [])])
			# async for i in Arange(len(openPortS)).__aiter__():
			try:
				requestTest = await io.wait_for(io.gather(*[await io.to_thread(reqTest, openPortS[i]) async for i in Arange(len(openPortS)).__aiter__()]), timeout = 60.0) 
			except:
				print(temp['results'])
			# runOpenPort = await io.gather(openPort())
			# print(portCheck, temp['portOpen'])
			# print(temp['portOpen'])
			# break
			# print(openPortS)

# for i in temp.keys():
# 		for j in temp[i]:
# 				openPort(j)

with timer('spidy prisma'):
	# loop = io.get_event_loop()
	# loop.run_until_complete(main())
	# loop.close()
	io.run(main())
# print(temp)