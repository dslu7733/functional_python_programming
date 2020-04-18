#!/usr/bin/env python
#-*- coding:utf-8 -*-
#+--+--+--+--+--+--+--+--+--+--
#author   : lds
#date     : 2020-04-16
#function :
#+--+--+--+--+--+--+--+--+--+--

__author__ = 'lds'


# sample 1
class Summable_List( list ):
    def sum(self):
        s = 0
        for i in self:
            s += i
        return s

sumOfList1 = Summable_List( [1,2,3] )
print( sumOfList1.sum() )



# sample 2
def sumr( seq ):
    if len(seq) == 0: return 0
    return seq[0] + sumr(seq[1:])

print( sumr([1,2,3]) )


# sample 3
def until( n, filter_func, v ):
    "从[v,n)中找出3或5的倍数"
    if v == n: return []
    if filter_func(v): return [v] + until(n, filter_func, v+1)
    else: return until(n, filter_func, v+1)


print( until(20, lambda x : x % 3 == 0 or x % 5 == 0, 4) )



# sample 4
# 混合范式
print( sum(x for x in range(1,10) if x % 3 == 0 or x % 5 == 0 )  )



# sample 5
import timeit
print(  timeit.timeit( "(((([]+[1])+[2])+[3])+[4])" )  )


# sample 6
def next_( n,x ):
    "牛顿法求n的平方根x"
    return (x + n / x) / 2.0

n = 2
a0 = 1.0
f = lambda x : next_(n,x)   #lambda还能这么用，封装了函数。函数f求x的平方根
print( [ round(x,4) for x in (a0, f(a0), f(f(a0)),  f(f(f(a0))) ) ] )


stmt = '''
def repeat( f, a0 ):
    yield a0
    while True:
        a0 = f(a0)
        yield a0

n = 2   #求2的平方根
r = repeat( lambda x : (x+n/x)/2 ,1)
for i in range(4):
    #print( next(r) )
    next(r)
'''
print(  "timeit1 = %f" % timeit.timeit( stmt=stmt )  )


stmt = '''
#a0是第一个猜测的数字
def repeat( f, a0 ):
    "牛顿法求平方根的迭代器"
    yield a0
    for res in repeat(f, f(a0)):
        yield res

n = 2   
r = repeat(lambda x : (x+n/x)/2, 1)
for i in range(4):
    #print( next(r) )
    next(r)
'''
print(  "timeit2 = %f" % timeit.timeit( stmt=stmt )  )




# sample 7
def repeat(f, a0):
    "生成平方根的迭代器，f生成下一个x迭代的值"
    yield a0
    for x in repeat(f, f(a0)):
        yield x


def findSqrt( pre, iterable, a ):
    "计算精度为pre的n的平方根"
    b = next(iterable)
    if abs(a-b) <= pre: return b
    return findSqrt(pre, iterable, b)

n = 2.0
a0 = 1.0
iterable = repeat( lambda x : (x+n/x)/2.0, a0 )
next(iterable)
print( findSqrt( 1e-4, iterable, a0 ) )


#闭包封装函数
def within( prec, iterable ):
    def head_tail( prec, a ):
        b = next(iterable)
        if abs(a-b) <= prec: return b
        return head_tail( prec, b )

    return head_tail(prec, next(iterable))

#调用封装函数
def sqrt(a0, prec, n):
    return within( prec, repeat( lambda x  : (x+n/x)/2.0, a0) )



print( sqrt(1.0, 1e-4, 2.0) )














