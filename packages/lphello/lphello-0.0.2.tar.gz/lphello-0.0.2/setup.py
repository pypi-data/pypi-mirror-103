from setuptools import setup, find_packages
__packages__ = ['hello_package','hello_package.sub_folder']

setup(
    name = "lphello",
    version = "0.0.2",
    description = "hello world",
    author = 'gxf',
    author_email = 'feng.gao@laipac.com',
    url = 'https://github.com/gxfca/gitTest',
    packages = __packages__,
    package_data = {'':['*.dat'],
                    'hello_package':['sub_folder/png/*.png'],
                    },
#    packages = find_packages(where = "hello_package"),
#    package_dir ={"":"hello_package"}
    entry_points={
    'console_scripts': [
        'hello=hello_package.hello:print_hello',
    ],
    },
    
    )

