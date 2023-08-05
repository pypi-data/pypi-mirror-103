from distutils.core import setup

setup(name='scraping-link',
      version='0.0.1',
      description='A Python module for web scraping',
      long_description='A Python module for web scraping, you will be able to scrape any website and solves typical blocking complications.',
      keywords=['web scraping', 'scraping', 'proxy rotating', 'html'],
      url='https://github.com/nicolasmarin/scraping-link-python',
      download_url='https://github.com/nicolasmarin/scraping-link-python/archive/refs/heads/main.zip',
      install_requires=[
          'requests',
          'urllib',
      ],
      author='nicolasmarin',
      license='GPLv3',
      packages=['scraping-link'],
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          ],
      zip_safe=False)
