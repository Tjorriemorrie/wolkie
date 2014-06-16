/*
 Navicat Premium Data Transfer

 Source Server         : MySQL @ localhost
 Source Server Type    : MySQL
 Source Server Version : 50617
 Source Host           : localhost
 Source Database       : kyc

 Target Server Type    : MySQL
 Target Server Version : 50617
 File Encoding         : utf-8

 Date: 06/09/2014 16:21:47 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `transactions`
-- ----------------------------
DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `transaction_date` datetime DEFAULT NULL,
  `transaction_customer_id` int(11) DEFAULT NULL,
  `account_type` varchar(255) DEFAULT NULL,
  `trans_type` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `in` float DEFAULT NULL,
  `out` float DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `international` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
