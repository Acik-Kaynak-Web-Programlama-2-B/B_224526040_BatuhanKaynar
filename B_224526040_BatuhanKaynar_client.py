# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 13:53:44 2023

@author: C-117
"""

from socket import *
from threading import *
from tkinter import *
from tkinter import filedialog


client = socket(AF_INET, SOCK_STREAM)

ip = '10.100.5.103'
port = 6666

client.connect((ip,port))

pencere = Tk()
pencere.title("Bağlandı : "   +ip      +" "      + str(port))

message = Text(pencere, width=50)
message.grid(row=0,column=0, 
             padx=10, pady=10)

mesaj_giris= Entry(pencere, width=50)
mesaj_giris.insert(0, "Adınız")

mesaj_giris.grid(row=1, column=0, 
                 padx=10, pady=10)
mesaj_giris.focus()
mesaj_giris.selection_range(0, END)

def mesaj_gonder():
    istemci_mesaji = mesaj_giris.get()
    message.insert(END, '\n' + 'Sen :'
                   + istemci_mesaji)
    client.send(istemci_mesaji.encode('utf8'))
    mesaj_giris.delete(0, END)

btn_msg_gonder = Button(pencere, text='Gönder',
                        width=10, 
                        command=mesaj_gonder)
btn_msg_gonder.grid(row=1, column=1, 
                    padx=5, pady=10)


def sendFile():
    file_path = filedialog.askopenfilename()  
    if file_path:  
        with open(file_path, "rb") as file:
            file_data = file.read()
            client.sendall(file_data) 
            messages.insert(END, '\nDosya gönderildi: ' + file_path)

bsendFile = Button(pencere, text="Gözat", width=10, command=sendFile)
bsendFile.grid(row=2, column=1, padx=5, pady=10)

def onEnter(event):
    mesaj_gonder()
   
mesaj_giris.bind("<Return>", onEnter)
    

def gelen_mesaj_kontrol():
    while True:
        server_msg=client.recv(1024).decode('utf8') 
        message.insert(END, '\n'+ server_msg)

recv_kontrol = Thread(target=gelen_mesaj_kontrol)
recv_kontrol.daemon = True
recv_kontrol.start()
pencere.mainloop()
