#!/usr/bin/env python

import setuptools

setuptools.setup(
  name = 'cresto',
  version = '0.0.1',
  description = 'A simple REST API wrapper',
  author = 'skelethon',
  license = 'GPL-3.0',
  url = 'https://github.com/skelethon/cresto',
  download_url = 'https://github.com/skelethon/cresto/downloads',
  keywords = ['sysops', 'devops', 'toolkit'],
  classifiers = [],
  install_requires = open("requirements.txt").readlines(),
  python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
  package_dir = {'':'src'},
  packages = setuptools.find_packages('src'),
)
