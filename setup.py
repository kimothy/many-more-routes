import setuptools

setuptools.setup(
    name='many-more-routes',
    version='1',
    description='A collection of tools to configure routes for M3',
    url='github.com/kimothy/many-more-routes',
    author='Kim Timothy Engh',
    install_requires=['pandas', 'pandera', 'openpyxl'],
    author_email='kim.timothy.engh@epiroc.com',
    packages=['outputs', 'procedures', 'sequence', 'templates'],
    zip_safe=False
)