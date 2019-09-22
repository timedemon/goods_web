/*
Navicat MySQL Data Transfer

Source Server         : zzy
Source Server Version : 50727
Source Host           : localhost:3306
Source Database       : user

Target Server Type    : MYSQL
Target Server Version : 50727
File Encoding         : 65001

Date: 2019-09-22 13:46:24
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for shop_user
-- ----------------------------
DROP TABLE IF EXISTS `shop_user`;
CREATE TABLE `shop_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uname` varchar(255) NOT NULL,
  `passwd` varchar(255) NOT NULL,
  `sex` varchar(255) NOT NULL,
  `interest` varchar(255) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `birth` varchar(255) NOT NULL,
  `edu` varchar(255) NOT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of shop_user
-- ----------------------------
INSERT INTO `shop_user` VALUES ('1', 'zzy123456', 'e10adc3949ba59abbe56e057f20f883e', '男', '足球', '123456@qq.com', '1997年9月20', '本科');
INSERT INTO `shop_user` VALUES ('2', 'zzy12345', '123456', 'man', 'on', '123456@qq.com', '2019-09-08', '本科');
INSERT INTO `shop_user` VALUES ('8', 'zzy1234567', 'e10adc3949ba59abbe56e057f20f883e', '男', '篮球', '123456@qq.com', '2019-09-10', '本科');
