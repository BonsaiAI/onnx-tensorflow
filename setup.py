import os
import setuptools
import subprocess
from textwrap import dedent

TOP_DIR = os.path.realpath(os.path.dirname(__file__))
SRC_DIR = os.path.join(TOP_DIR, 'onnx_tf')

with open(os.path.join(TOP_DIR, 'VERSION_NUMBER')) as version_file:
  version = version_file.read().strip()

if os.getenv('TRAVIS'):
  # On travis, we install from source, therefore no need to specify version.
  onnx_dep = "onnx"
else:
  # For user, we install the onnx release known to work with our release.
  with open(os.path.join(TOP_DIR, 'ONNX_VERSION_NUMBER')) as onnx_version_file:
    onnx_version = onnx_version_file.read().strip()
    onnx_dep = "onnx>=" + onnx_version
    # For ONNX 1.9.0 for the Bonsai fork we need to use ONNX 1.9.0
    # since we don't have an internal ONNX fork and the onnx_version above
    # will be the one generated by the build process (1.9.0.xxxx), which
    # does not exist in the ONNX repo
    if onnx_version.startswith("1.9.0"):
        onnx_dep = "onnx>=1.9.0"

try:
  git_version = subprocess.check_output(['git', 'rev-parse', 'HEAD'],
                                        cwd=TOP_DIR).decode('ascii').strip()
except (OSError, subprocess.CalledProcessError):
  git_version = None

with open(os.path.join(SRC_DIR, 'version.py'), 'w') as f:
  f.write(dedent('''\
  # This file is generated by setup.py. DO NOT EDIT!

  from __future__ import absolute_import
  from __future__ import division
  from __future__ import print_function
  from __future__ import unicode_literals

  version = '{}'
  git_version = '{}'
  '''.format(version, git_version)))

setuptools.setup(
    name='onnx-tf',
    version=version,
    description=
    'Tensorflow backend for ONNX (Open Neural Network Exchange).',
    install_requires=[onnx_dep, "PyYAML", "tensorflow_addons"],
    entry_points={
        "console_scripts": [
            "onnx-tf=onnx_tf.cli:main",
        ],
    },
    url='https://github.com/onnx/onnx-tensorflow/',
    author='Arpith Jacob, Tian Jin, Gheorghe-Teodor Bercea, Wenhao Hu',
    author_email='tian.jin1@ibm.com',
    license='Apache License 2.0',
    packages=setuptools.find_packages(),
    zip_safe=False, 
    classifiers=[
         "Programming Language :: Python :: 2",
         "Programming Language :: Python :: 3"
    ]
)
