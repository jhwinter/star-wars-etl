from setuptools import setup, find_packages

setup(
    name="star_wars_etl",
    version="1.0",
    packages=find_packages(exclude="test"),
    install_requires=[
        "certifi==2020.6.20",
        "chardet==3.0.4",
        "idna==2.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pymysql==0.10.0",
        "python-dotenv==0.14.0",
        "requests==2.24.0",
        "responses==0.10.16",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "urllib3==1.25.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
    ],
)
