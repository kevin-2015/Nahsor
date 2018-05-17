/*
 Navicat Premium Data Transfer

 Source Server         : 本机
 Source Server Type    : MySQL
 Source Server Version : 50722
 Source Host           : localhost:3306
 Source Schema         : nahsor

 Target Server Type    : MySQL
 Target Server Version : 50722
 File Encoding         : 65001

 Date: 17/05/2018 23:51:14
*/

DROP DATABASE IF EXISTS nahsor;
CREATE DATABASE nahsor DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;

USE nahsor;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_config
-- ----------------------------
DROP TABLE IF EXISTS `t_config`;
CREATE TABLE `t_config`  (
  `id` int(11) NOT NULL,
  `url` json NULL,
  `headers` json NULL,
  `method` json NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for t_modules
-- ----------------------------
DROP TABLE IF EXISTS `t_modules`;
CREATE TABLE `t_modules`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `projectid` int(16) NOT NULL COMMENT '所属项目id',
  `modules` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '模块名称',
  `explain` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '描述',
  `leader` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '负责人',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `createtime` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `updatatime` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `modules`(`modules`) USING BTREE,
  INDEX `project`(`projectid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_modules
-- ----------------------------
INSERT INTO `t_modules` VALUES (1, 1, 'WEB模块1', 'WEB端测试模块1', '浪晋', '备注', '2018-05-17 21:47:48', '2018-05-17 21:47:48');
INSERT INTO `t_modules` VALUES (6, 1, 'WEB模块2', 'WEB端测试模块2', 'snake', '备注', '2018-05-17 21:47:52', '2018-05-17 21:47:52');
INSERT INTO `t_modules` VALUES (7, 6, 'APP模块1', 'APP端测试模块1', 'snake', '备注', '2018-05-17 21:47:52', '2018-05-17 21:47:52');
INSERT INTO `t_modules` VALUES (8, 6, 'APP模块2', 'APP端测试模块2', 'snake', '备注', '2018-05-17 21:47:52', '2018-05-17 21:47:52');

-- ----------------------------
-- Table structure for t_product
-- ----------------------------
DROP TABLE IF EXISTS `t_product`;
CREATE TABLE `t_product`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `product` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '产品名称',
  `explain` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '负责人',
  `leader` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '状态，0可用，1不可用',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '说明，描述',
  `createtime` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `updatatime` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `product`(`product`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_product
-- ----------------------------
INSERT INTO `t_product` VALUES (1, 'Nahsor自动化测试平台', '一个接口自动化测试平台，功能强大，很厉害就是了。', '浪晋', '这是例子', '2018-05-11 05:41:08', '2018-05-11 05:41:08');

-- ----------------------------
-- Table structure for t_project
-- ----------------------------
DROP TABLE IF EXISTS `t_project`;
CREATE TABLE `t_project`  (
  `id` int(16) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `productid` int(16) NOT NULL COMMENT '关联的产品id',
  `project` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '项目名称',
  `explain` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '描述',
  `leader` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '负责人',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `createtime` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `updatatime` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `project`(`project`) USING BTREE,
  INDEX `product`(`productid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_project
-- ----------------------------
INSERT INTO `t_project` VALUES (1, 1, 'WEB项目', 'WEB端', '浪晋', '备注', '2018-05-17 21:48:25', '2018-05-17 21:48:25');
INSERT INTO `t_project` VALUES (6, 1, 'APP项目', 'APP端', 'snake', '备注', '2018-05-17 21:48:21', '2018-05-17 21:48:21');

-- ----------------------------
-- Table structure for t_reports
-- ----------------------------
DROP TABLE IF EXISTS `t_reports`;
CREATE TABLE `t_reports`  (
  `id` int(16) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `cassid` int(16) NOT NULL COMMENT '用例id',
  `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '状态，成功 失败 报错',
  `runtime` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '接口运行的耗时',
  `result` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '执行结果',
  `validate` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '校验结果',
  `createtime` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '运行时间',
  `version` int(255) NULL DEFAULT NULL COMMENT '运行版本',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 52 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_reports
-- ----------------------------
INSERT INTO `t_reports` VALUES (27, 2, '成功', '0.00298', '{\n  \"code\": 200, \n  \"data\": \"sjdh34gsalked23nlsakn45dudaj\", \n  \"msg\": \"u767bu9646u6210u529f\"\n}\n', 'r.status_code==200', '2018-05-17 23:24:14', 1);
INSERT INTO `t_reports` VALUES (28, 3, '成功', '0.00202', '{\n  \"code\": 200, \n  \"msg\": \"u64cdu4f5cu6210u529f\"\n}\n', 'r.status_code==200', '2018-05-17 23:24:14', 1);
INSERT INTO `t_reports` VALUES (29, 2, '成功', '0.001969', '{\n  \"code\": 200, \n  \"data\": \"sjdh34gsalked23nlsakn45dudaj\", \n  \"msg\": \"u767bu9646u6210u529f\"\n}\n', 'r.status_code==200', '2018-05-17 23:24:14', 2);
INSERT INTO `t_reports` VALUES (30, 3, '成功', '0.012585', '{\n  \"code\": 200, \n  \"msg\": \"u64cdu4f5cu6210u529f\"\n}\n', 'r.status_code==200', '2018-05-17 23:24:14', 2);
INSERT INTO `t_reports` VALUES (31, 2, '成功', '0.011257', '{\n  \"code\": 200, \n  \"data\": \"sjdh34gsalked23nlsakn45dudaj\", \n  \"msg\": \"登陆成功\"\n}\n', 'r.status_code==200', '2018-05-17 23:24:14', 3);
INSERT INTO `t_reports` VALUES (32, 3, '成功', '0.012227', '{\n  \"code\": 200, \n  \"msg\": \"操作成功\"\n}\n', 'r.status_code==200', '2018-05-17 23:24:14', 3);
INSERT INTO `t_reports` VALUES (33, 1, '报错', '', '', '', '2018-05-17 23:24:19', 4);
INSERT INTO `t_reports` VALUES (34, 1, '报错', '', '', '', '2018-05-17 23:25:38', 5);
INSERT INTO `t_reports` VALUES (35, 1, '报错', '', '', '', '2018-05-17 23:27:08', 6);
INSERT INTO `t_reports` VALUES (36, 1, '报错', '', '', '', '2018-05-17 23:27:51', 7);
INSERT INTO `t_reports` VALUES (37, 2, '报错', '', '', '', '2018-05-17 23:27:52', 7);
INSERT INTO `t_reports` VALUES (38, 3, '报错', '', '', '', '2018-05-17 23:27:52', 7);
INSERT INTO `t_reports` VALUES (39, 4, '报错', '', '', '', '2018-05-17 23:27:53', 7);
INSERT INTO `t_reports` VALUES (40, 5, '报错', '', '', '', '2018-05-17 23:27:53', 7);
INSERT INTO `t_reports` VALUES (41, 6, '报错', '', '', '', '2018-05-17 23:27:54', 7);
INSERT INTO `t_reports` VALUES (42, 7, '报错', '', '', '', '2018-05-17 23:27:54', 7);
INSERT INTO `t_reports` VALUES (43, 1, '成功', '0.002132', '{\n  \"aaa\": \"bbb\"\n}\n', 'r.status_code==200', '2018-05-17 23:32:12', 8);
INSERT INTO `t_reports` VALUES (44, 2, '成功', '0.001833', '{\n  \"code\": 200, \n  \"data\": \"sjdh34gsalked23nlsakn45dudaj\", \n  \"msg\": \"登陆成功\"\n}\n', 'r.status_code==200', '2018-05-17 23:32:12', 8);
INSERT INTO `t_reports` VALUES (45, 3, '成功', '0.001755', '{\n  \"code\": 200, \n  \"msg\": \"操作成功\"\n}\n', 'r.status_code==200', '2018-05-17 23:32:12', 8);
INSERT INTO `t_reports` VALUES (46, 4, '成功', '0.01259', '{\n  \"code\": 200, \n  \"data\": \"sjdh34gsalked23nlsakn45dudaj\", \n  \"msg\": \"登陆成功\"\n}\n', 'r.status_code==200', '2018-05-17 23:32:12', 8);
INSERT INTO `t_reports` VALUES (47, 5, '成功', '0.002564', '{\n  \"code\": 200, \n  \"msg\": \"操作成功\"\n}\n', 'r.status_code==200', '2018-05-17 23:32:12', 8);
INSERT INTO `t_reports` VALUES (48, 6, '成功', '0.006704', '{\n  \"code\": 200, \n  \"data\": \"sjdh34gsalked23nlsakn45dudaj\", \n  \"msg\": \"登陆成功\"\n}\n', 'r.status_code==200', '2018-05-17 23:32:12', 8);
INSERT INTO `t_reports` VALUES (49, 7, '成功', '0.00197', '{\n  \"code\": 200, \n  \"msg\": \"操作成功\"\n}\n', 'r.status_code==200', '2018-05-17 23:32:12', 8);
INSERT INTO `t_reports` VALUES (50, 1, '成功', '0.013385', '{\n  \"aaa\": \"bbb\"\n}\n', 'r.status_code==200', '2018-05-17 23:48:14', 9);
INSERT INTO `t_reports` VALUES (51, 1, '报错', '', '', '', '2018-05-17 23:49:42', 10);

-- ----------------------------
-- Table structure for t_testcass
-- ----------------------------
DROP TABLE IF EXISTS `t_testcass`;
CREATE TABLE `t_testcass`  (
  `id` int(16) NOT NULL AUTO_INCREMENT,
  `moduleid` int(16) NOT NULL COMMENT '所属模块id',
  `testname` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用例名称',
  `testtype` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用例类型',
  `explain` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用例描述',
  `request` json NOT NULL COMMENT '请求参数',
  `validate` json NULL COMMENT '校验参数',
  `extract` json NULL COMMENT '提取参数',
  `leader` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '负责人',
  `remark` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '备注',
  `createtime` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `updatatime` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_testcass
-- ----------------------------
INSERT INTO `t_testcass` VALUES (1, 1, 'WEB模块1的接口测试用例1', 'testcass', '测试输入和输出是否一致', '{\"url\": \"http://127.0.0.1:2333/test\", \"json\": {\"aaa\": \"bbb\"}, \"method\": \"POST\", \"headers\": {\"Content-Type\": \"application/json\"}, \"timeout\": 10}', '[{\"Equal\": [\"r.json()\", \"request[\\\"json\\\"]\"]}, {\"Equal\": [\"r.status_code\", \"200\"]}]', '{}', 'LangJin', '备注信息', '2018-05-17 22:10:44', '2018-05-17 22:10:44');
INSERT INTO `t_testcass` VALUES (2, 6, 'WEB模块2的接口测试用例1', 'testsuite', '获取token', '{\"url\": \"http://127.0.0.1:2333/login\", \"json\": {\"password\": \"123456\", \"username\": \"admin\"}, \"method\": \"POST\", \"headers\": {\"Content-Type\": \"application/json\"}, \"timeout\": 10}', '[{\"Equal\": [\"r.status_code\", \"200\"]}]', '[{\"token\": \"r.json()[\\\"data\\\"]\"}]', 'LangJin', '备注信息', '2018-05-17 22:10:52', '2018-05-17 22:10:52');
INSERT INTO `t_testcass` VALUES (3, 6, 'WEB模块2的接口测试用例2', 'testsuite', '传入token', '{\"url\": \"http://127.0.0.1:2333/chicktoken\", \"json\": {\"token\": \"$token\"}, \"method\": \"POST\", \"headers\": {\"Content-Type\": \"application/json\"}, \"timeout\": 10}', '[{\"Equal\": [\"r.status_code\", \"200\"]}]', '[]', 'LangJin', '备注信息', '2018-05-17 22:10:54', '2018-05-17 22:10:54');
INSERT INTO `t_testcass` VALUES (4, 7, 'APP模块1的接口测试用例1', 'testsuite', '获取token', '{\"url\": \"http://127.0.0.1:2333/login\", \"json\": {\"password\": \"123456\", \"username\": \"admin\"}, \"method\": \"POST\", \"headers\": {\"Content-Type\": \"application/json\"}, \"timeout\": 10}', '[{\"Equal\": [\"r.status_code\", \"200\"]}]', '[{\"token\": \"r.json()[\\\"data\\\"]\"}]', 'LangJin', '备注信息', '2018-05-17 22:10:42', '2018-05-17 22:10:42');
INSERT INTO `t_testcass` VALUES (5, 7, 'APP模块1的接口测试用例2', 'testsuite', '传入token', '{\"url\": \"http://127.0.0.1:2333/chicktoken\", \"json\": {\"token\": \"$token\"}, \"method\": \"POST\", \"headers\": {\"Content-Type\": \"application/json\"}, \"timeout\": 10}', '[{\"Equal\": [\"r.status_code\", \"200\"]}]', '[]', 'LangJin', '备注信息', '2018-05-17 22:10:40', '2018-05-17 22:10:40');
INSERT INTO `t_testcass` VALUES (6, 8, 'APP模块2的接口测试用例1', 'testsuite', '获取token', '{\"url\": \"http://127.0.0.1:2333/login\", \"json\": {\"password\": \"123456\", \"username\": \"admin\"}, \"method\": \"POST\", \"headers\": {\"Content-Type\": \"application/json\"}, \"timeout\": 10}', '[{\"Equal\": [\"r.status_code\", \"200\"]}]', '[{\"token\": \"r.json()[\\\"data\\\"]\"}]', 'LangJin', '备注信息', '2018-05-17 22:08:20', '2018-05-17 22:08:20');
INSERT INTO `t_testcass` VALUES (7, 8, 'APP模块2的接口测试用例2', 'testsuite', '传入token', '{\"url\": \"http://127.0.0.1:2333/chicktoken\", \"json\": {\"token\": \"$token\"}, \"method\": \"POST\", \"headers\": {\"Content-Type\": \"application/json\"}, \"timeout\": 10}', '[{\"Equal\": [\"r.status_code\", \"200\"]}]', '[]', 'LangJin', '备注信息', '2018-05-17 22:08:24', '2018-05-17 22:08:24');

SET FOREIGN_KEY_CHECKS = 1;
