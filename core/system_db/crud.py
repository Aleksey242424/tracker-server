from .utils import get_session,check_hash_password
from flask import abort
from psycopg2.errors import UniqueViolation
from uuid import UUID
from datetime import datetime

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
        SELECT id,name,hash_password,email,is_owner FROM person WHERE name = %(name)s;
        """,
        {
            "name":name
        })
            user:tuple = cursor.fetchone()
            if check_hash_password(
                hash_password = user[2].encode("utf-8"),
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
        date_create:datetime = datetime.utcnow().date(),
        db_session = next(get_session())
    ):
        with db_session.cursor() as cursor:
            cursor.execute("""INSERT INTO project(token,title,description,owner,date_create) VALUES(%(token)s,%(title)s,%(description)s,%(owner)s,%(date_create)s)""",
                           {
                               "token":token,
                               "title":title,
                                "description":description,
                                "owner":owner_id,
                                "date_create":date_create
                                })
            db_session.commit()

        

    @staticmethod
    def get_all_for_owner(
        owner_id:int,
        db_session = next(get_session())
        ) -> list:
        with db_session.cursor() as cursor:
            cursor.execute("""SELECT * FROM project WHERE owner = %(owner)s;""",
                           {"owner":owner_id})
            return cursor.fetchall()
        
        

    @staticmethod
    def get_by_id(
        id:int,
        db_session = next(get_session())
        ) -> tuple:
        with db_session.cursor() as cursor:
            cursor.execute("""SELECT * FROM project WHERE id = %(id)s;""",
                           {"id":id})
            return cursor.fetchone()
        
    @staticmethod
    def get_by_token(
        token:UUID,
        db_session = next(get_session())
        ) -> tuple:
        with db_session.cursor() as cursor:
            cursor.execute("""
                           SELECT CASE
                            WHEN tracker_info.time IS NULL THEN make_time(0,0,0.0)
                            ELSE tracker_info.time
                            END AS "time_work",project.title,project.description FROM project JOIN tracker_info ON project.token = tracker_info.token 
                           WHERE project.token = %(token)s""",
                           {"token":token})
            return cursor.fetchone()


class TrackerLink:
    @staticmethod
    def add(
        token:UUID,
        worker_id:int,
        db_session = next(get_session())
    ):
        with db_session.cursor() as cursor:
            cursor.execute('''
            INSERT INTO tracker_link(token,worker) VALUES(%(token)s,%(worker)s)
            ''',
            {
                "token":token,
                "worker":worker_id
            })
            db_session.commit()

    @staticmethod
    def get_all(
        person_id:int,
        db_session = next(get_session())
    ) -> list:
        with db_session.cursor() as cursor:
            cursor.execute(
            """
            SELECT CASE
            WHEN tracker_info.time IS NULL THEN make_time(0,0,0.0)
            ELSE tracker_info.time
            END AS "time_work",project.title,project.token FROM tracker_link 
            JOIN project ON tracker_link.token = project.token 
            JOIN tracker_info ON project.token = tracker_info.token WHERE person = %(person_id)s;
            """,
            {"person_id":person_id}
            )
            return cursor.fetchall()
        
    


class TrackerInfo:
    @staticmethod
    def add(
        person_id:int,
        token:UUID,
        when:datetime = datetime.utcnow().date(),
        db_session = next(get_session())
    ):
        with db_session.cursor() as cursor:
            cursor.execute('''
            INSERT INTO tracker_info(person,token,"when") VALUES(%(person_id)s,%(token)s,%(when)s)
            ''',
            {
                "person_id":person_id,
                "token":token,
                "when":when
            })
            db_session.commit()

    
    