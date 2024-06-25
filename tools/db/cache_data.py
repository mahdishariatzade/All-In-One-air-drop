import pickledb


class SimpleCache:
    def __init__(self, db_name):
        self.db = pickledb.load(f'databases/{db_name}.db', True)

    def set(self, key, value):
        status = self.db.set(key, value)
        self.db.dump()
        return status

    def get(self, key):
        return self.db.get(key)

    def exists(self, key):
        return key in self.db.getall()

    def clear(self):
        self.db.deldb()
