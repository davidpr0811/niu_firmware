#!/usr/bin/env python3
"""
NIU Firmware Toolkit - Complete Usage Example

This script demonstrates all features of the NIU firmware toolkit.
"""

import os
import subprocess

def print_section(title):
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print(f"{'='*60}")

def run_example(description, command):
    print(f"\n{description}")
    print(f"Command: {command}")
    print("-" * 40)
    os.system(command)

def main():
    print_section("NIU FIRMWARE TOOLKIT - COMPLETE DEMO")
    
    # Check available firmware files
    firmware_files = [
        "kiqi3pro(beta)/OTA_NIU_K3E13J24_32KPH_Pro_221114_modified.bin",
        "kiqi3pro(beta)/OTA_NIU_K3E13J24_40KPH_Patched.bin",
        "KQI 3/Sport/DE/OTA_NIU_K3E38J23_20KPH_Sport_220718.bin"
    ]
    
    available = [f for f in firmware_files if os.path.exists(f)]
    print(f"\nAvailable firmware files: {len(available)}")
    for f in available:
        print(f"  - {f}")
    
    if not available:
        print("No firmware files found! Please ensure firmware files are present.")
        return
    
    test_firmware = available[0]
    
    print_section("1. BASIC FIRMWARE ANALYSIS")
    run_example(
        "Analyze firmware structure and metadata:",
        f"python3 niu_firmware_patcher.py '{test_firmware}' --analyze"
    )
    
    print_section("2. SPEED PATTERN DETECTION")
    run_example(
        "Find all potential speed-related patterns:",
        f"python3 niu_firmware_patcher.py '{test_firmware}' --find-speeds | head -30"
    )
    
    print_section("3. MODIFICATION CANDIDATES")
    run_example(
        "Analyze best candidates for speed modifications:",
        f"python3 niu_firmware_patcher.py '{test_firmware}' --speed-candidates"
    )
    
    print_section("4. STRING EXTRACTION")
    run_example(
        "Extract readable strings from firmware:",
        f"python3 niu_firmware_patcher.py '{test_firmware}' --extract-strings"
    )
    
    if len(available) >= 2:
        print_section("5. FIRMWARE COMPARISON")
        run_example(
            "Compare two different firmware versions:",
            f"python3 niu_firmware_patcher.py '{available[0]}' --compare '{available[1]}'"
        )
    
    print_section("6. PATCH SUGGESTIONS")
    run_example(
        "Get suggestions for patching to 40 KPH:",
        f"python3 niu_firmware_patcher.py '{test_firmware}' --suggest-patch 40"
    )
    
    print_section("7. MANUAL PATCHING EXAMPLE")
    run_example(
        "Run comprehensive manual patching example:",
        "python3 example_patch.py"
    )
    
    print_section("TOOLKIT SUMMARY")
    print("""
The NIU Firmware Toolkit provides:

✓ Firmware Analysis Tools
  - Binary structure analysis
  - Entropy calculation
  - Magic byte detection
  
✓ Speed Modification Tools  
  - Pattern recognition for speed values
  - Confidence-based patch suggestions
  - Safe modification candidates
  
✓ Comparison Tools
  - Byte-level firmware comparison
  - Difference analysis
  - Pattern identification
  
✓ Safety Features
  - Backup recommendations
  - Confidence scoring
  - Conservative patching

USAGE SCENARIOS:
1. Research: Understand firmware structure
2. Modification: Change speed limits safely  
3. Recovery: Compare working vs broken firmware
4. Development: Create custom firmware variants

IMPORTANT NOTES:
- Always backup original firmware
- Test modifications thoroughly
- Understand legal implications
- Firmware may be encrypted/compressed
""")
    
    print_section("NEXT STEPS")
    print("""
To use this toolkit for your NIU scooter:

1. Identify your exact model and region
2. Download original firmware from the repository
3. Analyze the firmware structure
4. Create test patches with small modifications
5. Validate patches before applying to hardware

For questions or contributions, see the repository README.
""")

if __name__ == "__main__":
    main()