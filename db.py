import sqlite3
import logging

from sqlite3 import Error

from model import ItemsModel
from queries import CREATE_TABLE_LOST, CREATE_TABLE_FOUND, INSERT_LOST_ITEM, INSERT_FOUND_ITEM, SELECT_ALL_LOST_ITEMS, \
    SELECT_ALL_FOUND_ITEMS, SEARCH_LOST_ITEMS, SEARCH_FOUND_ITEMS, UPDATE_LOST_ITEM_BY_ID, UPDATE_FOUND_ITEM_BY_ID, \
    UPDATE_LOST_ITEM_TO_ARCHIVE, CLAIMED_LOST_ITEM, UNCLAIMED_LOST_ITEM, UNCLAIMED_FOUND_ITEM, CLAIMED_FOUND_ITEM, \
    UPDATE_FOUND_ITEM_TO_ARCHIVE, SELECT_ALL_LOST_ITEMS_A, SELECT_ALL_FOUND_ITEMS_A


class ItemsDb:
    def __init__(self):
        self.conn = sqlite3.connect("items_db.db")
        self.cur = self.conn.cursor()

    def create_table_lost(self):
        try:
            self.cur.execute(CREATE_TABLE_LOST)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def create_table_found(self):
        try:
            self.cur.execute(CREATE_TABLE_FOUND)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def insert_lost_item(self, lost_item):
        try:
            self.cur.execute(INSERT_LOST_ITEM, lost_item)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def insert_found_item(self, found_item):
        try:
            self.cur.execute(INSERT_FOUND_ITEM, found_item)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def select_all_lost_items_a(self):
        try:
            rows: list[ItemsModel] = self.cur.execute(SELECT_ALL_LOST_ITEMS_A).fetchall()
            return rows
        except Error as e:
            logging.error(e)
            return []

    def select_all_found_items_a(self):
        try:
            rows: list[ItemsModel] = self.cur.execute(SELECT_ALL_FOUND_ITEMS_A).fetchall()
            return rows
        except Error as e:
            logging.error(e)
            return []

    def select_all_lost_items(self):
        try:
            rows: list[ItemsModel] = self.cur.execute(SELECT_ALL_LOST_ITEMS).fetchall()
            return rows
        except Error as e:
            logging.error(e)
            return []

    def select_all_found_items(self):
        try:
            rows: list[ItemsModel] = self.cur.execute(SELECT_ALL_FOUND_ITEMS).fetchall()
            return rows
        except Error as e:
            logging.error(e)
            return []

    def search_engine_lost(self, search_text):
        try:
            rows = self.cur.execute(SEARCH_LOST_ITEMS, (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%", f"%{search_text}%", f"%{search_text}%", f"%{search_text}%")).fetchall()
            return rows
        except Error as e:
            logging.error(e)
            return []

    def search_engine_found(self, search_term):
        try:
            rows = self.cur.execute(SEARCH_FOUND_ITEMS, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")).fetchall()
            return rows
        except Error as e:
            logging.error(e)
            return []

    def update_lost_item_by_id(self, lost_item):
        try:
            self.cur.execute(UPDATE_LOST_ITEM_BY_ID, lost_item)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def update_found_item_by_id(self, found_item):
        try:
            self.cur.execute(UPDATE_FOUND_ITEM_BY_ID, found_item)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def archive_lost_item_by_id(self, lost_item_id):
        try:
            self.cur.execute(UPDATE_LOST_ITEM_TO_ARCHIVE, (lost_item_id,))
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def archive_found_item_by_id(self, found_item_id):
        try:
            self.cur.execute(UPDATE_FOUND_ITEM_TO_ARCHIVE, (found_item_id,))
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def claimed_lost_item(self):
        try:
            rows = self.cur.execute(CLAIMED_LOST_ITEM).fetchone()[0]
            return rows
        except Error as e:
            logging.error(e)
            return False

    def unclaimed_lost_item(self):
        try:
            rows = self.cur.execute(UNCLAIMED_LOST_ITEM).fetchone()[0]
            return rows
        except Error as e:
            logging.error(e)
            return False

    def claimed_found_item(self):
        try:
            rows = self.cur.execute(CLAIMED_FOUND_ITEM).fetchone()[0]
            return rows
        except Error as e:
            logging.error(e)
            return False

    def unclaimed_found_item(self):
        try:
            rows = self.cur.execute(UNCLAIMED_FOUND_ITEM).fetchone()[0]
            return rows
        except Error as e:
            logging.error(e)
            return False

db = ItemsDb()





