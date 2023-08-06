from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(name="fmri_anonymizer",
      version='0.1.3',
      __version__='0.1.3',
      description="Anonymize your DICOM and NIFTI files with this tool easily.",
      long_description=readme(),
      long_description_content_type="text/markdown",
      url="https://caoslab.psy.cmu.edu:32443/hugoanda/fmri_anonymizer",
      author="Hugo Angulo",
      author_email="hugoanda@andrew.cmu.edu",
      license="MIT",
      classifiers=["License :: OSI Approved :: MIT License",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.7", ],
      packages=find_packages(),
      include_package_data=True,
      package_data={'': ['util/deid.dicom']},
      install_requires=["deid==0.1.42", "dicom2nifti", "pydeface", "numpy", "nibabel", "nipype", "ttictoc"],
      entry_points={"console_scripts": ["fmri_anonymizer=fmri_anonymizer.__main__:main", ]},
      python_requires='>=3.7', )
