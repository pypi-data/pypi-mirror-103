import os
import setuptools

base_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(base_dir, "README.md"), "r") as f:
    long_description = f.read()

setuptools.setup(
    name="EncryptEnv",
    version="0.0.1",
    author="Thinktron",
    author_email="jeremywang@thinktronltd.com",
    description="Encrypt the passwords in the environment variables.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://rd.thinktronltd.com/jeremywang/EncryptEnv",
    packages=setuptools.find_packages(),
    # package_data={'TronGisPy': ['data/*', 'data/*/*']},
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
      install_requires=[
          'cryptography',
      ]
)