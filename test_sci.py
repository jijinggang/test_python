import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# 模拟幂函数
def func(x,a,b):
    return a*np.power((x),b)

# 拟合
def fit_func():
    xdata = np.array([1.0,2,4,8,16,32,64,128,256,512])
    ydata = np.zeros(len(xdata), dtype=float)
    ydata[0] = 1.0
    for i in range(1,len(ydata),1):
        ydata[i] = ydata[i-1]*1.75

    print(xdata)
    print(ydata)
    popt, pcov = curve_fit(func, xdata, ydata)
    print(popt)
    return popt

# 画图
def show(xdata,popt):
    plt.plot(xdata, func(xdata, *popt), 'g--',
            label='fit: a=%5.3f, b=%5.3f' % tuple(popt))

    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()


def main():
    popt = fit_func()
    xdata = np.arange(0, 240, 1)
    show(xdata,popt)


main()