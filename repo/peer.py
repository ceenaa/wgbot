import os
import subprocess
from contextlib import closing
from initializers.database import DB


def create_table():
    with closing(DB.cursor()) as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS peers
                     (name TEXT PRIMARY KEY,
                     public_key TEXT NOT NULL,
                     pre_shared_key TEXT NOT NULL,
                     endpoint TEXT NOT NULL,
                     allowed_ips TEXT NOT NULL,
                     latest_handshake TEXT NOT NULL,
                     transfer INTEGER NOT NULL,
                     active INTEGER NOT NULL)
        """
                  )


def get_all_peers():
    with closing(DB.cursor()) as c:
        c.execute("SELECT * FROM peers")
        return c.fetchall()


def get_peer_name(public_key):
    with closing(DB.cursor()) as c:
        c.execute("SELECT name FROM peers WHERE public_key = ?", (public_key,))
        return c.fetchone()[0]


def get_peer_transfer(public_key):
    with closing(DB.cursor()) as c:
        c.execute("SELECT transfer FROM peers WHERE public_key = ?", (public_key,))
        return c.fetchone()


def get_peer_by_name(name):
    with closing(DB.cursor()) as c:
        c.execute("SELECT * FROM peers WHERE name = ?", (name,))
        return c.fetchone()


def is_name_exists(name):
    with closing(DB.cursor()) as c:
        c.execute("SELECT * FROM peers WHERE name = ?", (name,))
        if c.fetchone() is None:
            return False
        return True


def update_peer(peer):
    with closing(DB.cursor()) as c:
        c.execute("INSERT OR REPLACE INTO peers VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                  (peer.name, peer.public_key, peer.pre_shared_key, peer.endpoint, peer.allowed_ips,
                   peer.latest_handshake, peer.transfer, peer.active))


def register_new_peers():
    with closing(DB.cursor()) as c:
        file = open("new_peers.txt", "r")
        lines = file.readlines()
        file.close()
        for i in range(0, len(lines), 6):
            name = lines[i]
            name = name.split(" ")[1]
            public_key = lines[i + 2]
            public_key = public_key.split(" = ")[1]
            public_key = public_key.strip()
            pre_shared_key = lines[i + 4]
            pre_shared_key = pre_shared_key.split(" = ")[1]
            pre_shared_key = pre_shared_key.strip()
            allowed_ips = lines[i + 3]
            allowed_ips = allowed_ips.split(" = ")[1]
            allowed_ips = allowed_ips.strip()
            transfer = 0
            last_handshake = "None"
            endpoint = "None"
            active = True
            sys_name = os.getenv("SYSTEM_NAME")

            c.execute("INSERT OR REPLACE INTO peers VALUES(? ,? ,? ,?, ?, ?, ?, ?)",
                      (name, public_key, pre_shared_key, endpoint, allowed_ips, last_handshake, transfer, active))

            command1 = f"wg set {sys_name} peer \"{public_key}\" allowed-ips {allowed_ips} " \
                       f"preshared-key <(echo \"{pre_shared_key}\")"
            command2 = f"ip -4 route add {allowed_ips} dev {sys_name}"
            subprocess.run(['bash', '-c', command1])
            subprocess.run(['bash', '-c', command2])


def import_data():
    with closing(DB.cursor()) as c:
        file = open("data.txt", "r")
        lines = file.readlines()
        file.close()
        for line in lines:
            line = line.split("\t")
            name = line[0]
            public_key = line[1]
            pre_shared_key = line[2]
            endpoint = line[3]
            allowed_ips = line[4]
            latest_handshake = line[5]
            transfer = line[6]
            active = line[7].strip()
            sys_name = os.getenv("SYSTEM_NAME")

            if active == "1":
                active = 1
            else:
                active = 0
            c.execute("INSERT OR REPLACE INTO peers VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                      (name, public_key, pre_shared_key, endpoint, allowed_ips,
                       latest_handshake, transfer, active))
            if active == 1:
                command1 = f"wg set {sys_name} peer \"{public_key}\" allowed-ips {allowed_ips} " \
                           f"preshared-key <(echo \"{pre_shared_key}\")"
                command2 = f"ip -4 route add {allowed_ips} dev {sys_name}"
                subprocess.run(['bash', '-c', command1])
                subprocess.run(['bash', '-c', command2])
