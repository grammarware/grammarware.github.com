#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
# -*- coding: utf-8 -*-

import glob, re, datetime

# Header Counter
p = re.compile('<(?P<tag>\w+)>(?P<txt>[^\<]+)</(?P=tag)+>')
d = ('Zeroary', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',\
	'September', 'October', 'November', 'December')[datetime.date.today().month]+\
	' '+str(datetime.date.today().year)
for dsl in glob.glob("*.dsl") + glob.glob("*/*.dsl"):
	HX = 0
	picdir = divclass = ''
	print('Processing', dsl)
	f = open(dsl, 'r', encoding='utf-8')
	lines = f.readlines()
	f.close()
	g = open(dsl.replace('.dsl', '.html'), 'w', encoding='utf-8')
	i = 0
	while i < len(lines):
		# skip comments
		if lines[i].strip().startswith('<!--'):
			while not lines[i].strip().endswith('-->'):
				i += 1
			i += 1
		# skip empty lines
		if not lines[i].strip():
			i += 1
			# to be on the safe side of the boundary bug
			continue
		# unified head
		if lines[i].strip().startswith('<head '):
			if lines[i].strip().find('viewport') < 0:
				vp = ''
			else:
				vp = '''
		<meta name="viewport" content="initial-scale=1.0"/>'''
			if lines[i].strip().find('title="') < 0:
				title = ''
			else:
				title = ' — ' + lines[i].split('"')[1]
			rootpath = '' if dsl.find('/') < 0 and dsl.find('\\') < 0 else '../'
			if lines[i].strip().find('jquery') < 0:
				end = '</script>'
			else:
				end = '''function onn(n) {$('.help:eq('+n+')').css('background-color','#552200');}
		function off(n) {$('.help:eq('+n+')').css('background-color','#ffdec9');}
		</script>
		<script src="../jquery.min.js" type="text/javascript"></script>'''
			g.write('''	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<meta http-equiv="x-ua-compatible" content="IE=9">%s
		<title>Dr. Vadim Zaytsev%s</title>
		<link href="%scommon.css" rel="stylesheet" type="text/css" />
		<script type="text/javascript">

		  var _gaq = _gaq || [];
		  _gaq.push(['_setAccount', 'UA-3743366-7']);
		  _gaq.push(['_setDomainName', 'github.io']);
		  _gaq.push(['_setAllowLinker', true]);
		  _gaq.push(['_trackPageview']);

		  (function() {
		    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
		    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
		    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
		  })();

		%s
	</head>
''' % (vp, title, rootpath, end))
			i += 1
		# useful macros
		if lines[i].strip() == '<header/>':
			lines[i] = '<div style="text-align:center;"><a href="http://grammarware.github.io">Vadim Zaytsev</a> aka @<a href="http://grammarware.net">grammarware</a></div><hr/>'
		if lines[i].strip() == '<html doctype>':
			lines[i] = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html version="-//W3C//DTD XHTML 1.1//EN" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/1999/xhtml http://www.w3.org/MarkUp/SCHEMA/xhtml11.xsd">'''
		if lines[i].strip() == '<valid/>':
			rootpath = '' if dsl.find('/') < 0 and dsl.find('\\') < 0 else '../'
			lines[i] = '''<br/><a href="http://validator.w3.org/check/referer"><img src="%slogos/xhtml.88.png" alt="XHTML 1.1" /></a>
			<a href="http://jigsaw.w3.org/css-validator/check/referer"><img src="%slogos/css.88.png" alt="CSS 3" /></a>''' % (rootpath, rootpath)
		if lines[i].strip().startswith('<footer'):
			rootpath = '' if dsl.find('/') < 0 and dsl.find('\\') < 0 else '../'
			content = ''
			if lines[i].strip() == '<footer/>':
				content = ''
			else:
				i += 1
				while lines[i].strip() != '</footer>':
					content += lines[i].strip() + ' '
					i += 1
			lines[i] = '''<div class="last"><br/><hr/>The page is maintained by <a href="http://grammarware.net/">Dr. Vadim Zaytsev</a> a.k.a. @<a href="http://twitter.com/grammarware">grammarware</a>. %sLast updated: #LASTMOD#.<br/>
			<a href="http://validator.w3.org/check/referer"><img src="%slogos/xhtml.88.png" alt="XHTML 1.1" /></a>
			<a href="http://jigsaw.w3.org/css-validator/check/referer"><img src="%slogos/css.88.png" alt="CSS 3" /></a></div>''' % (content, rootpath, rootpath)
		# jQuery use
		if lines[i].strip().startswith('<h2 help'):
			helptext = lines[i].split('"')[1]
			gist = lines[i].split('>')[1].split('<')[0]
			lines[i] = '<h2 onmouseover="onn(%s)" onmouseout="off(%s)">%s <span class="help">(%s)</span></h2>' % (HX, HX, gist, helptext)
			HX += 1
		# Ordered lists
		if lines[i].strip() == '<ol>':
			lines[i] = lines[i].replace('<ol>', '<ol class="fwd">')
		elif lines[i].strip() == '<ol back>':
			j = i
			lis = 1
			while lines[j].strip()!='</ol>':
				j += 1
				if lines[j].find('<li>') > -1:
					lis += 1
			lines[i] = '<ol class="back" style="counter-reset: item %s">' % lis
		# tiles
		if lines[i].strip().startswith('<picdir'):
			picdir = p.search(lines[i].strip()).groups()[1]+'/'
		elif lines[i].strip().startswith('<divclass'):
			divclass = p.search(lines[i].strip()).groups()[1]
		elif lines[i].strip().startswith('<pic'):
			classes = re.split('\W+', lines[i])[2:-1]
			if 'nopic' in classes:
				classes.remove('nopic')
			else:
				classes.append('pic')
			c = ' '.join(classes)
			i += 1
			pic = {}
			while lines[i].strip() != '</pic>':
				db = p.search(lines[i].strip()).groups()
				pic[db[0]] = db[1]
				i += 1
			if 'name' not in pic:
				pic['name'] = ''
			if 'alt' not in pic:
				pic['alt'] = pic['name']
			if 'title' not in pic:
				pic['title'] = pic['name']
			if 'text' in pic:
				pic['text'] = '<span class="p">%s</span>' % pic['text']
			else:
				pic['text'] = ''
			for key in pic:
				pic[key] = pic[key].replace('\\n', '<br/>')
			if divclass:
				div = '<div class="'+divclass+'">'
			else:
				div = '<div>'
			if pic['a'].find('/') < 0:
				pic['a'] += '/index.html'
			g.write(('\t\t{}<a href="{}"><span class="{}"><img src="{}{}" alt="{}" title="{}"/>'+\
				'<br/>{}{}</span></a></div>\n').format(\
					div,\
					pic['a'],\
					c,\
					picdir,\
					pic['img'],\
					pic['alt'],\
					pic['title'],\
					pic['name'],\
					pic['text'])\
				)
		elif lines[i].find('#LASTMOD#') > -1:
			g.write(lines[i].replace('#LASTMOD#', d))
		else:
			g.write(lines[i])
		i += 1
	g.close()
