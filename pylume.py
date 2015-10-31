#!/usr/bin/env python
# coding: utf-8

#   Please read API Terms at api.vagalume.com.br/terms/

#   Copyright Vagalume Midia Ltda. All rights reserved.

#   Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

#   The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

# More info: www.api.vagalume.com.br

from datetime import datetime
from Tkinter import *

import json
import urllib2

now = datetime.now()
print "---Buscador de letras do Vagalume---"
print "Data e hora da requisicao: %s/%s/%s %s:%s\n" % (now.day, now.month, now.year, now.hour, now.minute)

# Requisição do artista/música
def main():
	while True:
		try:
			# Entre com o nome do artista e da música
			step = '%20'
			artist = raw_input("Artist name? ").split()
			song = raw_input("Song Name? ").split()
			try:
				# Faz a requisição à API do Vagalume, usando o nome do artista e da música, através do urllib2
				response = urllib2.urlopen("http://api.vagalume.com.br/search.php?art=" + step.join(artist) + "&mus=" + step.join(song))
				data = json.load(response)
				# Pergunta ao usuário se ele deseja visualizar a música no idioma original, ou traduzida para pt-br
				version = raw_input("1 to visualize original lyrics, 2 to portuguese lyrics: ")
				if version == '1':
					# Retorna, na janela do Tkinter, a letra original da música. Caso a letra original já seja em Português, apenas retorna a letra
					letra = data["mus"][0]["text"]
					window(letra, data)
					break
				elif version == '2':
					# Retorna, na janela do Tkinter, a letra traduzida da música
					letra = data["mus"][0]["translate"][0]["text"]
					window(letra, data)
					break
				else:
					# Caso o usuário digite não digite uma opção válida para fins de idioma da letra...
					print ("Invalid entry. Try again!\n\n")
			except urllib2.URLError:
				# Caso o usuário não possua conexão com a internet...
				print ("\nSorry, no internet connection?\n")
				break
		except KeyError:
			# Caso haja erros de digitação nas entradas do nome do artista e da música
			if version == '2':
				print ("Something went wrong. Make sure that you're not selecting '2' for a portuguese song.\nCheck the artist and the song name, and then try again...\n")
			else:
				print "Something went wrong. Try again...\n"

# Criação da janela separada, que exibe a música
def window(letra, data):
	app = Tk()
	app.title("%s" % (data["mus"][0]["name"]))

	frame = Frame(app, width = 800, height = 600)
	frame.grid(row = 0, column = 0)
	canvas = Canvas(
		frame,
		bg = '#DCDCDC',
		width = 600,
		height = 600,
		scrollregion = (0,0,500,4000,)
		)

	texto = letra

	vbar = Scrollbar(frame, orient = VERTICAL)
	vbar.pack(side = RIGHT, fill = Y)
	vbar.config(command = canvas.yview)
	canvas.config(yscrollcommand = vbar.set)
	canvas.create_text((250, 20), text = texto, anchor = 'n')
	canvas.pack()

	app.mainloop()

if __name__ == "__main__":
    main()

print ('\n\n--End of file--\n')
