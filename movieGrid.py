import os
import urllib
import codecs
from BeautifulSoup import BeautifulSoup
import re

class Movie:
	def __init__(self, directory):
		self.directory = directory
		title = directory
		if re.match('.*\(\d{4}\).*', title):
			title = re.search('(.*) \(\d{4}\)', title).group(1).strip()
		if re.match('^\d{2}_', title):
			title = re.search('^\d{2}_(.*)', title).group(1).strip()
		self.title = title
		self.searchMovie()
		
	def searchMovie(self):
		params = urllib.urlencode({'q': self.title})
		f = urllib.urlopen("http://www.imdb.com/find?%s" % params)
		html = f.read()
		parsed_html = BeautifulSoup(html)
		result = parsed_html.find('table', attrs={'class':'findList'}).first()

		if re.match('.*/title/.*', result.find('a')['href']):
			self.id = re.search('/title/(.*)/', result.find('a')['href']).group(1).strip()
			self.found = True
			self.getInfos()
			print 'FOUND: ' + self.title
			print '    (id: '+self.id+')'
		else:
			self.found = False
			print 'NOT FOUND: ' + self.title

	def getInfos(self):
		f = urllib.urlopen("http://www.imdb.com/title/"+self.id)
		html = f.read()
		parsed_html = BeautifulSoup(html)
		infosDiv = parsed_html.find('div', attrs={'class':'maindetails_center'})

		# Image
		if infosDiv.find('div', attrs={'class':'image'}):
			self.image = infosDiv.find('div', attrs={'class':'image'}).find('img')['src']
		else:
			self.image = ''

def renderView(movies, output='view.html'):
	#out = open('view.html', 'w')
	out = codecs.open("view.html", "w", "utf-8")
	out.write(u'\ufeff')

	out.write('<!DOCTYPE html><html>')
	out.write('<head>')
	out.write('<style type="text/css"><!--')
	out.write('body {border: 10px 50px;}')
	out.write('.movie {margin: 0px 10px 10px 10px;}')
	out.write('div {float: left; text-align: left;}')
	out.write('div p {text-align: center; margin-top: 0px;}')
	out.write('hr{width:100%; margin: 120px 0px;}')
	out.write('--></style>')
	out.write('</head><body>')

	for movie in movies:
		if movie.found:
			if re.match('^00_.*', movie.directory):
				print '00: ' + movie.title
				out.write('<div class="movie">')
				out.write('<img height="210px" src="'+movie.image+'" />')
				out.write('<p><a href="http://www.imdb.com/title/'+ movie.id + '">' + movie.title.decode('utf8') + '</a></p>')
				out.write('</div>')
	
	out.write('<hr>')

	for movie in movies:
		if movie.found:
			if re.match('^01_(.*)', movie.directory):
				print '00: ' + movie.title
				out.write('<div class="movie">')
				out.write('<img height="210px" src="'+movie.image+'" />')
				out.write('<p><a href="http://www.imdb.com/title/'+ movie.id + '">' + movie.title.decode('utf8') + '</a></p>')
				out.write('</div>')
	
	out.write('<hr>')

	for movie in movies:
		if movie.found:
			if re.match('^02_(.*)', movie.directory):
				print '00: ' + movie.title
				out.write('<div class="movie">')
				out.write('<img height="210px" src="'+movie.image+'" />')
				out.write('<p><a href="http://www.imdb.com/title/'+ movie.id + '">' + movie.title.decode('utf8') + '</a></p>')
				out.write('</div>')
	
	out.write('<hr>')

	out.write('<div><ul>')
	for movie in movies:
		if not(movie.found):
			out.write('<li>'+movie.title+'</li>')
	out.write('</ul></div>')
	out.write('</body></html>')
	out.close()

movieDir = "/home/raph/movies/"

if os.path.isfile('view.html'):
	os.remove('view.html')

movies = []
directories = os.listdir(movieDir)
for directory in directories:
	if re.match('^\d\d_', directory):
		movies.append(Movie(directory))
print "------------ RENDERING ------------"
renderView(movies)