import xbmc,xbmcplugin,os,urlparse,re
import client
import kodi
import dom_parser2
import log_utils

from resources.lib.modules import utils
from resources.lib.modules import helper
buildDirectory = utils.buildDir

filename     = os.path.basename(__file__).split('.')[0]
base_domain  = 'https://www.tube8.com'
base_name    = base_domain.replace('www.',''); base_name = re.findall('(?:\/\/|\.)([^.]+)\.',base_name)[0].title()
type         = 'video'
menu_mode    = 250
content_mode = 251
player_mode  = 801

search_tag   = 1
search_base  = urlparse.urljoin(base_domain,'searches.html?q=%s')

@utils.url_dispatcher.register('%s' % menu_mode)
def menu():
    

    
    try:
        url = urlparse.urljoin(base_domain, 'categories.html')
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'li')
        r = [i for i in r if '<span class="category-thumb">' in i.content]
        r = [(dom_parser2.parse_dom(i, 'a'), dom_parser2.parse_dom(i, 'img')) for i in r]
        r = [(i[0][0].attrs['href'], re.sub('<.+?>','',i[1][0].content), i[1][0].attrs['data-thumb']) for i in r[1:]] 
        if ( not r ):
            log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
            kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
            quit()
    except Exception as e:
        log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
        kodi.notify(msg='Fatal Error', duration=4000, sound=True)
        quit()

    dirlst = []
    
    for i in r:
        try:
            name = kodi.sortX(i[1].encode('utf-8'))
            fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.wankbank.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': i[0], 'mode': content_mode, 'icon': i[2], 'fanart': fanarts, 'folder': True})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: buildDirectory(dirlst)    
    else:
        kodi.notify(msg='No Menu Items Found')
        quit()
        
@utils.url_dispatcher.register('%s' % content_mode,['url'],['searched'])
def content(url,searched=False):

	try:
		c = client.request(url)
		r = re.findall('class="thumb_box">(.*?)</div>',c,flags=re.DOTALL)
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
			title = re.findall('title="(.*?)"',i)[0]
			url = re.findall('<a href="(.*?)"',i)[0]
			icon = re.findall('data-thumb="(.*?)"',i)[0]
			fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.wankbank.artwork', 'resources/art/%s/fanart.jpg' % filename))
			dirlst.append({'name': title, 'url': url, 'mode': player_mode, 'icon': icon, 'fanart': fanarts, 'folder': False})
		except: pass


	if dirlst: buildDirectory(dirlst, stopend=True, isVideo = True, isDownloadable = True)
	else:
		if (not searched):
			kodi.notify(msg='No Content Found')
			quit()
		
	if searched: return str(len(r))

	if not searched:
		
		try:
			search_pattern = '''<link\s*rel=['"]next['"]\s*href=['"]([^'"]+)'''
			parse = base_domain        
			helper.scraper().get_next_page(content_mode,url,search_pattern,filename)
		except Exception as e: 
			log_utils.log('Error getting next page for %s :: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)