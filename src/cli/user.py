import typer
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import Session
from src.db_model import User, Translation, FileTranslation

app = typer.Typer()
DB_PATH = "sqlite:///db/translation_app.db"

def get_db_session():
    engine = create_engine(DB_PATH)
    return Session(engine)

@app.command()
def add_user(username: str = typer.Option(..., "--username"), 
             password: str = typer.Option(..., "--password")):
    session = get_db_session()
    try:
        new_user = User(username=username, password=password)
        session.add(new_user)
        session.commit()
        typer.echo(f"User '{username}' added successfully.")
    except exc.IntegrityError:
        session.rollback()
        typer.echo(f"User '{username}' already exists.")
    except Exception as e:
        session.rollback()
        typer.echo(f"An error occurred: {str(e)}")
    finally:
        session.close()

@app.command()
def delete_user(username: str = typer.Option(..., "--username")):
    session = get_db_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user:
            # Delete associated translations and file translations
            session.query(Translation).filter_by(user_id=user.id).delete()
            session.query(FileTranslation).filter_by(user_id=user.id).delete()
            session.delete(user)
            session.commit()
            typer.echo(f"User '{username}' and associated data deleted successfully.")
        else:
            typer.echo(f"User '{username}' not found.")
    except Exception as e:
        session.rollback()
        typer.echo(f"An error occurred: {str(e)}")
    finally:
        session.close()

@app.command()
def delete_all_users():
    session = get_db_session()
    try:
        # Delete all translations and file translations
        session.query(Translation).delete()
        session.query(FileTranslation).delete()
        # Delete all users
        session.query(User).delete()
        session.commit()
        typer.echo("All users and their associated data have been deleted.")
    except Exception as e:
        session.rollback()
        typer.echo(f"An error occurred: {str(e)}")
    finally:
        session.close()


@app.command()
def list_users():
    session = get_db_session()
    try:
        users = session.query(User).all()
        if users:
            typer.echo("List of users and passwords:")
            for user in users:
                typer.echo(f"Username: {user.username}, Password: {user.password}")
        else:
            typer.echo("No users found in the database.")
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    app()