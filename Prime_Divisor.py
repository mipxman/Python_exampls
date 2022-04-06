'''
Mojtaba Alipour ---- Find Prime Divisor of number
'''
t = 0
count = 0 #counter 
ans = 0 #answer
list = [] # entry list
prime = []  #prime_number list 


for i in range(1,11):
    number = int(input(''))
    list.append(number)

#find maximum number 
max_num=(max(list))

#find_prime_list
for numy in range (1, max_num):  
    if numy > 1:  
        for i in range (2, numy):  
            if (numy % i) == 0:  
                break  
        else:  
            prime.append(numy) 



for y in list:
    for x in prime:
        if (y % x == 0):
            t+=1
    if t > count :
        count = t 
        ans = y
    elif t == count:
        if( y > ans):
            ans = y
            count = t
    t = 0
print(ans , count )
