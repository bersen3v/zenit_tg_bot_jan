class Freebet:
    def __init__(self, name: str, summa, uuid: str):
        self.name = name,
        self.summa = summa,
        self.uuid = uuid,

    def to_json(self):
        return {'name': self.name[0], 'summa': self.summa, 'uuid': self.uuid}
