from app.database import get_connection
from app.domain.client_dto import Client
from datetime import datetime
from validate_docbr import CPF, CNPJ

import re


class Clients:
    def store_client(self, raw_client, file_id):
        with get_connection() as (conn, cur):
            try:
                sc = self.__sanitize_data(raw_client)
                cur.execute('INSERT INTO clients(doc_number, private, incomplete, last_purchase_at, average_ticket, '
                            'last_purchase_ticket, most_frequent_store, last_purchase_store, file_id, created_at) '
                            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())',
                            (sc.doc_number, sc.private, sc.incomplete, sc.last_purchase_date, sc.average_ticket,
                             sc.last_purchase_ticket, sc.most_frequent_store, sc.last_purchase_store, file_id))
                return None
            except Exception as e:
                return str(e)

    def store_error(self, client_data, file_id, msg):
        with get_connection() as (conn, cur):
            cur.execute('INSERT INTO error_logs(file_id, touple_content, message, occured_at) VALUES(%s, %s, %s, now())',
                        (file_id, client_data, msg))


    def __sanitize_data(self, client: Client):
        def strip_and_treat_null(value):
            value = value.strip()
            return None if value == 'NULL' else value

        def parse_date(value):
            return datetime.strptime(value, '%Y-%m-%d')

        def remove_punct(value):
            if not value:
                return value
            return re.sub('[-./]', '', value)

        def parse_decimal(value):
            if not isinstance(value, str):
                return value
            return value.replace(',', '.')

        doc_number = remove_punct(strip_and_treat_null(client.doc_number))
        is_valid_doc = CPF().validate(doc_number) if len(doc_number) == 11 else CNPJ().validate(doc_number)

        if not is_valid_doc:
            raise Exception('documento inválido')

        private = strip_and_treat_null(client.private)
        incomplete = strip_and_treat_null(client.incomplete)
        last_purch_at = strip_and_treat_null(client.last_purchase_date)
        last_purch_at = parse_date(last_purch_at) if last_purch_at else last_purch_at

        avg_ticket = strip_and_treat_null(client.average_ticket)
        avg_ticket = parse_decimal(avg_ticket)

        last_purch_ticket = strip_and_treat_null(client.last_purchase_ticket)
        last_purch_ticket = parse_decimal(last_purch_ticket)

        most_frqt_store = remove_punct(strip_and_treat_null(client.most_frequent_store))
        last_purch_store = remove_punct(strip_and_treat_null(client.last_purchase_store))

        return Client(doc_number, private, incomplete, last_purch_at, avg_ticket, last_purch_ticket,
                      most_frqt_store, last_purch_store)

