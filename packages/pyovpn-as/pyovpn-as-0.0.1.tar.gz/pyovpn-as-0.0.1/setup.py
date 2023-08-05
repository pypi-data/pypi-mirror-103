import setuptools
from distutils.core import setup

setup(
    name='pyovpn-as',
    packages=[
        'pyovpn_as',
        'pyovpn_as.api'
    ],
    version='0.0.1',
    license='GPL',
    description='A Python library built on XML-RPC that demystifies remote interaction with OpenVPN Access Server',
    long_description='README.md',
    long_description_content_type='text/markdown',
    author='Ryan Harrison',
    author_email='ryanharrison.opensource@protonmail.com',
    url='https://github.com/ryanharrison554/pyovpn-as',
    download_url='https://github.com/ryanharrison554/pyovpn-as/archive/v_0_0_1.tar.gz',
    keywords=['OpenVPN', 'AccessServer', 'Access Server', 'XML-RPC'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8', # This is due to the use of `headers` in the XML-RPC client,
    ],
    include_package_data=True
)