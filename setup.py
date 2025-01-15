from setuptools import setup, find_packages

setup(
    name="mediagui",
    version="1.0.0",
    author="Your Name",
    author_email="your_email@example.com",
    description="A media GUI application with command-line support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mediagui",  # Replace with your repository URL
    packages=find_packages(),  # Automatically find all packages
    python_requires=">=3.13",
    install_requires=[
        "numpy==2.2.1",
        "opencv-python==4.10.0.84",
        "PyQt6==6.8.0",
        "PyQt6-Qt6==6.8.1",
        "PyQt6-sip==13.9.1",
    ],
    entry_points={
        "console_scripts": [
            "mediagui=mediagui.main:main",  # CLI entry point
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={
        "mediagui": ["data/*"],  # Include any additional files like images, etc.
    },
)