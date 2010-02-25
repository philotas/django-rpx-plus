from setuptools import setup, find_packages

setup(
    name = 'django_rpx',
    #We exclude example app from installing since that may interfere from
    #someone testing out their own example app of the same name. I got 
    #bit by this :).
    packages = find_packages(exclude = ['example', 'example.*']),
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

