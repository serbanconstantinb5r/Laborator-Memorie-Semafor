"""Laborator Sisteme de Operare: doua procese, memorie partajata, semafor."""

import multiprocessing as mp
from multiprocessing import shared_memory
import os
import random
import struct
import time

LIMITA = 1000


def proces_numarare(nume, nume_memorie, semafor):
    """Citeste/incrementeaza contorul comun doar in sectiunea critica."""
    memorie = shared_memory.SharedMemory(name=nume_memorie)
    generator = random.Random()
    modificari = 0

    print(f"{nume} pornit (PID={os.getpid()})", flush=True)

    try:
        while True:
            semafor.acquire()  # Un singur proces poate accesa memoria.
            try:
                numar = struct.unpack_from("i", memorie.buf, 0)[0]

                if numar >= LIMITA:
                    break

                # 'Moneda' are doua rezultate posibile: 1 sau 2.
                # Cat timp rezultatul este 2, marim contorul comun.
                while numar < LIMITA and generator.randint(1, 2) == 2:
                    numar += 1
                    struct.pack_into("i", memorie.buf, 0, numar)
                    modificari += 1

                    # Un mesaj rar, ca sa nu afisam toate cele 1000 de numere.
                    if numar == 1 or numar % 100 == 0:
                        print(f"{nume} (PID={os.getpid()}): {numar}", flush=True)
            finally:
                semafor.release()  # Eliberam si cand am iesit prin break.

            # Oferim si celuilalt proces timp sa intre in sectiunea critica.
            time.sleep(0.001)
    finally:
        print(f"{nume}: a efectuat {modificari} incrementari.", flush=True)
        memorie.close()


def main():
    context = mp.get_context("spawn")  # Compatibil si cu Windows.
    semafor = context.Semaphore(1)
    memorie = shared_memory.SharedMemory(create=True, size=4)
    procese = []

    try:
        struct.pack_into("i", memorie.buf, 0, 0)

        for nume in ("Procesul 1", "Procesul 2"):
            proces = context.Process(
                target=proces_numarare,
                args=(nume, memorie.name, semafor),
                name=nume,
            )
            procese.append(proces)
            proces.start()

        for proces in procese:
            proces.join()  # Asteptam ca ambele procese sa termine.

        valoare_finala = struct.unpack_from("i", memorie.buf, 0)[0]
        print(f"\nValoarea finala din memoria partajata: {valoare_finala}")

        if valoare_finala == LIMITA and all(p.exitcode == 0 for p in procese):
            print("Succes: cele doua procese au numarat corect pana la 1000!")
        else:
            print("Eroare: verificati iesirea proceselor.")
    finally:
        for proces in procese:
            if proces.is_alive():
                proces.terminate()
                proces.join()
        memorie.close()
        memorie.unlink()  # Stergem zona partajata cand nu mai e folosita.


if __name__ == "__main__":
    mp.freeze_support()
    main()
