# GotoLong

GotoLong is being developed as a Portfolio Advisor.

It has an Indian Stock Advisor (ISA) that can be used to identify stocks for buy and sale.

It relies on

(a) Financial data (last 10 year) of Top 500 (BSE-500/Nifty-500) stocks

(b) investor's existing portfolio of stocks

It is still in Beta phase and developers can experiment with it.

Once it can be used by any user with basic knowledge of computer, it will be tagged as v1.0

## Sample Deployment

Check Sample deployment on heroku.
(NOTE: Site is down as heroku doesn't honor india issued credit card due to new RBI regulation. Still exploring an alternative deployment.)

https://gotolong.herokuapp.com/

# Quick setup on local box

## Clone repository

git clone https://github.com/gotolong/gotolong

## Software  Pre-Req

Download Python 3.*

Download mariadb (for DB) - used mariadb10.4

Download PostgreSQL (v13) - for validation with Heroku

## Install Python packages

pip install -r requirements/requirements-dev.txt

## Configure PATH, PYTHONPATH, DATABASE_URL

### Modify ~/.bashrc
Use git bash console to add following to ~/.bashrc

cd location of gotolong clone

. ./gotolong_config.sh
  
### Modify gotolong_config.sh for DB Versions

For Mariadb version, port# etc
For PostgreSQL version, port# etc

export PATH=${PATH}:/c/'Program Files'/'MariaDB 10.5'/bin

export PATH=${PATH}:/C/'Program Files'/PostgreSQL/13/bin

export GOTOLONG_MY_DATABASE_URL=mysql://root:root@localhost:3306/gotolong

export GOTOLONG_PG_DATABASE_URL=postgres://postgres:root@localhost:5432/gotolong

export DATABASE_URL=${GOTOLONG_MY_DATABASE_URL}

## Modify DB configuration

Modify data/config/gotolong-config.ini

[DATABASE]

db_type = mariadb

db_name = gotolong

db_user = root

db_pass = root

\# for postgresql

pg_user = postgres

pg_pass = root

## Create DB

gotolong_db_schema_install.sh mysql create

gotolong_db_schema_install.sh pgsql create

## Import Sample Data

gotolong_db_schema_install.sh mysql import

gotolong_db_schema_install.sh pgsql import "${PG_DATABASE_URL}"

## Start using App

The django project is capable of browsing the data stored in 'gotolong' database.

python manage.py runserver

Starting development server at http://127.0.0.1:8000/

Use the following URL to access the stuff

http://127.0.0.1:8000/

# Heroku Deployment

Check Sample deployment

(NOTE: Site is down as heroku doesn't honor india issued credit card due to new RBI regulation. Still looking for an altenative solution.)

https://gotolong.herokuapp.com/

NOTES:

* wait for 15 to 30 sec initially as free dyno sleeps after 30 mins of inactivity.

On Heroku, the clone of repository can be connected using github.

Attach postgresql database to the heroku app.

heroku login

heroku addons:create heroku-postgresql:hobby-dev

gotolong_db_schema_install.sh pgsql import "${HEROKU_DATABASE_URL}"

heroku pg:reset --confirm \<appname\> --app \<appname\>

# Quick Redeployment from github

## DB : Refresh on Heroku

gotolong_db_heroku_refresh.sh

## App : Refresh on Heroku

https://www.heroku.com/

https://dashboard.heroku.com/apps

personal : gotolong (1 app)

Pipeline : Production : gotolong (github link)

Deploy : https://dashboard.heroku.com/apps/gotolong/deploy/github

Manual Deploy : Deploy a github branch (master) : Deploy Branch

Your app was successfully deployed : View.

# Screenshots

## Home

<img src="https://github.com/gotolong/gotolong/blob/master/media/screenshots/gotolong-home-Screenshot.png" >
## Global Advisor
<img src="https://github.com/gotolong/gotolong/blob/master/media/screenshots/gotolong-advisor-Screenshot.png" >
## Global Fof/ETF
<img src="https://github.com/gotolong/gotolong/blob/master/media/screenshots/gotolong-fof-etf-Screenshot.png" >

## User broker summary

<img src="https://github.com/gotolong/gotolong/blob/master/media/screenshots/gotolong-user-broker-sum-Screenshot.png" >

## User broker transaction

<img src="https://github.com/gotolong/gotolong/blob/master/media/screenshots/gotolong-user-broker-txn-Screenshot.png" >

## User broker mutual fund

<img src="https://github.com/gotolong/gotolong/blob/master/media/screenshots/gotolong-user-broker-mf-Screenshot.png" >

## User portfolio health

<img src="https://github.com/gotolong/gotolong/blob/master/media/screenshots/gotolong-user-broker-phealth-Screenshot.png" >

# Modules Information

## amfi module

mapping of ticker and mcap and captype

## isin module

mapping of ticker and ISIN

## Giving Back Score

Module : bse -> corpact

## 52-week high and low and CMP

We are ok with data of yesterday as it is for investment and not for trading.

Modules : bhav, ftwhl, nse

## demat module (icici direct portfolio)

demat transaction details

demat summary details

Module name : demat

NOTE: add support for any broker.

## screener module

financial data of bse 500 for 10 years

## trendlyne module

for broker average target of healthy stocks

## gweight module

global weight module

assign weight by captype

user weight is not used right now

Name : global_weight

## fratio module

Financial Ratio module

You can specify financial ratio filters like debt to equity ratio (der)

## gfundareco module

Global recommendation module

Uses trendlyne module and fratio module

## phealth module

identify companies at healthy price

Dependency :

## dividend module

create dividend amfix by company and month.

Dependency : nach -> dividend

# Additional Softwares

Download PyCharm

Download HeidiSQL : DB browser

Download VIM

Download GoogleDrive to store the input data and output reports.

Download Git (includes Git-Bash)
