import setuptools
 
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
 
setuptools.setup(
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=['pytest'],
    name='linlangleyprime', # a unique name for PyPI
    version='0.7',
    author='Lin Chen, Yanhua Feng',
    author_email='lin.chen@ieee.org, yf@vims.edu',
    description='Demo for building a Python project',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='http://lin-chen-langley.github.io',
    project_urls = {
        'PyPI': 'https://pypi.org/manage/project/linlangleyprime/releases/',
        'Conda': 'https://anaconda.org/linchenVA/linlangleyprime'
        },
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: X11 Applications :: GTK',
      'Intended Audience :: End Users/Desktop',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License (GPL)',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python',
      'Topic :: Desktop Environment',
      'Topic :: Text Processing :: Fonts'
      ],
    install_requires=requirements,
    package_dir={'':'src'}, # location to find the packages
    packages=setuptools.find_packages(where="src"),
    #packages=['primepackage', ], # packages and subpackages containing .py files
    python_requires=">=3.9",
    scripts=['src/generator',], # the executable files will be installed for user
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
)
