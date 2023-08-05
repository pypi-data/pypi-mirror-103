from setuptools import setup, find_packages
from pypandoc import convert_file

VERSION = '1.0.4' 
DESCRIPTION = 'NulledAPI - UnOfficial Nulled API'
with open('readme.md', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
        name="NulledAPI", 
        version=VERSION,
        author="M3GZ",
        author_email="megzfromnulled@gmail.com",
        url="https://www.nulled.to/user/4103370-m3gz",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Programming Language :: Python :: 3.0',
            'Intended Audience :: Developers',
            'Topic :: Utilities'
        ],
        packages=find_packages(),
        install_requires=[
            'requests==2.25.1'
        ]
)