import xbmc,xbmcplugin,os,urlparse,re
import client
import kodi
import dom_parser2
import log_utils

from resources.lib.modules import utils
from resources.lib.modules import helper
buildDirectory = utils.buildDir 

filename     = os.path.basename(__file__).split('.')[0]
base_domain  = 'http://www.xvideos.com'
base_name    = base_domain.replace('www.',''); base_name = re.findall('(?:\/\/|\.)([^.]+)\.',base_name)[0].title()
type         = 'video'
menu_mode    = 238
content_mode = 239
player_mode  = 801

search_tag   = 1
search_base  = urlparse.urljoin(base_domain,'?k=%s')

@utils.url_dispatcher.register('%s' % menu_mode)
def menu():
    
    
    
    try:
        url = urlparse.urljoin(base_domain,'tags')
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'ul', {'class': 'tags-list'})
        r = dom_parser2.parse_dom(r, 'li')
        r = [(dom_parser2.parse_dom(i, 'a'), \
            dom_parser2.parse_dom(i, 'b'), \
            dom_parser2.parse_dom(i, 'span')) \
            for i in r if 'flag-small' not in i.content]
        r = [(urlparse.urljoin(base_domain,i[0][0].attrs['href']), i[1][0].content,  i[2][0].content) for i in r]
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
            name = name.title() + ' - [ %s ]' % i[2]
            icon = xbmc.translatePath(os.path.join('special://home/addons/script.wankbank.artwork', 'resources/art/%s/icon.png' % filename))
            fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.wankbank.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': i[0], 'mode': content_mode, 'icon': icon, 'fanart': fanarts, 'folder': True})
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
        r = dom_parser2.parse_dom(c, 'div', {'id': re.compile('video_\d+')})
        r = [(dom_parser2.parse_dom(i, 'a', req=['href','title']), \
            dom_parser2.parse_dom(i, 'span', {'class': 'duration'}), \
            dom_parser2.parse_dom(i, 'img', req='data-src'), \
            dom_parser2.parse_dom(i, 'span', {'class': 'video-hd-mark'})) \
            for i in r if i]
        r = [(urlparse.urljoin(base_domain,i[0][0].attrs['href']), i[0][0].attrs['title'],  i[1][0].content, i[2][0].attrs['data-src'], i[3][0].content if i[3] else 'SD') for i in r]
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
            name = '%s - [ %s - %s ]' % (kodi.sortX(i[1].encode('utf-8')).title(),kodi.sortX(i[2].encode('utf-8')),kodi.sortX(i[4].encode('utf-8')))
            if searched: description = 'Result provided by %s' % base_name.title()
            else: description = name
            icon = re.sub('(\.THUMBNUM\.)','.1.',i[3])
            content_url = i[0] + '|SPLIT|%s' % base_name
            fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.wankbank.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': content_url, 'mode': player_mode, 'icon': icon, 'fanart': fanarts, 'description': description, 'folder': False})
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
            search_pattern = '''href=['"]([^'"]+)"\s*class="no-page\s*next-page">Next'''
            parse = base_domain        
            helper.scraper().get_next_page(content_mode,url,search_pattern,filename,parse)
        except Exception as e: 
            log_utils.log('Error getting next page for %s :: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)