from setuptools import setup

setup(name='scraping-link',
      version='0.0.6',
      description='A Python module for web scraping',
      long_description=open('README.rst').read(),
      long_description_content_type="text/x-rst",
      keywords=['web scraping', 'scraping', 'proxy rotating', 'html'],
      url='https://github.com/nicolasmarin/scraping-link-python',
      download_url='https://github.com/nicolasmarin/scraping-link-python/archive/refs/heads/main.zip',
      install_requires=[
          'requests',
      ],
      author='nicolasmarin',
      author_email='info@scraping.link',
      license='GPLv3',
      packages=['scraping-link'],
      classifiers=[
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          ])
