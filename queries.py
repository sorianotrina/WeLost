CREATE_TABLE_LOST = """CREATE TABLE IF NOT EXISTS lost_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    student_number TEXT NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    date TEXT NOT NULL,
                    location TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    status TEXT NOT NULL,
                    updated TEXT NOT NULL,
                    archived INTEGER DEFAULT 0
                )"""

CREATE_TABLE_FOUND = """CREATE TABLE IF NOT EXISTS found_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    student_number TEXT NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    date TEXT NOT NULL,
                    location TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    status TEXT NOT NULL,
                    updated TEXT NOT NULL,
                    archived INTEGER DEFAULT 0
                )"""

INSERT_LOST_ITEM = """
    INSERT INTO lost_items (student_number, name, description, date, location, contact, status, updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

INSERT_FOUND_ITEM = """
    INSERT INTO found_items (student_number, name, description, date, location, contact, status, updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

SELECT_ALL_LOST_ITEMS = """SELECT * FROM lost_items"""

SELECT_ALL_FOUND_ITEMS = """SELECT * FROM found_items"""

SELECT_ALL_LOST_ITEMS_A = """SELECT * FROM lost_items WHERE archived = 0"""

SELECT_ALL_FOUND_ITEMS_A = """SELECT * FROM found_items WHERE archived = 0"""

SEARCH_LOST_ITEMS = """SELECT * FROM lost_items WHERE (student_number LIKE ? OR name LIKE ? OR description LIKE ? OR date LIKE ? OR location LIKE ? OR status like ?) AND archived = 0"""

SEARCH_FOUND_ITEMS = """SELECT * FROM found_items WHERE (student_number LIKE ? OR name LIKE ? OR description LIKE ? OR date LIKE ? OR location LIKE ? OR status like ?) AND archived = 0"""

UPDATE_LOST_ITEM_BY_ID = """
UPDATE lost_items set
student_number = ?,
name = ?,
description = ?,
date = ?,
location = ?,
contact = ?,
status = ?,
updated = ?
WHERE id = ?
"""

UPDATE_FOUND_ITEM_BY_ID = """
UPDATE found_items set
student_number = ?,
name = ?,
description = ?,
date = ?,
location = ?,
contact = ?,
status = ?,
updated = ?
WHERE id = ?
"""

UPDATE_LOST_ITEM_TO_ARCHIVE = """UPDATE lost_items SET archived = 1 WHERE id = ?"""

UPDATE_FOUND_ITEM_TO_ARCHIVE = """UPDATE found_items SET archived = 1 WHERE id = ?"""

CLAIMED_LOST_ITEM = """SELECT count(*) FROM lost_items WHERE status = 'Claimed' """

UNCLAIMED_LOST_ITEM = """SELECT count(*) FROM lost_items WHERE status = 'Unclaimed' OR status = '' """

CLAIMED_FOUND_ITEM = """SELECT count(*) FROM found_items WHERE status = 'Claimed' """

UNCLAIMED_FOUND_ITEM = """SELECT count(*) FROM found_items WHERE status = 'Unclaimed' OR status = '' """
