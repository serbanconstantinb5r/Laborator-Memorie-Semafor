# Laborator Sisteme de Operare — memorie partajata si semafor

## Scop
Doua procese distincte (cu PID-uri diferite) modifica acelasi contor stocat intr-o zona de memorie partajata, pana cand contorul ajunge la **1000**.

## Tehnologii
- Python 3.8+ (biblioteca standard, fara dependinte externe)
- `multiprocessing.shared_memory.SharedMemory`: memorie partajata, mapata in memoria proceselor
- `multiprocessing.Semaphore(1)`: acces exclusiv la zona critica
- `multiprocessing.Process`: creeaza doua procese distincte ale sistemului de operare

## Algoritm
1. Procesul principal creeaza 4 octeti de memorie partajata si initializeaza contorul cu 0.
2. Creeaza semaforul cu valoarea initiala 1.
3. Porneste doua procese copil, care deschid aceeasi memorie partajata.
4. Fiecare proces repeta:
   - rezerva semaforul (`acquire`);
   - citeste valoarea curenta din memoria partajata;
   - cat timp rezultatul aleator este **2**, creste contorul cu 1 si il scrie inapoi in memorie (fara a depasi 1000);
   - elibereaza semaforul (`release`);
   - face o pauza foarte scurta pentru a permite schimbarea procesului activ.
5. Cand contorul devine 1000, ambele procese se termina.
6. Procesul principal verifica rezultatul si elibereaza resursele.

> Folosim `random.randint(1, 2)` deoarece valorile posibile sunt 1 si 2. `random.randrange(2)` ar produce 0 sau 1, deci nu ar putea produce 2.

## Rulare pe Windows in VS Code
Deschideti folderul proiectului in VS Code si deschideti **Terminal > New Terminal**.

Verificati Python:

```powershell
py --version
```

Porniti programul:

```powershell
py main.py
```

Daca `py` nu este recunoscut, incercati `python --version` si `python main.py`.

Nu este necesara instalarea unor pachete externe.

## Rezultat asteptat
Mesajele vor fi intercalate diferit la fiecare rulare, deoarece numararea este aleatoare. Vor aparea doua PID-uri diferite si la final:

```text
Valoarea finala din memoria partajata: 1000
Succes: cele doua procese au numarat corect pana la 1000!
```

## Publicare pe GitHub
Din terminalul VS Code, aflat in acest folder:

```powershell
git init
git add .
git commit -m "Laborator memorie partajata si semafor"
git branch -M main
git remote add origin https://github.com/UTILIZATOR/NUME-REPO.git
git push -u origin main
```

Inlocuiti `UTILIZATOR` si `NUME-REPO` cu valorile depozitului pe care l-ati creat pe GitHub. Pentru un repo nou, nu initializati pe GitHub cu README separat (acest proiect include deja unul).
