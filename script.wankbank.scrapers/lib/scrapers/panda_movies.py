import xbmc,xbmcplugin,os,urlparse,re
import client
import kodi
import dom_parser2
import log_utils
from resources.lib.modules import utils
from resources.lib.modules import helper
buildDirectory = utils.buildDir #CODE BY NEMZZY AND ECHO

filename     = 'pandamovie'
base_domain  = 'https://123pandamovie.me'
base_name    = base_domain.replace('www.',''); base_name = re.findall('(?:\/\/|\.)([^.]+)\.',base_name)[0].title()
type         = 'movies'
menu_mode    = 297
content_mode = 298
player_mode  = 810

search_tag   = 0
search_base  = urlparse.urljoin(base_domain,'search.fcgi?query=%s')

@utils.url_dispatcher.register('%s' % menu_mode)
def menu():

	url = urlparse.urljoin(base_domain,'adult/genre/featured-movies/')
	content(url)
	# try:
		# url = urlparse.urljoin(base_domain,'xxx/movies/')
		# c = client.request(url)
		# r = re.findall('<div\s+class="mepo">(.*?)<div\s+class="rating">',c, flags=re.DOTALL)
		# if ( not r ):
			# log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
			# kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
			# quit()
	# except Exception as e:
		# log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
		# kodi.notify(msg='Fatal Error', duration=4000, sound=True)
		# quit()

	# dirlst = []

	# for i in r:
		# try:
			# name = re.findall('<h3><a href=".+?">(.*?)</a>',i,flags=re.DOTALL)[0]
			# url = re.findall('<h3><a href="(.*?)"',i,flags=re.DOTALL)[0]
			# icon = re.findall('<img src="(.*?)"',i,flags=re.DOTALL)[0]
			# desc = re.findall('<div class="texto">(.*?)</div>',i,flags=re.DOTALL)[0]
			# fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
			# dirlst.append({'name': name, 'url': url, 'mode': content_mode, 'icon': icon, 'description': desc, 'fanart': fanarts ,'folder': True})
		# except Exception as e:
			# log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)

	# if dirlst: buildDirectory(dirlst)    
	# else:
		# kodi.notify(msg='No Menu Items Found')
		# quit()
        
@utils.url_dispatcher.register('%s' % content_mode,['url'],['searched'])
def content(url,searched=False):

	try:
		if url == '':
			url = urlparse.urljoin(base_domain,'xxx/movies/')
		c = client.request(url)
		r = re.findall('<div\s+class="mepo">(.*?)<div\s+class="rating">',c, flags=re.DOTALL)
		if ( not r ) and ( not searched ):
			log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
			kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
	except Exception as e:
		if ( not searched ):
			log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
			kodi.notify(msg='Fatal Error', duration=4000, sound=True)
			quit()    
		else: pass

	dirlst = []
		
	for i in r:
		try:
			name = re.findall('<h3><a href=".+?">(.*?)</a>',i,flags=re.DOTALL)[0]
			url2 = re.findall('<h3><a href="(.*?)"',i,flags=re.DOTALL)[0]
			icon = re.findall('<img src="(.*?)"',i,flags=re.DOTALL)[0]
			desc = re.findall('<div class="texto">(.*?)</div>',i,flags=re.DOTALL)[0]
			fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
			dirlst.append({'name': name, 'url': url2, 'mode': player_mode, 'icon': icon, 'fanart': fanarts, 'description': desc, 'folder': False})
		except Exception as e:
			log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)

	if dirlst: buildDirectory(dirlst, stopend=True, isVideo = True, isDownloadable = True)
	else:
		if (not searched):
			kodi.notify(msg='No Content Found')
			quit()
		
	if searched: return str(len(r))

	if not searched:
		
		try:
			search_pattern = '''<link rel=['"]next['"]\s*href=['"]([^'"]+)'''
			helper.scraper().get_next_page(content_mode,url,search_pattern,filename)
		except Exception as e: 
			log_utils.log('Error getting next page for %s :: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)