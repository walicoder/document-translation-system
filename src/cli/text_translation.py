import typer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from src.db_model import User, Translation

app = typer.Typer()
DB_PATH = "sqlite:///db/translation_app.db"

def get_db_session():
    engine = create_engine(DB_PATH)
    # Base.metadata.create_all(engine)  # Ensure tables are created
    return Session(engine)

@app.command()
def add_translation(
    username: str = typer.Option(..., "--username"),
    english_text: str = typer.Option(..., "--english-text"),
    bengali_text: str = typer.Option(..., "--bengali-text")
):
    session = get_db_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            typer.echo(f"User '{username}' not found.")
            return

        new_translation = Translation(
            user_id=user.id,
            english_text=english_text,
            bengali_text=bengali_text,
            translated_at=datetime.now(),
            session_id=str(uuid.uuid4())
        )
        session.add(new_translation)
        session.commit()
        typer.echo(f"Translation added successfully for user '{username}'.")
    except Exception as e:
        session.rollback()
        typer.echo(f"An error occurred: {str(e)}")
    finally:
        session.close()

@app.command()
def list_translations(username: str = typer.Option(..., "--username")):
    session = get_db_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            typer.echo(f"User '{username}' not found.")
            return

        translations = session.query(Translation).filter_by(user_id=user.id).all()
        if translations:
            typer.echo(f"Translations for user '{username}':")
            for trans in translations:
                typer.echo(f"ID: {trans.id}")
                typer.echo(f"Session ID: {trans.session_id}")
                typer.echo(f"English: {trans.english_text}")
                typer.echo(f"Bengali: {trans.bengali_text}")
                typer.echo(f"Translated at: {trans.translated_at}")
                typer.echo("---")
        else:
            typer.echo(f"No translations found for user '{username}'.")
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}")
    finally:
        session.close()

@app.command()
def delete_translation(
    username: str = typer.Option(..., "--username"),
    translation_id: int = typer.Option(..., "--id")
):
    session = get_db_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            typer.echo(f"User '{username}' not found.")
            return

        translation = session.query(Translation).filter_by(id=translation_id, user_id=user.id).first()
        if translation:
            session.delete(translation)
            session.commit()
            typer.echo(f"Translation with ID {translation_id} deleted successfully for user '{username}'.")
        else:
            typer.echo(f"Translation with ID {translation_id} not found for user '{username}'.")
    except Exception as e:
        session.rollback()
        typer.echo(f"An error occurred: {str(e)}")
    finally:
        session.close()


@app.command()
def list_all_translations():
    session = get_db_session()
    try:
        translations = session.query(Translation).join(User).all()
        if translations:
            typer.echo("All translations:")
            for trans in translations:
                typer.echo(f"ID: {trans.id}")
                typer.echo(f"User: {trans.user.username}")
                typer.echo(f"Session ID: {trans.session_id}")
                typer.echo(f"English: {trans.english_text}")
                typer.echo(f"Bengali: {trans.bengali_text}")
                typer.echo(f"Translated at: {trans.translated_at}")
                typer.echo("---")
        else:
            typer.echo("No translations found in the database.")
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    app()   