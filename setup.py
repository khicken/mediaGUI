from setuptools import setup, find_packages

setup(
    name='mediagui',
    version='1.0.0',
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
)