"""
the base object for persisting into db in the consistent hash ring
"""
import uuid
import hashlib


class Base:
    def __init__(self):
        self.partition_id = uuid.uuid4().hex

    """
    the hashed value of the id(entry)
    """
    def hashed(self):
        sha1 = hashlib.sha1()
        sha1.update(bytes(self.partition_id, 'utf-8'))
        return int(sha1.hexdigest()[:16], 16)

    """
    raw of the id
    """
    def raw(self):
        return int(self.partition_id[:16], 16)


class vnodes:
    def __init__(self):
        self.vnodes = []
        self.counts = 0x2000
        step = int((1 << 64) / self.counts)
        for c in range(0,  self.counts):
            self.vnodes.append(tuple((c, c*step, (c+1)*step)))

    def dump(self):
        for v in self.vnodes:
            print(v)


class host:
    def __init__(self, rangeFrom, rangeTo, ip):
        self.rangeFrom = rangeFrom
        self.rangeTo = rangeTo
        self.ip = ip

    def __repr__(self):
        # return 'node:{} /{}/{}'.format(self.ip, self.rangeFrom, self.rangeTo)
        return 'node:{}'.format(int(self.rangeFrom/2048))


nodes = vnodes()
# nodes.dump()
hosts = []
span = int(nodes.counts/4)
for i in range(0, 4):
    hosts.append(host(i * span, (i + 1) * span - 1, '{}.{}'.format(i * span, (i + 1) * span - 1)))


def test_distribution():
    for i in range(0, 1000):
        b = Base()
        for n in nodes.vnodes:
            (c, rangeFrom, rangeTo) = n
            # hashed = b.raw()
            hashed = b.hashed()
            if hashed >= rangeFrom and hashed < rangeTo:
                # print('{} in {}'.format(hashed, c))
                for h in hosts:
                    if c in range(h.rangeFrom, h.rangeTo + 1):
                        print(h)

test_distribution()
