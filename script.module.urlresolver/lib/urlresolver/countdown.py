'''
Countdown XBMC 0.3
Copyleft Anarchintosh

Set a countdown dialog with a progress bar for XBMC.
Necessary for some filehosters eg. megaupload
'''

import xbmc, xbmcgui

def countdown( time_to_wait, title='', text='' ):

    time_to_wait = int(time_to_wait)
    
    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create(title)

    print 'waiting '+str(time_to_wait)+' secs'
    
    secs=0
    percent=0
    increment = 100 / time_to_wait

    cancelled = False
    while secs <= time_to_wait:

        percent = increment * secs

        secs_left = str((time_to_wait - secs))

        if secs != 0: xbmc.sleep(1000)

        if secs_left == '0': percent = 100
        
        remaining_display = ' Wait '+secs_left+' seconds for the video stream to activate...'
        pDialog.update(percent,' '+text,remaining_display)
        
        if (pDialog.iscanceled()):
             cancelled = True
             break

        secs += 1

    if cancelled == True:     
         print 'wait cancelled'
         return False
    else:
         print 'done waiting'
         return True
