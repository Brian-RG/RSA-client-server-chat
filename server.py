import socket
from _thread import start_new_thread as s
from threading import Thread
from multiprocessing import Process
import threading
from random import randint as r
from random import choice

def eratosthenes2(n):
    multiples = set()
    for i in range(2, n+1):
        if i not in multiples:
            yield i
            multiples.update(range(i*i, n+1, i))
##eratosthenes2 code taken from https://stackoverflow.com/questions/33395903/efficient-method-for-generating-lists-of-large-prime-numbers

def gcd(a,b):
    if(not a):
        return b
    if(not b):
        return a
    return gcd(b,a%b)

li=r(300,350)
l=list(eratosthenes2(li))
p=choice(l)
q=choice(l)
n=p*q
global e
e=2
f=(p-1)*(q-1)
while(e<f):
    if(gcd(e,f)==1):
        break
    else:
        e+=1
k=0
while(1):
    z=(k*f)+1
    if(z%e):
        k+=1
        continue
    else:
        d=((k*f)+1)//e     
        break


dic={}

clients = set()
clients_lock = threading.Lock()

def encrypt(b,c):
    n,e=dic[c]
    r=""
    for i in b:
        r+=chr(pow(ord(i),e,n))
    return r
        
def decrypt(s):
    global n
    global d
    q=""
    for i in s:
        q+=chr(pow(ord(i),d,n))
    return q


def client_thread(conn):

    global e
    #conn.send((str(n)+" "+str(e)).encode('utf-8'))
    publicn,publice=conn.recv(1024).decode('utf-8').split()
    if conn not in dic:
        dic[conn]=(int(publicn),int(publice))
    user=conn.recv(1024).decode('utf-8')
    with clients_lock:
        if(len(clients)):
            for i in clients:
                m=user+" ha entrado al chat"
                m=encrypt(m,i)
                i.sendall((m).encode('utf-8'))
        clients.add(conn)
    

    
    try:
        while True:
            
            data = conn.recv(1024)
            b=data.decode('utf-8')
            #print("Encrypted: "+b)
            b=decrypt(b)
            #print(b)
            aux=b
            if not data:
                break
            
            if b=="disconnect":
                with clients_lock:
                    for c in clients:
                        if c!=conn:
                            m=user+" se ha desconectado."
                            m=encrypt(m,c)
                            c.sendall((m).encode('utf-8'))
                break
            with clients_lock:
                for c in clients:
                    if c!=conn:
                        b=aux
                        b=user+":"+b
                        b=encrypt(b,c)
                        #print("Encrypted for user: "+b)
                        
                        c.send((b).encode('utf-8'))
    finally:
        with clients_lock:
            clients.remove(conn)
            conn.close()




sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost",8081)) #Using IP address
#sock.bind(("localhost", 8081)) #Using localhost. also works with loopback 127.0.0.1, Assigning the server port and host
sock.listen(10)
print("Server on")
while True:
    # blocking call, waits to accept a connection
    conn, addr = sock.accept()
    conn.send((str(n)+" "+str(e)).encode('utf-8'))
    print("[-] Connected to " + addr[0] + ":" + str(addr[1]))
    s(client_thread, (conn,))
#conn, addr = sock.accept() #returns tupple
#print("Connection from: "+str(addr))
sock.close()
