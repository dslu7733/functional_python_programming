#!/usr/bin/env python
#-*- coding:utf-8 -*-
#+--+--+--+--+--+--+--+--+--+--
#author   : lds
#date     : 2020-04-17
#function :
#+--+--+--+--+--+--+--+--+--+--

__author__ = 'lds'


#sample 1
#利用策略模式定义__init__()方法，避免出现状态变量
from typing import Callable
class Mersennel:
    def __init__( self, algorithm:Callable[[int],int] ) -> None:
        self.pow2 = algorithm

    def __call__(self, arg:int) -> int:
        return self.pow2(arg) - 1


def shifty(b:int) -> int:
    return 1 << b

def multy( b:int ) -> int:
    if b == 0: return 1
    return 2*multy( b-1 )

def faster( b:int ) -> int:
    if b == 0: return 1
    if b % 2 == 1: return 2*faster( b-1 )
    t = faster( b//2 )
    return t*t


mls = Mersennel( shifty )
mlm = Mersennel( multy )
mlf = Mersennel( faster )

print(mls(5))
print(mlm(5))
print(mlf(5))




# sample 2
# 如何更优雅地编写代码
from decimal import *
from typing import Text,Optional

str1 = '$123,3'

# version 1
def clean_decimal( text:Text ):
    if text is None: return None
    return Decimal(
            text.replace('$','').replace(',',''))

print( clean_decimal(str1) )


# version 2 (去掉函数的后缀写法)
def replace( str:Text, a:Text, b:Text ) -> Text:
    return str.replace(a,b)

print( Decimal( replace( replace(str1,'$',''), ',', '') ) )


# version 3
def remove( str:Text, delis:Text ) -> Text:
    if delis:
        return remove( 
                str.replace(delis[0], ''), delis[1:] )
    return str

print( remove(str1,'$,') )




# sample 3
# 使用命名元组

from typing import Tuple, Callable
RGB = Tuple[int, int, int]
red : Callable[[RGB], int] = lambda color : color[0]

print( red((1,2,3)) )
print( red((2,3)) )     #这种类型提示写法只是一种注释，没有实际作用，但是y可以使用mypy进行静态类型检查


from typing import NamedTuple
class Color(NamedTuple):
    """ An RGB color. """
    red : int
    green : int
    blue : int
    name : str

RGB = Color(1,2,3,'apple')
print(RGB.blue)




# sample 4
# python手动优化递归，改为生成器
from typing import Iterator 
import math
def pfactorl( x:int ) -> Iterator[int]:
    """计算x的所有质因数"""
    if x % 2 == 0:
        yield 2
        if x // 2 > 1:
            yield from pfactorl( x//2 )
        return      #表示结束生成

    for i in range( 3, int(math.sqrt(x))+1, 2 ):    #此处找到的第一个因数恰好就是质因数
        if x % i == 0:
            yield i
            if x // i > 1:
                yield from pfactorl( x//i )
            return

    yield x     #x只有一个质因数，就是自己


print('sample 4')
a = pfactorl(28)
print( next(a) )
print( next(a) )
print( next(a) )




# 将上面这个函数的for循环通过递归函数替换掉
def pfactorl( x:int ) -> Iterator[int]:

    def factor_n( x:int, n:int ) -> Iterator[int]:
        """判断n是否是x的质因数，并返回"""
        if x < n*n:
            yield x
            return  #z这个return的状态会一直上传，结束与之相关的其它yield from
        if x % n == 0:
            yield n
            if x // n > 1:
                yield from factor_n( x//n, n )
        else:
            yield from factor_n( x, n+2 )


    if x % 2 == 0:  #先去掉所有偶因数
        yield 2
        if x // 2 > 1:
            yield from pfactorl( x//2 )
        return
    
    yield from factor_n(x,3)




a = pfactorl(28)
print( next(a) )
print( next(a) )
print( next(a) )



# sample 5
# 针对生成器只能用一次
import itertools
from typing import Iterator, Any, Tuple, List
def limits( iterable:Iterator[Any] ) -> Any:
    g1, g2 = itertools.tee( iterable, 2 )   #可将生成器拷贝一份
    return max(g1), min(g2)


def generator():
    for i in range(3):
        yield f'i = {i}'

def split( g:Iterator[Any] ) -> Tuple[ Iterator[Any], Iterator[Any] ]:
    list1 = []  
    list2 = []

    def wrap( valList:List[Any] ) -> Iterator[Any]:
        """用yield来逐步获取g的值，并且使用列表保存这些值，进而使一个生成器可以多次使用
           参数valList是说明使用哪一个备份列表的
           函数wrap某种程度上也是惰性的
        """
        while True:     #实际由g来控制结束
            if not valList:     #列表为空, 需要备份
                try:
                    val = next(g)
                except StopIteration:
                    return  #生成器m结束
                list1.append(val)
                list2.append(val)
            
            yield valList.pop(0)

    
    g1 = wrap(list1)
    g2 = wrap(list2)

    return g1,g2


g = generator()
g1, g2 = split(g)
for i in g1:
    print( i )

for i in g2:
    print( i )



# sample 6
# 数据清洗


# step 1
import csv
from typing import IO, Text, List, Iterator
def row_iter( source:IO ) -> Iterator[List[Text]]:
    return csv.reader(source, delimiter='\t')

with open('source.txt') as source:
    print( list(row_iter(source)) )


def head_split_fixed(
        row_iter:Iterator[List[Text]] ) -> Iterator[List[Text]]:
    """数据清洗"""

    title = next( row_iter )
    assert ( len(title) == 1 
        and title[0] == 'source' )

    heading = next( row_iter )
    assert ( len(heading) == 4 
            and heading == ['I','II','III','IV'] )

    columns = next( row_iter )
    assert ( len(columns) == 8 
            and columns == ['x','y','x','y','x','y','x','y'])

    return row_iter


with open('source.txt') as source:
    print( list(head_split_fixed(row_iter(source))) )


# step 2
from typing import Tuple, cast
Pair = Tuple[str,str]
def series( 
        n:int, row_iter:Iterator[List[Text]] ) -> Iterator[Pair]:
    for row in row_iter:
        yield cast( Pair, tuple(row[2*n:2*n+2]) )     #m取每一行的相邻2列

with open('source.txt') as source:
    data = tuple(head_split_fixed(row_iter(source)))
    sample_I = tuple(series( 0, data ))
    sample_II = tuple(series( 1, data ))
    sample_III = tuple(series( 2, data ))
    sample_IV = tuple(series( 3, data ))

print( sample_I )
print( sample_II )
print( sample_III )
print( sample_IV )


# step 3
mean = (    #对sample_I的y值求平均
    sum( float(pair[1]) for pair in sample_I)  /  len(sample_I) 
)        

for subset in sample_I, sample_II, sample_III, sample_III:
    mean = (  
        sum( float(pair[1]) for pair in subset )  /  len(subset)
    )
    print(mean)



# sample 7
# 使用字典加快索引

# 命名元组
from collections import namedtuple
Color = namedtuple("Color", ("red","green","blue","name") )

# 颜色元组
seq = (Color(red=239, green=222, blue=205, name='Almond'),
       Color(red=205, green=149, blue=117, name='Antique Brass'),
       Color(red=255, green=174, blue=66, name='Yellow Orange'))

# 字典索引
name_map =  dict((c.name, c) for c in seq)
print( name_map['Almond'].red )



# 更省内存的索引方法
import bisect
from collections import Mapping

class StaticMapping( Mapping ):
    def __init__( self, 
            iterable:Iterator[Tuple[Any,Any]] ) -> None:
        self._data = tuple( sorted( (itr for itr in iterable),  key = lambda item : item[0] ) )     #sorted key通过一个函数指定排序标准
        self._keys = tuple( k for k,_ in self._data )

    def __getitem__(self, key):
        ix = bisect.bisect_left( self._keys, key )
        if ix != len(self._keys) and self._keys[ix] == key:
            return self._data[ix][1]
        raise ValueError( '{0!r} not found'.format(key) )
            

    def __iter__(self):
        return iter(self._keys)

    def __len__(self):
        return len(self._keys)


def g():
    for i in range(2,4):
        yield (i, i*i+10)
        yield (i*i, i)

map1 = StaticMapping( g() )     #这里参数写g的话b就不是生成器了，而是函数
for m in map1:
    print(m)

print( map1[2] )
print( map1[3] )
print( map1[4] )
print( map1[9] )
