#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#
# MODULE:	t.vect.list
# AUTHOR(S):	Soeren Gebbert
#
# PURPOSE:	List registered maps of a space time vector dataset
# COPYRIGHT:	(C) 2011-2014, Soeren Gebbert and the GRASS Development Team
#
#		This program is free software under the GNU General Public
#		License (version 2). Read the file COPYING that comes with GRASS
#		for details.
#
#############################################################################

#%module
#% description: Lists registered maps of a space time vector dataset.
#% keyword: temporal
#% keyword: map management
#% keyword: vector
#% keyword: list
#% keyword: time
#%end

#%option G_OPT_STVDS_INPUT
#%end

#%option
#% key: order
#% type: string
#% description: Sort the space time dataset by category
#% guisection: Formatting
#% required: no
#% multiple: yes
#% options: id,name,layer,creator,mapset,temporal_type,creation_time,start_time,end_time,north,south,west,east,points,lines,boundaries,centroids,faces,kernels,primitives,nodes,areas,islands,holes,volumes
#% answer: start_time
#%end

#%option
#% key: columns
#% type: string
#% description: Columns to be printed to stdout
#% guisection: Selection
#% required: no
#% multiple: yes
#% options: id,name,layer,creator,mapset,temporal_type,creation_time,start_time,end_time,north,south,west,east,points,lines,boundaries,centroids,faces,kernels,primitives,nodes,areas,islands,holes,volumes
#% answer: name,layer,mapset,start_time,end_time
#%end

#%option G_OPT_T_WHERE
#% guisection: Selection
#%end

#%option
#% key: method
#% type: string
#% description: Method used for data listing
#% required: no
#% multiple: no
#% options: cols,comma,delta,deltagaps,gran
#% answer: cols
#%end

#%option G_OPT_F_SEP
#% label: Field separator character between the output columns
#% guisection: Formatting
#%end

#%option G_OPT_F_OUTPUT
#% required: no
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
    columns = options["columns"]
    order = options["order"]
    where = options["where"]
    separator = grass.separator(options["separator"])
    method = options["method"]
    header = flags["s"]
    output = options["output"]

    # Make sure the temporal database exists
    tgis.init()

    tgis.list_maps_of_stds("stvds", input, columns, order, where, separator,
                           method, header, outpath=output)

if __name__ == "__main__":
    options, flags = grass.parser()
    main()
