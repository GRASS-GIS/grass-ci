#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#
# MODULE:	t.vect.univar
# AUTHOR(S):	Soeren Gebbert
#
# PURPOSE:	Calculates univariate statistics of attributes for each registered vector map of a space time vector dataset
# COPYRIGHT:	(C) 2011-2014 by the GRASS Development Team
#
#		This program is free software under the GNU General Public
#		License (version 2). Read the file COPYING that comes with GRASS
#		for details.
#
#############################################################################

#%module
#% description: Calculates univariate statistics of attributes for each registered vector map of a space time vector dataset
#% keyword: temporal
#% keyword: statistics
#% keyword: vector
#% keyword: time
#%end

#%option G_OPT_STVDS_INPUT
#%end

#%option G_OPT_F_OUTPUT
#% required: no
#%end

#%option G_OPT_V_FIELD
#%end

#%option G_OPT_DB_COLUMN
#% required: yes
#%end

#%option G_OPT_T_WHERE
#% guisection: Selection
#% key: twhere
#%end

#%option G_OPT_DB_WHERE
#% guisection: Selection
#%end

#%option G_OPT_V_TYPE
#% options: point,line,boundary,centroid,area
#% multiple: no
#% answer: point
#%end

#%option G_OPT_F_SEP
#% label: Field separator character between the output columns
#% guisection: Formatting
#%end

#%flag
#% key: e
#% description: Calculate extended statistics
#%end

#%flag
#% key: s
#% description: Suppress printing of column names
#% guisection: Formatting
#%end

import grass.script as grass
import grass.temporal as tgis

############################################################################

def main():

    # Get the options
    input = options["input"]
    output = options["output"]
    twhere = options["twhere"]
    layer = options["layer"]
    type = options["type"]
    column = options["column"]
    where = options["where"]
    extended = flags["e"]
    header = flags["s"]
    separator = grass.separator(options["separator"])

    # Make sure the temporal database exists
    tgis.init()

    if not output:
        output = None
    if output == "-":
        output = None

    tgis.print_vector_dataset_univar_statistics(
        input, output, twhere, layer, type, column, where, extended, header, separator)

if __name__ == "__main__":
    options, flags = grass.parser()
    main()
