from app.database import get_connection


class Files:
    def __init__(self):
        self.files_data_manager = None

    def store(self, name, content, file_type):
        conn = get_connection()
        cur = conn.cursor()

        filedata = content.read()
        cur.execute("INSERT INTO files(name, content, type, created_at) VALUES (%s,%s,%s,now()) RETURNING id",
                    (name, filedata, file_type))

        returned_id = cur.fetchone()[0]
        conn.commit()


    def get_one_from_unprocessed(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT id, content, type FROM files WHERE processed_at is null limit 1')
        return_value = cur.fetchone()
        conn.close()

        return return_value


if __name__ == "__main__":
    import os
    import tempfile
    from operator import itemgetter

    unprocessed_file = Files().get_first_unprocessed()
    new_file, filename = tempfile.mkstemp()

    with os.fdopen(new_file, 'wb') as tmp_write:
        tmp_write.write(unprocessed_file[1])

    with open(filename) as tmp_read:
        count = 0
        for line in tmp_read.readlines():
            if count == 0:
                count = count + 1
                continue

            get = itemgetter(slice(0, 19), slice(19, 31),
                             slice(31, 43), slice(43, 65),
                             slice(65, 87), slice(87, 111),
                             slice(111, 131), slice(131, 149))

            from collections import namedtuple
            Client = namedtuple('Client', ['doc_number', 'private', 'incomplete',
                                           'last_purchase_date', 'average_ticket',
                                           'last_purchase_ticket', 'most_frequent_store',
                                           'last_purchase_store'])
            Client(*get(line))


            print(line)
            count = count + 1

        x = 5


    x = 5
    os.remove(filename)