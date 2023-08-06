from setuptools import setup

setup(
    name='asd_py',
    version='0.1',
    description='site(canopy)/leaf hyperspectral proccessing program by python',
    author='Justin Guo',
    author_email='guojianbiao2008@gmail.com',
    url='https://github.com/justinG-29/asd_py',
    license='MIT',
    packages=['asd_py'],
    install_requires=['numpy', 'pandas', 'scipy','plotly','scikit-learn'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3',
    extras_require={'read asd data': ['specdal']})
