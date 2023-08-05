from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
      name="applied_stats",
      version='0.0.2',
      url='https://github.com/WillTirone/applied_stats',
      author='William Tirone',
      author_email='will.tirone1@gmail.com', 
      description="A basic statistics module to compute MLEs / probabilities",
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(where='applied_stats'), #instead of py_modules? 
      package_dir={'':"applied_stats"},
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        "Operating System :: OS Independent"
        ],
      install_requires = ['scipy > 1',
                          'numpy > 1', 
                          'matplotlib > 3']
      )