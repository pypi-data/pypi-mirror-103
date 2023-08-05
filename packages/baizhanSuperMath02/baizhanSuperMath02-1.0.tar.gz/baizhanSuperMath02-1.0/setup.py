#coding=utf-8
from distutils.core import setup
setup(
    name='baizhanSuperMath02', # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，测试哦', #描述
    author='chenying', # 作者
    author_email='964554398@qq.com',
    py_modules=['baizhanSuperMath02.demo1','baizhanSuperMath02.demo2'] # 要发布的模块
)