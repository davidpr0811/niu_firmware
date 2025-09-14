#!/usr/bin/env python3

# Quick test of firmware comparison
import os

# Simple file comparison
def compare_files(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()
    
    print(f"File 1: {len(data1)} bytes")
    print(f"File 2: {len(data2)} bytes")
    
    if len(data1) != len(data2):
        print("Different sizes!")
        return
    
    differences = []
    for i in range(len(data1)):
        if data1[i] != data2[i]:
            differences.append((i, data1[i], data2[i]))
    
    print(f"Total differences: {len(differences)}")
    print("First 20 differences:")
    for i, (offset, old, new) in enumerate(differences[:20]):
        print(f"  0x{offset:04x}: {old:02x} -> {new:02x}")

if __name__ == "__main__":
    file1 = "kiqi3pro(beta)/OTA_NIU_K3E13J24_32KPH_Pro_221114_modified.bin"
    file2 = "kiqi3pro(beta)/OTA_NIU_K3E13J24_40KPH_Patched.bin"
    compare_files(file1, file2)