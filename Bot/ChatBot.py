from textblob import TextBlob
import datetime, random

from urllib.request import Request, urlopen
import json, time


GREETING_KEYWORDS = ("olá", "oi")
GREETING_RESPONSES = ["oi, eu sou o BotCoin!", "olá!", "oi, estou a sua disposição...",
						"olá, estou as suas ordens :)", "oi, estou aqui pra lhe ajudar!"]

EXCHANGES = '''segue uma lista de algumas exchanges:
	-> Foxbit: www.foxbit.com.br
	-> Xapo: xapo.com
	-> Mercado Bitcoin: www.mercadobitcoin.com.br
	-> Bitcointoyou: www.bitcointoyou.com'''

def obter_valor_btc():
	url = "http://api.coindesk.com/v1/bpi/currentprice.json"
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	response = urlopen(req).read()
	data = json.loads(response.decode('utf-8'))
	valor = float(data['bpi']['USD']['rate'].replace(',', ''))
	return valor

# dicionário com possíveis respostas
RESPOSTAS = {
	'buy': 'você pode comprar bitcoin em www.foxbit.com.br.',
	'sell': 'você pode vender bitcoin em www.foxbit.com.br.',
	'price': '1 bitcoin vale %s dólares.' % obter_valor_btc(),
	'exchange': EXCHANGES,
	'create': 'bitcoin foi criado por Satoshi Nakamoto.',
	'blockchain': 'blockchain é um tecnologia fantástica :)'
}

def saudacao():

	mensagem = '\n' # mensagem do bot

	# obtém a hora atual para bom dia, boa tarde ou boa noite
	hora_atual = datetime.datetime.now().hour

	if hora_atual < 12:
		mensagem += 'Bom dia!'
	elif 12 <= hora_atual < 18:
		mensagem += 'Boa tarde!'
	else:
		mensagem += 'Boa noite!'

	mensagem += ''' Eu sou o BotCoin!
Eu estou aqui pra lhe ajudar sobre Bitcoin.
Digite SAIR para encerrar a nossa conversa.'''

	print(mensagem)


def chatbot():
	saudacao() # apresentação do bot

	# loop da conversação
	while True:
		frase = TextBlob(input('\nVocê: ').lower()) # obtém a mensagem do usuário

		# testa se o usuário quer encerrar a conversação
		if frase.replace(' ', '') == 'sair':
			print('Bot: Bye!')
			break # sai do loop

		'''se alguma das palavras do usuário for uma saudação,
		então responde com uma saudação'''
		for palavra in frase.words:
			if palavra.lower() in GREETING_KEYWORDS:
				print('Bot:', random.choice(GREETING_RESPONSES))
				break
		else:
			try:
				# se a mensagem não for inglês, então traduz pro inglês
				# os algoritmos da textblob só funcionam em inglês
				if frase.detect_language() != 'en':
					frase = TextBlob(str(frase.translate(to='en')))
			except:
				print('Bot: conte comigo pra lhe ajudar!')
			else:
				# analisando o sentimento
				if frase.sentiment.polarity < 0: # vai de -1 a 1
					print('Bot: não gostei do que você falou :(')
				else:
					print('Bot:', obter_resposta(frase))


def obter_resposta(frase):
	resposta = []
	verbos = encontrar_verbos(frase)
	substantivos = encontrar_substantivos(frase)

	if 'buy' in verbos:
		resposta.append(RESPOSTAS['buy'])
	if 'sell' in verbos:
		resposta.append(RESPOSTAS['sell'])
	if 'price' in substantivos or 'cost' in substantivos or 'value' in substantivos:
		resposta.append(RESPOSTAS['price'])
	if 'exchange' in substantivos or 'exchanges' in substantivos:
		resposta.append(RESPOSTAS['exchange'])
	if 'create' in verbos or 'creates' in verbos or 'created' in verbos:
		resposta.append(RESPOSTAS['create'])
	if 'blockchain' in substantivos:
		resposta.append(RESPOSTAS['blockchain'])

	if not resposta:
		return 'estou aqui pra lhe ajudar :)'
	return '\n'.join(resposta)


def encontrar_substantivos(frase):
	# encontra o substantivo
	#print(frase.pos_tags)
	substantivos = []
	for palavra, tag in frase.pos_tags:
		if tag.startswith('NN'): # se for substantivo
			substantivos.append(palavra) # adiciona na lista
	return substantivos

def encontrar_verbos(frase):
	# encontra o verbo
	#print(frase.pos_tags)
	verbos = []
	for palavra, tag in frase.pos_tags:
		if tag.startswith('VB'): # se for verbo
			verbos.append(palavra) # adiciona na lista
	return verbos


if __name__ == '__main__':
	chatbot()