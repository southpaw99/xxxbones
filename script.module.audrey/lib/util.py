import urllib, urllib2, ssl, sys, requests, re, os, json, ast
import xbmc, xbmcplugin, xbmcgui, xbmcaddon, xbmcvfs
from collections import OrderedDict
  
sysarg=str(sys.argv[1])
  
headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
           'Accept': '*/*',
           'Connection': 'keep-alive'}

addon=xbmcaddon.Addon()

profileDir = addon.getAddonInfo('profile')
profileDir = xbmc.translatePath(profileDir).decode("utf-8")

if not os.path.exists(profileDir):
    os.makedirs(profileDir) 
           
def get(path, args={}):
    #logError(path)
    r = requests.get(path, data=args, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}, verify=False)
    #logError(r.text)
    return r.text
 
def parseParameters(inputString=sys.argv[2]):
    """Parses a parameter string starting at the first ? found in inputString
    
    Argument:
    inputString: the string to be parsed, sys.argv[2] by default
    
    Returns a dictionary with parameter names as keys and parameter values as values
    """
    
    parameters = {}
    p1 = inputString.find('?')
    if p1 >= 0:
        splitParameters = inputString[p1 + 1:].split('&')
        for nameValuePair in splitParameters:
            try:
                if (len(nameValuePair) > 0):
                    pair = nameValuePair.split('=')
                    key = pair[0]
                    value = urllib.unquote(urllib.unquote_plus(pair[1])).decode('utf-8')
                    parameters[key] = value
            except:
                pass
    return parameters
    
def extractAll(text, startText, endText):
    result = []
    start = 0
    pos = text.find(startText, start)
    while pos != -1:
        start = pos + startText.__len__()
        end = text.find(endText, start)
        result.append(text[start:end].replace('\n', '').replace('\t', '').lstrip())
        pos = text.find(startText, end)
    return result

def extract(text, startText, endText):
    start = text.find(startText, 0)
    if start != -1:
        start = start + startText.__len__()
        end = text.find(endText, start + 1)
        if end != -1:
            return text[start:end]
    return None  
    
def getURL(url, header=headers, error=True):
    response=""
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib2.Request(url, headers=header)
            
        response = urllib2.urlopen(req, context=ctx)
    except:
        try:
            req = urllib2.Request(url, headers=header)
            
            response = urllib2.urlopen(req, timeout=int(xbmcaddon.Addon().getSetting("timeout")))
        except:
           pass
    
    if response and response.getcode() == 200:
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO.StringIO( response.read())
            gzip_f = gzip.GzipFile(fileobj=buf)
            content = gzip_f.read()
        else:
            content = response.read()
        content = content.decode('utf-8', 'ignore')
        return content
    else:
        if error:
            try:
                xbmc.log('Error Loading URL : '+str(response.getcode()), xbmc.LOGERROR)
            except:
                print 'Error Loading URL : '+url
    return False
    
def logError(error):
    try:
        xbmc.log(str(error.encode("utf-8")), xbmc.LOGERROR)
    except:
        print str(error)

def alert(alertText):
    try:
        dialog = xbmcgui.Dialog()
        ret = dialog.ok(addon.getAddonInfo('name'), alertText)
    except:
        print alertText
        
def progressStart(title, status):
    pDialog = xbmcgui.DialogProgress()
    pDialog.create(title, status)
    xbmc.executebuiltin( "Dialog.Close(busydialog)" )
    progressUpdate(pDialog, 1, status)
    return pDialog

def progressStop(pDialog):
    pDialog.close
    
def progressCancelled(pDialog):
    if pDialog.iscanceled():
        pDialog.close
        return True
    return False

def progressUpdate(pDialog, progress, status):
    pDialog.update(int(progress), status)

def searchDialog(searchText="Please enter search text") :    
    keyb=xbmc.Keyboard('', searchText)
    keyb.doModal()
    searchText=''
    
    if (keyb.isConfirmed()) :
        searchText = keyb.getText()
    if searchText!='':
        return searchText.replace(" ", "%20")
    return False

def playMedia(title, thumbnail, link, mediaType='Video', library=True, title2="", force=False) :
    li = xbmcgui.ListItem(label=title2, iconImage=thumbnail, thumbnailImage=thumbnail, path=link)
    li.setInfo( "video", { "Title" : title } )
    
    #if not force:
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
    #else:
    #   xbmc.Player().play(item=link, listitem=li)

def notify(message, reportError=False, timeShown=5000):
    """Displays a notification to the user
    
    Parameters:
    addonId: the current addon id
    message: the message to be shown
    timeShown: the length of time for which the notification will be shown, in milliseconds, 5 seconds by default
    """
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (addon.getAddonInfo('name'), message, timeShown, addon.getAddonInfo('icon')))
    if reportError:
        logError(message)

        
def addMenuItems(details):
    changed=False
    for detail in details:
        try:
            detail['title']=detail['title'].encode('utf-8')
        except:
            detail['title']=detail['title'].decode('utf-8')
        try:
            u=sys.argv[0]+"?url="+detail['url']+"&mode="+str(detail['mode'])+"&name="+urllib.quote_plus(detail['title'].encode("utf-8"))+"&icon="+detail['icon']
            liz=xbmcgui.ListItem(detail['title'].encode("utf-8"), iconImage=detail['icon'], thumbnailImage=detail['icon'])
            liz.setInfo(type='video', infoLabels={ "Title": detail['title'].encode("utf-8"),"Plot": detail['plot']} )
        except:
            u=sys.argv[0]+"?url="+detail['url']+"&mode="+str(detail['mode'])+"&name="+urllib.quote_plus(detail['title']).decode("utf-8")+"&icon="+detail['icon']
            liz=xbmcgui.ListItem(detail['title'].decode("utf-8"), iconImage=detail['icon'], thumbnailImage=detail['icon'])
            liz.setInfo(type='video', infoLabels={ "Title": detail['title'].decode("utf-8"),"Plot": detail['plot']} )
            
        try:
            liz.setProperty("Fanart_Image", detail['fanart'])
            u=u+"&fanart="+detail['fanart']
        except:
            pass
        try:
            liz.setProperty("Landscape_Image", detail['landscape'])
            u=u+"&landscape="+detail['landscape']
        except:
            pass
        try:
            liz.setProperty("Poster_Image", detail['poster'])
            u=u+"&poster="+detail['poster']
        except:
            pass
        try:
            u=u+"&extras="+str(detail["extras"])
        except:
            pass
            
        if 'isPlayable' in detail:
            liz.setProperty('IsPlayable', 'true')
        
        """
        *** download code, think about fixing and readding ***
        if detail['mode']=="111" and xbmcaddon.Addon().getSetting('folder'):
            download = (sys.argv[0] +
                "?url=" + detail['url'] +
                "&mode=" + "112" +
                "&poster="+detail['poster']+
                "&fanart="+detail['fanart']+
                "&name=" + urllib.quote_plus(detail['title'].replace("\t", "").replace("\r", "").replace("\t", "").encode('utf-8'))+
                "&extras="+ urllib.quote_plus(str(detail["extras"]))
            )
            liz.addContextMenuItems([('Download', 'xbmc.RunPlugin('+download+')')])"""
        if detail['isFolder']:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    xbmcplugin.setContent(int(sysarg), 'movies')
    xbmcplugin.endOfDirectory(int(sysarg))

def getFile(feed="", type=""):
    if feed=="" and type=="":
        if xbmcaddon.Addon().getSetting('type')=="0":
            type = "file"
            feed = xbmcaddon.Addon().getSetting('file')
        elif xbmcaddon.Addon().getSetting('type')=="1":
            type = "url"
            feed = xbmcaddon.Addon().getSetting('url')
    
    if feed=="":
        dialog = xbmcgui.Dialog()
        dialog.textviewer('Welcome to Audrey', 'Audrey is a new type of Kodi Addon, giving you the ability to write simple JSON files that will allow it to scrape content from websites.\n\nTutorials on how to create these JSON feeds coming soon, you can also load some feeds in from the next screen.')
        if xbmcgui.Dialog().yesno("No JSON file found","Do you want to load the demo JSON file?", "Alternatively you can find instructions on creating your own JSON file at http://ptom.co.uk/audrey]http://ptom.co.uk/audrey"):
            home=xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))
            xbmcaddon.Addon().setSetting('type', '0')
            xbmcaddon.Addon().setSetting('file', os.path.join(home, "resources", "sites.json"))
            type="file"
            feed=os.path.join(home, "resources", "sites.json")
        else:
            sys.exit()
    try:
        if type=="file":
            if feed:
                content = open(feed)
        elif type=="url":
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')]
            resp=opener.open(feed)
            content = resp
        bits = json.load(content, object_pairs_hook=OrderedDict)
        return bits
    except Exception as e:
        notify("Error loading JSON file")
        logError("Error : "+str(e))
        sys.exit()
        
def prepare(string):
    #logError(string.replace("?", "\?").replace("{*}", "[\s\S]*?").replace("{%}", "([\s\S]*?)"))
    return string.replace("?", "\?").replace("{*}", "[\s\S]*?").replace("{%}", "([\s\S]*?)")

def replaceParts(string, match):
    for x in range(0, len(match)):
        try:
            string=string.replace("{%"+str(x+1)+"}", match[x])
        except:
            string=string.replace("{%"+str(x+1)+"}", str(match[x]))
    string = execPy(string)
    return string

def execPy(string):
    #logError(string)
    if "{{" and "}}" in string:
        string = string.replace("{{", "").replace("}}", "")
        logError(string)
        with stdoutIO() as s:
            exec(string)
        #logError(s.getvalue().replace("\n", "").replace("\r", ""))
        return s.getvalue().replace("\n", "").replace("\r", "")
    else:
        return string
        
import sys
import StringIO
import contextlib

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
        
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()