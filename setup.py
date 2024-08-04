from setuptools import setup, find_packages

setup(
    name='simple_attack_simulator',
    version='0.1.0',
    description='Creates random attack graphs, simulates attacks, and produces logs.',
    author='Pontus Johnson',
    author_email='pontusj@kth.se',
    url='https://github.com/pontusj101/simple_attack_simulator',
    license='Apache-2.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List your project dependencies here
        # e.g., 'numpy', 'pandas',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
