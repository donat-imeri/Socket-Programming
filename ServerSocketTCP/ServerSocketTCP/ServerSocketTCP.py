import socket
import sys
from _thread import *
import random
import datetime
import os

#Definimi i metodave

def ipaddr(adresa):
    return adresa[0]

def portnr(adresa):
    return adresa[1]

def hostname(hosti):
    try:
        return socket.gethostbyaddr(hosti)[0]
    except Exception:
        return "Emri i hostit nuk u gjet!"

def timenow():
    time=datetime.datetime.now()           
    return time.strftime("%d-%m-%Y %I:%M:%S %p")

def zanore(fjalia):
    listaZanoreve = ['A', 'E', 'Ë', 'I', 'O','U','Y']
    fjalia=fjalia.upper()
    counter=0
    for shkronja in fjalia:
        if(shkronja in listaZanoreve ):
            counter=counter+1
    return counter

def printo(fjalia):
    fjalia=(str(fjalia)).strip()
    return fjalia

def loja():
    listaNumrave=""
    for number in range(0,20): 
        numriRandom=random.randint(1,99)
        listaNumrave+=str(numriRandom)
        if number!=19:
            listaNumrave+=", "
    return listaNumrave

def fibonacci(numri):
    if numri==0: return 0
    elif(numri>0):
         ipari=1
         idyti=1
         fibonacci=1
         for numeruesi in range(2,numri):
                fibonacci = ipari + idyti;
                ipari = idyti;
                idyti = fibonacci;
         return fibonacci
    else:
         return "Gabim"

def konverto(opsioni, vlera):
    if opsioni=="CelsiusToKelvin":
        rezultati=vlera+273

    elif opsioni=="KelvinToCelsius":
        rezultati=vlera-273 

    elif opsioni=="CelsiusToFahrenheit":
        rezultati = 9.0/5.0 * vlera + 32 

    elif opsioni=="FahrenheitToCelsius":
        rezultati = (vlera - 32) * 5.0/9.0 

    elif opsioni=="KelvinToFahrenheit":
         rezultati = ((9.0/5.0)*(vlera-273)) + 32 
     
    elif opsioni=="FahrenheitToKelvin":
         rezultati = (5.0/ 9.0)*(vlera-32)+273

    elif opsioni=="PoundToKilogram":
         rezultati = vlera * 0.453592

    elif opsioni=="KilogramToPound":
        rezultati = vlera/0.453592
    else:
        rezultati="Gabim"
    return rezultati

def caesar(fjalia,opsioni):
    fjalia=fjalia.upper()
    if(opsioni=="Enkripto"):
        tekstiEnkrpituar=""
        for shkronja in fjalia:
            if(shkronja.isalpha()):
                tekstiEnkrpituar+=str(chr(((ord(shkronja)-65+3)%26)+65))
            else:
                tekstiEnkrpituar+=shkronja
        return tekstiEnkrpituar
    elif(opsioni=="Dekripto"):
        tekstiDekriptuar=""
        for shkronja in fjalia:
            if(shkronja.isalpha()):
                tekstiDekriptuar+=str(chr(((ord(shkronja)-65-3)%26)+65))
            else:
                tekstiDekriptuar+=shkronja
        return tekstiDekriptuar
        
def reverse(fjalia):
    fjaliaReverse=""
    i=len(fjalia)-1
    while(i>=0):
        fjaliaReverse+=fjalia[i]
        i-=1
    return fjaliaReverse
                    

#Krijimi i Socket

host='localhost'
port=11000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try :
    serverSocket.bind((host,port))
except socket.error:
    print("Nuk u arrit te krijohet lidhja")
    sys.exit()

serverSocket.listen(5)


print("FIEK Server\nServeri tani eshte i gatshem per pranimin e kerkesave")

kaNdryshime=False
def clientthread(conn, addr):
    global host
    global port
    global kaNdryshime
    while True:
        try:
            data = conn.recv(128).decode()  
        except socket.error:
            break   

        #Kjo liste perban pjeset e ndryshme te input-it si: opsioni, teksti etj.  
        merrPjeset=str(data).rsplit(" ")  
        #Kjo pjese merr tekstin pas OPSIONIT
        teksti=""
        i=len(merrPjeset)
        for fjala in range(1,i):
            teksti=teksti+merrPjeset[fjala]          
            if(fjala!=i):
                teksti+=" "
        if not data:
            break
        elif(merrPjeset[0]=="IPADDR"):
            data="Adresa e klientit eshte: "+ipaddr(addr)
        elif(merrPjeset[0]=="PORTNR"):
            data="Porti i klientit: "+str(portnr(addr))
        elif(merrPjeset[0]=="ZANORE"):
            data="Numri zanoreve: "+str(zanore(teksti))
        elif(merrPjeset[0]=="PRINTO"):
            data="Teksti i formatizuar: "+str(printo(teksti))
        elif(merrPjeset[0]=="HOST"):
            data="Emri i hostit: "+str(hostname(host))            
        elif(merrPjeset[0]=="TIME"):          
            data="Koha aktuale eshte: "+ timenow()
        elif(merrPjeset[0]=="LOJA"):
            data="Loja ka gjeneruar keta numra: "+loja()
        elif(merrPjeset[0]=="FIBONACCI"):
            try:
                vlera=int(merrPjeset[1])   
                data="Vlera Fibonacci e numrit tuaj eshte: "+str(fibonacci(vlera))             
            except Exception:
                data="Keni shtruar kerkese te gabuar"                                       
        elif(merrPjeset[0]=="KONVERTO"):
            try:
                numri=float(merrPjeset[2]) 
                data="Vlera e konvertuar eshte: "+str(konverto(merrPjeset[1], numri))               
            except Exception:
                data="Keni shtruar kerkese te gabuar"
                   
        elif(merrPjeset[0]=="CEASAR"):
            fjaliaCeasarit=""
            for i in range(2,len(merrPjeset)):
                fjaliaCeasarit+=merrPjeset[i]
                if(fjala!=i):
                    fjaliaCeasarit+=" "
                
            if(merrPjeset[1]=="Enkripto"):
                data="Teksti i enkriptuar me Ceasar: "+caesar(fjaliaCeasarit,"Enkripto")
            elif(merrPjeset[1]=="Dekripto"):
                data="Teksti i dekriptuar me Ceasar: "+caesar(fjaliaCeasarit,"Dekripto")
            else:
                data="Keni shtruar kerkese te gabuar"
        elif(merrPjeset[0]=="REVERSE"):
                data="Fjalia e kthyer mbrapsht: "+reverse(teksti)
        elif(merrPjeset[0]=="NDRYSHO"):         
            if(merrPjeset[1]=="HOST"):
                host=merrPjeset[2]
                kaNdryshime=True
                data="Hosti u nderrua. Ristartoni lidhjen ne hostin e ri"
            elif(merrPjeset[1]=="PORT"):
                try:                
                    port=int(merrPjeset[2])
                    kaNdryshime=True
                except Exception:
                    data="Gabim"                
                data="Porti u nderrua. Ristartoni lidhjen ne portin e ri"
            else:
                data="Gabim"
        else:
            data="Serveri nuk mund ti pergjigjet kesaj kerkese"
        conn.send(data.encode())
    conn.close()


while True:     
    if(kaNdryshime==True):
        serverSocket.close()
        serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serverSocket.bind((host,port))
        serverSocket.listen(5)        
        kaNdryshime=False
    connection, address=serverSocket.accept()
    print("Ne server u konektua:"+str(address))
    start_new_thread(clientthread,(connection, address,)) 
         
serverSocket.close()
