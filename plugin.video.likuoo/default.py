import xbmc, xbmcaddon, os, audrey
addon=xbmcaddon.Addon()
home=xbmc.translatePath(addon.getAddonInfo("path"))
audrey.feedme(os.path.join(home, "sites.json"), "file")