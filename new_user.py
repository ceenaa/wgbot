from dotenv import load_dotenv
import repo.peer
import initializers.database

initializers.database.init()
load_dotenv()

repo.peer.register_new_peers()
initializers.database.DB.close()

