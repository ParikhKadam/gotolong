# !/usr/bin/python

import sys
import re
import csv
import traceback

import gotolong.cutil.cutil

from gotolong.amfi.amfi import *


class Weight(Amfi):

    def __init__(self):
        super(Weight, self).__init__()
        self.weight_type_list = []
        self.weight_units_list = []
        self.weight_type_units_dict = {}
        self.weight_ticker_type_dict = {}
        self.weight_ticker_units_dict = {}
        self.weight_captype_comp_count_dict = {}
        self.weight_captype_units_count_dict = {}
        self.debug_level = 0
        self.last_row = ""
        print('init : Weight')

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def weight_load_row(self, row):
        try:
            row_list = row

            ticker = row_list[0]
            weight_type = row_list[1]
            weight_units = row_list[2]
            if self.debug_level > 1:
                print('ticker, gcweight type, gcweight units ')
            if self.debug_level > 0:
                print(':', ticker, ':', weight_type, ':', weight_units, ':')
            # use ticker as an input
            # isin = self.amfi_get_isin_by_name(comp_ticker)
            self.weight_ticker_type_dict[ticker] = weight_type
            self.weight_ticker_units_dict[ticker] = weight_units

            captype = self.amfi_get_value_by_ticker(ticker, "captype")
            if self.debug_level > 0:
                print(ticker, captype)

            if captype in self.weight_captype_comp_count_dict:
                self.weight_captype_comp_count_dict[captype] += 1
            else:
                self.weight_captype_comp_count_dict[captype] = 1

            if captype in self.weight_captype_units_count_dict:
                self.weight_captype_units_count_dict[captype] += int(weight_units)
            else:
                self.weight_captype_units_count_dict[captype] = int(weight_units)

            return
        except TypeError:
            print('except : TypeError : ', row, "\n")
            traceback.print_exc()
        except ValueError:
            print('except : ValueError :', row, "\n")
            traceback.print_exc()
        except IndexError:
            print('except : IndexError : ', row, "\n")
            traceback.print_exc()
        except KeyError:
            print('except : KeyError : ', row, "\n")
            traceback.print_exc()
        except:
            print('except : ', row, "\n")
            traceback.print_exc()

    def weight_load_data(self, in_filename):
        table = "user_weight"
        # put this truncate under some other condition
        if self.debug_level > 0:
            self.db_table_truncate(table)

        row_count = self.db_table_count_rows(table)
        if row_count == 0:
            self.weight_insert_data(in_filename)
        else:
            print('gcweight data already loaded in db', row_count)
        print('display db data')
        self.weight_load_db()

    def weight_insert_data(self, in_filename):
        start_processing = False
        SQL = """insert into gcweight(comp_ticker, comp_weight_type, comp_weight_units) values(:comp_ticker, :comp_weight_type, :comp_weight_units)"""
        cursor = self.db_conn.cursor()
        with open(in_filename, 'rt') as csvfile:
            # future
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                # fix the stripping : redundant spaces etc
                row = [column.strip() for column in row]

                if self.debug_level > 0:
                    print('reading 3rd column :', row[3], ':')

                if row[2] == 'WEIGHT_TYPE':
                    self.weight_type_list = row
                    if self.debug_level > 0:
                        print('weight_type_list :', self.weight_type_list)

                if row[2] == 'WEIGHT_UNITS':
                    self.weight_units_list = row
                    if self.debug_level > 0:
                        print('weight_units_list :', self.weight_units_list)
                    # create a dictionary out of two lists
                    #  dict(zip(keys,values))
                    self.weight_type_units_dict = dict(zip(self.weight_type_list, self.weight_units_list))
                    if self.debug_level > 0:
                        print('weight_type_units_dict :', self.weight_type_units_dict)

                if row[0] == 'Category' and row[1] == 'NUM_ORGS':
                    start_processing = True
                    continue

                if start_processing:
                    for col_idx in [3, 4, 5, 6, 7]:
                        if row[col_idx] != '':
                            w_str = [row[col_idx], self.weight_type_list[col_idx], self.weight_units_list[col_idx]]
                            if self.debug_level > 0:
                                print('inserting :', w_str)
                            cursor.execute(SQL, w_str)

            # commit db changes
            self.db_conn.commit()

    def weight_load_db(self):
        table = "user_weight"
        cursor = self.db_table_load(table)
        for row in cursor.fetchall():
            if self.debug_level > 1:
                print(row)
            self.weight_load_row(row)

    def weight_dump_ticker(self, out_filename):
        lines = []
        fh = open(out_filename, "w")
        sorted_items = sorted(self.weight_ticker_type_dict)

        for ticker in sorted_items:
            try:
                p_str = ticker
                p_str += '\n'
                lines.append(p_str)
            except ValueError:
                print('except : ValueError :', comp_name)
        # already sorted
        # lines.sort()
        fh.writelines(lines)
        return

    def weight_dump_generic(self, out_filename, sort_type_name=None):
        total_units = 0
        cap_units = {}
        fh = open(out_filename, "w")
        fh.write('ticker, comp_name, isin, weight_units, rank, captype, mcap\n')
        if sort_type_name:
            sorted_items = sorted(self.weight_ticker_units_dict)
            if self.debug_level > 2:
                print(sorted_items)
        else:
            sorted_items = sorted(self.weight_ticker_units_dict, key=self.weight_ticker_units_dict.__getitem__,
                                  reverse=True)

        for ticker in sorted_items:
            try:
                # isin = self.amfi_get_isin_by_name(comp_name)
                isin = self.amfi_get_value_by_ticker(ticker, "isin")
                comp_name = self.amfi_get_value_by_ticker(ticker, "cname")
                if self.debug_level >= 2:
                    print(comp_name)
                mcap = self.amfi_get_value_by_ticker(ticker, "mcap")
                rank = self.amfi_get_value_by_ticker(ticker, "rank")
                captype = self.amfi_get_value_by_ticker(ticker, "captype")
                if self.debug_level > 0:
                    print(ticker, captype)
                if ticker in self.weight_ticker_units_dict:
                    units_1k = int(self.weight_ticker_units_dict[ticker])
                else:
                    units_1k = 0
                if self.debug_level >= 2:
                    print(units_1k)
                total_units += units_1k
                if captype in cap_units:
                    cap_units[captype] += units_1k
                else:
                    cap_units[captype] = units_1k
            except ValueError:
                print('except : ValueError :', comp_name)

            p_str = ticker
            p_str += ', '
            p_str += comp_name
            p_str += ', '
            p_str += isin
            p_str += ', '
            if ticker in self.weight_ticker_units_dict:
                p_str += str(self.weight_ticker_units_dict[ticker])
            else:
                p_str += '0'
            p_str += ', '
            p_str += str(rank)
            p_str += ', '
            p_str += captype
            p_str += ', '
            p_str += str(mcap)
            p_str += '\n'
            fh.write(p_str)

        # Summary of Portfolio
        if self.debug_level > 0:
            print(cap_units)

        # captype comp count
        ccc_dict = self.weight_captype_comp_count_dict
        total_units = 0
        # calculate total_units
        # fix missing values
        for captype in self.amfi_captype_list:
            if captype not in ccc_dict:
                ccc_dict[captype] = 0
            else:
                total_units += int(ccc_dict[captype])

        # Current portfolio distribution
        p_str = 'Companies'
        p_str += ', '
        p_str += '-'
        p_str += ', '
        p_str += '-'
        p_str += ', '
        p_str += str(total_units)
        p_str += ', '
        try:
            p_str += 'large ' + str(int(round(float((ccc_dict['Large Cap'] * 100.0) / total_units)))) + ' %'
            p_str += ', '
            p_str += 'mid ' + str(int(round(float((ccc_dict['Mid Cap'] * 100.0) / total_units)))) + ' %'
            p_str += ', '
            p_str += 'small ' + str(int(round(float(((ccc_dict['Small Cap']) * 100.0) / total_units)))) + ' %'
            p_str += '\n'
        except KeyError:
            print('except KeyError')
            traceback.print_exc()
        except TypeError:
            print('except TypeError')
            traceback.print_exc()

        fh.write(p_str)

        # Current portfolio distribution
        # captype units count
        cuc_dict = self.weight_captype_units_count_dict
        total_units = 0
        # calculate total_units
        # fix missing values
        for captype in self.amfi_captype_list:
            if captype not in cuc_dict:
                cuc_dict[captype] = 0
            else:
                total_units += int(cuc_dict[captype])

        p_str = 'Weight'
        p_str += ', '
        p_str += '-'
        p_str += ', '
        p_str += '-'
        p_str += ', '
        p_str += str(total_units)
        p_str += ', '
        try:

            p_str += 'large ' + str(int(round(float((cuc_dict['Large Cap'] * 100.0) / total_units)))) + ' %'
            p_str += ', '
            p_str += 'mid ' + str(int(round(float((cuc_dict['Mid Cap'] * 100.0) / total_units)))) + ' %'
            p_str += ', '
            p_str += 'small ' + str(int(round(float(((cuc_dict['Small Cap']) * 100.0) / total_units)))) + ' %'
            p_str += '\n'
        except KeyError:
            print('except KeyError')
            traceback.print_exc()
        except TypeError:
            print('except TypeError')
            traceback.print_exc()

        fh.write(p_str)

        # Ideal portfolio distribution

        p_str = 'Ideal'
        p_str += ', '
        p_str += '-'
        p_str += ', '
        p_str += '-'
        p_str += ', '
        p_str += '100'
        p_str += ', '
        p_str += 'large ' + '65-70' + ' %'
        p_str += ', '
        p_str += 'mid ' + '20' + ' %'
        p_str += ', '
        p_str += 'small ' + '10-15' + ' %'
        p_str += '\n'
        fh.write(p_str)
        fh.close()

    def weight_dump_sorted_name(self, out_filename):
        self.weight_dump_generic(out_filename, sort_type_name=True)

    def weight_dump_sorted_units(self, out_filename):
        self.weight_dump_generic(out_filename, sort_type_name=False)
