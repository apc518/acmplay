from setuptools import setup

setup(name='acmusicplayer',
    version='0.1',
    description='A simple music player',
    url='',
    author='Andy Chamberlain',
    author_email='andychamberlainmusic@gmail.com',
    license='MIT',
    packages=['acmusicplayer'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'acmplay = acmusicplayer.musicplayer:main'
        ]
    }
)