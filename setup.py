from setuptools import setup

# python setup.py sdist --formats=bztar

version = '0.3'
description = 'Beaker backend for redis'
long_description = open('README.rst', 'rb').read().decode('utf8')


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
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
    ],

    modules=['beaker_redis'],

    entry_points={
        'beaker.backends': [
            'redis = beaker_redis:RedisBackend',
        ],
    },
)
