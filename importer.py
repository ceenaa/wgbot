from dotenv import load_dotenv
# import repo.peer
import initializers.database
import service.peer

initializers.database.init()
load_dotenv()

# repo.peer.import_data()
service.peer.activate_active_peer()

initializers.database.DB.close()
