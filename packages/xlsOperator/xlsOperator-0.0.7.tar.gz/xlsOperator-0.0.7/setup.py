from setuptools import setup,find_packages

setup(
    name = 'xlsOperator',
    version = '0.0.7',
    keywords='xls excel',
    description = 'a library for read/write xls and xlsx document which can ideally keep graphics\' format in EXCEL '
                  'after modification .',
    license = 'MIT License',
    author = 'TreemanChou',
    url = '',
    author_email = '574747067@qq.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = ['xlwt','xlrd','numpy','pypiwin32'],
)

