from .utils import get_session,check_hash_password
from flask import abort
from psycopg2.errors import UniqueViolation


class PersonCRUD:
    @staticmethod
    def add(
        name:str,
        hash_password:str,
        email:str,
        is_owner:bool,
        db_session = next(get_session())
        ):
        with db_session.cursor() as cursor:
            try:
                cursor.execute("""
                INSERT INTO person(name,hash_password,email,is_owner) VALUES(%(name)s,%(hash_password)s,%(email)s,%(is_owner)s);
                """,
                {
                    "name":name,
                    "hash_password":hash_password,
                    "email":email,
                    "is_owner":is_owner
                    })
                
                db_session.commit()
            
            except UniqueViolation:
                abort(401)

    @staticmethod
    def get(
        name:str,
        password:str,
        db_session = next(get_session())
    ):
        with db_session.cursor() as cursor:
            cursor.execute("""
        SELECT name,hash_password,email,is_owner FROM person WHERE name = %(name)s;
        """,
        {
            "name":name
        })
            user:tuple = cursor.fetchone()
            if check_hash_password(
                hash_password = user[1].encode("utf-8"),
                password = password.encode("utf-8")
            ):
                return user
            
            abort(401)