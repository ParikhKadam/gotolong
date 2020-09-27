
#export PROJECT_ROOT=`pwd | sed -e"s/Google Drive/'Google Drive'/g"` 
export PROJECT_ROOT=`pwd` 
export PROJ_SOURCE_LOC=$PROJECT_ROOT/src
export PATH=${PROJ_SOURCE_LOC}:${PROJECT_ROOT}:.:${PATH}:$(dirname `which python`)/Scripts:/c/'Program Files (x86)'/'Microsoft Office'/Office16

export PYTHONPATH=${PROJ_SOURCE_LOC}:${PROJECT_ROOT}:$(dirname `which python`)/Scripts
export QUANDL_KEY=`cat $HOME/quandl.key`
export PLOTLY_API_KEY=`cat $HOME/plotly.key`

# if test "${PYTHONPATH}"  == ""
# then
# else
#  setenv PYTHONPATH ${PROJ_SOURCE_LOC}:${PYTHONPATH}
# endif
