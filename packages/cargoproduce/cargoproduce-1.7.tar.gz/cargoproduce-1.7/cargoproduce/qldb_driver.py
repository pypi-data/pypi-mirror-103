import json
import numbers

from pyqldb.driver.qldb_driver import QldbDriver
from amazon.ion.json_encoder import IonToJSONEncoder

class QLDBDriver:
    def __init__(self, ledger):
        self.qldb_driver = QldbDriver(ledger_name = ledger)
    
    def to_collection(self, cursor):
        collection = []
        
        for row in cursor:
            json_string = json.dumps(row, cls=IonToJSONEncoder)
            collection.append(json.loads(json_string))

        return collection


    def execute(self, transaction_executor, statement):
        cursor = transaction_executor.execute_statement(statement)
        
        return cursor


    def create_table(self, table_name, primary_key = None):
        statement = f"CREATE TABLE {table_name}"
        self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))

        if primary_key is not None:
            statement = f"CREATE INDEX ON {table_name}({primary_key})"
            self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))


    def drop_table(self, table_name):
        statement = f"DROP TABLE {table_name}"
        self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))


    def add_attribute(self, table_name, identifier, attribute_name, value = None):
        tables = self.list_tables()

        if not table_name in tables:
            raise Exception("Table not found!")

        if isinstance(value, str):
            default_value = f"'{value}'"
        elif isinstance(value, numbers.Number):
            default_value = f"{value}"
        elif value is None:
            default_value = "null"

        statement = f"SELECT {identifier} FROM {table_name}"
        
        ids = self.query(statement)

        for id in ids:
            if isinstance(id[identifier], str):
                statement = f"FROM {table_name} WHERE {identifier} = '{id[identifier]}' SET {attribute_name} = {default_value}"
            elif isinstance(id[identifier], numbers.Number):
                statement = f"FROM {table_name} WHERE {identifier} = {id[identifier]} SET {attribute_name} = {default_value}"

            self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))


    def remove_attribute(self, table_name, identifier, attribute_name):
        tables = self.list_tables()

        if not table_name in tables:
            raise Exception("Table not found!")

        statement = f"SELECT {identifier} FROM {table_name}"
        
        ids = self.query(statement)

        for id in ids:
            statement = f"FROM {table_name} WHERE {identifier} = {id[identifier]} REMOVE {attribute_name}"

            try:
                self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))
            except:
                pass

    def list_tables(self):
        collection = []

        for table in self.qldb_driver.list_tables():
            collection.append(table)

        return collection


    def insert_data(self, table_name, data):
        statement = f"INSERT INTO {table_name} `{json.dumps(data)}`"
        self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))


    def update_data(self, table_name, primary_key_field, primary_key_value, data):
        raw_data = str(data).replace("None", "null")

        statement = f"""
            UPDATE {table_name} AS x 
                SET x = {raw_data} 
            WHERE x.{primary_key_field} = {primary_key_value}"""
        
        self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))


    def query(self, statement):
        cursor = self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))

        return self.to_collection(cursor)


    def query_single(self, statement):
        cursor = self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))
        collection = self.to_collection(cursor)

        if len(collection) > 1:
            raise Exception('more than 1 result recived')

        return collection[0]


    def execute_statement(self, statement):
        self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))
