import socket
from _thread import start_new_thread as p
from random import randint as r
from random import choice as pl

def eratosthenes2(n):
    multiples = set()
    for i in range(2, n+1):
        if i not in multiples:
            yield i
            multiples.update(range(i*i, n+1, i))

def gcd(a,b):
    if(not a):
        return b
    if(not b):
        return a
    return gcd(b,a%b)

li=r(500,600)
l=list(eratosthenes2(li))
l=l[80:]
#print(l)
pp=pl(l)
q=pl(l)
n=pp*q
e=2
f=(pp-1)*(q-1)

while(e<f):
    if(gcd(e,f)==1):
        break
    else:
        e+=1
        
d=1
while(1):
    if((d*e)%f==1):
        break
    d+=1

'''
k=0
while(1):
    z=(k*f)+1
    if(z%e):
        k+=1
        continue
    else:
        d=((k*f)+1)//e     
        break
'''

def encrypt(s,n,e):
    r=""
    for i in s:
        c=pow(ord(i),e,n)
        r+=chr(c)
    return r

def decrypt(m):
    global n
    global d
    q=""
    for i in m:
        q+=chr(pow(ord(i),d,n))
    return q

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost",8081))
publicn,publice=sock.recv(1024).decode('utf-8').split()
sock.send((str(n)+" "+str(e)).encode('utf-8'))
#print(publicn,publice)
publicn=int(publicn)
publice=int(publice)
username=input("Enter an username: ")
sock.send(username.encode('utf-8'))


def r(sock):
    while True:
        msg=sock.recv(1024).decode('utf-8')
        msg=decrypt(msg)
        print(msg)
           
p(r,(sock,))

while True:
    m=input()
    #m=username+":" + t
    j=encrypt(m,publicn,publice)
    sock.send(j.encode('utf-8'))
    if(m=="disconnect"):
        break
sock.close()
