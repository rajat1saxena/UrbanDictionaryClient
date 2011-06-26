#udclient.py
#a very simple client for Urban Dictionary<www.urbandictionary.com>
# Copyright (C) 2011 Rajat Saxena
#
# rajat.saxena.work@gmail.com
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import BeautifulSoup
import pygtk
pygtk.require("2.0")
import gtk
import urllib

class udclient:
    def __init__(self):
        self.filename="./interface.glade"
        self.builder=gtk.Builder()
        self.builder.add_from_file(self.filename)
        
        #getting objects from glade file
        self.win=self.builder.get_object("mainwin")
        self.search=self.builder.get_object("search")
        self.send=self.builder.get_object("send")
        self.scrw=self.builder.get_object("scrw")
        self.result=self.builder.get_object("result")

        #main window's settings
        self.win.set_size_request(400,600)
        self.win.connect("destroy",self.destroy)
        self.win.connect("key-press-event",self.keypressed)

        #enabling wrap mode
        self.result.set_wrap_mode(gtk.WRAP_WORD)

        #connect callbacks
        self.send.connect("clicked",self.respond)

        self.result_buffer=self.result.get_buffer()

        self.win.set_title("Urban Dictionary-Version 1.0")
        self.win.show_all()

    #the callback for main window's destroy event
    def destroy(self,widget):
        gtk.main_quit()

    #the callback for keypress event
    def keypressed(self,widget,event):
        if event.keyval==65293:
            self.respond(self.send)
        
    #the function which activates httpreactor function and formats the result into readable form
    def respond(self,widget):
        self.query=self.search.get_text()
        self.query=self.query.replace(" ","+")
        print(self.query)
        self.response=self.httpreactor(self.query)
        print(self.response)
        self.real_result=""
        count=1
        for each in self.response:
            self.real_result=self.real_result+'\n'+'Definition: '+str(count)+'\n'+'\t'+str(each).replace("&quot;",'"')+'\n'
            count=count+1
        self.result_buffer.set_text(self.real_result)

    #This is the function which will contact Urban Dictionary
    def httpreactor(self,query):
        data=[]
        data_to_server="http://www.urbandictionary.com/define.php?term="+query
        sock=urllib.urlopen(data_to_server)
        data_received=sock.read()
        sock.close()
        soup=BeautifulSoup.BeautifulSoup(data_received)
        for elm in soup.findAll('div',{'class':'definition'}):
            data.append(elm.text)
            #print(elm.text)
        #print(data)
        return data

if __name__=="__main__":
    client=udclient()
    gtk.main()
