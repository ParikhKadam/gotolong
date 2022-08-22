#!/bin/sh

# NOTE : removed plan module data

TARGET_LIST=$1

if test "${TARGET_LIST}" = "daily" ; then

    for TARGET in bhav ftwhl demat phealth
    do
      gotolong_${TARGET}_invoke
      #${TARGET}_invoke.sh
    done

    if test -n "${GOTOLONG_EXCEL}"
    then
        CONFIG_PROFILE_REPORTS_LOC=`python -m gotolong.config.config_ini profile_reports`
        PHEALTH_OUT_FILE=${CONFIG_PROFILE_REPORTS_LOC}/phealth-reports/phealth-reports.csv
        excel ${PHEALTH_OUT_FILE} &
    fi
else

    # AMFI & ISIN
    for TARGET in amfi isin
    do
      gotolong_${TARGET}_invoke
      #${TARGET}_invoke.sh
    done

    for TARGET in screener trendlyne
    do
      gotolong_${TARGET}_invoke
    done

    # nse bhav and 52-w low and high
    for TARGET in bhav ftwhl
    do
      gotolong_${TARGET}_invoke
      # ${TARGET}_invoke.sh
    done

    # assign weights (global-gcweight)
    for TARGET in gcweight
    do
      gotolong_${TARGET}_invoke
    done

    for TARGET in bse
    do
      ${TARGET}_invoke.sh
    done

    # corpact uses bse reports
    for TARGET in corpact
    do
      gotolong_${TARGET}_invoke
    done

    for TARGET in demat
    do
      gotolong_${TARGET}_invoke
      # ${TARGET}_invoke.sh
    done

    for TARGET in phealth
    do
      gotolong_${TARGET}_invoke
    done

    # dividend
    for TARGET in nach
    do
        gotolong_${TARGET}_invoke
    done

    # bank stmt
    for TARGET in bstmt
    do
      gotolong_${TARGET}_invoke.sh
    done

    # dividend
    for TARGET in dividend
    do
      gotolong_${TARGET}_invoke.sh
    done

    # anomaly-invoke.sh
    # generate DB statistics
    gotolong_db_stats.sh
fi