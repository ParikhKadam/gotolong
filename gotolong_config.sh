
#export PROJECT_ROOT=`pwd | sed -e"s/Google Drive/'Google Drive'/g"`

# export PROJECT_ROOT=/d/GoogleDrive/my_github/GitHub/gotolong
export PROJECT_ROOT=`pwd`
export PKG_ROOT=$PROJECT_ROOT
export PROJ_SCRIPTS_LOC=$PROJECT_ROOT/scripts
# note - modules installed using pip install --user <>
export USER_SCRIPTS_LOC=/c/Users/SURIKUMA/AppData/Roaming/Python/Python310
export PATH=${PROJ_SCRIPTS_LOC}:${PROJECT_ROOT}:.:${PATH}:$(dirname `which python`)/Scripts:${USER_SCRIPTS_LOC}/Scripts
# add excel path
export PATH=${PATH}:/c/'Program Files (x86)'/'Microsoft Office'/Office16
# add mysql PATH
export PATH=${PATH}:/c/'Program Files'/'MariaDB 10.5'/bin
# add psql (PostgreSQL) PATH, createdb
export PATH=${PATH}:/C/'Program Files'/PostgreSQL/13/bin

export PYTHONPATH=${PKG_ROOT}:${PROJ_SCRIPTS_LOC}:.:

# set DATABASE_URL for django
# check django/mysite/settings.py
# export DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME
export GOTOLONG_MY_DATABASE_URL=mysql://root:root@localhost:3306/gotolong
# postgres://USER:PASSWORD@HOST:PORT/NAME
export GOTOLONG_PG_DATABASE_URL=postgres://postgres:root@localhost:5432/gotolong

export DATABASE_URL=${GOTOLONG_MY_DATABASE_URL}

# uses heroku cli
# echo Trying to get DATABASE_URL ... timeout of 1 minute
# export HEROKU_DATABASE_URL=`heroku config:get --app gotolong DATABASE_URL`

# set the home : contains variable data : to be used by the package by user
export GOTOLONG_DATA=$PROJECT_ROOT/data

# export QUANDL_KEY=`cat $HOME/quandl.key`
# export PLOTLY_API_KEY=`cat $HOME/plotly.key`

# if test "${PYTHONPATH}"  == ""
# then
# else
#  setenv PYTHONPATH ${PKG_LOC}:${PYTHONPATH}
# endif
