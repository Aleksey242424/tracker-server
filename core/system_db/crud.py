from .utils import get_session,check_hash_password
from flask import abort
from psycopg2.errors import UniqueViolation
from uuid import UUID

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
                db_session.rollback()
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


class ProjectCRUD:
    @staticmethod
    def add(
        token:UUID,
        title:str,
        description:str,
        owner_id:int,
        db_session = next(get_session())
    ):
        with db_session.cursor() as cursor:
            cursor.execute("""INSERT INTO project(title,description,owner) VALUES(%(title)s,%(description)s,%(owner)s)""",
                           {"title":title,
                            "description":description,
                            "owner":owner_id})
            db_session.commit()
        

    @staticmethod
    def get_all(
        owner_id:int,
        db_session = next(get_session())
        ) -> list:
        with db_session.cursor() as cursor:
            cursor.execute("""SELECT * FROM project WHERE owner = %(owner)s""",
                           {"owner":owner_id})
            return cursor.fetchall()
        

    @staticmethod
    def get_by_id(
        id:int,
        db_session = next(get_session())
        ) -> tuple:
        with db_session.cursor() as cursor:
            cursor.execute("""SELECT * FROM project WHERE id = %(id)s""",
                           {"id":id})
            return cursor.fetchone()
        
    @staticmethod
    def get_by_token(
        token:UUID,
        db_session = next(get_session())
        ) -> tuple:
        with db_session.cursor() as cursor:
            cursor.execute("""SELECT * FROM project WHERE token = %(token)s""",
                           {"token":token})
            return cursor.fetchone()
