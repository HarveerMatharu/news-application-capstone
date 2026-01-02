-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               12.1.2-MariaDB - MariaDB Server
-- Server OS:                    Win64
-- HeidiSQL Version:             12.11.0.7065
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for news_db
DROP DATABASE IF EXISTS `news_db`;
CREATE DATABASE IF NOT EXISTS `news_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `news_db`;

-- Dumping structure for table news_db.auth_group
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.auth_group: ~3 rows (approximately)
INSERT INTO `auth_group` (`id`, `name`) VALUES
	(1, 'Reader'),
	(2, 'Editor'),
	(3, 'Journalist');

-- Dumping structure for table news_db.auth_group_permissions
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.auth_group_permissions: ~17 rows (approximately)
INSERT INTO `auth_group_permissions` (`id`, `group_id`, `permission_id`) VALUES
	(1, 1, 33),
	(2, 1, 28),
	(3, 2, 32),
	(4, 2, 33),
	(5, 2, 26),
	(6, 2, 27),
	(7, 2, 28),
	(8, 2, 29),
	(9, 2, 31),
	(10, 3, 32),
	(11, 3, 33),
	(12, 3, 25),
	(13, 3, 26),
	(14, 3, 27),
	(15, 3, 28),
	(16, 3, 30),
	(17, 3, 31);

-- Dumping structure for table news_db.auth_permission
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.auth_permission: ~37 rows (approximately)
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 3, 'add_permission'),
	(6, 'Can change permission', 3, 'change_permission'),
	(7, 'Can delete permission', 3, 'delete_permission'),
	(8, 'Can view permission', 3, 'view_permission'),
	(9, 'Can add group', 2, 'add_group'),
	(10, 'Can change group', 2, 'change_group'),
	(11, 'Can delete group', 2, 'delete_group'),
	(12, 'Can view group', 2, 'view_group'),
	(13, 'Can add content type', 4, 'add_contenttype'),
	(14, 'Can change content type', 4, 'change_contenttype'),
	(15, 'Can delete content type', 4, 'delete_contenttype'),
	(16, 'Can view content type', 4, 'view_contenttype'),
	(17, 'Can add session', 5, 'add_session'),
	(18, 'Can change session', 5, 'change_session'),
	(19, 'Can delete session', 5, 'delete_session'),
	(20, 'Can view session', 5, 'view_session'),
	(21, 'Can add user', 9, 'add_user'),
	(22, 'Can change user', 9, 'change_user'),
	(23, 'Can delete user', 9, 'delete_user'),
	(24, 'Can view user', 9, 'view_user'),
	(25, 'Can add article', 6, 'add_article'),
	(26, 'Can change article', 6, 'change_article'),
	(27, 'Can delete article', 6, 'delete_article'),
	(28, 'Can view article', 6, 'view_article'),
	(29, 'Can approve article', 6, 'approve_article'),
	(30, 'Can add newsletter', 7, 'add_newsletter'),
	(31, 'Can change newsletter', 7, 'change_newsletter'),
	(32, 'Can delete newsletter', 7, 'delete_newsletter'),
	(33, 'Can view newsletter', 7, 'view_newsletter'),
	(34, 'Can add publisher', 8, 'add_publisher'),
	(35, 'Can change publisher', 8, 'change_publisher'),
	(36, 'Can delete publisher', 8, 'delete_publisher'),
	(37, 'Can view publisher', 8, 'view_publisher');

-- Dumping structure for table news_db.django_admin_log
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_news_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_news_user_id` FOREIGN KEY (`user_id`) REFERENCES `news_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.django_admin_log: ~4 rows (approximately)
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(1, '2026-01-01 16:21:49.495973', '1', 'editor1 (EDITOR)', 2, '[{"changed": {"fields": ["Role"]}}]', 9, 1),
	(2, '2026-01-01 16:22:20.793285', '2', 'journalist1 (JOURNALIST)', 1, '[{"added": {}}]', 9, 1),
	(3, '2026-01-01 16:22:34.763551', '3', 'reader1 (READER)', 1, '[{"added": {}}]', 9, 1),
	(4, '2026-01-01 16:23:04.997503', '1', 'Tech News Daily', 1, '[{"added": {}}]', 8, 1),
	(5, '2026-01-01 19:25:09.353161', '1', 'Tech News Daily', 2, '[{"changed": {"fields": ["Editors", "Journalists"]}}]', 8, 1);

-- Dumping structure for table news_db.django_content_type
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.django_content_type: ~9 rows (approximately)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(2, 'auth', 'group'),
	(3, 'auth', 'permission'),
	(4, 'contenttypes', 'contenttype'),
	(5, 'sessions', 'session'),
	(6, 'news', 'article'),
	(7, 'news', 'newsletter'),
	(8, 'news', 'publisher'),
	(9, 'news', 'user');

-- Dumping structure for table news_db.django_migrations
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.django_migrations: ~19 rows (approximately)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2026-01-01 16:19:22.021517'),
	(2, 'contenttypes', '0002_remove_content_type_name', '2026-01-01 16:19:22.047009'),
	(3, 'auth', '0001_initial', '2026-01-01 16:19:22.132791'),
	(4, 'auth', '0002_alter_permission_name_max_length', '2026-01-01 16:19:22.149591'),
	(5, 'auth', '0003_alter_user_email_max_length', '2026-01-01 16:19:22.154090'),
	(6, 'auth', '0004_alter_user_username_opts', '2026-01-01 16:19:22.158616'),
	(7, 'auth', '0005_alter_user_last_login_null', '2026-01-01 16:19:22.162673'),
	(8, 'auth', '0006_require_contenttypes_0002', '2026-01-01 16:19:22.164010'),
	(9, 'auth', '0007_alter_validators_add_error_messages', '2026-01-01 16:19:22.167401'),
	(10, 'auth', '0008_alter_user_username_max_length', '2026-01-01 16:19:22.170900'),
	(11, 'auth', '0009_alter_user_last_name_max_length', '2026-01-01 16:19:22.174848'),
	(12, 'auth', '0010_alter_group_name_max_length', '2026-01-01 16:19:22.185875'),
	(13, 'auth', '0011_update_proxy_permissions', '2026-01-01 16:19:22.190211'),
	(14, 'auth', '0012_alter_user_first_name_max_length', '2026-01-01 16:19:22.193702'),
	(15, 'news', '0001_initial', '2026-01-01 16:19:22.571258'),
	(16, 'admin', '0001_initial', '2026-01-01 16:19:22.616501'),
	(17, 'admin', '0002_logentry_remove_auto_add', '2026-01-01 16:19:22.628753'),
	(18, 'admin', '0003_logentry_add_action_flag_choices', '2026-01-01 16:19:22.638404'),
	(19, 'sessions', '0001_initial', '2026-01-01 16:19:22.654353');

-- Dumping structure for table news_db.django_session
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.django_session: ~1 rows (approximately)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('jc5bejx6oqavsjr8j5oyhutnv1khfqbj', '.eJxVjMsOwiAQRf-FtSFQOjxcuvcbyAwwUjUlKe3K-O_apAvd3nPOfYmI21rj1ssSpyzOwojT70aYHmXeQb7jfGsytXldJpK7Ig_a5bXl8rwc7t9BxV6_9cjKJFQImskpZYkLwGBcIPIGOSSrM1gCYshm0InYaR9yGEYG5zWI9wftETfV:1vbO9j:11-9SVjr0VURnfBInMF7K-uQLdAyhR04TwPXk3S7Dns', '2026-01-15 19:16:19.673440'),
	('q2l1ns6fw6815w435pn1zokc8bti8bat', '.eJxVjEEOwiAQRe_C2pAygcK4dO8ZmmEYpGogKe3KeHdt0oVu_3vvv9RE21qmrcsyzUmdlVGn3y0SP6TuIN2p3prmVtdljnpX9EG7vrYkz8vh_h0U6uVbxwEERwcwsHiwENggAGI0ziOTDymzdciWSEwQynkIaHym4B0ZHNX7A8qQN4g:1vbLcx:gUmbpgFjQ9FQl3Y8_f-fRWiKz9P3omOvXBmqCoT-wkU', '2026-01-15 16:34:19.902088');

-- Dumping structure for table news_db.news_article
DROP TABLE IF EXISTS `news_article`;
CREATE TABLE IF NOT EXISTS `news_article` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(300) NOT NULL,
  `content` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approved` tinyint(1) NOT NULL,
  `author_id` bigint(20) NOT NULL,
  `publisher_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `news_article_publisher_id_79babb86_fk_news_publisher_id` (`publisher_id`),
  KEY `news_article_author_id_11c60ced_fk_news_user_id` (`author_id`),
  CONSTRAINT `news_article_author_id_11c60ced_fk_news_user_id` FOREIGN KEY (`author_id`) REFERENCES `news_user` (`id`),
  CONSTRAINT `news_article_publisher_id_79babb86_fk_news_publisher_id` FOREIGN KEY (`publisher_id`) REFERENCES `news_publisher` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.news_article: ~2 rows (approximately)
INSERT INTO `news_article` (`id`, `title`, `content`, `created_at`, `updated_at`, `approved`, `author_id`, `publisher_id`) VALUES
	(1, 'Test', 'This is a test article', '2026-01-01 16:26:52.183033', '2026-01-01 16:29:25.600100', 1, 2, 1),
	(2, 'Test - MariaDB', 'This is a test article to verify MariaDB integration is working correctly.', '2026-01-01 16:33:47.594709', '2026-01-01 16:34:31.594998', 1, 2, 1);

-- Dumping structure for table news_db.news_newsletter
DROP TABLE IF EXISTS `news_newsletter`;
CREATE TABLE IF NOT EXISTS `news_newsletter` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(300) NOT NULL,
  `description` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `author_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `news_newsletter_author_id_53781a36_fk_news_user_id` (`author_id`),
  CONSTRAINT `news_newsletter_author_id_53781a36_fk_news_user_id` FOREIGN KEY (`author_id`) REFERENCES `news_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.news_newsletter: ~0 rows (approximately)
INSERT INTO `news_newsletter` (`id`, `title`, `description`, `created_at`, `author_id`) VALUES
	(1, 'Test Newsletter', 'This is a test newsletter', '2026-01-01 17:04:58.945485', 2);

-- Dumping structure for table news_db.news_newsletter_articles
DROP TABLE IF EXISTS `news_newsletter_articles`;
CREATE TABLE IF NOT EXISTS `news_newsletter_articles` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `newsletter_id` bigint(20) NOT NULL,
  `article_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `news_newsletter_articles_newsletter_id_article_id_b6195a5a_uniq` (`newsletter_id`,`article_id`),
  KEY `news_newsletter_articles_article_id_8411a996_fk_news_article_id` (`article_id`),
  CONSTRAINT `news_newsletter_arti_newsletter_id_aa2bcc6d_fk_news_news` FOREIGN KEY (`newsletter_id`) REFERENCES `news_newsletter` (`id`),
  CONSTRAINT `news_newsletter_articles_article_id_8411a996_fk_news_article_id` FOREIGN KEY (`article_id`) REFERENCES `news_article` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.news_newsletter_articles: ~0 rows (approximately)
INSERT INTO `news_newsletter_articles` (`id`, `newsletter_id`, `article_id`) VALUES
	(1, 1, 1),
	(2, 1, 2);

-- Dumping structure for table news_db.news_publisher
DROP TABLE IF EXISTS `news_publisher`;
CREATE TABLE IF NOT EXISTS `news_publisher` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.news_publisher: ~1 rows (approximately)
INSERT INTO `news_publisher` (`id`, `name`, `description`, `created_at`) VALUES
	(1, 'Tech News Daily', 'Technology news and updates', '2026-01-01 16:23:04.994861');

-- Dumping structure for table news_db.news_publisher_editors
DROP TABLE IF EXISTS `news_publisher_editors`;
CREATE TABLE IF NOT EXISTS `news_publisher_editors` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `publisher_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `news_publisher_editors_publisher_id_user_id_ea1697bf_uniq` (`publisher_id`,`user_id`),
  KEY `news_publisher_editors_user_id_1e2c6e95_fk_news_user_id` (`user_id`),
  CONSTRAINT `news_publisher_edito_publisher_id_b8d8fa26_fk_news_publ` FOREIGN KEY (`publisher_id`) REFERENCES `news_publisher` (`id`),
  CONSTRAINT `news_publisher_editors_user_id_1e2c6e95_fk_news_user_id` FOREIGN KEY (`user_id`) REFERENCES `news_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.news_publisher_editors: ~0 rows (approximately)
INSERT INTO `news_publisher_editors` (`id`, `publisher_id`, `user_id`) VALUES
	(1, 1, 1);

-- Dumping structure for table news_db.news_publisher_journalists
DROP TABLE IF EXISTS `news_publisher_journalists`;
CREATE TABLE IF NOT EXISTS `news_publisher_journalists` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `publisher_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `news_publisher_journalists_publisher_id_user_id_a8d66f8f_uniq` (`publisher_id`,`user_id`),
  KEY `news_publisher_journalists_user_id_cdbe38a5_fk_news_user_id` (`user_id`),
  CONSTRAINT `news_publisher_journ_publisher_id_1994a4f6_fk_news_publ` FOREIGN KEY (`publisher_id`) REFERENCES `news_publisher` (`id`),
  CONSTRAINT `news_publisher_journalists_user_id_cdbe38a5_fk_news_user_id` FOREIGN KEY (`user_id`) REFERENCES `news_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.news_publisher_journalists: ~0 rows (approximately)
INSERT INTO `news_publisher_journalists` (`id`, `publisher_id`, `user_id`) VALUES
	(1, 1, 2);

-- Dumping structure for table news_db.news_user
DROP TABLE IF EXISTS `news_user`;
CREATE TABLE IF NOT EXISTS `news_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
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
  `role` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.news_user: ~3 rows (approximately)
INSERT INTO `news_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `role`) VALUES
	(1, 'pbkdf2_sha256$1200000$uKQLNZEBCxjLWr1fwTotaR$5Qj5Sk7VPwuNUh6Gmlgzv6BhKZM6zgY8XktjN0N3Sl8=', '2026-01-01 17:05:55.137553', 1, 'editor1', '', '', 'editor@test.com', 1, 1, '2026-01-01 16:20:53.000000', 'EDITOR'),
	(2, 'pbkdf2_sha256$1200000$V47jmqGQ0SnqfMvb8Brm8I$pFyOqFtr29HJOjsy9cLYZt2zUfDHQh6C18xq5FI87SE=', '2026-01-01 17:01:52.185541', 0, 'journalist1', '', '', '', 0, 1, '2026-01-01 16:22:20.063932', 'JOURNALIST'),
	(3, 'pbkdf2_sha256$1200000$MkurHcBkFSSpxJMRK0IjnC$CkV4GEPFNTay53Db7d1cda9WPkKqYc0VBJTK8rjuqEY=', '2026-01-01 19:16:19.672072', 0, 'reader1', '', '', '', 0, 1, '2026-01-01 16:22:34.046423', 'READER');

-- Dumping structure for table news_db.news_user_groups
DROP TABLE IF EXISTS `news_user_groups`;
CREATE TABLE IF NOT EXISTS `news_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `news_user_groups_user_id_group_id_bd4e5506_uniq` (`user_id`,`group_id`),
  KEY `news_user_groups_group_id_50a63dc2_fk_auth_group_id` (`group_id`),
  CONSTRAINT `news_user_groups_group_id_50a63dc2_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `news_user_groups_user_id_9b3265f9_fk_news_user_id` FOREIGN KEY (`user_id`) REFERENCES `news_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.news_user_groups: ~3 rows (approximately)
INSERT INTO `news_user_groups` (`id`, `user_id`, `group_id`) VALUES
	(1, 1, 1),
	(2, 2, 3),
	(3, 3, 1);

-- Dumping structure for table news_db.news_user_subscribed_journalists
DROP TABLE IF EXISTS `news_user_subscribed_journalists`;
CREATE TABLE IF NOT EXISTS `news_user_subscribed_journalists` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `from_user_id` bigint(20) NOT NULL,
  `to_user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `news_user_subscribed_jou_from_user_id_to_user_id_47c81291_uniq` (`from_user_id`,`to_user_id`),
  KEY `news_user_subscribed_to_user_id_557d9a8f_fk_news_user` (`to_user_id`),
  CONSTRAINT `news_user_subscribed_from_user_id_38d4e236_fk_news_user` FOREIGN KEY (`from_user_id`) REFERENCES `news_user` (`id`),
  CONSTRAINT `news_user_subscribed_to_user_id_557d9a8f_fk_news_user` FOREIGN KEY (`to_user_id`) REFERENCES `news_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.news_user_subscribed_journalists: ~0 rows (approximately)
INSERT INTO `news_user_subscribed_journalists` (`id`, `from_user_id`, `to_user_id`) VALUES
	(1, 3, 2);

-- Dumping structure for table news_db.news_user_subscribed_publishers
DROP TABLE IF EXISTS `news_user_subscribed_publishers`;
CREATE TABLE IF NOT EXISTS `news_user_subscribed_publishers` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `publisher_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `news_user_subscribed_pub_user_id_publisher_id_206d190d_uniq` (`user_id`,`publisher_id`),
  KEY `news_user_subscribed_publisher_id_e0f211b0_fk_news_publ` (`publisher_id`),
  CONSTRAINT `news_user_subscribed_publisher_id_e0f211b0_fk_news_publ` FOREIGN KEY (`publisher_id`) REFERENCES `news_publisher` (`id`),
  CONSTRAINT `news_user_subscribed_publishers_user_id_2666438d_fk_news_user_id` FOREIGN KEY (`user_id`) REFERENCES `news_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.news_user_subscribed_publishers: ~0 rows (approximately)
INSERT INTO `news_user_subscribed_publishers` (`id`, `user_id`, `publisher_id`) VALUES
	(2, 3, 1);

-- Dumping structure for table news_db.news_user_user_permissions
DROP TABLE IF EXISTS `news_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `news_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `news_user_user_permissions_user_id_permission_id_b670b838_uniq` (`user_id`,`permission_id`),
  KEY `news_user_user_permi_permission_id_59134022_fk_auth_perm` (`permission_id`),
  CONSTRAINT `news_user_user_permi_permission_id_59134022_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `news_user_user_permissions_user_id_65dbb36a_fk_news_user_id` FOREIGN KEY (`user_id`) REFERENCES `news_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table news_db.news_user_user_permissions: ~0 rows (approximately)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
