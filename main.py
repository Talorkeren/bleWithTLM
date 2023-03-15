import asyncio
import hashlib
import time
global new_list
global client
global combine_after_cut
from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
global hash_str_cutted


ADDRESS = "D0:EA:DB:27:FE:17"
UUID = "00001800-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID_READ = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
CHARACTERISTIC_UUID_WRITE = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
CHARACTERISTIC_UUID_SERVICE = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
SECRET_KEY = b'\xCC\xFA\x25\xB7\x4D\x4F\x83\xFD\x5C\x85\xCD\x71\xC6\x79\x6D\x1E'
x = [b'get_param:0001', b'get_param:0002', b'get_param:0003', b'get_param:0008', b'get_param:0097']


async def main():
    global client
    async with BleakClient(ADDRESS, timeout=20.0) as client:
        print(f'Connected - {client.is_connected}')
        print(f'Address - {client.address}')
        # services = await client.get_services()
        # for service in services:
        #     print(f"Service - {service.uuid}")
        #     for char in service.characteristics:
        #         print(f"Characteristic - {char.uuid}")
        await client.start_notify(CHARACTERISTIC_UUID_READ, notification_handler)
        await client.stop_notify(CHARACTERISTIC_UUID_READ)

        await client.start_notify(CHARACTERISTIC_UUID_READ, send_key)
        await client.write_gatt_char(CHARACTERISTIC_UUID_WRITE, hash_str_cutted, True)
        time.sleep(1)
        await client.stop_notify(CHARACTERISTIC_UUID_READ)

        i = 0
        for i in x:
            # new_list = ''
            # print(list)
            print(f'Command --> {i}')
            await client.start_notify(CHARACTERISTIC_UUID_READ, info_from_unit)
            await client.write_gatt_char(CHARACTERISTIC_UUID_WRITE, i, True)
            time.sleep(3)
            # await client.stop_notify(CHARACTERISTIC_UUID_READ)
            print(f' for loop --> {new_list}')

            # val = find_in_str(new_list)

            # print(val)
            # print("endddddddd")

            await client.stop_notify(CHARACTERISTIC_UUID_READ)
            # new_list = ""
            # time.sleep(1)



list = []


def info_from_unit(characteristic: BleakGATTCharacteristic, sent):
    global new_list
    # print(f' info from unit "sent" {sent}')
    sent2 = sent.decode('utf-8')
    list.append(sent2)
    new_list = ''.join(list)
    print(f' info fdrom unit {new_list}')
    # print(new_list)


def find_in_str(new_list):
    val_start = new_list.find('"val":') + 7
    val_end = new_list.find('"', val_start)
    val = new_list[val_start:val_end]
    # print(val)
    return val





def send_key(characteristic: BleakGATTCharacteristic, sent):
    for val in sent:
        print(chr(val), end='')


def notification_handler(characteristic: BleakGATTCharacteristic, data):
    global hash_str_cutted
    print(f'Data from unit --> {data}')
    time.sleep(1)
    print(f'Secret Key --> {SECRET_KEY}')
    secret_sha = hashlib.new("sha256")
    secret_sha.update(data)
    secret_sha.update(SECRET_KEY)
    result = secret_sha.digest()
    print(f'RESULT - {result}')
    hash_str_cutted = result[:20]
    print(f'hash_str_cutted - {hash_str_cutted}')


# asyncio.run(main())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
