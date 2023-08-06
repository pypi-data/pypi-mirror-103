from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='addoneexample',
    version='0.0.1',
    description='A very basic function which adds 1 to any number',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Isaac Cobb',
    author_email='cobbcoding@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='add one',
    packages=find_packages(),
    install_requires=['']
)
