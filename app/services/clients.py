from app.database import get_connection, release_connection
from app.domain.client_dto import Client
import re


class Clients:
    def store_client(cls, raw_client, file_id):
        conn = get_connection()
        cur = conn.cursor()

        sc = cls.__sanitize_data(raw_client)
        cur.execute('INSERT INTO clients(doc_number, private, incomplete, last_purchase_at, average_ticket, '
                    'last_purchase_ticket, most_frequent_store, last_purchase_store, file_id, created_at) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())',
                    (sc.doc_number, sc.private, sc.incomplete, sc.last_purchase_date, sc.average_ticket,
                     sc.last_purchase_ticket, sc.most_frequent_store, sc.last_purchase_store, file_id))

        conn.commit()
        release_connection(conn)


    def __sanitize_data(cls, client: Client):
        def strip_and_treat_null(value):
            value = value.strip()
            return None if value in ['', 'NULL'] else value

        doc_number = re.sub('[-.]', '', strip_and_treat_null(client.doc_number))
        private = strip_and_treat_null(client.private)
        incomplete = strip_and_treat_null(client.incomplete)
        last_purch_at = strip_and_treat_null(client.last_purchase_date)
        avg_ticket = strip_and_treat_null(client.average_ticket)
        last_purch_ticket = strip_and_treat_null(client.last_purchase_ticket)
        most_frqt_store = strip_and_treat_null(client.most_frequent_store)
        last_purch_store = strip_and_treat_null(client.last_purchase_store)

        return Client(doc_number, private, incomplete, last_purch_at, avg_ticket, last_purch_ticket,
                      most_frqt_store, last_purch_store)

