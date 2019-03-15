import util, search as db
import threading, time, json
import xbmc, xbmcplugin, xbmcaddon
import urllib, urllib2, cookielib

client_id="HQWCL2WKYEAM4" #realdebrid clientid

# reset realdebrid, for testing
"""xbmcaddon.Addon().setSetting('rd_id', "")
xbmcaddon.Addon().setSetting('rd_secret', "")
xbmcaddon.Addon().setSetting('rd_access', "")
xbmcaddon.Addon().setSetting('rd_refresh', "")"""

def auth():
    xbmc.executebuiltin('ActivateWindow(10138)')
    authData=util.getURL("https://api.real-debrid.com/oauth/v2/device/code?client_id="+client_id+"&new_credentials=yes")
    authThread=threading.Thread(target=verifyThread, args=(authData,))
    
    authThread.start()
    
def verifyThread(authData):
    xbmc.executebuiltin('Dialog.Close(10138)') 
    # convert string to JSON
    authJSON=json.loads(authData)
    
    # create dialog with progress to show information
    authMsg="To authorise your RealDebrid account, use a browser to browse to [B]"+authJSON['verification_url']+"[/B] and enter the verification code [B]"+authJSON['user_code']+"[/B]"
    authDialog=util.progressStart("RealDebrid Authentication", authMsg)
    
    authorised=False
    timer=0
    credJSON=""
    while not authorised:
        time.sleep(2)
        timer=timer+2
        
        util.progressUpdate(authDialog, timer, authMsg)
        # check if we need to exit
        if util.progressCancelled(authDialog)==True:
            util.progressStop(authDialog)
            break
        if timer==100:
            util.progressStop(authDialog)
            util.alert("RealDebrid aithentication has timed out. Please try again.")
            break
            
        # all good to carry on lets check auth
        credentials=util.getURL("https://api.real-debrid.com/oauth/v2/device/credentials?client_id="+client_id+"&code="+authJSON['device_code'])
        
        if credentials!=False:
            try:
                if "error" in credentials:
                    util.logError(credentials)
                else:
                    credJSON=json.loads(credentials)
                    #store credentials in settings
                    xbmcaddon.Addon().setSetting('rd_id', credJSON['client_id'])
                    xbmcaddon.Addon().setSetting('rd_secret', credJSON['client_secret'])
                    
                    cj_rd = cookielib.CookieJar()
                    opener_rd = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj_rd))
                    
                    data_rd = urllib.urlencode({'client_id' : credJSON['client_id'], 'client_secret' : credJSON['client_secret'], 'code': authJSON['device_code'], 'grant_type' : 'http://oauth.net/grant_type/device/1.0'})
                    
                    try:
                        #util.logError(str(data_rd))
                    
                        resp = opener_rd.open('https://api.real-debrid.com/oauth/v2/token', data_rd)
                        content=resp.read()
                        
                        credJSON=json.loads(content)
                        
                        xbmcaddon.Addon().setSetting('rd_access', credJSON['access_token'])
                        xbmcaddon.Addon().setSetting('rd_refresh', credJSON['refresh_token'])
                            
                        authorised=True
                    except Exception as e:
                        util.logError(str(e))
            except Exception as e:
                util.logError(str(e))
    # check how we exited loop
    util.progressStop(authDialog)
    if authorised==True:
        util.alert("RealDebrid authenticated.")
    else:
        util.alert("There was an error authenticating with RealDebrid")

def refreshToken():
    cj_rd = cookielib.CookieJar()
    opener_rd = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj_rd))
    data_rd = urllib.urlencode({'client_id' : xbmcaddon.Addon().getSetting('rd_id'), 'client_secret' : xbmcaddon.Addon().getSetting('rd_secret'), 'code': xbmcaddon.Addon().getSetting('rd_refresh'), 'grant_type' : 'http://oauth.net/grant_type/device/1.0'})
    
    try:
        util.logError("starting refresh")
        resp = opener_rd.open('https://api.real-debrid.com/oauth/v2/token', data_rd)
        content=resp.read()
        util.logError("refresh complete")
        
        credJSON=json.loads(content)
        
        xbmcaddon.Addon().setSetting('rd_access', credJSON['access_token'])
        xbmcaddon.Addon().setSetting('rd_refresh', credJSON['refresh_token'])
        
        util.logError("write complete: "+str(credJSON))
        util.logError("checking values"+xbmcaddon.Addon().getSetting('rd_access')+" "+xbmcaddon.Addon().getSetting('rd_refresh'))
        
        authorised=True
    except Exception as e:
        util.logError("Error Refreshing Token: "+str(e))

def hostStatus():
    from collections import OrderedDict
    
    cj_rd = cookielib.CookieJar()
    opener_rd = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj_rd))
    opener_rd.addheaders=[("Authorization", "Bearer "+str(xbmcaddon.Addon().getSetting('rd_access')))]

    error=True
    attempts=0
    
    while error:
        try:
            resp = opener_rd.open('https://api.real-debrid.com/rest/1.0/hosts/status')
            content=resp.read()
            
            credJSON=json.loads(content, object_pairs_hook=OrderedDict)
            util.logError(credJSON)
            return credJSON
        except Exception as e:
            e=str(e)
            util.logError("hoststaus error: "+e)
            attempts=attempts+1
            if attempts>3:
                error=True
                break
            elif "Unauthorized" in e:
                refreshToken()
        
def unrestrict(link):
    cj_rd = cookielib.CookieJar()
    opener_rd = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj_rd))
    opener_rd.addheaders=[("Authorization", "Bearer "+str(xbmcaddon.Addon().getSetting('rd_access')))]

    data_rd = urllib.urlencode({'link' : link})

    error=True
    attempts=0
    while error:
        try:
            util.logError(str(data_rd))

            resp = opener_rd.open('https://api.real-debrid.com/rest/1.0/unrestrict/link', data_rd)
            content=resp.read()
            
            credJSON=json.loads(content)
            util.logError(credJSON)
            error=True
            return credJSON['download']
        except Exception as e:
            util.logError("realdebrid error: "+str(e))
            attempts=attempts+1
            if attempts>3:
                error=True
                break
            elif "Unauthorized" in e:
                refreshToken()
                