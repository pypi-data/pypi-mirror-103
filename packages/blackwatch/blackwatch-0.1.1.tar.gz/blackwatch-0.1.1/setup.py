from distutils.core import setup


setup(
    name="blackwatch",
    packages=["blackwatch", "blackwatch.commands", "blackwatch.handlers"],
    version="0.1.1",
    license="MIT",
    description="Watches a folder for file system events and run optional command (if required)",
    author="Naveen Anil",
    author_email="blackwatch@nvn-nil.in",
    url="https://github.com/nvn-nil/blackwatch",
    download_url="https://github.com/nvn-nil/blackwatch/archive/refs/tags/0.1.1.tar.gz",
    entry_points={"console_scripts": ["blackwatch = blackwatch:main"]},
    keywords=["DEVTOOL", "UTILITY", "CLI"],
    install_requires=["cleo==0.8.1", "watchdog==2.0.3"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
