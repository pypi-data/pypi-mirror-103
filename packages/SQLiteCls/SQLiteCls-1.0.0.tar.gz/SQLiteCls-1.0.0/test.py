#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2021, Matjaž Guštin <dev@matjaz.it> <https://matjaz.it>.
# Released under the BSD 3-Clause License

"""Unit tests for the SQLiteCls library."""

import os
import unittest

import sqlitecls as sc

DB_NAME = 'testing_sqlite.db'
WAL_NAME = 'testing_sqlite.db-wal'
DB_INIT_SCRIPT_NAME = 'testing_init.sql'
CONNECTION_INIT_SCRIPT_NAME = 'testing_pragmas.sql'


class TestSqliteDb(unittest.TestCase):
    def tearDown(self) -> None:
        """Deletes any generated SQLite files, if existing."""
        try:
            os.remove(DB_NAME)
        except FileNotFoundError:
            pass
        try:
            os.remove(WAL_NAME)
        except FileNotFoundError:
            pass

    def test_closed_at_construction_in_memory(self):
        db = sc.SqliteDb()
        self.assertIsNone(db.connection)
        self.assertIsNone(db.cursor)
        self.assertTrue(db.is_in_memory())

    def test_closed_at_construction_on_file(self):
        db = sc.SqliteDb(DB_NAME)
        self.assertIsNone(db.connection)
        self.assertIsNone(db.cursor)
        self.assertFalse(db.is_in_memory())

    def test_constructor_on_file_with_init_script(self):
        db = sc.SqliteDb(DB_NAME, DB_INIT_SCRIPT_NAME)
        self.assertIsNone(db.connection)
        self.assertIsNone(db.cursor)
        self.assertFalse(db.is_in_memory())

    def test_construct_and_open_in_memory(self):
        with sc.SqliteDb() as db:
            self.assertIsNotNone(db.connection)
            self.assertIsNotNone(db.cursor)
            self.assertTrue(db.is_in_memory())
            self.assertTrue(db.is_empty_db())
            db.execute('CREATE TABLE aaa(x INTEGER)')
            self.assertFalse(db.is_empty_db())
            # Connection pragmas were not run
            self.assertFalse(db.pragma('foreign_keys'))
            self.assertNotEqual(-123, db.pragma('cache_size'))
        self.assertIsNone(db.connection)
        self.assertIsNone(db.cursor)

    def test_construct_and_open_on_file(self):
        with sc.SqliteDb(DB_NAME) as db:
            self.assertIsNotNone(db.connection)
            self.assertIsNotNone(db.cursor)
            self.assertFalse(db.is_in_memory())
            self.assertTrue(db.is_empty_db())
            db.execute('CREATE TABLE aaa(x INTEGER)')
            self.assertFalse(db.is_empty_db())
            self.assertTrue(os.path.isfile(DB_NAME))
            # Connection pragmas were not run
            self.assertFalse(db.pragma('foreign_keys'))
            self.assertNotEqual(-123, db.pragma('cache_size'))
        self.assertIsNone(db.connection)
        self.assertIsNone(db.cursor)

    def test_construct_and_open_and_init_on_file(self):
        with sc.SqliteDb(DB_NAME, DB_INIT_SCRIPT_NAME) as db:
            self.assertIsNotNone(db.connection)
            self.assertIsNotNone(db.cursor)
            self.assertFalse(db.is_in_memory())
            self.assertFalse(db.is_empty_db())
            self.assertTrue(os.path.isfile(DB_NAME))
            cursor = db.execute('SELECT count(*) FROM test_points')
            amount = cursor.fetchone()[0]
            self.assertEqual(3, amount)
            # Connection pragmas were NOT executed
            self.assertNotEqual(-123, db.pragma('cache_size'))
        self.assertIsNone(db.connection)
        self.assertIsNone(db.cursor)

    def test_construct_and_open_init_connection(self):
        db = sc.SqliteDb(
            on_connect_script_file_name=CONNECTION_INIT_SCRIPT_NAME)
        with db:
            self.assertIsNotNone(db.connection)
            self.assertIsNotNone(db.cursor)
            self.assertTrue(db.is_in_memory())
            # Connection pragmas WERE executed
            self.assertEqual(-123, db.pragma('cache_size'))
        self.assertIsNone(db.connection)
        with db:  # Also when reopening
            self.assertIsNotNone(db.connection)
            self.assertIsNotNone(db.cursor)
            self.assertTrue(db.is_in_memory())
            # Connection pragmas WERE executed
            self.assertEqual(-123, db.pragma('cache_size'))
        self.assertIsNone(db.connection)

    def test_construct_and_open_and_init_db_and_connection(self):
        db = sc.SqliteDb(DB_NAME, DB_INIT_SCRIPT_NAME,
                         CONNECTION_INIT_SCRIPT_NAME)
        with db:
            self.assertIsNotNone(db.connection)
            self.assertIsNotNone(db.cursor)
            self.assertFalse(db.is_in_memory())
            self.assertFalse(db.is_empty_db())
            self.assertTrue(os.path.isfile(DB_NAME))
            cursor = db.execute('SELECT count(*) FROM test_points')
            amount = cursor.fetchone()[0]
            self.assertEqual(3, amount)
            # Connection pragmas WERE executed
            self.assertEqual(-123, db.pragma('cache_size'))
        self.assertIsNone(db.connection)
        self.assertIsNone(db.cursor)

    def test_reopening_closed_connection(self):
        db = sc.SqliteDb(DB_NAME, DB_INIT_SCRIPT_NAME)
        db.open()
        db.execute('INSERT INTO test_points(x, y) VALUES (100, 200)')
        db.commit()
        db.close()
        self.assertTrue(os.path.isfile(DB_NAME))
        self.assertIsNone(db.connection)
        self.assertIsNone(db.cursor)
        db.open()
        self.assertIsNotNone(db.connection)
        self.assertIsNotNone(db.cursor)
        self.assertFalse(db.is_empty_db())
        cursor = db.execute('SELECT count(*) FROM test_points')
        amount = cursor.fetchone()[0]
        self.assertEqual(3 + 1, amount)

    def test_tables_names(self):
        with sc.SqliteDb(DB_NAME, DB_INIT_SCRIPT_NAME) as db:
            tables = db.tables_names()
            self.assertListEqual(['test_points', 'test_lines'], tables)
            db.execute('CREATE TABLE abc (x INTEGER)')
            tables = db.tables_names()
            self.assertListEqual(['test_points', 'test_lines', 'abc'], tables)

    def test_column_names(self):
        with sc.SqliteDb(DB_NAME, DB_INIT_SCRIPT_NAME) as db:
            columns = db.columns_names('test_points')
            self.assertListEqual(['id', 'x', 'y'], columns)
            columns = db.columns_names('UNEXISTING_TABLE____Aaaaaa')
            self.assertListEqual([], columns)

    def test_pragma(self):
        with sc.SqliteDb(DB_NAME, DB_INIT_SCRIPT_NAME,
                         CONNECTION_INIT_SCRIPT_NAME) as db:
            self.assertIsInstance(db.pragma('busy_timeout'), int)
            self.assertTrue(db.pragma('foreign_keys'))
            self.assertEqual(-123, db.pragma('cache_size'))
            self.assertEqual(3, db.pragma('synchronous'))  # 3 == 'EXTRA'

    def test_db_size(self):
        with sc.SqliteDb() as db:
            size = db.size_bytes()
            self.assertIsInstance(size, int)
            self.assertEqual(size, 0)
        with sc.SqliteDb(db_init_script_file_name=DB_INIT_SCRIPT_NAME) as db:
            size = db.size_bytes()
            self.assertIsInstance(size, int)
            self.assertGreater(size, 0)


class TestModule(unittest.TestCase):
    def test_cursor_column_name(self):
        db = sc.SqliteDb(DB_NAME, DB_INIT_SCRIPT_NAME)
        db.open()
        cursor = db.execute('SELECT * FROM test_points')
        columns = sc.cursor_column_names(cursor)
        self.assertListEqual(['id', 'x', 'y'], columns)


if __name__ == '__main__':
    unittest.main()
