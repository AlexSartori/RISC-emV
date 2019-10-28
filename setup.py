import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="riscemv",
    version="0.0.1",
    author="Alessandro Sartori, Davide Zanella",
    author_email="alex.sartori1997@gmail.com",
    description="Graphical emulation tool for the RISC-V architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexsartori/RISC-emV",
    install_requires=["pyqt5"],
    packages=setuptools.find_packages(),
    package_data={ },
    entry_points={
        # 'console_scripts': [
        #     'foo = my_package.some_module:main_func',
        #     'bar = other_module:some_func',
        # ],
        'gui_scripts': [
            'riscemv=riscemv:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
        "Topic :: Software Development",
        "Natural Language :: English"
    ],
    keywords='risc-v graphical emulator',
    python_requires='>=3.6',
)
