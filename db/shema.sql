-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'prog's'
-- 
-- ---

DROP TABLE IF EXISTS `prog's`;
		
CREATE TABLE `prog's` (
  `p_id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `name` MEDIUMTEXT NULL DEFAULT NULL,
  `s_id` MEDIUMTEXT NULL DEFAULT NULL,
  `t_id` INTEGER NULL DEFAULT NULL,
  `run_status` INTEGER NULL DEFAULT NULL,
  `result_status` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`p_id`)
);

-- ---
-- Table 'syntax'
-- 
-- ---

DROP TABLE IF EXISTS `syntax`;
		
CREATE TABLE `syntax` (
  `s_id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `err_data` MEDIUMTEXT NULL DEFAULT NULL,
  `date` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`s_id`)
);

-- ---
-- Table 'traceback'
-- 
-- ---

DROP TABLE IF EXISTS `traceback`;
		
CREATE TABLE `traceback` (
  `t_id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `err_data` MEDIUMTEXT NULL DEFAULT NULL,
  `date` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`t_id`)
);

-- ---
-- Table 'reports'
-- 
-- ---

DROP TABLE IF EXISTS `reports`;
		
CREATE TABLE `reports` (
  `rep_id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `name_prog` INTEGER NULL DEFAULT NULL,
  `data` INTEGER NULL DEFAULT NULL,
  PRIMARY KEY (`rep_id`)
);

-- ---
-- Foreign Keys 
-- ---

ALTER TABLE `prog's` ADD FOREIGN KEY (s_id) REFERENCES `syntax` (`s_id`);
ALTER TABLE `prog's` ADD FOREIGN KEY (t_id) REFERENCES `traceback` (`t_id`);

-- ---
-- Table Properties
-- ---

-- ALTER TABLE `prog's` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `syntax` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `traceback` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `reports` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `prog's` (`p_id`,`name`,`s_id`,`t_id`,`run_status`,`result_status`) VALUES
-- ('','','','','','');
-- INSERT INTO `syntax` (`s_id`,`err_data`,`date`) VALUES
-- ('','','');
-- INSERT INTO `traceback` (`t_id`,`err_data`,`date`) VALUES
-- ('','','');
-- INSERT INTO `reports` (`rep_id`,`name_prog`,`data`) VALUES
-- ('','','');