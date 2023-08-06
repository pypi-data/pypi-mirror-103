import setuptools

with open('README.md') as readme:
    long_description = readme.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()

setuptools.setup(
    name='django-ts-bridge',
    version='1.2.1',
    author='ChickenF622',
    author_email='chickenf622@gmail.com',
    description='Management commands in Django that give defintions for Django models returned by DRF along with any model fields limited by choices',
    long_description=long_description,
    include_package_data=True,
    package_data= {
        'django_ts_bridge': [
            'templates/django_ts_bridge/*.tpl'
        ]
    },
    install_requires=requirements,
    url='https://gitlab.com/ChickenF622/django-ts-bridge',
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires=">=3.8"
)
