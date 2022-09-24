#!/bin/sh

if test -n "${GOTOLONG_DEBUG_LEVEL}"
then
    DEBUG_LEVEL=${GOTOLONG_DEBUG_LEVEL}
else
    DEBUG_LEVEL=0
fi

MODULE_NAME=peqia

CONFIG_GLOBAL_DATA_LOC=`python -m gotolong.config.config_ini global_data`
CONFIG_GLOBAL_REPORTS_LOC=`python -m gotolong.config.config_ini global_reports`
CONFIG_PROFILE_DATA_LOC=`python -m gotolong.config.config_ini profile_data`
CONFIG_PROFILE_REPORTS_LOC=`python -m gotolong.config.config_ini profile_reports`

OUT_DIR_1=$CONFIG_PROFILE_REPORTS_LOC/${MODULE_NAME}-reports
OUT_FILE_1=${OUT_DIR_1}/${MODULE_NAME}-reports.csv
OUT_FILE_2=${OUT_DIR_1}/${MODULE_NAME}-reports.txt

mkdir -p ${OUT_DIR_1}

#python plan_invoke.py --truncate_table --debug_level ${DEBUG_LEVEL} --in_files ${IN_FILE_PLAN} --out_files ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5}
# python plan_invoke.py --debug_level ${DEBUG_LEVEL} --in_files ${IN_FILE_PLAN} --out_files ${OUT_FILE_1} ${OUT_FILE_2} ${OUT_FILE_3} ${OUT_FILE_4} ${OUT_FILE_5}
python ${MODULE_NAME}.py -l DEBUG -d ${DEBUG_LEVEL} -o ${OUT_FILE_1} ${OUT_FILE_2}

if test -n "${GOTOLONG_EXCEL}"
then
  excel ${OUT_FILE_1} &
fi

