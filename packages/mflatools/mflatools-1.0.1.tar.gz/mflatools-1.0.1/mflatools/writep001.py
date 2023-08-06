'''
提供文件写入的相关函数
'''
import time

def writeFileinDesk(info,encoding='utf-8'):
    '''将内容写入到文件并保存到D盘根目录'''
    path=r'd:\\'+time.strftime(r"%Y%m%d%H%M%S", time.localtime())+r'.txt'
    with open(path,'w',encoding=encoding) as f:
        f.write(info)
    print('完成写入')

if __name__=='__main__':
    writeFileinDesk('再次测试')


