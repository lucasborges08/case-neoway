import os
import tempfile
from operator import itemgetter
from app.services.files import Files
from app.services.clients import Clients
from app.domain.client_dto import Client

attr_slicer = itemgetter(slice(0, 19), slice(19, 31), slice(31, 43), slice(43, 65),
                         slice(65, 87), slice(87, 111), slice(111, 131), slice(131, 149))


def process():
    unprocessed_file = Files().get_one_from_unprocessed()
    new_file, filename = tempfile.mkstemp()

    with os.fdopen(new_file, 'wb') as tmp_write:
        tmp_write.write(unprocessed_file[1])

    with open(filename) as tmp_read:
        count = 0
        for line in tmp_read.readlines():
            if count == 0:
                count = count + 1
                continue

            raw_client_data = Client(*attr_slicer(line))
            Clients().store_client(raw_client_data, unprocessed_file[0])

            print(line)
            count = count + 1

    os.remove(filename)


if __name__ == '__main__':
    process()
