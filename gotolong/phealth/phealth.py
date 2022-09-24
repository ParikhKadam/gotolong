# !/usr/bin/python

import sys
import re
import csv
import traceback

import gotolong.cutil.cutil

from datetime import datetime, date

import logging

from gotolong.amfi.amfi import *
from gotolong.isin.isin import *
from gotolong.bhav.bhav import *
from gotolong.corpact.corpact import *
from gotolong.demat.demat import *
from gotolong.ftwhl.ftwhl import *
from gotolong.gfundareco.gfundareco import *
from gotolong.gcweight.gcweight import *

from gotolong.screener.screener import *
from gotolong.trendlyne.trendlyne import *


# gfundareco - includes fratio and trendlyne
class Peqia(Screener, Gfundareco, Demat, Gcweight, Bhav, Ftwhl, Corpact):

    def __init__(self):
        super(Peqia, self).__init__()
        # years of investing. started in 2017
        # self.plan_multiply = self.INVEST_YEARS
        self.peqia_values = {}
        self.debug_level = 0
        logging.debug('init : peqia')

    def set_log_level(self, log_level):
        log_level_number = getattr(logging, log_level.upper(), None)
        logging.basicConfig(level=log_level_number)

    def set_debug_level(self, debug_level):
        self.debug_level = debug_level

    def peqia_dump_report(self, out_filename, out_filename_2):

        bat_missing_list = []

        fh = open(out_filename, "w")

        # oku - one k units
        p_str = "ticker,comp_name,cap_type,bat,cmp,low_52w,high_52w,up_52w_low,mos,txn_gap,plan_oku,cur_oku,tbd_oku,gb_score,funda_reco_type,funda_reco_cause"
        p_str += '\n'

        fh.write(p_str)

        logging.debug(len(self.sc_nsecode))

        for ticker in self.amfi_ticker_list:

            rank = self.amfi_rank[ticker]
            logging.debug(ticker, 'rank', self.amfi_rank[ticker])

            captype = self.amfi_captype[ticker]

            # capture only large cap and mid cap
            if rank > 500:
                continue

            try:

                p_str = ticker
                p_str += ','

                p_str += self.amfi_cname[ticker]
                p_str += ','

                p_str += captype
                p_str += ','

                if self.tl_ratio_values.get((ticker, "bat")):
                    bat = self.tl_ratio_values[ticker, "bat"]
                    p_str += str(bat)
                else:
                    bat = '-'
                    p_str += bat
                    bat_missing_list.append(ticker)
                p_str += ','

                cmp = self.bhav_ticker_cmp_dict[ticker]
                p_str += str(cmp)
                p_str += ','

                low_52w = self.ftwhl_ticker_low_dict[ticker]
                p_str += str(low_52w)
                p_str += ','

                high_52w = self.ftwhl_ticker_high_dict[ticker]
                p_str += str(high_52w)
                p_str += ','

                # up_52w_low
                up_52w_low = round(((cmp - low_52w) * 100.0 / low_52w))
                p_str += str(up_52w_low)
                p_str += ','

                # mos
                if bat != '-':
                    mos = round(((int(bat) - int(cmp)) * 100.0 / int(cmp)))
                else:
                    mos = '-'

                p_str += str(mos)
                p_str += ','

                last_date = self.demat_txn_get_last_date_by_ticker(ticker)

                # old_date_format = "%d-%b-%Y"
                new_date_format = '%Y-%m-%d'
                if last_date != '-':
                    someday = datetime.datetime.strptime(last_date, new_date_format).date()
                    today = datetime.date.today()
                    logging.debug(someday, 'next', today)

                    delta = today - someday
                    # find months
                    months = str(int(delta.days / 30))
                else:
                    months = '-'

                p_str += months
                p_str += ','

                weight = self.gcweight_captype_dict[captype]

                plan_units = int(weight)
                current_units = self.demat_sum_get_units_by_ticker(ticker)
                tbd_units = plan_units - current_units

                p_str += str(plan_units)
                p_str += ','

                p_str += str(current_units)
                p_str += ','

                p_str += str(tbd_units)
                p_str += ','

                if ticker in self.corpact_total:
                    giveback_score = self.corpact_total[ticker]
                else:
                    giveback_score = '-'
                p_str += str(giveback_score)
                p_str += ','

                if ticker in self.gfunda_reco_type:
                    funda_reco_type = self.gfunda_reco_type[ticker]
                else:
                    funda_reco_type = '-'
                p_str += funda_reco_type
                p_str += ','

                if ticker in self.gfunda_reco_cause:
                    funda_reco_cause = self.gfunda_reco_cause[ticker]
                else:
                    funda_reco_cause = '-'
                p_str += funda_reco_cause
                p_str += '\n'

                logging.debug(p_str)

                fh.write(p_str)

            except ValueError:
                logging.error('except : ValueError : %s', ticker)
                traceback.print_exc()
            except KeyError:
                logging.error('except : KeyError : %s', ticker)
                traceback.print_exc()

        logging.debug("Tickers with bat missing : ", len(bat_missing_list))
        logging.debug(bat_missing_list)

        return


def main():
    print('in main')

    parser = argparse.ArgumentParser(description='Process arguments')
    # dest= not required as option itself is the destination in args
    parser.add_argument('-l', '--log_level', default='INFO', help='DEBUG|INFO|WARNING|ERROR|CRITICAL', type=str,
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('-d', '--debug_level', default='0', help='debug level 0|1|2|3', type=int, choices=[0, 1, 2, 3])
    parser.add_argument('-o', '--out_files', required=True, nargs='+', dest='out_files', help='out files')

    args = parser.parse_args()

    debug_level = args.debug_level
    log_level = args.log_level

    # dummy assignment
    out_filename_phase = []
    for index, filename in enumerate(args.out_files):
        print('index = ', index, filename);
        out_filename_phase.append(filename)

    # Main caller
    program_name = sys.argv[0]

    # debug_level = int(sys.argv[1])
    # in_plan_filename = sys.argv[2]
    # out_filename_phase1 = sys.argv[3]
    # out_filename_phase2 = sys.argv[4]
    # out_filename_phase3 = sys.argv[5]
    # out_filename_phase4 = sys.argv[6]
    # out_filename_phase5 = sys.argv[7]

    if debug_level > 1:
        print('args :', len(sys.argv))

    peqia = Peqia()

    peqia.set_log_level(log_level)

    peqia.set_debug_level(debug_level)

    peqia.amfi_load_data_from_db()
    peqia.isin_load_data_from_db()
    peqia.demat_txn_load_data_from_db()
    peqia.demat_sum_load_data_from_db()
    peqia.screener_load_db()
    peqia.trendlyne_load_data_from_db()
    peqia.gfunda_reco_load_data_from_db()
    peqia.gcweight_load_data_from_db()
    peqia.bhav_load_data_from_db()
    peqia.ftwhl_load_data_from_db()
    peqia.corpact_load_data_from_db()

    peqia.peqia_dump_report(out_filename_phase[0], out_filename_phase[1])


if __name__ == "__main__":
    main()
