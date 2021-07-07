from  datetime import datetime
import os
import tempfile
from time import sleep
from operator import itemgetter
from app.services.files import Files
from app.services.clients import Clients
from app.domain.client_dto import Client
from concurrent.futures.thread import ThreadPoolExecutor
import itertools

attr_slicer = itemgetter(slice(0, 19), slice(19, 31), slice(31, 43), slice(43, 65),
                         slice(65, 87), slice(87, 111), slice(111, 131), slice(131, 149))

clients_service = Clients()
files_service = Files()


def store_client(line, file_id):
    raw_client_data = Client(*attr_slicer(line))

    error = clients_service.store_client(raw_client_data, file_id)
    if error:
        clients_service.store_error(line, file_id, error)


def process():
    with ThreadPoolExecutor(max_workers=8) as executor:
        while True:
            unprocessed_file = files_service.get_one_from_unprocessed()
            if not unprocessed_file:
                sleep(5)
                continue

            print('processando arquivo')

            new_file, filename = tempfile.mkstemp()
            with os.fdopen(new_file, 'wb') as tmp_write:
                tmp_write.write(unprocessed_file[1])

            started = datetime.now()
            file_id = unprocessed_file[0]
            with open(filename) as tmp_read:
                count = 0
                batch = []
                for line in tmp_read.readlines():
                    if count == 0:
                        count = count + 1
                        continue

                    batch.append(line)
                    if len(batch) >= 40:
                        _ = list(executor.map(store_client, batch, itertools.repeat(file_id)))
                        batch = []

                    count = count + 1

                if len(batch) >= 1:
                    _ = list(executor.map(store_client, batch, itertools.repeat(file_id)))

                print(count)

            files_service.mark_processed(file_id)
            os.remove(filename)
            print('started: ' + started.strftime('%Y-%m-%d %H:%M:%S'))
            print('finished: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    # sem paralelismo
    # started: 2021-07-06 20: 59:20
    # finished: 2021-07-06 21: 07:04

    # com paralelismo
    # started: 2021-07-07 00:04:09
    # finished: 2021-07-07 00:07:06
    process()
