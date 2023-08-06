from setuptools import setup, find_packages

GFICLEE_VERSION = '1.0.0'

setup(
    name='akafra-demo',
    version=GFICLEE_VERSION,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ['akafra-demo = StringUtils:test']
    },
    install_requires=[
        "django"
    ],
    py_modules=["akafra-demo"],
    url='https://github.com/ChuXiaoYi/fastproject',
    license='GNU General Public License v3.0',
    author='Xiaoyi Chu',
    author_email='895706056@qq.com',
    description='More convenient to create fastapi project'
)
