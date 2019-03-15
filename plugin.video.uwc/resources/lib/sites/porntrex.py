'''
    Ultimate Whitecream
    Copyright (C) 2018 Whitecream, holisticdioxide

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
from random import randint

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils

progress = utils.progress


@utils.url_dispatcher.register('50')    
def PTMain():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]', 'https://www.porntrex.com/categories/', 53, '', '')
    utils.addDir('[COLOR hotpink]Search[/COLOR]', 'https://www.porntrex.com/search/', 54, '', '')
    PTList('https://www.porntrex.com/latest-updates/1/', 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('55')    
def JHMain():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]', 'https://www.javwhores.com/categories/', 53, '', '')
    utils.addDir('[COLOR hotpink]Search[/COLOR]', 'https://www.javwhores.com/search/', 54, '', '')
    JHList('https://www.javwhores.com/latest-updates/1/', 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)

@utils.url_dispatcher.register('51', ['url'], ['page'])
def PTList(url, page=1, onelist=None):
    if onelist:
        url = url.replace('/1/', '/' + str(page) + '/')
    try:
        listhtml = utils.getHtml(url, '')
    except:
        return None
#   Changed regex current 19.01.22
    match = re.compile ('data-item-id=.*?href="([^"]+)".*?data-src="([^"]+)"(.*?)clock-o"></i>([^<]+)<.*?title="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
#   Changed var order 19.01.22
    for videopage, img, hd, duration, name in match:

        name = utils.cleantext(name)
        if 'private' in hd:
            continue
#       Changed labelling adding Video quality
        if hd.find('4k') > 0:
            hd = " [COLOR orange]4K[/COLOR] "
        elif hd.find('2160p') > 0:
            hd = " [COLOR orange]4K[/COLOR] "
        elif hd.find('1080p') > 0:
            hd = " [COLOR orange]1080p[/COLOR] "
        elif hd.find('720p') > 0:
            hd = " [COLOR orange]720p[/COLOR] "
        elif hd.find('1440p') > 0:
            hd = " [COLOR orange]1440p[/COLOR] "
        else:
            hd = " "
        name = name + hd + "[COLOR deeppink]" + duration + "[/COLOR]"
        if img.startswith('//'):
            img = 'https:' + img
        img = re.sub(r"http:", "https:", img)
        domain = img.split('/')[2].split('.')[-2]
        img = img.split('.')
        if not img[0] == 'https://' + domain:
            img[0] = 'https://static'

        img = ('.').join(img)
        imgint = randint(1, 10)
        newimg = str(imgint) + '.jpg'
        img = img.replace('1.jpg', newimg)
        utils.addDownLink(name, videopage, 52, img, '')
    if not onelist:
        if re.search('<li class="next">', listhtml, re.DOTALL | re.IGNORECASE):
            npage = page + 1
            if '/categories/' in url:
                url = url.replace('from=' + str(page), 'from=' + str(npage))
            elif '/search/' in url:
#               19.02.01 Added to fix Search Pagination for PornTrex
                if page == 1:
                  searchphrase = url.split('/')[5]
                  url = url + '?mode=async&function=get_block&block_id=list_videos_videos&q=' + searchphrase + '&category_ids=&sort_by=post_date&from_videos=' + str(page) + '&from_albums=' + str(page)
                url = url.replace('from_videos=' + str(page), 'from_videos=' + str(npage)).replace('from_albums=' + str(page), 'from_albums=' + str(npage))
            else:
                url = url.replace('/' + str(page) + '/', '/' + str(npage) + '/')
            utils.addDir('Next Page (' + str(npage) + ')', url, 51, '', npage)
        xbmcplugin.endOfDirectory(utils.addon_handle)

@utils.url_dispatcher.register('451', ['url'], ['page'])
def JHList(url, page=1, onelist=None):
    if onelist:
        url = url.replace('/1/', '/' + str(page) + '/')
    try:
        listhtml = utils.getHtml(url, '')
    except:
        return None
    match = re.compile('class="video-item.*?href="([^"]+)" title="([^"]+)".*?original="([^"]+)"(.*?)clock-o"></i>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, name, img, hd, duration in match:
        name = utils.cleantext(name)
        if 'private' in hd:
            continue
        if hd.find('HD') > 0:
            hd = " [COLOR orange]HD[/COLOR] "
        elif hd.find('4k') > 0:
            hd = " [COLOR orange]4K[/COLOR] "
        else:
            hd = " "
        name = name + hd + "[COLOR deeppink]" + duration + "[/COLOR]"
        if img.startswith('//'):
            img = 'https:' + img
        img = re.sub(r"http:", "https:", img)
        domain = img.split('/')[2].split('.')[-2]
        img = img.split('.')
        if not img[0] == 'https://' + domain:
            img[0] = 'https://www'
        img = ('.').join(img)
        imgint = randint(1, 10)
        newimg = str(imgint) + '.jpg'
        img = img.replace('1.jpg', newimg)
        utils.addDownLink(name, videopage, 52, img, '')
    if not onelist:
        if re.search('<li class="next">', listhtml, re.DOTALL | re.IGNORECASE):
            npage = page + 1
            if '/categories/' in url:
                url = url.replace('from=' + str(page), 'from=' + str(npage))
            elif '/search/' in url:
#               19.02.01 Added to fix Search Pagination for JAVWhores
                if page == 1:
                  searchphrase = url.split('/')[5]
                  url = url + '?mode=async&function=get_block&block_id=list_videos_videos_list_search_result&q=' + searchphrase + '&category_ids=&sort_by=&from_videos=' + str(page) + '&from_albums=' + str(page)
                url = url.replace('from_videos=' + str(page), 'from_videos=' + str(npage)).replace('from_albums=' + str(page), 'from_albums=' + str(npage))
            else:
                url = url.replace('/' + str(page) + '/', '/' + str(npage) + '/')
            utils.addDir('Next Page (' + str(npage) + ')', url, 451, '', npage)
        xbmcplugin.endOfDirectory(utils.addon_handle)



@utils.url_dispatcher.register('52', ['url', 'name'], ['download'])
def PTPlayvid(url, name, download=None):
    progress.create('Play video', 'Searching for videofile.')
    progress.update(25, "", "Loading video page", "")
    videopage = utils.getHtml(url, '')
    if 'video_url_text' not in videopage:
        videourl = re.compile("video_url: '([^']+)'", re.DOTALL | re.IGNORECASE).search(videopage).group(1)
    else:
        sources = {}
        srcs = re.compile("video(?:_alt_|_)url(?:[0-9]|): '([^']+)'.*?video(?:_alt_|_)url(?:[0-9]|)_text: '([^']+)'", re.DOTALL | re.IGNORECASE).findall(videopage)
        for src, quality in srcs:
            sources[quality] = src
        videourl = utils.selector('Select quality', sources, dont_ask_valid=True, sort_by=lambda x: int(''.join([y for y in x if y.isdigit()])), reverse=True)
    if not videourl:
        progress.close()
        return
    progress.update(75, "", "Video found", "")
    progress.close()
    if download == 1:
        utils.downloadVideo(videourl, name)
    else:
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(videourl, listitem)


@utils.url_dispatcher.register('53', ['url'])
def PTCat(url):
    cathtml = utils.getHtml(url, '')
    cat_block = re.compile('<span class="icon type-video">(.*?)<div class="footer-margin">', re.DOTALL | re.IGNORECASE).search(cathtml).group(1)
    match = re.compile('<a class="item" href="([^"]+)" title="([^"]+)".*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(cat_block)
    for catpage, name, img in sorted(match, key=lambda x: x[1]):
        if img.startswith('//'):
            img = 'https:' + img
        img = re.sub(r"cdn\d?", "www", img)
        catpage = catpage + '?mode=async&function=get_block&block_id=list_videos_common_videos_list&sort_by=post_date&from=1'
#   Changed 19.01.25
        if url.find('javwhores') > 0:
            utils.addDir(name, catpage, 451, img, 1)
        else:
            utils.addDir(name, catpage, 51, img, 1)       
    xbmcplugin.endOfDirectory(utils.addon_handle)

@utils.url_dispatcher.register('54', ['url'], ['keyword'])
def PTSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 54)
    else:
        searchUrl = searchUrl + '/' + keyword + '/'
#   Changed 19.01.25
        if url.find('javwhores') > 0:
            JHList(searchUrl, 1)
        else:
            PTList(searchUrl, 1)
