#!/bin/bash


if [[ ! -e primeenv ]]; then
  virtualenv primeenv
  primeenv/bin/pip install -r requirements.txt
fi

primeenv/bin/nosetests
