# 各种自省功能
import dis
import inspect

def f1(x,y):
    return x+y
def f2(x:int,y:int)->int:
    return x+y
def test_dir():
    # dir:列出对象支持的方法和睡醒
    print(dir(f1))
    print(dir(f1.__dict__))


def test_dis():
    # dis.dis 显示对象的字节码
    dis.dis(f1)

def test_inspect():
    # 列出函数签名
    print(inspect.signature(f1))
    print(inspect.signature(f2))
    print(inspect.signature(open).parameters)

    # 函数对象的成员
    print(inspect.getmembers(list))

test_dir()
test_dis()
test_inspect()