from distutils.core import setup
setup(
  name = 'custom_loggers',
  packages = ['custom_loggers'],
  version = '1.0.0',
  license='MIT',
  description = 'A Custom Logger Class for creating colored, adding level, other misc features',
  author = 'Austin Stromness',
  author_email = 'stromnessdevelopment@gmail.com',
  url = 'https://github.com/astromness/custom_loggers',
  download_url = 'https://github.com/astromness/custom_loggers/archive/refs/tags/1.0.0.tar.gz',
  keywords = ['logging', 'colored', 'loglevel', 'console', 'custom'],
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.9',
  ],
)