import setuptools

readme = open("README.md").read()

setuptools.setup(
    name="gear_score",
    version="0.0.2",
    author="Eugene Prodan",
    author_email="mora9715@gmail.com",
    description="Python implementation of GearScore WoW addon",
    long_description=readme,
    long_description_content_type='text/markdown',
    url="https://github.com/mora9715/gearscore",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers"

    ],
    python_requires='>=3.6',
    install_requires=[
        'aiohttp',
        'pydantic',
        'sqlalchemy',
        'aiosqlite'
    ]
)