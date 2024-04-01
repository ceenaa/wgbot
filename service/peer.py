import model.peer
import repo.peer
import wg_tools.wg as wg_tools


# get a peer by name first from the database and then from the wireguard interface
# then return the peer
def get_peer(name):
    data = repo.peer.get_peer_by_name(name)

    # if the peer is not found in the database, raise an exception
    if data is None:
        raise Exception("Peer not found")

    peer = model.peer.Peer(
        name=data[0],
        public_key=data[1],
        pre_shared_key=data[2],
        endpoint=data[3],
        allowed_ips=data[4],
        latest_handshake=data[5],
        transfer=data[6],
        active=data[7]
    )

    updated_peer = wg_tools.get_peer(peer.public_key)

    # if the peer is found in the wireguard interface, update the peer's latest handshake, transfer, and endpoint
    if updated_peer is not None:
        peer.latest_handshake = updated_peer.latest_handshake
        peer.transfer += updated_peer.transfer
        peer.endpoint = updated_peer.endpoint

    # if the peer is not found in the wireguard interface, return the peer from the database
    return peer


# get all peers like get_peer
def get_all_peers():
    datas = repo.peer.get_all_peers()
    peers = []
    for data in datas:
        peer = get_peer(data[0])
        peers.append(peer)

    return peers


def get_all_active_peers():
    datas = repo.peer.get_all_active_peers()
    peers = []
    for data in datas:
        peer = get_peer(data[0])
        peers.append(peer)

    return peers


# get short form of a peer by name, return the name, transfer, and active status
# used for displaying peers in the Google sheet interface
# totally works like get_peer
def get_short_peer(name):
    data = repo.peer.get_short_peer(name)

    if data is None:
        raise Exception("Peer not found")

    public_key = data[0]
    transfer = data[1]
    active = data[2]

    updated_peer = wg_tools.get_peer(public_key)
    if updated_peer is not None:
        transfer += updated_peer.transfer

    return [name, transfer, active]


# get all peers in short form, with the same logic as get_all_peers
def get_short_all_peers():
    datas = repo.peer.get_all_peers()
    peers = []
    for data in datas:
        peer = get_short_peer(data[0])
        peers.append(peer)

    return peers


# pause a peer by name
def pause_peer(name):
    # get the peer by name (it get updated from the wireguard interface)
    peer = get_peer(name)
    # set the active status to 0
    peer.active = 0
    # update the peer in the database
    repo.peer.update_peer(peer)
    # pause the peer in the wireguard interface
    wg_tools.pause_peer(peer.public_key, peer.allowed_ips)


# resume a peer by name
def resume_peer(name):
    # get the peer by name (it get updated from the wireguard interface)
    peer = get_peer(name)
    # set the active status to 1
    peer.active = 1
    # update the peer in the database
    repo.peer.update_peer(peer)
    # resume the peer in the wireguard interface
    wg_tools.resume_peer(peer.public_key, peer.allowed_ips, peer.pre_shared_key)


# reset a peer transfer by name
def reset_peer(name):
    # get the peer by name (it get updated from the wireguard interface)
    peer = get_peer(name)

    # if the peer is inactive, activate it and reset the transfer
    if peer.active == 0:
        peer.active = 1
        peer.transfer = 0
        # then resume the peer in the wireguard interface
        wg_tools.resume_peer(peer.public_key, peer.allowed_ips, peer.pre_shared_key)

    # if the peer is active, just reset the transfer
    else:
        peer.transfer = 0
        # then pause the peer in the wireguard interface
        wg_tools.pause_peer(peer.public_key, peer.allowed_ips)
        # then resume the peer in the wireguard interface
        wg_tools.resume_peer(peer.public_key, peer.allowed_ips, peer.pre_shared_key)
    # at the end, update the peer in the database
    repo.peer.update_peer(peer)


# get all peers (which get updated from the wireguard interface) and update them in the database
def update_all_peers():
    peers = get_all_peers()
    for peer in peers:
        repo.peer.update_peer(peer)


def activate_active_peer():
    active_peers = get_all_active_peers()
    for peer in active_peers:
        wg_tools.resume_peer(peer.public_key, peer.allowed_ips, peer.pre_shared_key)
