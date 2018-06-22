"""
Flask-InfluxDB
"""
from setuptools import setup

setup(
    name='Flask-InfluxDB',
    version='0.2',
    url='http://github.com/ombitron/flask-influxdb',
    license='BSD',
    author='Brennan Ashton',
    author_email='brennan@ombitron.com',
    description='Flask bindings for the InfluxDB time series database',
    long_description=__doc__,
    py_modules=['flask_influxdb'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'influxdb==5.0.0',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

