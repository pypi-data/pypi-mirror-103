from setuptools import setup, find_packages
from my_package import __version__
import pathlib

work_dir=pathlib.Path(__file__).parent
readme=(work_dir / "README.md").read_text()

setup(
  name='code_package',
  version=__version__,
  description="You dont want this package",
  url="https://go_somewhere_else.com",
  long_description=readme,
  long_description_content_type='text/markdown',
  author="bg",
  author_email="bg@gb.com",
  install_requires=["numpy==1.20.2"],
  packages=find_packages()
)