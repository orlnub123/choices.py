import os
import re

from setuptools import setup


os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('choices/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)

with open('README.md') as f:
    readme = f.read()

setup(
    name='choices.py',
    version=version,
    description="A wrapper around Django's choices.",
    long_description=readme,
    url='https://github.com/orlnub123/choices.py',
    author='orlnub123',
    license='MIT',
    packages=['choices'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ]
)
