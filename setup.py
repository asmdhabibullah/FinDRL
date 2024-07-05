from setuptools import setup, find_packages

setup(
    name='FinDRL',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'ta>=0.11.0',
        'click>=8.1.7',
        'numpy>=2.0.0',
        'pandas>=2.2.2',
        'requests>=2.32.3',
        'yfinance>=0.2.40',
        'matplotlib>=3.9.0',
        'backtesting>=0.3.3',
        'setuptools>=70.1.0',
        'python-dotenv>=1.0.1'
    ],
    entry_points={
        'console_scripts': [
            'findrl=app.cli:main',
        ],
    },
    include_package_data=True,
    description='A CLI app to fetch financial data',
    author='As Md Habibullah',
    author_email='asmdhabibullah@yahoo.com',
    url='https://github.com/asmdhabibullah/findrl.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
