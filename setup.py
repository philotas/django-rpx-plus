from setuptools import setup, find_packages

setup(
    name = 'django_rpx',
    packages = find_packages(),
    version = '1.0.0',
    description  = 'RPX auth support for django',
    author='Michael Huynh',
    author_email='mike@mikexstudios.com',
    url='http://github.com/mikexstudios/django-rpx',
    install_requires = ['django-picklefield'],
    classifiers = [
        'Programming Language :: Python', 
        'Framework :: Django', 
        'License :: OSI Approved :: BSD License',
    ]
)

