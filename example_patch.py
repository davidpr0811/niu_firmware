#!/usr/bin/env python3
"""
NIU Firmware Manual Patching Example

This example shows how to manually patch firmware using knowledge
gained from firmware analysis. Since the firmware appears to be 
encrypted/compressed, we'll demonstrate pattern-based patching.
"""

import os
import sys
from niu_firmware_patcher import FirmwareAnalyzer, FirmwarePatcher

def create_test_patch():
    """Create a test patch based on analysis findings"""
    
    # Use the 32KPH firmware as base
    source_firmware = "kiqi3pro(beta)/OTA_NIU_K3E13J24_32KPH_Pro_221114_modified.bin"
    
    if not os.path.exists(source_firmware):
        print(f"Source firmware not found: {source_firmware}")
        return False
    
    print("NIU Firmware Manual Patching Example")
    print("=" * 50)
    
    # 1. Analyze the source firmware
    print("\n1. Analyzing source firmware...")
    analyzer = FirmwareAnalyzer(source_firmware)
    header = analyzer.analyze_header()
    
    print(f"   Source: {source_firmware}")
    print(f"   Size: {header['size']} bytes")
    print(f"   MD5: {header['md5']}")
    print(f"   Entropy: {header['entropy_estimate']:.2f}")
    
    # 2. Find speed patterns
    print("\n2. Finding speed-related patterns...")
    patcher = FirmwarePatcher(source_firmware)
    candidates = patcher.analyze_speed_candidates()
    
    # Show the most promising candidates (moderate occurrence count)
    promising = [c for c in candidates if 2 <= c['occurrences'] <= 20]
    
    print("   Most promising candidates for patching:")
    for candidate in promising[:5]:
        print(f"     {candidate['speed']} KPH: {candidate['occurrences']} occurrences")
        print(f"       Pattern: {candidate['representation']}")
        print(f"       Positions: {[f'0x{p:04x}' for p in candidate['positions'][:5]]}")
    
    # 3. Create a conservative patch
    print("\n3. Creating conservative test patch...")
    
    # Let's try to patch the most conservative candidate
    if promising:
        target_candidate = promising[0]  # Least occurrences
        print(f"   Targeting: {target_candidate['speed']} KPH pattern")
        print(f"   Pattern bytes: {target_candidate['representation']}")
        
        # Create a simple modification: change the first occurrence
        test_patches = []
        original_pattern = target_candidate['byte_pattern']
        
        # Create a modified pattern (just increment the value slightly)
        try:
            original_value = int(target_candidate['speed'])
            new_value = original_value + 2  # Small increment for safety
            
            if len(original_pattern) == 1:
                new_pattern = new_value.to_bytes(1, 'little')
            elif len(original_pattern) == 2:
                # Try to preserve the same format
                if original_pattern == original_value.to_bytes(2, 'little'):
                    new_pattern = new_value.to_bytes(2, 'little')
                elif original_pattern == original_value.to_bytes(2, 'big'):
                    new_pattern = new_value.to_bytes(2, 'big')
                elif original_pattern == (original_value * 10).to_bytes(2, 'little'):
                    new_pattern = (new_value * 10).to_bytes(2, 'little')
                else:
                    new_pattern = new_value.to_bytes(2, 'little')
            else:
                print("   Pattern too complex for simple patching")
                return False
            
            # Apply patch to first occurrence only (conservative)
            first_position = target_candidate['positions'][0]
            test_patches.append((first_position, new_pattern))
            
            print(f"   Patch: position 0x{first_position:04x}")
            print(f"   Change: {original_pattern.hex()} -> {new_pattern.hex()}")
            print(f"   Meaning: {original_value} -> {new_value}")
            
            # 4. Create the patched firmware
            output_file = "test_patched_example.bin"
            print(f"\n4. Creating patched firmware: {output_file}")
            
            success = patcher.create_patched_firmware(output_file, test_patches)
            
            if success:
                # 5. Verify the patch
                print("\n5. Verifying patch...")
                patched_analyzer = FirmwareAnalyzer(output_file)
                patched_header = patched_analyzer.analyze_header()
                
                print(f"   Patched file size: {patched_header['size']} bytes")
                print(f"   Patched MD5: {patched_header['md5']}")
                
                # Quick verification - check if the byte was changed
                with open(source_firmware, 'rb') as f1, open(output_file, 'rb') as f2:
                    data1 = f1.read()
                    data2 = f2.read()
                
                if data1[first_position:first_position+len(original_pattern)] == original_pattern:
                    if data2[first_position:first_position+len(new_pattern)] == new_pattern:
                        print("   ✓ Patch applied successfully!")
                        print(f"   ✓ Verified byte change at position 0x{first_position:04x}")
                    else:
                        print("   ✗ Patch verification failed")
                else:
                    print("   ✗ Original pattern not found at expected position")
                
                print(f"\n6. Example patch completed!")
                print(f"   Original: {source_firmware}")
                print(f"   Patched:  {output_file}")
                print(f"   Change:   {original_value} -> {new_value} at 0x{first_position:04x}")
                
                return True
                
        except ValueError as e:
            print(f"   Error creating patch: {e}")
            return False
    
    else:
        print("   No suitable candidates found for patching")
        return False

def demonstrate_analysis_workflow():
    """Demonstrate the complete analysis workflow"""
    
    print("\n" + "=" * 50)
    print("FIRMWARE ANALYSIS WORKFLOW DEMONSTRATION")
    print("=" * 50)
    
    firmware_files = [
        "kiqi3pro(beta)/OTA_NIU_K3E13J24_32KPH_Pro_221114_modified.bin",
        "kiqi3pro(beta)/OTA_NIU_K3E13J24_40KPH_Patched.bin"
    ]
    
    available_files = [f for f in firmware_files if os.path.exists(f)]
    
    if len(available_files) < 2:
        print("Need at least 2 firmware files for comparison")
        return
    
    print(f"\nAnalyzing {len(available_files)} firmware files...")
    
    for i, firmware in enumerate(available_files):
        print(f"\n--- File {i+1}: {os.path.basename(firmware)} ---")
        analyzer = FirmwareAnalyzer(firmware)
        header = analyzer.analyze_header()
        
        print(f"Size: {header['size']} bytes")
        print(f"MD5: {header['md5']}")
        print(f"Entropy: {header['entropy_estimate']:.2f}")
        
        # Find top speed candidates
        patcher = FirmwarePatcher(firmware)
        candidates = patcher.analyze_speed_candidates()
        
        # Show most likely speed indicators
        likely_speeds = [c for c in candidates if 5 <= c['occurrences'] <= 15]
        if likely_speeds:
            print("Likely speed indicators:")
            for candidate in likely_speeds[:3]:
                print(f"  {candidate['speed']} KPH: {candidate['occurrences']} times")

def main():
    # First run the manual patching example
    success = create_test_patch()
    
    if success:
        print("\n" + "=" * 50)
        print("SUCCESS: Manual patch example completed!")
        print("\nThis demonstrates how the tool can:")
        print("- Analyze firmware structure")
        print("- Find speed-related patterns")
        print("- Apply targeted modifications")
        print("- Verify changes")
        print("\nFor production use:")
        print("- Always backup original firmware")
        print("- Test patches thoroughly")
        print("- Understand risks and legal implications")
    
    # Then demonstrate the analysis workflow
    demonstrate_analysis_workflow()

if __name__ == "__main__":
    main()