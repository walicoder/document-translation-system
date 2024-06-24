# Document Translation Service
A bengali to english document translation service based on HF sequence model.
model source: https://huggingface.co/csebuetnlp/banglat5_nmt_bn_en

## DataBase CLI Commands:
- add_user: Adds a new user with the provided username and password.
    - Usage: PYTHONPATH=. python src/cli/user.py add-user --username <username> --password <password>
- delete_user: Deletes a user by username and cleans up associated translations and file translations.
    - Usage: PYTHONPATH=. python src/cli/user.py delete-user --username <username>
- delete_all_users: Deletes all users from the database and their associated translations and file translations.
    - Usage: PYTHONPATH=. python src/cli/user.py delete-all-users


## Text Translation CLI

This CLI script provides functionalities for managing text translations. To run the CLI, use the following command: `PYTHONPATH=. python src/cli/text_translation.py`. 

Available Commands: 
1. **Add Translation**: Adds a new translation with the provided English and Bengali text for a specific user. Usage: `PYTHONPATH=. python src/cli/text_translation.py add-translation --username <username> --english-text "<english text>" --bengali-text "<bengali text>"`. 
2. **List Translations**: Lists all translations for a specific user. Usage: `PYTHONPATH=. python src/cli/text_translation.py list-translations --username <username>`. 
3. **Delete Translation**: Deletes a specific translation by its ID for a given user. Usage: `PYTHONPATH=. python src/cli/text_translation.py delete-translation --username <username> --id <translation_id>`. 

**Note:** Ensure to use quotes around the English and Bengali text inputs if they contain spaces or special characters.

# FastApi Commands:
- Authenticate a user:
    - Usage: `curl -X POST "http://localhost:8000/validate-user" -H "Content-Type: application/json" -d '{"username":"walima","password":"123456"}'`
- Get all the translation: 
    - Usage: `curl -X GET "http://localhost:8000/users/walima/translations/"`
- Create a New translation:
    - Usage `curl -X POST "http://localhost:8000/users/johndoe/translations/" \
     -H "Content-Type: application/json" \
     -d '{
           "english_text": "Hello, how are you?",
           "bengali_text": "হ্যালো, আপনি কেমন আছেন?",
           "session_id": "03b9c1b8-b2f3-46eb-953c-94446464bf45"
         }'`
