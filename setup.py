from setuptools import setup, find_packages

setup(
    name='mediagui',
    version='1.0.0',
    author='Kaleb Kim',
    author_email='mail@kalebkim.com',
    description='A Python package with a GUI for video formatting',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/khicken/mediaGUI',
    packages=find_packages(),
    install_requires=[
        'numpy==2.2.2',
        'opencv-python==4.11.0.86',
        'opencv-python-headless==4.11.0.86',
        'PyQt6==6.8.0',
        'PyQt6-Qt6==6.8.1',
        'PyQt6_sip==13.10.0'
    ],
    entry_points={
        'console_scripts': [
            'mediagui=mediagui.gui:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)