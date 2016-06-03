/*  
 ****************************************************************************
 *
 * MODULE:       g.proj 
 * AUTHOR(S):    Paul Kelly - paul-grass@stjohnspoint.co.uk
 * PURPOSE:      Provides a means of reporting the contents of GRASS
 *               projection information files and creating
 *               new projection information files.
 * COPYRIGHT:    (C) 2003-2007 by the GRASS Development Team
 *
 *               This program is free software under the GNU General Public
 *               License (>=v2). Read the file COPYING that comes with GRASS
 *               for details.
 *
 *****************************************************************************/

#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <proj_api.h>

#include <grass/gis.h>
#include <grass/gprojects.h>
#include <grass/glocale.h>
#include <grass/config.h>

#include "local_proto.h"

static int check_xy(int shell);

void print_projinfo(int shell, const char *force_epsg)
{
    int i;
    char path[GPATH_MAX];

    if (check_xy(shell))
	return;

    if (!shell)
	fprintf(stdout,
		"-PROJ_INFO-------------------------------------------------\n");
    for (i = 0; i < projinfo->nitems; i++) {
	if (shell)
	    fprintf(stdout, "%s=%s\n", projinfo->key[i], projinfo->value[i]);
	else
	    fprintf(stdout, "%-11s: %s\n", projinfo->key[i], projinfo->value[i]);
    }

    /* EPSG code is preserved for historical metadata interest only:
	the contents of this file are not used by pj_*() routines at all */
    G_file_name(path, "", "PROJ_EPSG", "PERMANENT");
    if (access(path, F_OK) == 0) {
        const char *epsg_value, *epsg_key;
        struct Key_Value *in_epsg_key;
        
        if (force_epsg) {
            epsg_key = "epsg";
            epsg_value = force_epsg;
        }
        else {
            in_epsg_key = G_read_key_value_file(path);
            epsg_key = in_epsg_key->key[0];
            epsg_value = in_epsg_key->value[0];
        }
	if (!shell) {
	    fprintf(stdout,
		"-PROJ_EPSG-------------------------------------------------\n");
	    fprintf(stdout, "%-11s: %s\n", epsg_key, epsg_value);
	}
	else
	    fprintf(stdout, "%s=%s\n", epsg_key, epsg_value);

        if (!force_epsg)
            G_free_key_value(in_epsg_key);
    }
 
    if (!shell)
	fprintf(stdout,
		"-PROJ_UNITS------------------------------------------------\n");
    for (i = 0; i < projunits->nitems; i++) {
	if (shell)
	    fprintf(stdout, "%s=%s\n",
		    projunits->key[i], projunits->value[i]);
	else
	    fprintf(stdout, "%-11s: %s\n",
		    projunits->key[i], projunits->value[i]);
    }
    
    return;
}

void print_datuminfo(void)
{
    char *datum, *params;
    struct gpj_datum dstruct;
    int validdatum = 0;

    if (check_xy(FALSE))
	return;

    GPJ__get_datum_params(projinfo, &datum, &params);

    if (datum)
	validdatum = GPJ_get_datum_by_name(datum, &dstruct);

    if (validdatum > 0)
	fprintf(stdout, "GRASS datum code: %s\nWKT Name: %s\n",
		dstruct.name, dstruct.longname);
    else if (datum)
	fprintf(stdout, "Invalid datum code: %s\n", datum);
    else
	fprintf(stdout, "Datum name not present\n");

    if (params)
	fprintf(stdout,
		"Datum transformation parameters (PROJ.4 format):\n"
		"\t%s\n", params);
    else if (validdatum > 0) {
	char *defparams;

	GPJ_get_default_datum_params_by_name(dstruct.name, &defparams);
	fprintf(stdout,
		"Datum parameters not present; default for %s is:\n"
		"\t%s\n", dstruct.name, defparams);
	G_free(defparams);
    }
    else
	fprintf(stdout, "Datum parameters not present\n");

    if (validdatum > 0)
	GPJ_free_datum(&dstruct);

    return;
}

void print_proj4(int dontprettify)
{
    struct pj_info pjinfo;
    char *proj4, *proj4mod, *i;
    const char *unfact;

    if (check_xy(FALSE))
	return;

    pj_get_kv(&pjinfo, projinfo, projunits);
    proj4 = pj_get_def(pjinfo.pj, 0);
    pj_free(pjinfo.pj);

    /* GRASS-style PROJ.4 strings don't include a unit factor as this is
     * handled separately in GRASS - must include it here though */
    unfact = G_find_key_value("meters", projunits);
    if (unfact != NULL && (strcmp(pjinfo.proj, "ll") != 0))
	G_asprintf(&proj4mod, "%s +to_meter=%s", proj4, unfact);
    else
	proj4mod = G_store(proj4);
    pj_dalloc(proj4);

    for (i = proj4mod; *i; i++) {
	/* Don't print the first space */
	if (i == proj4mod && *i == ' ')
	    continue;

	if (*i == ' ' && *(i+1) == '+' && !(dontprettify))
	    fputc('\n', stdout);
	else
	    fputc(*i, stdout);
    }
    fputc('\n', stdout);
    G_free(proj4mod);

    return;
}

#ifdef HAVE_OGR
void print_wkt(int esristyle, int dontprettify)
{
    char *outwkt;

    if (check_xy(FALSE))
	return;

    outwkt = GPJ_grass_to_wkt(projinfo, projunits, esristyle,
			      !(dontprettify));
    if (outwkt != NULL) {
	fprintf(stdout, "%s\n", outwkt);
	G_free(outwkt);
    }
    else
	G_warning(_("%s: Unable to convert to WKT"), G_program_name());

    return;
}
#endif

static int check_xy(int shell)
{
    if (cellhd.proj == PROJECTION_XY) {
	if (shell)
	    fprintf(stdout, "name=xy_location_unprojected\n");
	else
	    fprintf(stdout, "XY location (unprojected)\n");
	return 1;
    }
    else
	return 0;
}
