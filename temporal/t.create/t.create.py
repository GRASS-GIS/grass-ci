#!/usr/bin/env python
# -*- coding: utf-8 -*-
############################################################################
#
# MODULE:       t.create
# AUTHOR(S):    Soeren Gebbert
#
# PURPOSE:      Create a space time dataset
# COPYRIGHT:    (C) 2011-2014 by the GRASS Development Team
#
#		This program is free software under the GNU General Public
#		License (version 2). Read the file COPYING that comes with GRASS
#		for details.
#
#############################################################################

#%module
#% description: Creates a space time dataset.
#% keyword: temporal
#% keyword: map management
#% keyword: create
#% keyword: time
#%end

#%option G_OPT_STDS_OUTPUT
#%end

#%option G_OPT_STDS_TYPE
#% description: Type of the output space time dataset
#%end

#%option G_OPT_T_TYPE
#%end

#%option
#% key: semantictype
#% type: string
#% description: Semantic type of the space time dataset
#% required: yes
#% multiple: no
#% options: min,max,sum,mean
#% answer: mean
#%end

#%option
#% key: title
#% type: string
#% description: Title of the new space time dataset
#% required: yes
#% multiple: no
#%end

#%option
#% key: description
#% type: string
#% description: Description of the new space time dataset
#% required: yes
#% multiple: no
#%end

import grass.script as grass
import grass.temporal as tgis

############################################################################


def main():

    # Get the options
    name = options["output"]
    type = options["type"]
    temporaltype = options["temporaltype"]
    title = options["title"]
    descr = options["description"]
    semantic = options["semantictype"]

    # Make sure the temporal database exists
    tgis.init()
    
    tgis.open_new_stds(name, type, temporaltype, title, descr, 
                                     semantic, None, grass.overwrite())

if __name__ == "__main__":
    options, flags = grass.parser()
    main()
