BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "employees" (
	"id"	INTEGER,
	"first_name"	TEXT NOT NULL,
	"last_name"	TEXT NOT NULL,
	"department_id"	integer,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "divisions" (
	"id"	INTEGER,
	"division_name"	TEXT NOT NULL,
	"head_id"	integer,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "departments" (
	"id"	INTEGER,
	"division_id"	TEXT NOT NULL,
	"department_name"	TEXT NOT NULL,
	"manager_id"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "department_members" (
	"id"	INTEGER,
	"department_ID"	INTEGER NOT NULL,
	"employee_id"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "projects" (
	"id"	INTEGER,
	"project_name"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "project_assignments" (
	"id"	INTEGER,
	"project_id"	TINTEGER NOT NULL,
	"employee_id"	INTGER NOT NULL,
	PRIMARY KEY("id")
);
COMMIT;
