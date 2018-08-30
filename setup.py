from setuptools import setup

version = '1.1.0'
description = 'Beaker backend for redis'

with open('README.rst') as f:
    long_description = f.read()


setup(
    name='beaker_redis',
    version=version,
    description=description,
    long_description=long_description,
    author='Zelenyak "ZZZ" Aleksander',
    author_email='zzz.sochi@gmail.com',
    url='https://github.com/zzzsochi/beaker_redis',
    license='BSD',
    platforms='any',
    install_requires=['beaker', 'redis'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],

    py_modules=['beaker_redis'],

    entry_points={
        'beaker.backends': [
            'redis = beaker_redis:RedisBackend',
        ],
    },
)
