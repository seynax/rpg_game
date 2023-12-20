import sqlite3
import os

class Database:
    def __init__(self, path, remove=False):
        if remove:
            os.remove(path)
        parentPath=os.path.abspath(os.path.join(path, os.pardir))
        if not os.path.exists(parentPath):
            os.makedirs(parentPath)
        self.connection = sqlite3.connect(path) ## Create if not exists
        self.cursor     = self.connection.cursor()

    def request(self, request, parameters=None, reset=True, commit=True):
        if reset:
            self.cursor = self.connection.cursor()

        if parameters == None:
            self.cursor.execute(request)
        else:
            self.cursor.execute(request, parameters)
        if commit:
            self.connection.commit()

    def make_table(self, name, columns, contrainsts=None, parameters=None):
        request = "CREATE TABLE IF NOT EXISTS " + name + "("
        i = 0
        for column in columns:
            if i > 0:
                request += ","
            request += "    " + column
            i += 1
        if(contrainsts != None):
            request += "," + contrainsts
        request += ")"
        self.request(request, parameters)

    def insert(self, table, parameters=None, or_ignore=True):
        request_str = "INSERT "
        if or_ignore:
            request_str += "OR IGNORE "
        request_str += "INTO " + table + "("
        self.request("PRAGMA table_info(" + table + ");", None, True, False)
        table_info = self.cursor.fetchall()
        i = 0
        values = "VALUES ("
        for column_info in table_info:
            if not column_info[5]:
                if i > 0:
                    request_str += ", "
                    values += ", "
                request_str += column_info[1]
                values += "?"
                i += 1
        values += ")"
        request_str += ") " + values
        print("REQ : " + request_str)

        self.request(request_str, parameters)

    def select(self, condition, table, parameters=None):
        self.request("SELECT " + condition + " FROM " + table, parameters, True, False)
        return self.cursor.fetchall()

    def select_print(self, condition, table, parameters=None):
        selecteds = self.select(condition, table, parameters)

        print((len(selecteds)))
        for selected in selecteds:
            print(str(selected))

        return selecteds

    def close(self):
        self.connection.close()