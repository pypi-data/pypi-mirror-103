from setuptools import setup, find_packages

setup(
    name='easyorm-mysql',
    version='1.0.0',
    packages=find_packages(),  # 自动搜索
    include_package_data=True,   # 添加/排除额外文件，结合MANIFEST.in使用
    author='yxb',
    author_email='yuexba@yutong.com',
    url='https://www.cnblogs.com/yxb-blog/',
    description='a easy orm framework for mysql',
    install_requires=['mysql-connector>=2.2.9']  # 依赖项，在安装该模块时会自动安装依赖项
)
