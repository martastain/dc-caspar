#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import telnetlib
from xml.etree import ElementTree as ET


def basefname(fname):
    return os.path.splitext(fname.split("\\")[-1])[0].lower()


class CasparLayer():
    def __init__(self):
        self.cued_file = False
        self.current_file = False

    def __repr__(self):
        return ("CURRENT: %s , CUED: %s" % (self.current_file, self.cued_file))


class CasparChannel():
    def __init__(self, server, id_channel):
        self.server = server
        self.id_channel = id_channel
        self.layers = {}
        self.default_layer = CasparLayer()

    def __getitem__(self, key):
        return self.layers.get(key, self.default_layer)


    def main(self):
        stat, res = self.server.query("INFO %d" % self.id_channel)

        if not stat: 
            return False
        try:    
            xstat = ET.XML(res)
        except: 
            return False
        
        self.layers = {}

        
        try:
            xlayers = xstat.find("stage").find("layers").findall("layer")
        except:
            return


        for xlayer in xlayers:
                id_layer = int(xlayer.find("index").text)
                
                layer = CasparLayer()

                fg_prod = xlayer.find("foreground").find("producer")
                if fg_prod.find("type").text == "image-producer":
                    layer.current_file = basefname(fg_prod.find("location").text)    
                elif fg_prod.find("type").text == "ffmpeg-producer":
                    layer.current_file = basefname(fg_prod.find("filename").text)
                
                try:
                    bg_prod = xlayer.find("background").find("producer").find("destination").find("producer")
                except:
                    pass
                else:
                    if bg_prod.find("type").text == "image-producer":
                        layer.cued_file = basefname(bg_prod.find("location").text)    
                    elif bg_prod.find("type").text == "ffmpeg-producer":
                        layer.cued_file = basefname(bg_prod.find("filename").text)
                        
                self.layers[id_layer] = layer



class CasparServer():
    def __init__(self, host="localhost", port=5250):
        self.host = host
        self.port = port
        self.connect()

        self.channels = {1: CasparChannel(self, 1)}

    def connect(self):
        try:    
            self.cmd_conn = telnetlib.Telnet(self.host,self.port)
            self.inf_conn = telnetlib.Telnet(self.host,self.port)
        except:
            return False
        else:
            return True
     
    def query(self,q):
        if q.startswith("INFO"):
            conn = self.inf_conn
        else:
            print q
            conn = self.cmd_conn
        
        try:
            conn.write("%s\r\n" % q.encode("utf-8"))
            result = conn.read_until("\r\n").strip() 
        except:
            return (False, "Connection failed")
        
        if not result: 
            return (False, "No result")
        
        try:
            if result[0:3] == "202":
                return (True, result)
            elif result[0:3] in ["201","200"]:
                result = conn.read_until("\r\n").strip()
                return (True, result)
            elif int(result[0:1]) > 3:
                return (False, result)
        except:
            return (False, "Malformed result")
        return (False, "Very strange result")


    def __getitem__(self, key):
        return self.channels.get(int(key), False)


    def main(self):
        for id_channel in self.channels:
            self.channels[id_channel].main()