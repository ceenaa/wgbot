from dotenv import load_dotenv
import repo.peer
import initializers.database

initializers.database.init()
load_dotenv()

repo.peer.import_data()
initializers.database.DB.close()

