# __init__.py

import logging
from typing import Union

from .exceptions import MissingFieldsError, MissingTableError
from .model import CfLogPostgresModel

logger = logging.getLogger(__name__)


class CfLogPostgres(CfLogPostgresModel):
    """Send logs to and read logs from a SQLite database.

    CfLogPostgres -> CfLogPostgresModel -> CfLogPostgresConnection
    """
    def __init__(self):
        super().__init__()
        # Default log table design.
        self.field_list = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'message': 'TEXT',
            'timestamp': 'TEXT DEFAULT CURRENT_TIMESTAMP',
        }

    #
    # CLASS METHODS
    #

    @classmethod
    def connect(cls, host: str = '127.0.0.1', port: Union[str, int] = None, encoding: str = None, database: str = None,
                user: str = None, password: str = None, schema: str = 'public', table: str = 'log',
                field_list: dict = None):
        """Make a SQLite connection to a database file.

        If the database file exists, use it. If not, create it. If the file exists, but the table fields do not match,
        create a new file.

        Args:
            host: Postgres server hostname or IP.
            port: Postgres server port.
            encoding:
            database:
            user: Account username on Postgres server.
            password: Account password on Postgres server.
            schema:
            table:
            field_list:
        """
        log = cls()
        if field_list is None:
            raise ValueError('Missing field_list')
        else:
            log.field_list = field_list

        # Connect to database
        logger.debug(f'Connecting to database: {user}@{host}:{port}/{database}')
        log._connect(host=host, port=port, database=database, user=user, password=password)

        # Audit table
        log.schema = schema
        log.table = table

        logger.debug(f'Testing table: {log.database}.{log.schema}.{log.table}')
        log._test_database()

        logger.debug(f'Connected to log database: {log.database}.{log.schema}.{log.table}')
        return log
