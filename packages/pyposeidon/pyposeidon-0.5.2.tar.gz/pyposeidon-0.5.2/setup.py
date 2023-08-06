# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyposeidon', 'pyposeidon.tide', 'pyposeidon.utils']

package_data = \
{'': ['*'], 'pyposeidon': ['misc/*']}

install_requires = \
['Cartopy>=0.18.0,<0.19.0',
 'Shapely>=1.7.1,<2.0.0',
 'branca>=0.4.2,<0.5.0',
 'cfgrib>=0.9.8,<0.10.0',
 'colorlog>=4.7.2,<5.0.0',
 'dask>=2021.2.0,<2022.0.0',
 'datashader>=0.12.0,<0.13.0',
 'eccodes>=1.1.0,<2.0.0',
 'f90nml>=1.2,<2.0',
 'geopandas>=0.8.2,<0.9.0',
 'geoviews>=1.8.1,<2.0.0',
 'gmsh>=4.7.1,<5.0.0',
 'holoviews>=1.14.1,<2.0.0',
 'hvplot>=0.7.0,<0.8.0',
 'ipython>=7.20.0,<8.0.0',
 'llvmlite>=0.36.0,<0.37.0',
 'matplotlib>=3.3.4,<4.0.0',
 'moviepy>=1.0.3,<2.0.0',
 'netCDF4>=1.5.6,<2.0.0',
 'numpy>=1.20.1,<2.0.0',
 'panel>=0.10.3,<0.11.0',
 'pygeos>=0.9,<0.10',
 'pyresample>=1.17.0,<2.0.0',
 'rasterio>=1.2.0,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'scipy>=1.6.1,<2.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'tqdm>=4.58.0,<5.0.0',
 'xarray>=0.16.2,<0.17.0']

setup_kwargs = {
    'name': 'pyposeidon',
    'version': '0.5.2',
    'description': 'Framework for Sea Level Hydrodynamic simulations',
    'long_description': "Framework for Sea Level Hydrodynamic simulations\n================================================\n\n[![Documentation Status](https://readthedocs.org/projects/pyposeidon/badge/?version=latest)](https://pyposeidon.readthedocs.io/en/latest/?badge=latest) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/ec-jrc/pyPoseidon) ![CI](https://github.com/ec-jrc/pyPoseidon/actions/workflows/conda_and_nested_venv.yml/badge.svg) ![CI](https://github.com/ec-jrc/pyPoseidon/actions/workflows/conda.yml/badge.svg) ![CI](https://github.com/ec-jrc/pyPoseidon/actions/workflows/code_quality.yml/badge.svg) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ec-jrc/pyPoseidon/master?urlpath=%2Flab)\n\nThis is a development project utilising multiple solvers (currently DELFT3D & SCHISM) for simulating sea level height (currently only storm surge). The purpose is to create a simple, portable and transparent way of setting up, running and analysing hydrodynamic computations through python scripts and Jupyter Notebooks (http://jupyter.org). See Notebooks in Tutorial/ for relevant prototypes.\n\n## Installation\n\n\n`conda install -c gbrey pyposeidon`\n\nAfterwards, for now, one needs to install gmsh manually with\n\n`pip install gmsh`\n\n**Note**: Due to an upstream issue, *pydap* needs to be installed manually. See *environment.yml* for info.\n\n### Prerequisities\n\nDELFT3D needs to be compiled for your system. You can download it from http://oss.deltares.nl/web/delft3d/source-code. See Wiki for more details.\n\nSCHISM needs to be compiled for your system. You can download it from  http://columbia.vims.edu/schism/tags/. See http://ccrm.vims.edu/schismweb/ for more info.\n\n\nYou can also install the solvers easily with conda\n\n`conda install -c gbrey pschism delft3d4`\n\n\n## Tests\n\nThere are several sets of tests. You can run pyPoseidon unitests with\n\n`pytest`\n\nIn order to test also the solver integration use\n\n`pytest --runschism`\n\nor\n\n`python --rundelft`\n\nif you are using a local installation of the solvers please specify the PATH to the executables in your system such as\n\n`export D3D = '/path_to_folder_bin/lnx64/flow2d3d/'`\n\n`export LD3D = '/path_to_folder_bin/lnx64/flow2d3d/'`\n\n`export SCHISM = '/path_to_schism_executable'`\n\n## docs\n\n```\nmkdocs build\nmkdocs serve\n```\n\n## License\n* The project is released under the EUPL v1.2 license.\n",
    'author': 'George Breyiannis',
    'author_email': 'breyiannis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ec-jrc/pyposeidon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
