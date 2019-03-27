import xbmc,xbmcplugin,os,urlparse,re
import log_utils
import kodi
import cache
import client
import dom_parser2
import lover
from resources.lib.modules import utils
from resources.lib.modules import helper
buildDirectory = utils.buildDir #CODE BY NEMZZY AND ECHO

filename     = os.path.basename(__file__).split('.')[0]
base_domain  = 'https://justporno.tv'
base_name    = base_domain.replace('www.',''); base_name = re.findall('(?:\/\/|\.)([^.]+)\.',base_name)[0].title()
type         = 'video'
menu_mode    = 202
content_mode = 203
player_mode  = 801

search_tag   = 1
search_base  = urlparse.urljoin(base_domain,'search?query=%s')

@utils.url_dispatcher.register('%s' % menu_mode)
def menu():
    
    lover.checkupdates()
    
    try:
        url = base_domain
        c = client.request(url)
        r = dom_parser2.parse_dom(c, 'li')
        r = dom_parser2.parse_dom(r, 'a', req='title')
        r = [(urlparse.urljoin(base_domain,i.attrs['href']),i.content) for i in r if '/tag' in i.attrs['href']]
        if ( not r ):
            log_utils.log('Scraping Error in %s:: Content of request: %s' % (base_name.title(),str(c)), log_utils.LOGERROR)
            kodi.notify(msg='Scraping Error: Info Added To Log File', duration=6000, sound=True)
            quit()
    except Exception as e:
        log_utils.log('Fatal Error in %s:: Error: %s' % (base_name.title(),str(e)), log_utils.LOGERROR)
        kodi.notify(msg='Fatal Error', duration=4000, sound=True)
        quit()
        
    dirlst = []

    if r:
        for i in r:
            try:
                iconimage = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/icon.png' % filename))
                fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
                name = kodi.sortX(i[1].encode('utf-8'))
                dirlst.append({'name': name, 'url': i[0], 'mode': content_mode, 'icon': iconimage, 'fanart': fanarts, 'folder': True})
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
        r = dom_parser2.parse_dom(c, 'li')
        r = [(dom_parser2.parse_dom(i, 'a', req=['href','title']), \
              dom_parser2.parse_dom(i, 'i'), \
              dom_parser2.parse_dom(i, 'img', req='data-original')) \
              for i in r if '<noscript>' in i.content]
        r = [(urlparse.urljoin(base_domain,i[0][0].attrs['href']), i[0][0].attrs['title'], i[1][0].content, \
            i[2][0].attrs['data-original'] if i[2][0].attrs['data-original'].startswith('http') else 'https:' + i[2][0].attrs['data-original']) for i in r if i[2][0].attrs['data-original']]
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
            name = kodi.sortX(i[1].encode('utf-8'))
            name = name.title() + ' - [ %s ]' % i[2]
            if searched: description = 'Result provided by %s' % base_name.title()
            else: description = name
            content_url = i[0] + '|SPLIT|%s' % base_name
            fanarts = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/fanart.jpg' % filename))
            dirlst.append({'name': name, 'url': content_url, 'mode': player_mode, 'icon': i[3], 'fanart': fanarts, 'description': description, 'folder': False})
        except Exception as e:
            log_utils.log('Error adding menu item %s in %s:: Error: %s' % (i[0].title(),base_name.title(),str(e)), log_utils.LOGERROR)
    
    if dirlst: buildDirectory(dirlst, stopend=True, isVideo = True, isDownloadable = True)
    else:
        if (not searched):
            kodi.notify(msg='No Content Found')
            quit()
        
    if searched: return str(len(r))
    
    if not searched:
        search_pattern = '''<a\s*href=['"]([^'"]+)['"]\s*title=['"]Next\s*Page['"]>Next<\/a>'''
        parse = base_domain

        helper.scraper().get_next_page(content_mode,url,search_pattern,filename,parse)