import pathlib
from setuptools import find_packages, setup

ROOT_DIR = pathlib.Path(__file__).parent

setup(
    name="observer-config-json",
    packages=find_packages(),
    include_package_data=True,
    version="0.1.5",
    description="...",
    long_description=(ROOT_DIR / "README.md").read_text(),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=('facade-edit-file-json'),
    entry_points={},
    author="Tyshko Stanislav",
    author_email="admin@toqp.ru",
    url="https://github.com/RivalStorms/OBSERVER_CONFIG_JSON",
)
