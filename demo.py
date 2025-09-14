#!/usr/bin/env python3
"""
NIU Firmware Patcher Demo

This demonstrates how to use the NIU firmware patching tool
to modify speed limits and other parameters.
"""

import os
import subprocess
import sys

def run_command(cmd):
    """Run a shell command and return output"""
    print(f"\n> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Error:", result.stderr)
    return result.returncode == 0

def main():
    print("NIU Firmware Patcher Demo")
    print("=" * 40)
    
    # Check if we have firmware files
    test_firmware = "kiqi3pro(beta)/OTA_NIU_K3E13J24_32KPH_Pro_221114_modified.bin"
    if not os.path.exists(test_firmware):
        print(f"Error: Test firmware not found: {test_firmware}")
        return 1
    
    # 1. Analyze firmware structure
    print("\n1. Analyzing firmware structure...")
    run_command(f"python3 niu_firmware_patcher.py '{test_firmware}' --analyze")
    
    # 2. Find speed patterns
    print("\n2. Finding speed patterns...")
    run_command(f"python3 niu_firmware_patcher.py '{test_firmware}' --find-speeds | head -20")
    
    # 3. Analyze speed modification candidates  
    print("\n3. Analyzing speed modification candidates...")
    run_command(f"python3 niu_firmware_patcher.py '{test_firmware}' --speed-candidates")
    
    # 4. Extract strings
    print("\n4. Extracting readable strings...")
    run_command(f"python3 niu_firmware_patcher.py '{test_firmware}' --extract-strings")
    
    # 5. Compare firmware files if we have them
    comparison_firmware = "kiqi3pro(beta)/OTA_NIU_K3E13J24_40KPH_Patched.bin"
    if os.path.exists(comparison_firmware):
        print("\n5. Comparing firmware files...")
        run_command(f"python3 niu_firmware_patcher.py '{test_firmware}' --compare '{comparison_firmware}'")
    
    print("\n" + "=" * 40)
    print("Demo completed!")
    print("\nTo patch firmware:")
    print(f"python3 niu_firmware_patcher.py '{test_firmware}' --patch-speed 32 40 --apply-patches --output patched.bin")
    print("\nNote: Actual patching requires careful validation and may need manual adjustment")
    print("based on the specific firmware encryption/compression used.")

if __name__ == "__main__":
    sys.exit(main())