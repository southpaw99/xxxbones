# from kodi_six import xbmc, xbmcaddon
# import os
# from packlib import kodi, client, cache, log_utils
 
# def check(scraper):
#     return
    # try:
        # disable_check = xbmcaddon.Addon('plugin.video.adultflix').getSetting('dev_scrapers')

        # if ( not disable_check == 'true' ): 
            # scraperFile = xbmc.translatePath(os.path.join('special://home/addons/script.adultflix.scrapers', 'lib/scrapers/%s.py' % scraper.lower()))
            # scraperLink = 'https://raw.githubusercontent.com/tvaddonsco/script.adultflix.scrapers/master/lib/scrapers/%s.py' % scraper.lower()
            # r = cache.get(client.request, 4, scraperLink)

            # if len(r)>1:
                # with open(scraperFile,'r') as f: compfile = f.read()
                # if 'import' in r:
                    # if compfile == r: 
                        # log_utils.log('%s checked and up to date!' % scraper.title(), log_utils.LOGNOTICE)
                        # pass
                    # else:
                        # with open(scraperFile,'w') as f: f.write(r)
                        # icon = xbmc.translatePath(os.path.join('special://home/addons/script.adultflix.artwork', 'resources/art/%s/icon.png' % scraper.lower()))
                        # log_utils.log('%s updated!' % scraper.title(), log_utils.LOGNOTICE)
                        # kodi.notify(msg='%s Updated.' % scraper.title(), duration=1250, sound=True, icon_path=icon)
    # except Exception as e:
        # log_utils.log('Error checking for scraper update %s :: Error: %s' % (scraper.title(),str(e)), xbmc.LOGERROR)