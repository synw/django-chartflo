from setuptools import setup, find_packages


version = __import__('chartflo').__version__

setup(
    name='django-chartflo',
    packages=find_packages(),
    version=version,
    description='Charts for the lazy ones in Django',
    author='synw',
    author_email='synwe@yahoo.com',
    url='https://github.com/synw/chartflo',
    download_url='https://github.com/synw/chartflo/releases/tag/' + version,
    keywords=["charts", "altair", "vega_lite"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    zip_safe=False,
    install_requires=[
        'altair',
        'gencharts',
        'goerr',
        "blessings",
    ],
)
