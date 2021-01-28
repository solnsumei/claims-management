-- upgrade --
CREATE TABLE IF NOT EXISTS `departments` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `created_at` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `status` VARCHAR(8) NOT NULL  COMMENT 'ACTIVE: active\nINACTIVE: inactive' DEFAULT 'active',
    `name` VARCHAR(70) NOT NULL UNIQUE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `users` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `created_at` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `status` VARCHAR(8) NOT NULL  COMMENT 'ACTIVE: active\nINACTIVE: inactive' DEFAULT 'active',
    `name` VARCHAR(50) NOT NULL,
    `username` VARCHAR(30) NOT NULL UNIQUE,
    `email` VARCHAR(50) NOT NULL UNIQUE,
    `password` VARCHAR(250) NOT NULL,
    `is_admin` BOOL NOT NULL  DEFAULT 0,
    `role` VARCHAR(10) NOT NULL  COMMENT 'Admin: Admin\nManager: Manager\nStaff: Staff\nContractor: Contractor' DEFAULT 'Staff',
    `uses_default_password` BOOL NOT NULL  DEFAULT 1,
    `department_id` CHAR(36),
    CONSTRAINT `fk_users_departme_31a8aa1c` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `projects` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `created_at` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `status` VARCHAR(8) NOT NULL  COMMENT 'ACTIVE: active\nINACTIVE: inactive' DEFAULT 'active',
    `name` VARCHAR(70) NOT NULL,
    `code` VARCHAR(15) NOT NULL UNIQUE,
    `description` LONGTEXT NOT NULL,
    `budget` DECIMAL(12,2) NOT NULL,
    `duration` INT NOT NULL,
    `department_id` CHAR(36),
    `manager_id` CHAR(36) NOT NULL,
    CONSTRAINT `fk_projects_departme_30001828` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_projects_users_20418afb` FOREIGN KEY (`manager_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `claims` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `created_at` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `title` VARCHAR(100) NOT NULL,
    `claim_id` VARCHAR(20) NOT NULL UNIQUE,
    `invoice_no` VARCHAR(12) NOT NULL UNIQUE,
    `description` LONGTEXT NOT NULL,
    `amount` DECIMAL(12,2) NOT NULL,
    `approval_date` DATE,
    `payment_date` DATE,
    `file_url` VARCHAR(255) NOT NULL UNIQUE,
    `status` VARCHAR(9) NOT NULL  COMMENT 'New: New\nPending: Pending\nApproved: Approved\nPaid: Paid\nCancelled: Cancelled' DEFAULT 'New',
    `remark` LONGTEXT,
    `department_id` CHAR(36),
    `user_id` CHAR(36) NOT NULL,
    `project_id` CHAR(36),
    CONSTRAINT `fk_claims_departme_d76e8ead` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_claims_users_77a83080` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_claims_projects_652d5db7` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(20) NOT NULL,
    `content` LONGTEXT NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `projects_users` (
    `projects_id` CHAR(36) NOT NULL,
    `user_id` CHAR(36) NOT NULL,
    FOREIGN KEY (`projects_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
