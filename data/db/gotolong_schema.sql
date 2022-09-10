-- MariaDB dump 10.18  Distrib 10.5.8-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: gotolong
-- ------------------------------------------------------
-- Server version	10.5.8-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `both_lastrefd`
--

DROP TABLE IF EXISTS `both_lastrefd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `both_lastrefd` (
  `lastrefd_module` varchar(50) DEFAULT NULL,
  `lastrefd_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `broker_mf`
--

DROP TABLE IF EXISTS `broker_mf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `broker_mf` (
  `bmf_id` int(11) DEFAULT NULL,
  `bmf_user_id` int(11) DEFAULT NULL,
  `bmf_broker` text DEFAULT NULL,
  `bmf_amc` text DEFAULT NULL,
  `bmf_name` text DEFAULT NULL,
  `bmf_category` text DEFAULT NULL,
  `bmf_subcat` text DEFAULT NULL,
  `bmf_rating` text DEFAULT NULL,
  `bmf_units` float DEFAULT NULL,
  `bmf_acp` float DEFAULT NULL,
  `bmf_cost_value` float DEFAULT NULL,
  `bmf_nav_date` text DEFAULT NULL,
  `bmf_nav` float DEFAULT NULL,
  `bmf_nav_value` float DEFAULT NULL,
  `bmf_pnl_realized` float DEFAULT NULL,
  `bmf_pnl` float DEFAULT NULL,
  `bmf_pnl_pct` float DEFAULT NULL,
  `bmf_research_reco` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `broker_sum`
--

DROP TABLE IF EXISTS `broker_sum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `broker_sum` (
  `bs_id` int(11) DEFAULT NULL,
  `bs_user_id` int(11) DEFAULT NULL,
  `bs_broker` text DEFAULT NULL,
  `bs_stock_symbol` text DEFAULT NULL,
  `bs_company_name` text DEFAULT NULL,
  `bs_isin_code_id` text DEFAULT NULL,
  `bs_qty` int(11) DEFAULT NULL,
  `bs_acp` float DEFAULT NULL,
  `bs_cmp` text DEFAULT NULL,
  `bs_pct_change` text DEFAULT NULL,
  `bs_value_cost` float DEFAULT NULL,
  `bs_value_market` float DEFAULT NULL,
  `bs_days_gain` text DEFAULT NULL,
  `bs_days_gain_pct` text DEFAULT NULL,
  `bs_realized_pl` text DEFAULT NULL,
  `bs_unrealized_pl` text DEFAULT NULL,
  `bs_unrealized_pl_pct` text DEFAULT NULL,
  `bs_unused1` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `broker_txn`
--

DROP TABLE IF EXISTS `broker_txn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `broker_txn` (
  `bt_id` int(11) DEFAULT NULL,
  `bt_user_id` int(11) DEFAULT NULL,
  `bt_broker` text DEFAULT NULL,
  `bt_stock_symbol` text DEFAULT NULL,
  `bt_company_name` text DEFAULT NULL,
  `bt_isin_code` text DEFAULT NULL,
  `bt_action` text DEFAULT NULL,
  `bt_quantity` int(11) DEFAULT NULL,
  `bt_txn_price` float DEFAULT NULL,
  `bt_brokerage` text DEFAULT NULL,
  `bt_txn_charges` text DEFAULT NULL,
  `bt_stamp_duty` text DEFAULT NULL,
  `bt_segment` text DEFAULT NULL,
  `bt_stt` text DEFAULT NULL,
  `bt_remarks` text DEFAULT NULL,
  `bt_txn_date` date DEFAULT NULL,
  `bt_exchange` text DEFAULT NULL,
  `bt_unused1` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `broker_zerodha_sum`
--

DROP TABLE IF EXISTS `broker_zerodha_sum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `broker_zerodha_sum` (
  `bzs_id` int(11) DEFAULT NULL,
  `bzs_user_id` int(11) DEFAULT NULL,
  `bzs_instrument` text DEFAULT NULL,
  `bzs_quantity` int(11) DEFAULT NULL,
  `bzs_average_cost` float DEFAULT NULL,
  `bzs_ltp` float DEFAULT NULL,
  `bzs_cur_value` float DEFAULT NULL,
  `bzs_pnl` float DEFAULT NULL,
  `bzs_net_chg` float DEFAULT NULL,
  `bzs_day_chg` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `broker_zerodha_txn`
--

DROP TABLE IF EXISTS `broker_zerodha_txn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `broker_zerodha_txn` (
  `bzt_id` int(11) DEFAULT NULL,
  `bzt_user_id` int(11) DEFAULT NULL,
  `bzt_tdate` date DEFAULT NULL,
  `bzt_tsymbol` text DEFAULT NULL,
  `bzt_exchange` text DEFAULT NULL,
  `bzt_segment` text DEFAULT NULL,
  `bzt_trade_type` text DEFAULT NULL,
  `bzt_quantity` float DEFAULT NULL,
  `bzt_price` text DEFAULT NULL,
  `bzt_order_id` text DEFAULT NULL,
  `bzt_trade_id` text DEFAULT NULL,
  `bzt_order_exec_time` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cadmin_cadmin`
--

DROP TABLE IF EXISTS `cadmin_cadmin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cadmin_cadmin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cadmin_xyz` longtext DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `global_amfi`
--

DROP TABLE IF EXISTS `global_amfi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `global_amfi` (
  `comp_rank` int(11) DEFAULT NULL,
  `comp_name` text DEFAULT NULL,
  `comp_isin` text DEFAULT NULL,
  `bse_symbol` text DEFAULT NULL,
  `nse_symbol` text DEFAULT NULL,
  `mse_symbol` text DEFAULT NULL,
  `avg_mcap` text DEFAULT NULL,
  `cap_type` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `global_bhav`
--

DROP TABLE IF EXISTS `global_bhav`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `global_bhav` (
  `bhav_ticker` varchar(50) DEFAULT NULL,
  `bhav_price` float DEFAULT NULL,
  `bhav_isin` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `global_bucc`
--

DROP TABLE IF EXISTS `global_bucc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `global_bucc` (
  `bucc_id` int(11) DEFAULT NULL,
  `bucc_name` varchar(256) DEFAULT NULL,
  `bucc_value` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `global_corpact`
--

DROP TABLE IF EXISTS `global_corpact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `global_corpact` (
  `ca_ticker` text DEFAULT NULL,
  `ca_total` int(11) DEFAULT NULL,
  `ca_bonus` int(11) DEFAULT NULL,
  `ca_buyback` int(11) DEFAULT NULL,
  `ca_dividend` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `global_cweight`
--

DROP TABLE IF EXISTS `global_cweight`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `global_cweight` (
  `gcw_cap_type` text DEFAULT NULL,
  `gcw_cap_weight` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `global_gmutfun`
--

DROP TABLE IF EXISTS `global_gmutfun`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `global_gmutfun` (
  `gmutfun_scheme` text DEFAULT NULL,
  `gmutfun_type` text DEFAULT NULL,
  `gmutfun_benchmark` text DEFAULT NULL,
  `gmutfun_aum` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `global_fratio`
--

DROP TABLE IF EXISTS `global_fratio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `global_fratio` (
  `fratio_name` text DEFAULT NULL,
  `fratio_buy` float DEFAULT NULL,
  `fratio_hold` float DEFAULT NULL,
  `fratio_enabled` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `global_ftwhl`
--

DROP TABLE IF EXISTS `global_ftwhl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `global_ftwhl` (
  `ftwhl_ticker` text DEFAULT NULL,
  `ftwhl_high` float DEFAULT NULL,
  `ftwhl_high_dt` text DEFAULT NULL,
  `ftwhl_low` float DEFAULT NULL,
  `ftwhl_low_dt` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `global_funda_reco`
--

DROP TABLE IF EXISTS `global_funda_reco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `global_funda_reco` (
  `funda_reco_ticker` text DEFAULT NULL,
  `funda_reco_isin` text DEFAULT NULL,
  `funda_reco_type` text DEFAULT NULL,
  `funda_reco_cause` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `global_indices`
--

DROP TABLE IF EXISTS `global_indices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `global_indices` (
  `ind_name` text DEFAULT NULL,
  `ind_industry` text DEFAULT NULL,
  `ind_ticker` text DEFAULT NULL,
  `ind_series` text DEFAULT NULL,
  `ind_isin` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `global_nach`
--

DROP TABLE IF EXISTS `global_nach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `global_nach` (
  `name` text DEFAULT NULL,
  `ticker` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `global_paytxn`
--

DROP TABLE IF EXISTS `global_paytxn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `global_paytxn` (
  `pt_made_by` int(11) DEFAULT NULL,
  `pt_made_on` text DEFAULT NULL,
  `pt_amount` int(11) DEFAULT NULL,
  `pt_order_id` text DEFAULT NULL,
  `pt_checksum` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `global_trendlyne`
--

DROP TABLE IF EXISTS `global_trendlyne`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `global_trendlyne` (
  `tl_stock_name` text DEFAULT NULL,
  `tl_nse` text DEFAULT NULL,
  `tl_isin` text DEFAULT NULL,
  `tl_bat` float DEFAULT NULL,
  `tl_der` float DEFAULT NULL,
  `tl_roce3` float DEFAULT NULL,
  `tl_roe3` float DEFAULT NULL,
  `tl_dpr2` float DEFAULT NULL,
  `tl_sales2` float DEFAULT NULL,
  `tl_profit5` float DEFAULT NULL,
  `tl_icr` float DEFAULT NULL,
  `tl_pledge` float DEFAULT NULL,
  `tl_low_3y` float DEFAULT NULL,
  `tl_low_5y` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `plan`
--

DROP TABLE IF EXISTS `plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `plan` (
  `comp_industry` text DEFAULT NULL,
  `comp_name` text DEFAULT NULL,
  `comp_ticker` text DEFAULT NULL,
  `comp_selected` text DEFAULT NULL,
  `comp_desc` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `screener`
--

DROP TABLE IF EXISTS `screener`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `screener` (
  `name` text DEFAULT NULL,
  `bse_code` text DEFAULT NULL,
  `nse_code` text DEFAULT NULL,
  `industry` text DEFAULT NULL,
  `cmp` text DEFAULT NULL,
  `filter` text DEFAULT NULL,
  `filter_52w_low` text DEFAULT NULL,
  `up_52w_low` text DEFAULT NULL,
  `low_52w` text DEFAULT NULL,
  `high_52w` text DEFAULT NULL,
  `sales` text DEFAULT NULL,
  `np` text DEFAULT NULL,
  `mcap` text DEFAULT NULL,
  `d2e` text DEFAULT NULL,
  `roe3` text DEFAULT NULL,
  `roce3` text DEFAULT NULL,
  `dp3` text DEFAULT NULL,
  `pe` text DEFAULT NULL,
  `pe5` text DEFAULT NULL,
  `peg` text DEFAULT NULL,
  `opm` text DEFAULT NULL,
  `icr` text DEFAULT NULL,
  `ev` text DEFAULT NULL,
  `nw` text DEFAULT NULL,
  `reserves` text DEFAULT NULL,
  `roa3` text DEFAULT NULL,
  `p2bv` text DEFAULT NULL,
  `p2ocf` text DEFAULT NULL,
  `p2sales` text DEFAULT NULL,
  `ev2ebitda` text DEFAULT NULL,
  `dp` text DEFAULT NULL,
  `dy` text DEFAULT NULL,
  `cr` text DEFAULT NULL,
  `sales5` text DEFAULT NULL,
  `profit5` text DEFAULT NULL,
  `pledge` text DEFAULT NULL,
  `prom_hold` text DEFAULT NULL,
  `piotski` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_bstmt_div`
--

DROP TABLE IF EXISTS `user_bstmt_div`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_bstmt_div` (
  `bsdiv_id` int(11) NOT NULL AUTO_INCREMENT,
  `bsdiv_user_id` int(11) NOT NULL DEFAULT 0,
  `bsdiv_date` date DEFAULT NULL,
  `bsdiv_remarks` text DEFAULT NULL,
  `bsdiv_amount` float DEFAULT NULL,
  UNIQUE KEY `id` (`bsdiv_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=210623 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_demat_sum`
--

DROP TABLE IF EXISTS `user_demat_sum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_demat_sum` (
  `ds_id` int(11) DEFAULT NULL,
  `ds_user_id` int(11) DEFAULT NULL,
  `ds_broker` text DEFAULT NULL,
  `ds_ticker` text DEFAULT NULL,
  `ds_isin` text DEFAULT NULL,
  `ds_qty` int(11) DEFAULT NULL,
  `ds_acp` int(11) DEFAULT NULL,
  `ds_costvalue` float DEFAULT NULL,
  `ds_mktvalue` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_demat_txn`
--

DROP TABLE IF EXISTS `user_demat_txn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_demat_txn` (
  `dt_id` int(11) DEFAULT NULL,
  `dt_user_id` int(11) DEFAULT NULL,
  `dt_broker` text DEFAULT NULL,
  `dt_ticker` text DEFAULT NULL,
  `dt_isin` text DEFAULT NULL,
  `dt_action` text DEFAULT NULL,
  `dt_quantity` int(11) DEFAULT NULL,
  `dt_price` float DEFAULT NULL,
  `dt_amount` float DEFAULT NULL,
  `dt_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_dividend`
--

DROP TABLE IF EXISTS `user_dividend`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_dividend` (
  `divi_id` int(11) NOT NULL AUTO_INCREMENT,
  `divi_user_id` int(11) NOT NULL DEFAULT 0,
  `divi_date` date DEFAULT NULL,
  `divi_remarks` text DEFAULT NULL,
  `divi_company` text DEFAULT NULL,
  `divi_ticker` text DEFAULT NULL,
  `divi_amount` float DEFAULT NULL,
  `divi_score` float DEFAULT NULL,
  UNIQUE KEY `id` (`divi_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=210623 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_doc`
--

DROP TABLE IF EXISTS `user_doc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_doc` (
  `uploaddoc_id` int(11) NOT NULL AUTO_INCREMENT,
  `uploaddoc_scope` text DEFAULT NULL,
  `uploaddoc_type` text DEFAULT NULL,
  `uploaddoc_year` text DEFAULT NULL,
  `uploaddoc_fpath` text DEFAULT NULL,
  PRIMARY KEY (`uploaddoc_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_iweight`
--

DROP TABLE IF EXISTS `user_iweight`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_iweight` (
  `uiw_user_id` int(11) DEFAULT NULL,
  `uiw_name` text DEFAULT NULL,
  `uiw_value` double DEFAULT NULL,
  `uiw_value_pct` double DEFAULT NULL,
  `uiw_constituents` tinyint(4) DEFAULT NULL,
  `uiw_tickers` text DEFAULT NULL,
  `uiw_companies` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_mufu`
--

DROP TABLE IF EXISTS `user_mufu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_mufu` (
  `mf_id` int(11) DEFAULT NULL,
  `mf_user_id` int(11) DEFAULT NULL,
  `mf_broker` text DEFAULT NULL,
  `mf_amc` text DEFAULT NULL,
  `mf_name` text DEFAULT NULL,
  `mf_category` text DEFAULT NULL,
  `mf_subcat` text DEFAULT NULL,
  `mf_rating` text DEFAULT NULL,
  `mf_cost_value` float DEFAULT NULL,
  `mf_nav_value` float DEFAULT NULL,
  `mf_research_reco` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_othinv`
--

DROP TABLE IF EXISTS `user_othinv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_othinv` (
  `othinv_id` int(11) DEFAULT NULL,
  `othinv_user_id` int(11) DEFAULT NULL,
  `othinv_name` text DEFAULT NULL,
  `othinv_details` text DEFAULT NULL,
  `othinv_equity` float DEFAULT NULL,
  `othinv_debt` float DEFAULT NULL,
  `othinv_gold` float DEFAULT NULL,
  `othinv_intl` float DEFAULT NULL,
  `othinv_realty` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-08-26 21:27:27
