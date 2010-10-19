from setuptools import setup, find_packages
import os

version = open("ftw/dashboard/portlets/postit/version.txt").read().strip()

setup(name='ftw.dashboard.portlets.postit',
      version=version,
      description="portlets in the ftw.dashboard",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='philippe gross',
      author_email='mailto:info@4teamwork.ch',
      url='http://plone.org/products/ftw.dashboard.portlets.postit/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', 'ftw.dashboard', 'ftw.dashboard.portlets'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
