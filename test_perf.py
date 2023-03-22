# 每秒打印一次cpu使用率，写入文件file中
def test_perf():
    import time
    import psutil
    import os
    
    file = open('cpu_usage.txt', 'w')
    while True:
        # 写入当前时间
        file.write(time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time())))
        cpu_usage = psutil.cpu_percent(interval=1)
        file.write(str(cpu_usage) + "%\n")


# main
if __name__ == '__main__':  
    test_perf()