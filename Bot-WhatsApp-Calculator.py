# -- coding:utf-8 --

import re
from time import sleep
from selenium import webdriver

#Perguntar o Path do sistema da pessoa
#Path/Caminho do perfil do chrome pegar em chrome://version/
#Caminho ex: C:\\Users\\Jonathan\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1
path = input('\nInsira o Path do seu perfil do Chrome: ')

#Entrar no Whats e aguardar 10 segundos para carregar o QR Code e a pessoa escanear
#Salvar a sessão do Whats para nao precisar escanear todas as vezes que entrar
options = webdriver.ChromeOptions() 


#Inserir o caminho do seu perfil no google chrome para o Bot sempre entrar no seu WhatsApp por padrão
options.add_argument("user-data-dir={}".format(path)) 


options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
driver.get("http://web.whatsapp.com")
sleep(10)

#Listar TODAS  as conversas
def conversas():
	#Retornar valor do tipo lista contendo todas as conversas 
	conversas = driver.find_elements_by_class_name('_3j7s9') 
	return conversas

#Reconhecer a última mensagem enviada pela pessoa (para chamar a função, já tem que estar dentro do chat para nao dar erro)
def ultima_msg():
	#Listar todas as mensagens da pessoa (retornar valor do tipo lista)
	all_msg = driver.find_elements_by_css_selector('div.message-in')
	#Selecionar a última mensagem que ela enviou
	ultima_mensagem = all_msg[-1] 
	#Pegar o texto da ultima mensagem da pessoa
	txt_ultima = ultima_mensagem.find_element_by_css_selector('span.selectable-text').text
	#retornar SOMENTE O TEXTO da ultima mensagem à função
	return txt_ultima

#Responder as pessoas de forma predefinida
def responder(texto):
	
	#achar o campo da caixa de mensagens, escrever a mensagem e clicar no botão enviar
	caixa_mensagem = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
	caixa_mensagem.send_keys('{}'.format(texto))
	sleep(2)
	botao_enviar = driver.find_element_by_class_name('_35EW6')
	botao_enviar.click()
	sleep(1)

#Verificar se a ultima mensagem começa com a palavra "Operação"
def ver_op(texto):
	op = ['operacao', 'operação']
	x = re.search("^{}".format(op), texto.lower())
	if x:
		return True

#Verificar se a ultima mensagem começa com a palavra "Tabuada"
def ver_tab(texto):
	op = ['tabuada']
	x = re.search("^{}".format(op), texto.lower())
	if x:
		return True

#Identificar a operação matemática requerida pela pessoa
def sel_operacao(texto):
	indice = -1
	while texto[indice].isdigit() == True:
		operacao = ""
		indice -= 1
		while texto[indice] == " ":
			indice -= 1
	else:
		operacao =  texto[indice]
	return operacao

#Identificar o primeiro número em que a operação irá ser efetuada
def num1(texto):
	numero = []
	separator = ""
	num = 0
	for n in texto:
		#verificar se o dígito é um número, e caso for, adicionar na lista
		if n.isdigit():
			numero.append(n)
		#verificar se a lista está com algum dado e se o número acabou
		if len(numero) > 0 and n.isdigit() != True:
			num = separator.join(numero)
	
	return int(num)

#Identificar o segundo número em que a operação irá ser efetuada
def num2(texto):
	indice = -1
	numero = []
	separator = ""
	num = 0
	while texto[indice].isdigit() == True or texto[indice] == '0':
		num = texto[indice]
		numero.insert(0, num)
		indice -= 1
	num = separator.join(numero)
	return int(num)

#Realizar a soma dos números
def soma(n1, n2):
	soma = n1 + n2
	responder('Você escolheu: *SOMA*.')
	responder('Resultado: {} + {} = *{}*'.format(n1, n2, soma))
	driver.refresh()

#Realizar a subtração dos números
def subtrair(n1, n2):
	subtrair = n1 - n2
	responder('Você escolheu: *SUBTRAÇÃO*.')
	responder('Resultado: {} - {} = *{}*'.format(n1, n2, subtrair))
	driver.refresh()

#Realizar a multiplicação dos números
def multiplicar(n1, n2):
	multiplicar = n1 * n2
	responder('Você escolheu: *MULTIPLICAÇÃO*.')
	responder('Resultado: {} * {} = *{}*'.format(n1, n2, multiplicar))
	driver.refresh()

#Realizar a divisão dos números
def dividir(n1, n2):
	dividir = n1 / n2
	responder('Você escolheu: *DIVISÃO*')
	responder('Resultado: {} / {} = *{}*'.format(n1, n2, dividir))
	driver.refresh()

def tabuada(n1):
	responder('Enviando tabuada do *{}*'.format(n1))
	for x in range(1, 11):
		m = x * n1
		r = '{} x {} = {}'.format(n1, x, m)
		responder(r)
	driver.refresh()

while True:
	# selecionar cada uma das conversas/chat
	for conversa in conversas():
		try:
			#Verificar se na conversa tem notificação
			ntf = conversa.find_element_by_css_selector('span.OUeyt')
			#Abrir a conversa/chat que estiver com notificação
			if ntf != "" or ntf != " ":
				conversa.click()
				#aguardar 5 segundos para carregar as mensagens
				sleep(5)

				#armazenar a ultima mensagem enviada pela pessoa
				ultima = ultima_msg()

				if ver_op(ultima):
					#Definir a operação a ser feita e os valores
					operacao = sel_operacao(ultima)
					n1 = num1(ultima)
					n2 = num2(ultima)
					
					if operacao == '+':
						soma(n1, n2)
							

					elif operacao == '-':
						subtrair(n1, n2)
						

					elif operacao == '*':
						multiplicar(n1, n2)
						

					elif operacao == '/':
						dividir(n1, n2)
				
				elif ver_tab(ultima):
					n2 = num2(ultima)
					tabuada(n2)

		#Caso nao tenha notificação no Chat, passar para o próximo
		except Exception as e:
			pass					


		