from gui import *
from server import start_server

import threading

server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

root.mainloop()
