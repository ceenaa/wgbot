from dotenv import load_dotenv
import repo.peer
import initializers.database

initializers.database.connect_to_db()
load_dotenv()

repo.peer.import_data()

