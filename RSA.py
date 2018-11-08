from random import randint as r
from random import choice as pl

def eratosthenes2(n):
    multiples = set()
    for i in range(2, n+1):
        if i not in multiples:
            yield i
            multiples.update(range(i*i, n+1, i))
#eratosthenes2 code taken from https://stackoverflow.com/questions/33395903/efficient-method-for-generating-lists-of-large-prime-numbers

def gcd(a,b):
    if(not a):
        return b
    if(not b):
        return a
    return gcd(b,a%b)

li=r(1150,1200)
l=list(eratosthenes2(li))
l=l[25:]
p=pl(l)
q=pl(l)
n=p*q
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
r=""
u=""

print("RSA ENCRYPTION ALGORITHM")
mes=input("Insert message to encrypt: ")
for i in mes:
    encryp=pow(ord(i),e,n)
    r+=chr(encryp)
print("encrypted= " + r)
for k in r:
    des=pow(ord(k),d,n)
    u+=chr(des)
print("Descencrypted= "+u)
