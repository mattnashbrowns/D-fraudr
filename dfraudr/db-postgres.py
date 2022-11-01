import psycopg2
import psycopg2.extras

import click
from flask import current_app, g

def get_db():
    conn = psycopg2.connect(
        host = "localhost",
        database = "dfraudr",
        user = "dfraud_user",
        password = "dfraud_pass")
    conn.set_session(autocommit=True)
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    
    return cur
    
def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()

def init_db():
    # psycopg2 DictCursor object
    cur = get_db()
    
    try:
        cur.execute(open("dfraudr/schema.sql","r").read())
    except psycopg2.Error as e:
        pass
    
        
@click.command('init-db')
def init_db_command():
    """Drop the database contents and make new tables"""
    init_db()
    click.echo('Initialized the database.')
    
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    
