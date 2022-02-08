# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        sfp_ping
# Purpose:     SpiderFoot plug-in for creating new modules.
#
# Author:      Jullien Madera Zuñiga 
# Based on the template: Daniel Garcia Baameiro <dagaba13@gmail.com>
#
# Created:     07/02/2022
# Copyright:   (c) Jullien Madera Zuñiga 2022
# Licence:     GPL
# -------------------------------------------------------------------------------

import subprocess
from spiderfoot import SpiderFootEvent, SpiderFootPlugin


class sfp_ping(SpiderFootPlugin):

    meta = {
        'name': "Ping and TTL",
        'summary': "Traduce la Ip desde el Dominio y su TTL",
        'flags': [""],
        'useCases': ["Custom"],
        'categories': ["Passive DNS"]
    }

    # Default options
    opts = {
    }

    # Option descriptions
    optdescs = {
    }

    results = None

    def setup(self, sfc, userOpts=dict()):
        self.sf = sfc
        self.results = self.tempStorage()

        for opt in list(userOpts.keys()):
            self.opts[opt] = userOpts[opt]

    # What events is this module interested in for input
    # Datos de entrada
    def watchedEvents(self):
        #return ["INTERNET_NAME"]
        return ["DOMAIN_NAME"]

    # What events this module produces
    # This is to support the end user in selecting modules based on events
    # produced.

    # Datos de Salida
    def producedEvents(self):
        return ["IP_ADDRESS"]
        #return ["DOMAIN_NAME"]

    # Handle events sent to this module
    def handleEvent(self, event):
        eventName = event.eventType
        srcModuleName = event.module
        eventData = event.data

        if eventData in self.results:
            return

        self.results[eventData] = True

        self.sf.debug(f"Received event, {eventName}, from {srcModuleName}")

        try:
            self.sf.debug(f"We use the data: {eventData}")
            print(f"We use the data: {eventData}")

            ########################
            # Insert here the code #
            ########################
           
            results = subprocess.run(["ping","-c","1", eventData], stdout=subprocess.PIPE)
            ip = results.stdout.decode('utf-8').split(' ')
            resultado = "Ip " + ip[2].replace('(','').replace(')','')
            resultado2 = ip[12].replace('(','').replace(')','')
            if resultado2 >= "117":
                ttl = "Es un Servidor Windows"
            elif resultado2 <= "65":
                ttl = "Es un Servidor Linux"
            
        except Exception as e:
            self.sf.error("Unable to perform the <ACTION MODULE> on " + eventData + ": " + str(e))
            return
        
        typ = "IP_ADDRESS"
        data = resultado
        data2 = ttl

        evt = SpiderFootEvent(typ, data, self.__name__, event)
        self.notifyListeners(evt)

        evt = SpiderFootEvent(typ, data2, self.__name__, event)
        self.notifyListeners(evt)


# End of sfp_new_module class