# NIU Firmware Decompiler/Patcher Tool

Ein Python-Tool zum Analysieren, Dekompilieren, Modifizieren und Recompilieren von NIU Scooter Firmware-Dateien.

## Features

- **Firmware-Analyse**: Analysiert Binärstruktur, Entropie und Magic Bytes
- **Geschwindigkeits-Pattern-Erkennung**: Findet potentielle Geschwindigkeitswerte in verschiedenen Byte-Repräsentationen
- **Patch-Vorschläge**: Schlägt sichere Modifikationen für Geschwindigkeitslimits vor
- **Firmware-Vergleich**: Vergleicht verschiedene Firmware-Versionen
- **String-Extraktion**: Extrahiert lesbare Strings aus der Firmware
- **Automatisches Patching**: Erstellt gepatchte Firmware-Dateien

## Installation

Keine zusätzlichen Dependencies erforderlich - verwendet nur Python Standard-Bibliotheken.

## Verwendung

### Grundlegende Analyse

```bash
# Firmware-Struktur analysieren
python3 niu_firmware_patcher.py firmware.bin --analyze

# Geschwindigkeits-Pattern finden
python3 niu_firmware_patcher.py firmware.bin --find-speeds

# Patch-Kandidaten analysieren
python3 niu_firmware_patcher.py firmware.bin --speed-candidates
```

### Firmware-Vergleich

```bash
# Zwei Firmware-Dateien vergleichen
python3 niu_firmware_patcher.py firmware1.bin --compare firmware2.bin
```

### Geschwindigkeit patchen

```bash
# Von 32 KPH auf 40 KPH patchen
python3 niu_firmware_patcher.py firmware.bin --patch-speed 32 40 --apply-patches --output patched.bin
```

### Vollständige Demo

```bash
# Demo-Script ausführen
python3 demo.py
```

## Unterstützte NIU Modelle

- KQI2 Pro (DE, EU, US)
- KQI3 Sport (DE, EU, US) 
- KQI3 Pro (DE, EU, US)
- KQI3 Max (DE, EU, US)
- KQI300 X (DE)

## Geschwindigkeitswerte

Das Tool erkennt folgende Geschwindigkeitswerte:
- 20 KPH (Sport DE)
- 25 KPH (Sport EU)
- 28 KPH (Sport US)
- 32 KPH (Pro)
- 38 KPH (Max Trick-Modus)
- 40 KPH (Max)

## Sicherheitshinweise

⚠️ **WICHTIG**: 
- Immer ein Backup der Original-Firmware erstellen
- Gepatchte Firmware vor der Installation gründlich testen
- Modifikationen können die Garantie verlieren lassen
- In einigen Ländern können Geschwindigkeitsmodifikationen illegal sein

## Technische Details

### Firmware-Format
- Binärdateien (~27KB)
- Hohe Entropie (verschlüsselt/komprimiert)
- Verschiedene Byte-Repräsentationen für Geschwindigkeitswerte

### Pattern-Erkennung
Das Tool sucht nach Geschwindigkeitswerten in folgenden Formaten:
- Single Byte (Little Endian)
- 2 Bytes (Little/Big Endian) 
- Geschwindigkeit × 10
- Geschwindigkeit × 100

### Konfidenz-Bewertung
Patch-Vorschläge erhalten Konfidenz-Scores basierend auf:
- Anzahl der Vorkommen (2-5 = hohe Konfidenz)
- Pattern-Konsistenz
- Byte-Alignment

## Beispiele

### Beispiel 1: Firmware analysieren
```bash
python3 niu_firmware_patcher.py "KQI 3/Pro/DE/OTA_NIU_K3E13J24_32KPH_Pro_221114.bin" --analyze
```

Ausgabe:
```
Firmware Analysis:
  Size: 27648 bytes
  MD5: 7c0d3cbd8e0828c8921b44ec156191ed
  First 16 bytes: 390b8188551bd6e391606ddcd4b64d3f
  Entropy estimate: 5.91
```

### Beispiel 2: Geschwindigkeits-Kandidaten finden
```bash
python3 niu_firmware_patcher.py firmware.bin --speed-candidates
```

Ausgabe:
```
Speed Modification Candidates:
  32 KPH (20):
    Occurrences: 103
    Sample positions: ['0x0011', '0x0304', '0x0461']
  40 KPH (28):
    Occurrences: 121
    Sample positions: ['0x0083', '0x00a8', '0x0157']
```

## Entwicklung

### Code-Struktur
- `FirmwareAnalyzer`: Analysiert Firmware-Binärdateien
- `FirmwarePatcher`: Führt Modifikationen durch
- `compare_firmware_files()`: Vergleicht verschiedene Versionen

### Erweiterung
Das Tool kann erweitert werden für:
- Weitere Parameter (Beschleunigung, Bremsung)
- Andere Scooter-Modelle
- Verschlüsselung/Kompression-Handling
- GUI-Interface

## Troubleshooting

### Problem: "No suitable patterns found"
- Firmware könnte stark verschlüsselt sein
- Versuche `--find-speeds` um alle Pattern zu sehen
- Nutze `--compare` mit bekannten Firmware-Varianten

### Problem: "Files are very different"
- Normal bei verschlüsselten Firmware-Dateien
- Jede Firmware-Version kann komplett anders encodiert sein

## Lizenz

Dieses Tool ist für Bildungs- und Forschungszwecke gedacht. Nutzer sind selbst verantwortlich für die Einhaltung lokaler Gesetze und Garantiebestimmungen.