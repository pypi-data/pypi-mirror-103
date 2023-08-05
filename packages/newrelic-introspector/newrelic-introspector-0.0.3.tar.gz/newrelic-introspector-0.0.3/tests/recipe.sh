#!/bin/bash

# Potential python executables
PYTHON3_EXE=$(which python3)
PYTHON_EXE=$(which python)
PYPY3_EXE=$(which pypy3)
PYPY_EXE=$(which pypy)
CONDA_EXE=$(which conda)

# Set exit behavior after attempting to resolve python versions


# Coalesce python executable names
PYTHON=${PYTHON3_EXE:-${PYTHON_EXE:-${PYPY3_EXE:-${PYPY_EXE:-${CONDA_EXE}}}}}

if [[ -z "${PYTHON}" ]]; then
    echo "Failed to find python executable. Is python available in your PATH?"
else
    $PYTHON ./lsi.py
    if [ $? == 1 ]
    then
      echo "No instrumentable Python processes found on host."
      exit 1
    fi
fi