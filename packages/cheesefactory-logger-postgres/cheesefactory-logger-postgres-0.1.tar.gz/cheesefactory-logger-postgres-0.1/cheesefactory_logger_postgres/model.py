# model.py

import logging
from typing import List, Tuple
from .connection import CfLogPostgresConnection
from .exceptions import MissingFieldsError, MissingTableError, TablePrimaryKeyError

logger = logging.getLogger(__name__)


class CfLogPostgresModel(CfLogPostgresConnection):
    """

    CfLogPostgres -> CfLogPostgresModel -> CfLogPostgresConnection
    """
    def __init__(self):
        super().__init__()
        self.schema: str = 'public'
        self.table: str = 'log'
        self.field_list: dict = {}

    #
    # PROPERTIES
    #

    @property
    def pk_field(self) -> str:
        """Find and return a table's primary key field. Because of how the table is automatically created, there can
        be only one pk.

        Return:
            A table's primary key field.
        """
        results = self.execute(f"""
            SELECT
                table_constraints.table_schema,
                table_constraints.table_name,
                constraint_column_usage.column_name,
                table_constraints.constraint_name,
                table_constraints.constraint_type
            FROM
                information_schema.table_constraints AS table_constraints
                INNER JOIN information_schema.constraint_column_usage AS constraint_column_usage
                    ON table_constraints.table_schema = constraint_column_usage.table_schema
                    AND table_constraints.table_name = constraint_column_usage.table_name
                    AND table_constraints.constraint_name = constraint_column_usage.constraint_name
            WHERE
                table_constraints.constraint_type = 'PRIMARY KEY'
                AND table_constraints.table_schema = '{self.schema}'
                AND table_constraints.table_name = '{self.table}';
        """)
        logger.debug(f'Query results: {str(results)}')
        if len(results) < 1:
            return ''
        if len(results) > 1:
            raise TablePrimaryKeyError(database=self.database, table=f'{self.schema}.{self.table}',
                                       message='Table has more than 1 primary key.')
        return str(results[0][2])  # constraint_column_usage.column_name

    #
    # PROTECTED METHODS
    #

    def _create_table(self):
        """Create a log table."""
        # Dynamically create SQL based on field dict.
        sql = f'CREATE TABLE {self.schema}.{self.table} ('
        for field, field_type in self.field_list.items():
            sql += f' {field} {field_type},'
        sql = sql[:-1]  # Erase trailing comma
        sql += ');'

        logger.debug(f'Creating table ({self.schema}.{self.table}): {sql}')
        try:
            self.execute(sql)
        except AttributeError as e:
            raise AttributeError(f'No Postgres connection exists. Connect before creating table. ({str(e)})')
        logger.debug(f'New table created: {self.schema}.{self.table}')

        if self.pk_field == '':
            logger.debug(f'Table ({self.schema}.{self.table}) has no primary key. UPDATEs are not possible.')

    def _test_database(self):
        """Check database sanity."""
        # Does a field_list exist to compare things to?
        if self.field_list == {} or self.field_list is None:
            raise ValueError('Missing field_list.')

        # Does the log table exist in the database?
        results = self.get_fields()
        if len(results) == 0:
            raise MissingTableError(table=self.table, database=f'{self.schema}.{self.table}')

        # Build a list of fields present in the table
        table_fields = []
        for result in results:
            table_fields.append(result[1])

        # Does the table contain all of the required fields?
        missing_fields = []
        for field in self.field_list.keys():
            if field not in table_fields:
                missing_fields.append(field)
        if len(missing_fields) > 0:
            raise MissingFieldsError(
                f'Table {self.schema}.{self.table} is missing required fields: {", ".join(missing_fields)}'
            )
        logger.debug(f'Table successfully tested: {self.schema}.{self.table}')

    #
    # PUBLIC METHODS
    #

    def exists(self, where=None):
        """Does the query return results?

        Args:
            where: SQL WHERE to filter data.
        """
        result = self.read_records(where=where)
        if len(result) == 0:
            return False
        else:
            return True

    def get_fields(self) -> List:
        """Return list of table fields."""
        return self.execute(f"""
            SELECT table_name, column_name, data_type
            FROM information_schema.columns 
            WHERE table_name = '{self.table}' AND table_schema = '{self.schema}';
        """)

    def read_records(self, where: str = None, exclude_pk: bool = False) -> List[Tuple]:
        """Produce record entries.

        Args:
            where: SQL WHERE to filter data.
            exclude_pk: Exclue the primary key in the results
        Notes:
            The SQL SELECT needs to be explicit with column names. We are going to enforce the names and
            order given in self.field_list.
        """
        field_list = ''
        pk_field = ''

        if exclude_pk is True:
            # No need to go through the cost of running this property multiple times in the following loop.
            pk_field = self.pk_field
        for field in self.field_list.keys():
            if exclude_pk is True and field == pk_field:
                continue
            field_list = field_list + f'{field}, '
        field_list = field_list[:-2]  # Remove trailing comma and space.
        sql = f'SELECT {field_list} FROM {self.schema}.{self.table}'

        if where is not None:
            sql += f' WHERE {where}'

        logger.debug(sql)
        result = self.execute(sql)
        if result is None:
            return []
        else:
            return result

    def table_exists(self) -> bool:
        """Does the log table exist?"""
        if self.schema in (None, ''):
            raise ValueError('Schema is not defined. Cannot continue.')
        if self.table in (None, ''):
            raise ValueError('Table is not defined. Cannot continue.')

        results = self.execute(f"""
            SELECT tablename 
            FROM pg_catalog.pg_tables 
            WHERE schemaname = '{self.schema}' AND tablename = '{self.table}';
        """)

        if len(results) == 0:
            return False
        else:
            return True

    def write_kwargs(self, pk=None, **kwargs) -> int:
        """Insert record into database from keyword arguments.

        Args:
            pk: Primary key. If present, performs an UPDATE on that record.
            kwargs: key-value pairs. The keys should match field names.
        Returns:
            If an INSERT was performed, returns the primary key of the affected record, else 0 is returned.
        """

        if len(kwargs) == 0:
            raise ValueError('Missing kwargs. Cannot write to database.')

        # Are all given fields present in self.field_list? If not, raise an error.
        field_map = ''  # Prep for possible UPDATE. So fields don't need to be traversed again.
        ordered_keys = ''
        ordered_values = ''
        invalid_keys = ''
        field_list = self.field_list.keys()

        for key, value in kwargs.items():
            if key not in field_list:
                invalid_keys += f'{key}, '
            if key == 'id':  # If primary key, skip
                continue
            elif isinstance(value, int):
                field_map += f'{key} = {str(value)}, '
                ordered_keys += f'{key}, '
                ordered_values += f'{str(value)}, '
            elif isinstance(value, str):
                field_map += f"{key} = '{value}', "
                ordered_keys += f'{key}, '
                ordered_values += f"'{str(value)}', "
        field_map = field_map[:-2]  # Clean up the trailing comma and whitespaces

        if invalid_keys != '':
            invalid_keys = invalid_keys[:-2]  # Clean up the trailing commas and whitespaces
            raise ValueError(f'Invalid key(s): {invalid_keys}. '
                             f'Acceptable values are {", ".join(field_list)}')

        # Determine if this is an INSERT or UPDATE
        pk_field = self.pk_field
        if pk is None:  # New record. Do an INSERT.
            logger.debug(f'Inserting new record.')
            ordered_keys = ordered_keys[:-2]  # Clean up the trailing comma and whitespaces
            ordered_values = ordered_values[:-2]  # Clean up the trailing comma and whitespaces
            sql = f'INSERT INTO {self.schema}.{self.table} ({ordered_keys}) ' \
                  f'VALUES ({ordered_values})'
            if pk_field != '':
                sql = sql + f' RETURNING {pk_field};'
            logger.debug(f'write(): {sql}')
            results = self.execute(sql)
            if pk_field != '':
                pk = results[0][0]  # New primary key value

        else:  # Existing record. Do an UPDATE.
            if pk_field == '':
                raise TablePrimaryKeyError(database=self.database, table=f'{self.schema}.{self.table}',
                                           message='The table has no primary key. SQL UPDATE cannot happen.')
            logger.debug(f'Updating record. {pk_field}={str(pk)}')
            sql = f'UPDATE {self.schema}.{self.table} SET {field_map} WHERE {pk_field} = {str(pk)};'
            logger.debug(f'write(): {sql}')
            self.execute(sql)

        return pk
