import re
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('redgifs/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE)[1] # type: ignore

with open('README.md') as f:
    readme = f.read()

extras_require = {
    'docs': [
        'Sphinx==4.4.0',
        'furo==2022.2.23'
    ],
    'test': [
        'pytest==7.1.1'
    ],
}

setup(
    name='redgifs',
    author='scrazzz',
    url='https://github.com/scrazzz/redgifs',
    project_urls={
        'Documentation': 'https://redgifs.rtfd.io',
        'Issue tracker': 'https://github.com/scrazzz/redgifs/issues'
    },
    version=version,
    packages=['redgifs'],
    extras_require=extras_require,
    license='MIT',
    description='Async and Sync Python Wrapper for the RedGifs API.',
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.7.0'
)
