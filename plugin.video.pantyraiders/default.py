import xbmcplugin, xbmc, xbmcaddon, urllib, xbmcgui, traceback, requests, re, os, base64 , liveresolver 
from lib import process
from BeautifulSoup import BeautifulSoup
import os, shutil, xbmcgui
addon_id = 'plugin.video.pantyraiders'
addons = xbmc.translatePath('special://home/addons/')
ADDON = xbmcaddon.Addon(id=addon_id)
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.pantyraiders/')
ICON = ADDON_PATH + 'icon.png'
FANART = ADDON_PATH + 'fanart.jpg'
ADDON = xbmcaddon.Addon(id=addon_id)

def Main_Menu():
	process.Menu('XVideos','',700,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg',FANART,'','')
	process.Menu('PornHub','',708,'http://cdimage.debian.org/mirror/addons.superrepo.org/v7/addons/plugin.video.pornhub/icon.png',FANART,'','')
	# process.Menu('XHamster','',714,'http://www.logospike.com/wp-content/uploads/2016/05/Xhamster_Logo_03.png',FANART,'','')
	process.Menu('Chaturbate','',720,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png',FANART,'','')
	process.Menu('YouPorn','',723,'http://pool.img.aptoide.com/rico-heat/e83b919fd9245aa2b31457929bb73f08_icon.png',FANART,'','')
	process.Menu('RedTube','',730,'https://i2.wp.com/now24.gr/wp-content/uploads/2013/12/redtube-icon.png',FANART,'','')
	process.Menu('Tube 8','',738,'https://i.imgur.com/PMIMLrE.jpg',FANART,'','')
	process.Menu('Thumbzilla','',745,'https://bi.phncdn.com/www-static/thumbzilla/images/pc/logo.png?cache=2018031523',FANART,'','')
	# process.Menu('XTube','',753,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg',FANART,'','')
	process.Menu('Eporner','',760,'https://i.imgur.com/cZ0oEj2.jpg',FANART,'','')
	process.Menu('YouJizz','',771,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png',FANART,'','')
	# process.Menu('SpankWire','',772,'https://pbs.twimg.com/profile_images/665600820419952640/POpDwoka_400x400.png',FANART,'','')
	process.Menu('Best Porn Collection','',100,'https://i.imgur.com/Rb3AZGF.png',FANART,'','')
	process.Menu('XNXX','',107,'https://i.imgur.com/vQmrXsw.png',FANART,'','')
	# process.Menu('PlusOne8','',118,'https://i.imgur.com/NfUL3zz.png',FANART,'','')
	process.Menu('PornDig','',1000,'https://assets.porndig.com/assets/porndig/img/logo/logo_1.png?ver=1484644435',FANART,'','')
	process.Menu('Porn 300','',1007,'https://www.porn300.com/android-icon-192x192.png',FANART,'','')
	process.Menu('PervClips','',1014,'https://pervclips.com/tube/images/favicon-152.png',FANART,'','')
	process.Menu('Watch My GF','',1019,'https://www.watchmygf.me/images/logo.png',FANART,'','')
	
 

def get_params():
		param=[]
		paramstring=sys.argv[2]
		if len(paramstring)>=2:
				params=sys.argv[2]
				cleanedparams=params.replace('?','')
				if (params[len(params)-1]=='/'):
						params=params[0:len(params)-2]
				pairsofparams=cleanedparams.split('&')
				param={}
				for i in range(len(pairsofparams)):
						splitparams={}
						splitparams=pairsofparams[i].split('=')
						if (len(splitparams))==2:
								param[splitparams[0]]=splitparams[1]

		return param

params=get_params()
title=None
show_year=None
season=None
episode=None
url=None
name=None
iconimage=None
mode=None
description=None
extra=None
fanart=None
fav_mode=None
regexs=None
playlist=None

try:
	title=urllib.unquote_plus(params["title"])
except:
	pass
try:
	show_year=urllib.unquote_plus(params["show_year"])
except:
	pass
try:
	season=urllib.unquote_plus(params["season"])
except:
	pass
try:
	episode=urllib.unquote_plus(params["episode"])
except:
	pass
try:
	regexs=params["regexs"]
except:
	pass

try:
	fav_mode=int(params["fav_mode"])
except:
	pass
try:
	extra=urllib.unquote_plus(params["extra"])
except:
	pass
try:
		url=urllib.unquote_plus(params["url"])
except:
		pass
try:
		name=urllib.unquote_plus(params["name"])
except:
		pass
try:
		iconimage=urllib.unquote_plus(params["iconimage"])
except:
		pass
try:
		mode=int(params["mode"])
except:
		pass
try:
		fanart=urllib.unquote_plus(params["fanart"])
except:
		pass
try:
		description=urllib.unquote_plus(params["description"])
except:
		pass
try:
	playitem=urllib.unquote_plus(params["playitem"])
except:
	pass
try:
	playlist=eval(urllib.unquote_plus(params["playlist"]).replace('||',','))
except:
	pass
try:
	regexs=params["regexs"]
except:
	pass

if mode == None: Main_Menu()
elif mode == 699: from lib import xxx_vids;xxx_vids.Xbest_videos(url)
elif mode == 700: from lib import xxx_vids;xxx_vids.X_vid_Menu()
elif mode == 701: from lib import xxx_vids;xxx_vids.XNew_Videos(url)
elif mode == 702: from lib import xxx_vids;xxx_vids.XGenres(url)
elif mode == 703: from lib import xxx_vids;xxx_vids.XPornstars(url)
elif mode == 704: from lib import xxx_vids;xxx_vids.XSearch_X()
elif mode == 705: from lib import xxx_vids;xxx_vids.Xtags(url)
elif mode == 706: from lib import xxx_vids;xxx_vids.XPlayLink(url)
elif mode == 707: from lib import xxx_vids;xxx_vids.Porn_Menu()
elif mode == 708: from lib import xxx_vids;xxx_vids.Porn_Hub()
elif mode == 709: from lib import xxx_vids;xxx_vids.get_video_item(url)
elif mode == 710: from lib import xxx_vids;xxx_vids.get_cat_item(url)
elif mode == 711: from lib import xxx_vids;xxx_vids.get_pornhub_playlinks(url)
elif mode == 712: from lib import xxx_vids;xxx_vids.get_pornstar(url)
elif mode == 713: from lib import xxx_vids;xxx_vids.search_pornhub()
elif mode == 714: from lib import xxx_vids;xxx_vids.XHamster()
elif mode == 715: from lib import xxx_vids;xxx_vids.hamster_cats(url)
elif mode == 716: from lib import xxx_vids;xxx_vids.get_hamster_vid(url)
elif mode == 717: from lib import xxx_vids;xxx_vids.chaturbate_tags(url)
elif mode == 718: from lib import xxx_vids;xxx_vids.hamster_cats_split(name,url)
elif mode == 719: from lib import xxx_vids;xxx_vids.get_hamster_playlinks(url)
elif mode == 720: from lib import xxx_vids;xxx_vids.chaturbate()
elif mode == 721: from lib import xxx_vids;xxx_vids.chaturbate_videos(url)
elif mode == 722: from lib import xxx_vids;xxx_vids.chaturbate_playlink(url)
elif mode == 723: from lib import xxx_vids;xxx_vids.YouPorn()
elif mode == 724: from lib import xxx_vids;xxx_vids.youporn_new_video(url)
elif mode == 725: from lib import xxx_vids;xxx_vids.youporn_video(url)
elif mode == 726: from lib import xxx_vids;xxx_vids.youporn_collections(url)
elif mode == 727: from lib import xxx_vids;xxx_vids.youporn_categories(url)
elif mode == 728: from lib import xxx_vids;xxx_vids.youporn_playlink(url)
elif mode == 729: from lib import xxx_vids;xxx_vids.search_youporn(url)
elif mode == 730: from lib import xxx_vids;xxx_vids.redtube()
elif mode == 731: from lib import xxx_vids;xxx_vids.redtube_video(url)
elif mode == 732: from lib import xxx_vids;xxx_vids.redtube_playlink(url)
elif mode == 733: from lib import xxx_vids;xxx_vids.redtube_channels(url)
elif mode == 734: from lib import xxx_vids;xxx_vids.redtube_pornstars(url)
elif mode == 735: from lib import xxx_vids;xxx_vids.redtube_collections(url)
elif mode == 736: from lib import xxx_vids;xxx_vids.redtube_cats(url)
elif mode == 737: from lib import xxx_vids;xxx_vids.redtube_search(url)
elif mode == 738: from lib import xxx_vids;xxx_vids.tube8()
elif mode == 739: from lib import xxx_vids;xxx_vids.tube8_videos(url)
elif mode == 740: from lib import xxx_vids;xxx_vids.tube8_playlink(url)
elif mode == 741: from lib import xxx_vids;xxx_vids.tube8_cats(url)
elif mode == 742: from lib import xxx_vids;xxx_vids.tube8_tags(url)
elif mode == 743: from lib import xxx_vids;xxx_vids.tube8_search()
elif mode == 744: from lib import xxx_vids;xxx_vids.tube8_letters(name,url)
elif mode == 745: from lib import xxx_vids;xxx_vids.thumbzilla()
elif mode == 746: from lib import xxx_vids;xxx_vids.thumbzilla_videos(url)
elif mode == 747: from lib import xxx_vids;xxx_vids.thumbzilla_tags(url)
elif mode == 748: from lib import xxx_vids;xxx_vids.thumbzilla_pornstars(url)
elif mode == 749: from lib import xxx_vids;xxx_vids.thumbzilla_cats(url)
elif mode == 750: from lib import xxx_vids;xxx_vids.thumbzilla_search()
elif mode == 751: from lib import xxx_vids;xxx_vids.thumbzilla_tags_letters(name,url)
elif mode == 752: from lib import xxx_vids;xxx_vids.thumbzilla_playlink(url)
elif mode == 753: from lib import xxx_vids;xxx_vids.xtube()
elif mode == 754: from lib import xxx_vids;xxx_vids.xtube_videos(url)
elif mode == 755: from lib import xxx_vids;xxx_vids.xtube_cats(url)
elif mode == 756: from lib import xxx_vids;xxx_vids.xtube_search(url)
elif mode == 757: from lib import xxx_vids;xxx_vids.xtube_playlink(url)
elif mode == 759: from lib import xxx_vids;xxx_vids.eporner_playlink(url)
elif mode == 760: from lib import xxx_vids;xxx_vids.eporner()
elif mode == 761: from lib import xxx_vids;xxx_vids.eporner_video(url)
elif mode == 762: from lib import xxx_vids;xxx_vids.eporner_pornstar(url)
elif mode == 763: from lib import xxx_vids;xxx_vids.eporner_cats(url)
elif mode == 764: from lib import xxx_vids;xxx_vids.eporner_search()
elif mode == 765: from lib import xxx_vids;xxx_vids.youjizz_videos(url)
elif mode == 766: from lib import xxx_vids;xxx_vids.youjizz_tags(url)
elif mode == 767: from lib import xxx_vids;xxx_vids.youjizz_pornstars(url)
elif mode == 768: from lib import xxx_vids;xxx_vids.youjizz_search()
elif mode == 769: from lib import xxx_vids;xxx_vids.youjizz_playlink(url)
elif mode == 770: from lib import xxx_vids;xxx_vids.youjizz_tags_letters(name,url)
elif mode == 771: from lib import xxx_vids;xxx_vids.youjizz()
elif mode == 772: from lib import xxx_vids;xxx_vids.spank_wire()
elif mode == 773: from lib import xxx_vids;xxx_vids.spank_cats(url)
elif mode == 774: from lib import xxx_vids;xxx_vids.spank_tags(url)
elif mode == 775: from lib import xxx_vids;xxx_vids.spank_videos(url)
elif mode == 776: from lib import xxx_vids;xxx_vids.spank_search()
elif mode == 777: from lib import xxx_vids;xxx_vids.spank_playlink(url)
elif mode == 778: from lib import xxx_vids;xxx_vids.spank_tags_letter(name,url)
elif mode == 906: process.Big_Resolve(name,url)
elif mode == 907: from lib import xxx_vids;xxx_vids.xvid_link(url)
elif mode == 908: from lib import xxx_vids;xxx_vids.play_now(url)
elif mode == 909: from lib import xxx_vids;xxx_vids.xvid_intag(url)
elif mode == 910: from lib import xxx_vids;xxx_vids.redtube_in_channel(url)
elif mode == 911: from lib import xxx_vids;xxx_vids.get_in_star_item(url)
elif mode == 912: from lib import xxx_vids;xxx_vids.pornhub_get_search(url)
elif mode == 100: from lib import xxx_vids;xxx_vids.best_porn_menu()
elif mode == 101: from lib import xxx_vids;xxx_vids.best_porn_vids(url) 
elif mode == 102: from lib import xxx_vids;xxx_vids.best_porn_cat_page(url)
elif mode == 103: from lib import xxx_vids;xxx_vids.best_porn_get_cat(url)
elif mode == 104: from lib import xxx_vids;xxx_vids.best_porn_Search()
elif mode == 105: from lib import xxx_vids;xxx_vids.best_porn_links(url)
elif mode == 106: from lib import xxx_vids;xxx_vids.best_porn_resolve(name,url)
elif mode == 107: from lib import xxx_vids;xxx_vids.XNXX_Menu()
elif mode == 108: from lib import xxx_vids;xxx_vids.XNXX_Vid_Page(url)
elif mode == 109: from lib import xxx_vids;xxx_vids.XNXX_popular(url)
elif mode == 110: from lib import xxx_vids;xxx_vids.xnxx_starz(url)
elif mode == 111: from lib import xxx_vids;xxx_vids.xnxx_instarz(url)
elif mode == 112: from lib import xxx_vids;xxx_vids.xnxx_link(url)
elif mode == 113: from lib import xxx_vids;xxx_vids.xnxx_play_now(url)
elif mode == 114: from lib import xxx_vids;xxx_vids.xnxx_Search()
elif mode == 115: from lib import xxx_vids;xxx_vids.xnxx_search_link(url)
elif mode == 116: from lib import xxx_vids;xxx_vids.xnxx_resolve(url)
elif mode == 117: from lib import xxx_vids;xxx_vids.Plus_one_playlink(url)
elif mode == 118: from lib import xxx_vids;xxx_vids.Plus_one_Menu()
elif mode == 119: from lib import xxx_vids;xxx_vids.Plus_one_vids(url)
elif mode == 120: from lib import xxx_vids;xxx_vids.Plus_one_Search()
elif mode == 121: from lib import xxx_vids;xxx_vids.Plus_one_cats(url)
elif mode == 1000: from lib import xxx_vids;xxx_vids.porndig_menu()
elif mode == 1001: from lib import xxx_vids;xxx_vids.porndig_vids(url)
elif mode == 1002: from lib import xxx_vids;xxx_vids.porndig_playlink(url)
elif mode == 1003: from lib import xxx_vids;xxx_vids.porndig_studios(url)
elif mode == 1004: from lib import xxx_vids;xxx_vids.porndig_4k_menu()
elif mode == 2000: from lib import xxx_vids;xxx_vids.porndig_4k_vids(url)

elif mode == 1005: from lib import xxx_vids;xxx_vids.porndig_starz(url)
elif mode == 1006: from lib import xxx_vids;xxx_vids.Porndig_Search()
elif mode == 1007: from lib.sites import porn300;porn300.porn_300_menu()
elif mode == 1008: from lib.sites import porn300;porn300.porn300_playlinks(url)
elif mode == 1009: from lib.sites import porn300;porn300.porn300_vids(url)
elif mode == 1010: from lib.sites import porn300;porn300.porn300_cats(url)
elif mode == 1011: from lib.sites import porn300;porn300.porn300_search()
elif mode == 1012: from lib.sites import porn300;porn300.porn300_starz(url)
elif mode == 1013: from lib.sites import porn300;porn300.porn300_channels(url)
elif mode == 1014: from lib.sites import pervclips;pervclips.perv_clips_menu()
elif mode == 1015: from lib.sites import pervclips;pervclips.pervclips_vids(url)
elif mode == 1016: from lib.sites import pervclips;pervclips.pervclips_playlinks(url)
elif mode == 1017: from lib.sites import pervclips;pervclips.pervclips_cats(url)
elif mode == 1018: from lib.sites import pervclips;pervclips.pervclips_search()
elif mode == 1019: from lib.sites import watchmygf;watchmygf.watchmygf_menu()
elif mode == 1020: from lib.sites import watchmygf;watchmygf.watchmygf_vids(url)
elif mode == 1021: from lib.sites import watchmygf;watchmygf.watchmygf_playlink(url)
elif mode == 1022: from lib.sites import watchmygf;watchmygf.watchmygf_search()
elif mode == 1023: from lib.sites import watchmygf;watchmygf.watchmygf_cats(url)




xbmcplugin.endOfDirectory(int(sys.argv[1]))
