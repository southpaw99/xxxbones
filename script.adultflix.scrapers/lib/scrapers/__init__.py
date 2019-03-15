from kodi_six import xbmc
import os.path
from packlib import log_utils, kodi
files = os.listdir(os.path.dirname(__file__))
__all__ = [filename[:-3] for filename in files if not filename.startswith('__') and filename.endswith('.py')]


def sources():

    import pkgutil
    import os.path

    __all__ = [x for x in os.walk(os.path.dirname(__file__))][0]

    kodi.notify(msg=str(__all__))

    try:
        sourceDict = []
        for i in __all__:
            log_utils.log('{0}'.format(i), xbmc.LOGDEBUG)

            for loader, module_name, is_pkg in pkgutil.walk_packages([i]):
                if is_pkg:
                    continue

                try:
                    module = loader.find_module(module_name).load_module(module_name)
                    sourceDict.append((module_name, module.source()))
                except Exception as e:
                    log_utils.log('Could not load "%s": %s' % (module_name, e), xbmc.LOGDEBUG)
        return sourceDict
    except:
        return []