from sqlalchemy import create_engine
import pandas as pd
import datetime
from collections import namedtuple
from typing import Tuple


class Metadata:
    def __init__(self, 
                host: str,
                port: str,
                username: str,
                password: str,
                database: str,
                data_source: str
                ):
        self.connection_string = self._create_connection_string(host, port, username, password, database)
        self.engine = create_engine(self.connection_string)
        self.table_name = f'metadata_{data_source}'
        self.conn = None
    
    def _create_connection_string(self, host: str, port: str, username: str, password: str, database: str):
        return f"postgres://{username}:{password}@{host}:{port}/{database}"
    
    def _get_connection(self):
        """ Create a singleton connection object """
        if self.conn is None:
            self.conn = self.engine.connect()
        return self.conn

    def report(self) -> pd.DataFrame:
        """ Print out all the related information """
        # read table
        table = pd.read_sql(
            sql = f"select * from metadata.{self.table_name}",
            con = self.engine
        )
        return table

    def validate_if_need_the_load(self, business_key) -> bool:

        exp = " AND ".join([f"{name}='{value}'" for name, value in business_key._asdict().items()])
        filtering_condition = f'WHERE {exp}'
        sql_statement = f""" 
            SELECT last_modified
            FROM metadata.{self.table_name} 
            {filtering_condition}
        """
        print(sql_statement)
        response = self._get_connection().execute(sql_statement)

        now = datetime.datetime.utcnow()
        result = response.fetchone()
        if result:
            last_modified = result[0].replace(tzinfo=None)
            return False if  now - last_modified  < datetime.timedelta(days=1) else True
        else:
            return True
    
    def _construct_parenthesis_string(self, l: list, type: str):
        """ Construct following component for sql statement
        ({column}, {column}, {column}, {column}, {column})
        ({value}, {value}, {value}, {value}, {value})

        type is either column or value
        """
        if type == 'column':
            wrapper = '"'
        else:
            # type == 'value'
            wrapper = "'"
        stringfied_l = [f"{wrapper}{elem}{wrapper}" for elem in l]
        return f"({', '.join(stringfied_l)})"


    def update_as_succeeded(self, business_key: namedtuple):
        """Insert metadata or update last_modified when data pulling succeeded
        """
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        columns = list(business_key._fields) + ['last_modified']
        values = [business_key._asdict()[field] for field in business_key._fields] + [now]

        columns_exp = self._construct_parenthesis_string(columns, type='column')
        values_exp = self._construct_parenthesis_string(values, type='value')
        sql_statement = f"""
            INSERT INTO metadata.{self.table_name} {columns_exp}
            VALUES{values_exp}
            ON CONFLICT ON CONSTRAINT unique_constraint 
            DO UPDATE SET
                last_modified = excluded.last_modified
        """
        print(sql_statement)
        print('update_as_succeeded')
        try:
            self._get_connection().execute(sql_statement)
        except Exception as e:
            raise e