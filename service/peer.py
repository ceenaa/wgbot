import model.peer
import repo.peer
import wg_tools.wg as wg_tools


def get_peer(name):
    data = repo.peer.get_peer_by_name(name)

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
    peer.latest_handshake = updated_peer.latest_handshake
    peer.transfer += updated_peer.transfer
    peer.endpoint = updated_peer.endpoint

    return peer


def get_all_peers():
    datas = repo.peer.get_all_peers()
    peers = []
    for data in datas:
        peer = get_peer(data[0])
        peers.append(peer)

    return peers


def pause_peer(name):
    peer = get_peer(name)
    peer.active = 0
    repo.peer.update_peer(peer)

    wg_tools.pause_peer(peer.public_key, peer.allowed_ips)


def resume_peer(name):
    peer = get_peer(name)
    peer.active = 1
    repo.peer.update_peer(peer)

    wg_tools.resume_peer(peer.public_key, peer.allowed_ips, peer.pre_shared_key)


def reset_peer(name):
    peer = get_peer(name)

    if peer.active == 0:
        peer.active = 1
        peer.transfer = 0

        wg_tools.resume_peer(peer.public_key, peer.allowed_ips, peer.pre_shared_key)

    else:
        peer.transfer = 0

        wg_tools.pause_peer(peer.public_key, peer.allowed_ips)
        wg_tools.resume_peer(peer.public_key, peer.allowed_ips, peer.pre_shared_key)

    repo.peer.update_peer(peer)


def update_all_peers():
    peers = get_all_peers()
    for peer in peers:
        updated_peer = wg_tools.get_peer(peer.public_key)
        peer.latest_handshake = updated_peer.latest_handshake
        peer.transfer += updated_peer.transfer
        peer.endpoint = updated_peer.endpoint
        repo.peer.update_peer(peer)
