#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# File: pylaServer.py
# Copyright (c) 2011 by None
#
# GNU General Public Licence (GPL)
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
__author__    = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'plaintext'
__date__      = '26/01/2011'

import sys, socket, os
from tempfile import NamedTemporaryFile
from subprocess import Popen, PIPE

def faxServer(host, port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind((host,port))
    buf = 4096
    sock.listen(1)
    try:
        while 1:
            conn, addr = sock.accept()
            tempFile = NamedTemporaryFile(delete=False)
            while conn:
                data,addr = conn.recvfrom(buf)
                if not data:
                    break
                else:
                    tempFile.write(data)
            tempFile.close()
            printToPyla(tempFile.name)
            conn.close()
    except:
        sock.close()
        print 'The server exited'
        return False
         
def printToPyla(fileName):
    pyla = os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))),'pyla.py')
    text = file(fileName,'rb').read()
    os.remove(fileName)
    python = Popen(['which', 'python'], stdout=PIPE).stdout.read().strip()
    Pyla = Popen([python, pyla,'-i'], stdin=PIPE)
    Pyla.communicate(text)
    Pyla.wait()
    
def createPrinter(name, port):
    cmd = ['lpadmin', '-p', name, '-E', '-v', 'socket://localhost:'+str(port)]
    create = Popen(cmd)
    create.wait()    

def deletePrinter(name):
    cmd = ['lpadmin', '-x', name]
    delete = Popen(cmd)
    delete.wait()    
    
if __name__ == "__main__":
    host = 'localhost'
    port = 50007
    printerName = 'Fax-Server'
    createPrinter(printerName, port)
    faxServer(host, port)
    deletePrinter(printerName)
