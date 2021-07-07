from app.database import get_connection


class Files:
    def __init__(self):
        self.files_data_manager = None

    def store(self, name, content, file_type):
        with get_connection() as (conn, cur):
            filedata = content.read()
            cur.execute("INSERT INTO files(name, content, type, created_at) VALUES (%s,%s,%s,now()) RETURNING id",
                        (name, filedata, file_type))

    def get_one_from_unprocessed(self):
        with get_connection() as (conn, cur):
            cur.execute('SELECT id, content, type FROM files WHERE processed_at is null limit 1')
            return_value = cur.fetchone()
            return return_value

    def mark_processed(self, file_id):
        with get_connection() as (conn, cur):
            cur.execute('UPDATE files SET processed_at = now() WHERE  id = %s', [file_id])
