# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 13:25:27 2022

@author: Tshegofatso Mohlala
"""

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self, data):
        HTMLParser.__init__(self)
        self.starttags = []
        self.endtags = []
        self.data = data
        self.data_list = data.split('\n')
        
    def handle_starttag(self, tag, attrs):
        (line, column) = self.getpos()
        length = 0
        i = 0
        while i<line-1:
            length += len(self.data_list[i])
            i += 1
            
        try:
            if self.data_list[line-1][column+len(tag)+1]=='>' or self.data_list[line-1][column+len(tag)+2]=='>':
                self.starttags.append(length+column)
        except:
            pass

    def handle_endtag(self, tag):
        (line, column) = self.getpos()
        length = 0
        i = 0
        while i<line-1:
            length += len(self.data_list[i])
            i += 1
        
        if self.data_list[line-1][column]=='/' or self.data_list[line-1][column+1]=='/' or self.data_list[line-1][column+2]=='/':
            self.endtags.append(length+column+len(tag)+4)
        
    def get_tagpos(self):
        return (self.starttags, self.endtags)
    
    def handle_startendtag(self, tag, attrs):
        (line, column) = self.getpos()
        length = 0
        i = 0
        while i<line-1:
            length += len(self.data_list[i])
            i += 1
            
        self.starttags.append(length+column)

def get_js_only(data):
    parser = MyHTMLParser(data)
    parser.feed(data)
    text1 = ""
    text2 = ""
    if parser.get_tagpos()[0]!=[]:
        startpos = parser.get_tagpos()[0][0]
        text1 = data[0:startpos:]
    if parser.get_tagpos()[1]!=[]:
        endpos = parser.get_tagpos()[1][-1]
        text2 = data[endpos::]
    
    if text1+text2:
        return text1+text2
    else:
        return data
