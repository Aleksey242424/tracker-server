from psycopg2 import connect
from instance.config import setting
from bcrypt import checkpw
import click


def get_session(DSN:str = setting.DB_CONNECTION):
    with connect(DSN) as db_session:
        yield db_session
    db_session.close()


def check_hash_password(hash_password:bytes,password:bytes) -> bool:
    return checkpw(password=password,hashed_password=hash_password)


@click.command("init-db")
def init_db(db_session = next(get_session())):
    with db_session.cursor() as cursor,open("core/system_db/schem.sql","r") as f:
        cursor.execute(f.read())
        db_session.commit()