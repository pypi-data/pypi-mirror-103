"""
Documentation
-------------
pctools/AutoTestManager

"""

from setuptools import setup, find_packages

long_description = __doc__

def main():
    setup(
        name="GxAutoTestManager",
        description="pctools",
        keywords="",
        long_description=long_description,
        version="0.1.0",
        author="DancePerth",
        author_email="28daysinperth@gmail.com",
        url="https://github.com/DancePerth/GxAutoTestManager",
        packages=find_packages(),
        package_data={},
        install_requires=['pyserial', 'goto-statement', 'python-redmine', 
            'pygerrit2','psutil'],
        entry_points={
            'console_scripts':[
                'gxserverstart=AutoTestManager.server.main:main',
                'gxclientstart=AutoTestManager.client.main:main',
                'gxcmdclient=AutoTestManager.server.modules.cmdclient:main',
                ]
            }
    )


if __name__ == "__main__":
    main()
