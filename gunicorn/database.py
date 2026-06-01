import jaydebeapi

from config import (
    JDBC_DRIVER,
    JDBC_URL,
    JDBC_USER,
    JDBC_PASSWORD,
    JDBC_JAR
)

def get_connection():

    return jaydebeapi.connect(
        JDBC_DRIVER,
        JDBC_URL,
        [JDBC_USER, JDBC_PASSWORD],
        JDBC_JAR
    )
