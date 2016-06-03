#!/usr/bin/env sh
# Author: Rainer M. Krug, Rainer@krugs.de

## some tests for the recipe 
# brew audit -v $RECIPE

## install GRASS 7.1 
brew install --HEAD \
             --with-nc_spm_08_grass7 \
             --with-ffmpeg \
             --with-mysql \
             --with-netcdf \
             --with-postgresql \
             --with-openblas \
             --with-liblas \
             grass-71

brew test -v grass-71
brew info grass-71

## run tests
## grass71 ./nc_basic_spm_grass7/PERMANENT --exec python -m grass.gunittest.main --location './nc_basic_spm_grass7' --location-type nc

## uninstall grass-71
brew uninstall grass-71
