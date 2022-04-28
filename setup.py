import setuptools

setuptools.setup(
    name='route_tools',
    version='0.1',
    description='A collection of tooles used for the route sequence',
    url='#',
    author='Kim Timothy Engh',
    install_requires=['pandas', 'pandera', 'openpyxl'],
    author_email='kim.timothy.engh@epiroc.com',
    packages=setuptools.find_packages(),
    zip_safe=False
)