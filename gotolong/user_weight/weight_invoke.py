#!/usr/bin/python

import sys
from django_gotolong import gcweight

# Main caller
program_name = sys.argv[0]

if len(sys.argv) < 6:
    print("usage: " + program_name + " <debug_level : 1-4> <amfi.csv> <gcweight.csv> ... ")
    sys.exit(1)

debug_level = int(sys.argv[1])
in_weight_filename = sys.argv[2]
out_filename_phase1 = sys.argv[3]
out_filename_phase2 = sys.argv[4]
out_filename_phase3 = sys.argv[5]

if debug_level > 1:
    print('args :', len(sys.argv))

weight = gcweight.Weight()

weight.set_debug_level(debug_level)

weight.amfi_load_db()
weight.weight_load_data(in_weight_filename)

weight.weight_dump_ticker(out_filename_phase1)
weight.weight_dump_sorted_units(out_filename_phase2)
weight.weight_dump_sorted_name(out_filename_phase3)
