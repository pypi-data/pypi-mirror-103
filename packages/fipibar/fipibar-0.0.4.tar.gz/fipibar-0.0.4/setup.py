from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = [
    'pylast',
    'spotibar'
]

setup(
    name='fipibar',
    description='Fip radio plugin for Polybar',
    version='0.0.4',
    url='https://github.com/conor-f/fipibar',
    python_requires='>=3.6',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'fipibar = fipibar.client:main'
        ]
    }
)
