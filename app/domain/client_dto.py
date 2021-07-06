from collections import namedtuple

Client = namedtuple('Client', ['doc_number', 'private', 'incomplete',
                               'last_purchase_date', 'average_ticket',
                               'last_purchase_ticket', 'most_frequent_store',
                               'last_purchase_store'])