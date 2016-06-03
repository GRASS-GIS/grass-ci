#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#
# MODULE:	t.sample
# AUTHOR(S):	Soeren Gebbert
#
# PURPOSE:	Sample the input space time dataset(s) with a sample space time dataset and print the result to stdout
# COPYRIGHT:	(C) 2011-2014, Soeren Gebbert and the GRASS Development Team
#
#		This program is free software under the GNU General Public
#		License (version 2). Read the file COPYING that comes with GRASS
#		for details.
#
#############################################################################

#%module
#% description: Samples the input space time dataset(s) with a sample space time dataset and print the result to stdout.
#% keyword: temporal
#% keyword: sampling
#% keyword: time
#%end

#%option G_OPT_STDS_INPUTS
#%end

#%option G_OPT_STDS_INPUT
#% key: sample
#% description: Name of the sample space time dataset
#%end

#%option G_OPT_STDS_TYPE
#% key: intype
#% guisection: Required
#%end

#%option G_OPT_STDS_TYPE
#% key: samtype
#% guisection: Required
#% description: Type of the sample space time dataset
#%end

#%option G_OPT_T_SAMPLE
#% key: method
#% answer: during,overlap,contain,equal
#%end

#%option G_OPT_F_SEP
#% description: Field separator between output columns, default is tabular " | "
#% label: Do not use "," as this char is reserved to list several map ids in a sample granule
#%end

#%flag
#% key: c
#% description: Print the column names as first row
#%end

#%flag
#% key: s
#% description: Check spatial overlap
#%end

import grass.script as grass
import grass.temporal as tgis

############################################################################

def main():

    # Get the options
    inputs = options["inputs"]
    sampler = options["sample"]
    samtype = options["samtype"]
    intype = options["intype"]
    separator = grass.separator(options["separator"])
    method = options["method"]
    header = flags["c"]
    spatial = flags["s"]

    # Make sure the temporal database exists
    tgis.init()

    tgis.sample_stds_by_stds_topology(intype, samtype, inputs, sampler,
                                      header, separator, method, spatial,
                                      True)

if __name__ == "__main__":
    options, flags = grass.parser()
    main()
