# -*- coding: utf-8 -*-

"""	Injector SSL com SNI Host em Python
	Não suporta proxy.
	Criado por Marcone.
	Não sei se funciona...
"""

import socket, threading, select

SNI_HOST = 'www.example.com'
LISTEN_PORT = 8088


def conecta(c, a):
	print('<#> Cliente {} recebido!'.format(a[-1]))
	request = c.recv(8192)

	host = request.split(':')[0].split()[-1]
	port = request.split(':')[-1].split()[0]


	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((str(host), int(port)))

	# Wrap o SSL.
	import ssl
	ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
	s = ctx.wrap_socket(s, server_hostname=str(SNI_HOST))

	# Direta
	c.send(b"HTTP/1.1 200 Established\r\n\r\n")



	connected = True
	while connected == True:
		r, w, x = select.select([c,s], [], [c,s], 3)
		if x: connected = False; break
		for i in r:
			try:
				# Break if not data.
				data = i.recv(8192)
				if not data: connected = False; break
				if i is s:
					# Download.
					c.send(data)
				else:
					# Upload.
					s.send(data)
			except:
				connected = False
				break
	c.close()
	s.close()
	print('<#> Cliente {} Desconectado!'.format(a[-1]))
	

# Listen
print('Injector SSL com SNI Host em Python\n\
Versao de Teste.\n\
Criado por Marcone.\n')
l = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
l.bind(('', int(LISTEN_PORT)))
l.listen(0)
print('Esperando Cliente no Ip e Porta: 127.0.0.1:{}\n'.format(LISTEN_PORT))
while True:
	c, a = l.accept()
	threading.Thread(target=conecta, args=(c, a)).start()
l.close()