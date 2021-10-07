"""A setuptools based setup module.
Based on setup.py from https://github.com/pypa/sampleproject
"""

from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    # See https://packaging.python.org/specifications/core-metadata/#name
    name='dbapi2abc',  # Required

    # See https://www.python.org/dev/peps/pep-0440/
    version='1.1.3',  # Required

    # See https://packaging.python.org/specifications/core-metadata/#summary
    description='Provide an Abstract Base Class for PEP249 compliant databases',

    # long_description taken from README.md (see above)
    # See https://packaging.python.org/specifications/core-metadata/#description-optional  # noqa: E501
    long_description=long_description,  # Optional

    # Optional if long_description is written in reStructuredText (rst) but
    # See https://packaging.python.org/specifications/core-metadata/#description-content-type-optional  # noqa: E501
    long_description_content_type='text/markdown',  # Optional (see note above)

    # See https://packaging.python.org/specifications/core-metadata/#home-page-optional  # noqa: E501
    url='https://github.com/campbsb/dbapi2abc',  # Optional

    author='Steve Campbell',  # Optional
    # author_email='',  # Optional

    # List additional URLs that are relevant to your project as a dict.
    # See https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use  # noqa: E501
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/campbsb/dbapi2abc/issues',
        # 'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'https://saythanks.io/to/campbsb',
        'Source': 'https://github.com/campbsb/dbapi2abc/',
    },

    # See https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Database',
        'Typing :: Typed',

        # Pick your license as you wish
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a list of additional keywords, separated
    # by commas, to be used to assist searching for the distribution in a
    # larger catalog.
    keywords='PEP249, Database, Database API',  # Optional

    package_dir={'dbapi2abc': 'dbapi2abc'},
    packages=['dbapi2abc'],  # Required

    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. See
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires='>=3.5, <4',
)
