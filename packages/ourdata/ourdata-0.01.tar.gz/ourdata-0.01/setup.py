VERSION = '0.01'
from distutils.core import setup
setup(
  name = 'ourdata',
  packages = ['ourdata'],
  version = VERSION,
  license='MIT',
  description = 'A bundle with modules that use data from open APIs ',
  author = 'Iris Unicamp',
  author_email = 'xande.okita@gmail.com',
  url = 'https://github.com/IRIS-UNICAMP/our-data',
  download_url = f'https://github.com/IRIS-UNICAMP/our-data/archive/{VERSION}.tar.gz',
  keywords = ['data', 'api', 'public', 'miscelaneous', "open", 'source'],
  install_requires=[
    'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)
