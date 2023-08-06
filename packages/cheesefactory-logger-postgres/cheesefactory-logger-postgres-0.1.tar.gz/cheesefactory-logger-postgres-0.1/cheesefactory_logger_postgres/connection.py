# connection.py

import logging
from typing import List, Tuple, Union

import psycopg2
import psycopg2.extensions

logger = logging.getLogger(__name__)


class CfLogPostgresConnection:
    """Manage a SQLite connection.

    CfLogPostgres -> CfLogPostgresModel -> CfLogPostgresConnection
    """

    def __init__(self):
        """
        Attributes:
            self._connection: Postgres connection.
            self._cursor: Postgres cursor.
        """
        self._connection = None
        self._cursor = None
        self.host = None
        self.port = None
        self.encoding = None
        self.database = None
        self.username = None
        self.password = None
        self.create_table = None

    #
    # PROPERTIES
    #

    @property
    def status(self):
        """Retrieve connection status.

        status() for cheesefactory programs should return True/False along with any reasons.

        Returns:
            True, if live. False, if not live.
            Additional info, such as error codes. (not implemented)
        """
        if self._connection is None:
            return False, 'No connection detected.'
        if self._cursor is None:
            return False, 'Connection exists. No cursor.'

        try:
            status = self._connection.status

            if status == psycopg2.extensions.STATUS_READY:  # 1
                status_text = 'ready'
            elif status == psycopg2.extensions.STATUS_BEGIN:
                status_text = 'begin'
            elif status == psycopg2.extensions.STATUS_IN_TRANSACTION:
                status_text = 'in transaction'
            elif status == psycopg2.extensions.STATUS_PREPARED:
                status_text = 'prepared'
            else:
                status_text = f'unknown (psycopg2.extension = {str(status)})'

            logger.debug(f'Postgres connection status: {status} ({status_text})')
            return True, status_text

        except ValueError:
            return False, 'No connection detected.'

    #
    # PROTECTED METHODS
    #

    def _connect(self, host: str = '127.0.0.1', port: Union[str, int] = None, encoding: str = None,
                 database: str = None, user: str = None, password: str = None):
        """Connect to a PostgreSQL server.

        Args:
            host: Postgres server hostname or IP.
            port: Postgres server port.
            encoding:
            database:
            user: Account username on Postgres server.
            password: Account password on Postgres server.
        """
        self.host = host
        self.port = str(port)
        self.database = database
        self.user = user
        self.password = password
        self.encoding = encoding

        self._connection = psycopg2.connect(f'dbname={database} user={user} password={password} host={host} '
                                            f'port= {port}')
        self._cursor = self._connection.cursor()

    #
    # PUBLIC METHODS
    #

    def close(self):
        """Close the Postgres connection, if it is open."""
        if self.status[0] is True:
            logger.debug('Closing Postgres connection.')
            self._connection.close()

    def execute(self, sql: str = None) -> List[Tuple]:
        """Execute a query against the Postgres database.

        Returns:
            A list of tuples. Each tuple is a resulting record of the query.
        """
        self._cursor.execute(sql)
        self._connection.commit()
        try:
            result = self._cursor.fetchall()
        except psycopg2.ProgrammingError as e:
            logger.debug(f'Error while fetching results: {e}')
            result = None
        return result
