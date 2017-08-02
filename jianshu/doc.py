class Doc:
    title = ''
    date = ''
    tf = 0
    ld = 0
    _id = 0

    def __init__(self, title, date, tf, ld, _id):
        self.title = title
        self.date = date
        self.tf = tf
        self.ld = ld
        self._id = _id

    def __repr__(self):
        return 'title=' + self.title + ', date=' + self.date + ', tf=' + str(self.tf) + ', ld=' + str(self.ld) + \
               ', id=' + self._id

    def __str__(self):
        return 'title=' + self.title + ', date=' + self.date + ', tf=' + str(self.tf) + ', ld=' + str(self.ld) + \
               ', id=' + self._id
