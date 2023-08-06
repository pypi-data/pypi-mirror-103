'''

提供时间相关的函数

'''
import time

def showTimeNow():
    '''打印当前时间'''
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

def getFormatTime():
    '''返回字符串形式的当前时间'''
    return time.strftime(r"%Y%m%d%H%M%S", time.localtime())

# 通过获取程序名称判断该程序是被作为主程序运行还是作为模块被导入
# 当本文件作为程序直接运行时,下面语句会执行
# 当本文件作为模块被导入其他文件内时,下面语句不会执行
# 因此加入if __name__ == '__main__'的作用是用来测试模块内函数的功能
if __name__ == '__main__':
    print(__name__)
    showTimeNow()
    print(getFormatTime())

