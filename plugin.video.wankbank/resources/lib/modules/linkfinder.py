import re
import kodi
import client
import player
import dom_parser2
import log_utils
import utils
import resolveurl

@utils.url_dispatcher.register('810', ['url'], ['name', 'iconimage', 'pattern']) 
def find(url, name=None, iconimage=None, pattern=None):

    #kodi.busy()
    
    try: url,site = url.split('|SPLIT|')
    except: 
        site = 'Unknown'
        log_utils.log('Error getting site information from :: %s' % (url), log_utils.LOGERROR)
    
    try:
        if 'streamingporn.xyz' in url:
            c = client.request(url)
            r = dom_parser2.parse_dom(c, 'iframe', req=['src'])
            r = [i.attrs['src'] for i in r if resolveurl.HostedMediaFile(i.attrs['src']).valid_url()]
            url = multi(r)
        elif 'spreadporn.org' in url:
            c = client.request(url)
            r = dom_parser2.parse_dom(c, 'li', req=['data-show','data-link'])
            r = [(i.attrs['data-link']) for i in r]
            url = multi(r)
        elif 'pandamovie.eu' in url:
            c = client.request(url)
            r = dom_parser2.parse_dom(c, 'a', req='id')
            r = [(i.attrs['href']) for i in r]
            url = multi(r)
        elif 'xtheatre.net' in url:
            c = client.request(url)
            pattern = '''<iframe\s*src=['"](?:[^'"]+)['"]\s*data-lazy-src=['"]([^'"]+)'''
            r = re.findall(pattern,c)
            url = multi(r)
        elif 'sexkino.to' in url:   
            c = client.request(url)
            u = dom_parser2.parse_dom(c, 'iframe', {'class': ['metaframe','rptss']})
            r = dom_parser2.parse_dom(c, 'tr')
            r = [dom_parser2.parse_dom(i, 'a', req='href') for i in r]
            r = [client.request(i[0].attrs['href']) for i in r if i]
            r = [i.attrs['src'] for i in u] + [re.findall("window.location.href='([^']+)", i)[0] for i in r]
            url = multi(r)     
        elif 'qwertty.net' in url:  
            c = client.request(url)
            r = dom_parser2.parse_dom(c, 'div', {'class': 'full-text'})
            r = dom_parser2.parse_dom(r, 'a', req='href')
            r = [(i.attrs['href']) for i in r]
            url = multi(r)     
        elif 'pornfree.me' in url:
            c = client.request(url)
            r = dom_parser2.parse_dom(c, 'li', {'class': 'hosts-buttons-wpx'})
            r = dom_parser2.parse_dom(r, 'a', req='href')
            r = [(i.attrs['href']) for i in r]
            url = multi(r)   
    except:
        kodi.idle()
        kodi.notify(msg='Error getting link for (Link Finer) %s' % name)
        kodi.idle()
        quit()
    
    url += '|SPLIT|%s' % site
    kodi.idle()
    player.resolve_url(url, name, iconimage)
    
def multi(r):
     
    r = [(re.findall('(?://)(?:www.)?([^.]+).', i)[0].title(), i) for i in r if resolveurl.HostedMediaFile(i).valid_url()]
     
    names = []
    srcs  = []

    if len(r) > 1:
        for i in sorted(r, reverse=True):
            names.append(kodi.giveColor(i[0],'white',True))
            srcs.append(i[1])
        selected = kodi.dialog.select('Select a link.',names)
        if selected < 0:
            kodi.notify(msg='No option selected.')
            kodi.idle()
            quit()
        else:
            url = srcs[selected]
            return url
    else: return r[0][1]