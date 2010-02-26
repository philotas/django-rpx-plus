from setuptools import setup, find_packages

setup(
    name = 'django_rpx_plus',
    #We exclude example app from installing since that may interfere from
    #someone testing out their own example app of the same name. I got 
    #bit by this :). We also put django_rpx/ inside of a src/ dir so that
    #installations using 'setup.py develop' don't install example/ (since
    #'setup.py develop' ignores exclude).
    packages = find_packages('src', exclude = ['example', 'example.*']),
    package_dir={'' : 'src'},
    version = '1.0.0',
    description  = 'RPX auth support for django',
    author='Michael Huynh',
    author_email='mike@mikexstudios.com',
    url='http://github.com/mikexstudios/django-rpx-plus',
    install_requires = ['django-picklefield'],
    classifiers = [
        'Programming Language :: Python', 
        'Framework :: Django', 
        'License :: OSI Approved :: BSD License',
    ]
)

