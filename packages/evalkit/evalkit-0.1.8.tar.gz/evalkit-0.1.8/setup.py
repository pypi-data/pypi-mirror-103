from setuptools import setup, find_packages
import evalkit



setup(name='evalkit',
    version=evalkit.__version__,
    description='EVolutionary ALgorithms KITs',
    author='Parviz Mirzoev',
    author_email='parvector@yandex.com',
    url='https://github.com/parvector/evalkit',
    packages=find_packages(where=(".")),
    install_requires=['numpy'],
)