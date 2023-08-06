from setuptools import find_packages, setup

setup(
    name='PrettyPlotting',
    packages=find_packages(include=['prettyplotting']),
    version='0.1.0',
    description='A simple matplotlib wrapper',
    url = 'https://github.com/chrisnav/PrettyPlotting',
    author='Christian Øyn Naversen',
    author_email='christian.oyn.naversen@gmail.com',
    install_requires=['matplotlib>=3.4.1'],
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows :: Windows 10',        
        'Programming Language :: Python :: 3.9',
    ],    
)