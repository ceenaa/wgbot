from dotenv import load_dotenv

import initializers.database
import service.peer

initializers.database.connect_to_db()
load_dotenv()

service.peer.update_all_peers()
initializers.database.DB.close()

