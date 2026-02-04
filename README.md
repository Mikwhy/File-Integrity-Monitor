# File Integrity Monitor

[![Website](https://img.shields.io/badge/Website-mikwhy.dev-blue?style=for-the-badge&logo=googlechrome&logoColor=white)](https://mikwhy.dev)
[![Python](https://img.shields.io/badge/Python-3.7+-green?style=for-the-badge&logo=python&logoColor=white)]()
[![Security](https://img.shields.io/badge/Type-Security%20Tool-red?style=for-the-badge&logo=shield&logoColor=white)]()

---

**[English](#english)** | **[Polski](#polski)**

---

## English

### What is FIM?

A simple **File Integrity Monitor** that detects unauthorized changes to your files. It creates SHA256 hashes of files and alerts you when something changes.

### Features

- Monitor files or entire folders
- SHA256 hashing
- Detect modified files
- Detect deleted files
- JSON baseline storage
- Zero dependencies (stdlib only)

### Installation

```bash
git clone https://github.com/Mikwhy/File-Integrity-Monitor.git
cd FileIntegrityMonitor
```

### Usage

```bash
# create baseline from folder
python fim.py init C:\path\to\folder

# create baseline from specific files
python fim.py init config.ini data.db

# check for changes
python fim.py check

# add new files to monitor
python fim.py add newfile.txt

# accept changes (update baseline)
python fim.py update

# show status
python fim.py status

# remove file from monitoring
python fim.py remove oldfile.txt
```

### Commands

| Command | Description |
|---------|-------------|
| `init <path>` | Create baseline from files/folders |
| `add <path>` | Add files to existing baseline |
| `remove <path>` | Remove files from baseline |
| `check` | Check files against baseline |
| `update` | Update baseline with current hashes |
| `status` | Show baseline info |

---

## Polski

### Czym jest FIM?

Prosty **File Integrity Monitor** wykrywajacy nieautoryzowane zmiany w plikach. Tworzy hashe SHA256 plikow i alertuje gdy cos sie zmieni.

### Funkcje

- Monitorowanie plikow lub calych folderow
- Hashowanie SHA256
- Wykrywanie zmodyfikowanych plikow
- Wykrywanie usunietych plikow
- Przechowywanie baseline w JSON
- Zero zaleznosci (tylko stdlib)

### Instalacja

```bash
git clone https://github.com/Mikwhy/File-Integrity-Monitor.git
cd FileIntegrityMonitor
```

### Uzycie

```bash
# stworz baseline z folderu
python fim.py init C:\sciezka\do\folderu

# stworz baseline z konkretnych plikow
python fim.py init config.ini data.db

# sprawdz zmiany
python fim.py check

# dodaj nowe pliki do monitorowania
python fim.py add nowyplik.txt

# zaakceptuj zmiany (zaktualizuj baseline)
python fim.py update

# pokaz status
python fim.py status

# usun plik z monitorowania
python fim.py remove staryplik.txt
```

### Komendy

| Komenda | Opis |
|---------|------|
| `init <sciezka>` | Tworzy baseline z plikow/folderow |
| `add <sciezka>` | Dodaje pliki do baseline |
| `remove <sciezka>` | Usuwa pliki z baseline |
| `check` | Sprawdza pliki vs baseline |
| `update` | Aktualizuje baseline |
| `status` | Pokazuje info o baseline |

### Przyklad

```
C:\> python fim.py init C:\wazne\pliki
[*] hashing 15 files...
  [+] C:\wazne\pliki\config.ini
  [+] C:\wazne\pliki\data.db
  ...
[ok] baseline created: 15 files

C:\> python fim.py check
[*] checking 15 files...

[!] MODIFIED FILES:
  C:\wazne\pliki\config.ini
    old: a1b2c3d4e5f6...
    new: 9f8e7d6c5b4a...

--- summary ---
ok: 14 | modified: 1 | deleted: 0
```

---

## How it works

```
                    INIT                              CHECK
                     |                                  |
    [your files] --> | --> SHA256 hash                  |
                     |        |                         |
                     v        v                         v
              +------------------+              +------------------+
              |  baseline.json   |  <-------->  |  compare hashes  |
              +------------------+              +------------------+
                                                        |
                                         +--------------+--------------+
                                         |              |              |
                                        OK          MODIFIED       DELETED
```

---

## Use Cases

- Monitor server config files
- Detect malware file modifications
- Verify backup integrity
- Track changes in critical directories

---

<p align="center">
  <a href="https://mikwhy.dev">
    <img src="https://img.shields.io/badge/Made%20by-Mikwhy-black?style=for-the-badge" alt="Made by Mikwhy">
  </a>
</p>
