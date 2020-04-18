#!/usr/bin/env python
#-*- coding:utf-8 -*-
#+--+--+--+--+--+--+--+--+--+--
#author   : lds
#date     : 2020-04-17
#function : 
#+--+--+--+--+--+--+--+--+--+--

__author__ = 'lds'


# sample 1
# 下面通过找寻元组最大值问题，来展示unwrap设计模式
# 打包 -》处理 -》 拆包

tuple_list = [(1,2),(3,4),(5,6),(7,8)]

snd = lambda x : x[1]
#优雅的前缀语法
print(  snd( max( map(lambda t : (t[1], t), tuple_list) ) )  )



# sample 2
# 展示惰性求值
def numbers():
    for i in range(1024):
        print( f"= {i}" )   #python3 语法
        yield i

def sum_to( n:int )->int:
    sum:int = 0
    for i in numbers():
        if i == n: break
        sum += i
    return sum

print( sum_to(5) )



# sample 3
# 判断数n是否是质数
import math
x = 13
print(  not any( x % p == 0 for p in range(2,int(math.sqrt(x))+1) )  )
x = 12
print(  not any( x % p == 0 for p in range(2,int(math.sqrt(x))+1) )  )




# sample 3
# 判断数n是否是质数（优化版）
def isprimer( n:int )->bool:
    def isprime( k:int, coprime:int )->bool:
        """ Is K relatively prime to value coprime ? """
        if k < coprime*coprime: return True
        if k % coprime == 0: return False
        return isprime( k, coprime+2)

    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    return isprime( n, 3 )

print( isprimer(12) )
print( isprimer(13) )



# 对于python来说，使用c生成器语法比递归效率高
def isprimer( n:int )->bool:
    if n < 2:
        return False

    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range( 3, 1+int(math.sqrt(n)), 2 ):
        if n % i == 0:
            return False
    return True






































