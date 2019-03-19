'''
    Bonecrusher White Goo
    Copyright (C) 2015  WhiteGoo

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re

import xbmcplugin
from resources.lib import utils

addon = utils.addon

sortlistwxf = [addon.getLocalizedString(30012), addon.getLocalizedString(30013), addon.getLocalizedString(30014)]


@utils.url_dispatcher.register('10')
def WXFMain():
    utils.addDir('[COLOR white]Categories[/COLOR]','https://watchxxxfreeinhd.com/categories/',12,'','')
    utils.addDir('[COLOR white]Search[/COLOR]','https://watchxxxfreeinhd.com/page/1/?s=',14,'','')
    utils.addDir('[COLOR white]Top Pornstars[/COLOR]','https://watchxxxfreeinhd.com/actress-performes/',15,'','')
    Sort = '[COLOR white]Current sort:[/COLOR] ' + sortlistwxf[int(addon.getSetting("sortwxf"))]
    utils.addDir(Sort, '', 16, '', '')
    WXFList('https://watchxxxfreeinhd.com/index11/page/1/',1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('16')
def WXFSort():
    addon.openSettings()
    WXFMain()


@utils.url_dispatcher.register('12', ['url'])
def WXFCat(url):
    cathtml = utils.getHtml(url, '')  #
#    match = re.compile('<img width=.+?src="(.+?)".+?a href="(.+?)"\s+title="(.+?)".+?span class="nb_cat border.+?>(.+?)<', re.DOTALL | re.IGNORECASE).findall(cathtml)
    match = re.compile('<article id=.*?<a href="([^"]+)" title="([^"]+)".*?data-lazy-src="([^"]+)".*? alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(cathtml) # Current as of 19.02.23
    for catpage, name, img, videos in match:      # Current as of 19.02.23
#    for img, catpage, name, videos in match:
        catpage = catpage + 'page/1/'
        name = utils.cleantext(name)
        name = name #  + ' [COLOR deeppink]' + videos + '[/COLOR]'
        utils.addDir(name, catpage, 11, img, 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('15', ['url'])
def WXFTPS(url):
	tpshtml = utils.getHtml(url, '')
#	match = re.compile('<li><a href="([^"]+)[^>]+>([^<]+)', re.DOTALL | re.IGNORECASE).findall(tpshtml)
	match = re.compile('aria-label=.*?item.*?>([^<]+)</a><a href="([^"]+)', re.DOTALL | re.IGNORECASE).findall(tpshtml)   # Current as of 19.02.23
#	for tpsurl, name in match:
	for name, tpsurl in match:   # Current as of 19.02.23
		tpsurl = tpsurl + 'page/1/'
		utils.addDir(name, tpsurl, 11, '', 1)
	xbmcplugin.endOfDirectory(utils.addon_handle)    


@utils.url_dispatcher.register('14', ['url'], ['keyword'])
def WXFSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 14)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        WXFList(searchUrl, 1)


@utils.url_dispatcher.register('11', ['url'], ['page'])
def WXFList(url, page=1, onelist=None):
    if onelist:
        url = url.replace('/page/1/','/page/'+str(page)+'/')
    sort = getWXFSortMethod()
    if re.search('\?', url, re.DOTALL | re.IGNORECASE):
        url = url + '&filtre=' + sort + '&display=extract'
    else:
        url = url + '?filtre=' + sort + '&display=extract'
    try:
        listhtml = utils.getHtml(url, '')
    except Exception as e:
        return None
#    match = re.compile('src="([^"]+)" class="attachment-thumb_site.*?<a href="([^"]+)" title="([^"]+)".*?<p>([^<]+)</p>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    match = re.compile('<article id=.*?<a href="([^"]+)" title="([^"]+)".*?<img data-src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml) # Current as of 19.02.23
#    for img, videopage, name, desc in match:
    for videopage, name, img, desc in match:      # Current as of 19.02.23
        name = utils.cleantext(name)
        desc = utils.cleantext(desc)
        utils.addDownLink(name, videopage, 13, img, desc)
    if not onelist:
        if re.search('<link rel="next"', listhtml, re.DOTALL | re.IGNORECASE):
            npage = page + 1
            url = url.replace('/page/' + str(page) + '/', '/page/' + str(npage) + '/')
            utils.addDir('Next Page ('+str(npage)+')', url, 11, '', npage)
        xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('13', ['url', 'name'], ['download'])
def WXFVideo(url, name, download=None):
    vp = utils.VideoPlayer(name, download)
    vp.play_from_site_link(url, url)


def getWXFSortMethod():
    sortoptions = {0: 'date',
                   1: 'rate',
                   2: 'views'}
    sortvalue = addon.getSetting("sortwxf")
    return sortoptions[int(sortvalue)]
