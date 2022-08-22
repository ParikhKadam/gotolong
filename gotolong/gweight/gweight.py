#!/usr/bin/python

import sys
import re
import csv
import traceback
import operator

import argparse

import gotolong.cutil.cutil

from gotolong.database.database import *


class Gcweight(Database):
    def __init__(self):
        super(Gcweight, self).__init__()
        self.gcweight_captype_dict = {}
        self.gcweight_table_truncate = False
        self.gcweight_table_name = "global_weight"
        self.gcweight_table_dict = {
            "cap_type": "text",
            "cap_weight": "int"
        }
        self.debug_level = 0

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def gcweight_table_reload(self, truncate=False):
        self.gcweight_table_truncate = truncate

    def gcweight_table_create(self):
        # dump the sql for creation of table
        create_sql = gotolong.cutil.cutil.get_create_sql(self.gcweight_table_name, self.gcweight_table_dict)
        if self.debug_level > 0:
            print(create_sql)

    def gcweight_load_row(self, row):
        try:
            row_list = row
            if len(row_list) == 0:
                print('ignored empty row', row_list)
                return

            cap_type = row_list[0]
            cap_weight = row_list[1]

            self.gcweight_captype_dict[cap_type] = cap_weight

            if self.debug_level > 1:
                print('cop_type : ', cap_type, '\n')
                print('cap_weight : ', cap_weight, '\n')

        except IndexError:
            print('except ', row)
        except:
            print('except ', row)
            traceback.print_exc()

    def gcweight_load_data(self, in_filename):
        table = self.gcweight_table_name

        if self.gcweight_table_truncate:
            self.db_table_truncate(table)

        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.gcweight_insert_data(in_filename)
        else:
            print('gcweight data already loaded in db', row_count)
        print('display db data')
        self.gcweight_load_data_from_db()

    def gcweight_get_insert_row(self, line, row_bank):

        # split on comma
        row_list = line.split(',')

        if self.debug_level > 1:
            print('row_list', row_list)
            print('len row_list', len(row_list))

        (cap_type, cap_weight) = row_list

        if cap_type == 'Cap Type' or cap_weight == "Cap Weight":
            if self.debug_level > 0:
                print('skipped header line', row_list)
            return

        # remove any un-required stuff
        new_row = (cap_type, cap_weight)
        row_bank.append(new_row)

    def gcweight_insert_data(self, in_filename):
        insert_sql = gotolong.cutil.cutil.get_insert_sql(self.gcweight_table_name, self.gcweight_table_dict)

        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # insert row
            row_bank = []
            for line in csvfile:
                self.gcweight_get_insert_row(line, row_bank)
            print('loaded gcweight : ', len(row_bank))
            # insert row
            cursor.executemany(insert_sql, row_bank)
            # commit db changes
            self.db_conn.commit()

    def gcweight_load_data_from_db(self):
        table_name = self.gcweight_table_name
        cursor = self.db_table_load(table_name)
        for row in cursor.fetchall():
            if self.debug_level > 1:
                print(row)
            self.gcweight_load_row(row)

    def gcweight_dump_report_full(self, out_filename):

        fh = open(out_filename, "w")
        fh.write('cap_type, cap_weight\n')
        for cap_type, cap_weight in self.gcweight_captype_dict.items():
            p_str = str(cap_type)
            p_str += ', '
            p_str += str(cap_weight)
            p_str += '\n'
            fh.write(p_str);
        fh.close()


def main():
    parser = argparse.ArgumentParser(description='Process arguments')
    # dest= not required as option itself is the destination in args
    parser.add_argument('-l', '--log_level', default='INFO', help='DEBUG|INFO|WARNING|ERROR|CRITICAL', type=str,
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('-d', '--debug_level', default='0', help='debug level 0|1|2|3', type=int,
                        choices=[0, 1, 2, 3])
    parser.add_argument('-t', '--truncate_table', default='False', help='specify to truncate', action='store_true')
    parser.add_argument('-i', '--in_files', required=True, nargs='+', dest='in_files', help='in files')
    parser.add_argument('-o', '--out_files', required=True, nargs='+', dest='out_files', help='out files')

    args = parser.parse_args()

    debug_level = args.debug_level
    truncate_table = args.truncate_table

    # dummy assignment
    in_filename_phase = []
    out_filename_phase = []
    # use the argument as pattern
    for index, filename in enumerate(args.in_files):
        print('index = ', index, filename);
        in_filename_phase.append(filename)

    for index, filename in enumerate(args.out_files):
        print('index = ', index, filename);
        out_filename_phase.append(filename)

    # Main caller
    program_name = sys.argv[0]

    if len(sys.argv) < 4:
        print("usage: " + program_name + " <debug_level : 1-4> <amfi.csv> ... ")
        sys.exit(1)

    if debug_level > 1:
        print('args :', len(sys.argv))

    gcweight = Gcweight()

    gcweight.set_debug_level(debug_level)

    if truncate_table:
        gcweight.gcweight_table_reload(truncate_table)

    gcweight.gcweight_load_data(in_filename_phase[0])

    gcweight.gcweight_dump_report_full(out_filename_phase[0])


if __name__ == "__main__":
    main()
