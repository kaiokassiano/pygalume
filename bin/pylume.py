#!/usr/bin/env python
#  coding: utf-8

#  You can make any modifications to this code.
#  Please read API Terms at api.vagalume.com.br/terms/

#  Copyright Vagalume Midia Ltda. All rights reserved.

#  Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

#  The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
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
print "\n---Buscador de letras do Vagalume---"
print "Data e hora da requisicao: %s/%s/%s %s:%s" % (now.day, now.month, now.year, now.hour, now.minute)

# Requisição do artista/música
def main():
	while 1:
		try:
			# Entre com o nome do artista e da música
			step = '%20'
			artist = raw_input("\nArtist name? ").split()
			song = raw_input("Song Name? ").split()
			
			try:
				# Faz a requisição à API do Vagalume, usando o nome do artista e da música, através do urllib2
				response = urllib2.urlopen("http://api.vagalume.com.br/search.php?art=" + step.join(artist) + "&mus=" + step.join(song))
				data = json.load(response)
				
				# Ocorrências para músicas que não possuem tradução
				if 'translate' not in data["mus"][0]:
					
					if data["mus"][0]["lang"] == 1:
						raw_input("\nMusic already in portuguese\nPress Enter to continue and show portuguese lyrics...")
						letra = data["mus"][0]["text"]
						window(letra, data)
						break
					elif data["mus"][0]["lang"] == 2:
						raw_input("\nThis music ain't got portuguese version\nPress Enter to continue and show original lyrics...")
						letra = data["mus"][0]["text"]
						window(letra, data)
						break
				
				# Ocorrências para músicas que possuem tradução
				elif 'translate' in data["mus"][0]:
					
					while 1:
						version = raw_input("\n1 to show original lyrics, 2 to show portuguese lyrics: ")
						
						if version == "1":
							letra = data["mus"][0]["text"]
							window(letra, data)
							break
						
						elif version == "2":
							letra = data["mus"][0]["translate"][0]["text"]
							window(letra, data)
							break
						
						else:
							print "Invalid entry. Try again!\n\n"
					
					break
			
			# Caso o usuário não possua conexão com a internet...
			except urllib2.URLError:
				print ("\nSorry, no internet connection?\n")
				break
		
		# Caso hajam erros de digitação no nome do artista e da música
		except KeyError:
				print "Something went wrong. Check artist and song name, and try again...\n"

# Criação da janela separada, que exibe a música
def window(letra, data):
	app = Tk()
	app.title("%s" % (data["mus"][0]["name"]))
	
	frame = Frame(app, width = 1366,	 height = 768)
	frame.grid(row = 0, column = 0)
	canvas = Canvas(
		frame,
		bg = '#DCDCDC',
		width = 600,
		height = 600,
		scrollregion = (0,0,500,letra.count('\n') * 16)
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
