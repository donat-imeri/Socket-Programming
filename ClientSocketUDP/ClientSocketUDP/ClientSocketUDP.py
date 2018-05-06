import socket
import sys

print("FIEK Klient")

host=input("Hosti: ")
try:
    port=int(input("Porti: "))
except Exception:
    sys.exit("Gabim")

socketClient = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

print("Perdorni komanden h ose H per te shfaqur ndihmen")
message=input("Shkruani komanden tuaj >>> ")
while(message!='Q' and (message !="")):   
    if(message=='h' or message=='H'):
        print("Opsionet qe mund ti shfrytezoni jane: \nIPADDR\nPORTNR\nHOST\nZANORE [Teksti]\nPRINTO [Teksti]\nHOST\nTIME\nLOJA\nFIBONACCI [Numri]\nKONVERTO [Opsioni] [Vlera]\nCAESAR [Opsioni] [Teksti]\nREVERSE [Teksti]\nNDRYSHO [Opsioni] [Vlera]\n")
        message=input("Shkruani komanden tuaj >>> ")
    else:
        socketClient.sendto(message.encode(),(host,port))                
        data=socketClient.recv(128).decode()
        print(data)
        if(data=="Porti u nderrua" or data=="Hosti u nderrua"):
            print("Ristartoni aplikacionin")
            break
        else:
            message=input("Shkruani komanden tuaj >>> ")

socketClient.close();
