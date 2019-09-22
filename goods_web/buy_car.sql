/*
Navicat MySQL Data Transfer

Source Server         : zzy
Source Server Version : 50727
Source Host           : localhost:3306
Source Database       : user

Target Server Type    : MYSQL
Target Server Version : 50727
File Encoding         : 65001

Date: 2019-09-22 13:46:34
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for buy_car
-- ----------------------------
DROP TABLE IF EXISTS `buy_car`;
CREATE TABLE `buy_car` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `uname` varchar(255) NOT NULL,
  `goods_name` varchar(255) NOT NULL,
  `goods_num` varchar(255) NOT NULL,
  `goods_price` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of buy_car
-- ----------------------------
INSERT INTO `buy_car` VALUES ('7', 'zzy123456', '辣条', '2', '0.50');
INSERT INTO `buy_car` VALUES ('8', 'zzy123456', '可乐', '3', '4.00');
INSERT INTO `buy_car` VALUES ('9', 'zzy123456', '豆奶', '3', '5.00');
INSERT INTO `buy_car` VALUES ('10', 'zzy1234567', '辣条', '1', '0.50');
INSERT INTO `buy_car` VALUES ('11', 'zzy1234567', '饼干', '4', '6.00');
