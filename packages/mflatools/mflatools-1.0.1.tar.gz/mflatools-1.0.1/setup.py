from distutils.core import setup

setup(
    name='mflatools',  # 对外我们模块的名字
    version='1.0.1',  # 版本号
    description='mfla的工具箱',  # 描述
    author='mfla',  # 作者
    author_email='871494698@qq.com',
    py_modules=['mflatools.timep001', 'mflatools.writep001']  # 要发布的模块
)
