# -*- coding: utf-8 -*-
import xbmc,xbmcplugin,os,urlparse,re
import client
import kodi
import dom_parser2
import log_utils
import scraper_updater
from resources.lib.modules import utils
from resources.lib.modules import helper
from resources.lib.modules import linkfinder
buildDirectory = utils.buildDir

filename     = 'sexvideos'
base_domain  = 'http://qwertty.net'
base_name    = base_domain.replace('www.',''); base_name = re.findall('(?:\/\/|\.)([^.]+)\.',base_name)[0].title()
type         = 'movies'
menu_mode    = 503
player_mode  = 810
        
@utils.url_dispatcher.register('%s' % menu_mode, ['url'])
def content(url):

    try:
        if not url: url = 'http://qwertty.net/'
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'div',  {'class': 'movie-item'})
        r = [(dom_parser2.parse_dom(i, 'div', req='data-link'), \
              dom_parser2.parse_dom(i, 'img', req=['src', 'alt'])) \
              for i in r]
        r = [(i[0][0].attrs['data-link'], i[1][0].attrs['alt'], re.sub('/uploads/.*?','http://qwertty.net/uploads/',i[1][0].attrs['src'])) for i in r]
        if ( not r ):
            log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
            kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
    except Exception as e:
        log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
        kodi.notify(msg='Fatal Error', duration=4000, sound=True)
        quit()    

    dirlst = []
    
    for i in r:
        try:
            name = i[1].title()
            description = name
            content_url = i[0] + '|SPLIT|%s' % base_name
            fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.wankstains.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': content_url, 'mode': player_mode, 'icon': i[2], 'fanart': fanarts, 'description': description, 'folder': False})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[1].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: buildDirectory(dirlst, stopend=True, isVideo = True, isDownloadable = True)
    else:
        kodi.notify(msg='No Content Found')
        quit()

    search_pattern = '''<a\s*href=['"]([^'"]+)['"]>Next'''
    helper.scraper().get_next_page(menu_mode,url,search_pattern,filename)