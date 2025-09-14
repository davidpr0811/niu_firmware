#!/usr/bin/env python3
"""
NIU Firmware Decompiler/Patcher Tool

This tool can analyze, decompile, modify parameters (like speed limits),
and recompile NIU scooter firmware files.

Author: Firmware Analysis Tool
"""

import os
import sys
import struct
import hashlib
import argparse
import binascii
from typing import Dict, List, Optional, Tuple, Any


class FirmwareAnalyzer:
    """Analyzes NIU firmware binary structure"""
    
    def __init__(self, firmware_path: str):
        self.firmware_path = firmware_path
        self.data = None
        self.size = 0
        self.header_info = {}
        self.load_firmware()
    
    def load_firmware(self):
        """Load firmware binary data"""
        try:
            with open(self.firmware_path, 'rb') as f:
                self.data = f.read()
            self.size = len(self.data)
            print(f"Loaded firmware: {self.firmware_path} ({self.size} bytes)")
        except Exception as e:
            raise Exception(f"Failed to load firmware: {e}")
    
    def analyze_header(self) -> Dict[str, Any]:
        """Analyze firmware header structure"""
        if not self.data or len(self.data) < 64:
            return {}
        
        # Try to identify header patterns
        header = self.data[:64]
        
        # Check for common patterns
        analysis = {
            'size': self.size,
            'md5': hashlib.md5(self.data).hexdigest(),
            'first_bytes': header[:16].hex(),
            'possible_magic': [],
            'entropy_estimate': self._calculate_entropy(header)
        }
        
        # Look for potential magic bytes or signatures
        for i in range(0, min(32, len(header) - 4)):
            chunk = header[i:i+4]
            if chunk == b'\x00\x00\x00\x00' or chunk == b'\xFF\xFF\xFF\xFF':
                continue
            analysis['possible_magic'].append((i, chunk.hex()))
        
        self.header_info = analysis
        return analysis
    
    def _calculate_entropy(self, data: bytes) -> float:
        """Calculate Shannon entropy of data"""
        if not data:
            return 0.0
        
        # Count byte frequencies
        freq = {}
        for byte in data:
            freq[byte] = freq.get(byte, 0) + 1
        
        # Calculate entropy
        import math
        entropy = 0.0
        length = len(data)
        for count in freq.values():
            p = count / length
            if p > 0:
                entropy -= p * math.log2(p)
        
        return entropy
    
    def find_speed_patterns(self) -> List[Tuple[int, str, bytes]]:
        """Find potential speed-related patterns in firmware"""
        patterns = []
        
        # Common speed values in different representations
        speed_values = [
            (20, "20 KPH"),
            (25, "25 KPH"), 
            (28, "28 KPH"),
            (32, "32 KPH"),
            (38, "38 KPH"),
            (40, "40 KPH")
        ]
        
        for speed, desc in speed_values:
            # Check different byte representations
            representations = [
                speed.to_bytes(1, 'little'),  # Single byte
                speed.to_bytes(2, 'little'),  # 2 bytes little endian
                speed.to_bytes(2, 'big'),     # 2 bytes big endian
                (speed * 10).to_bytes(2, 'little'),  # Speed * 10
                (speed * 100).to_bytes(2, 'little'), # Speed * 100
            ]
            
            for rep in representations:
                offset = 0
                while True:
                    pos = self.data.find(rep, offset)
                    if pos == -1:
                        break
                    patterns.append((pos, f"{desc} ({rep.hex()})", rep))
                    offset = pos + 1
        
        return patterns
    
    def extract_strings(self, min_length: int = 4) -> List[Tuple[int, str]]:
        """Extract printable strings from firmware"""
        strings = []
        current_string = ""
        start_pos = 0
        
        for i, byte in enumerate(self.data):
            if 32 <= byte <= 126:  # Printable ASCII
                if not current_string:
                    start_pos = i
                current_string += chr(byte)
            else:
                if len(current_string) >= min_length:
                    strings.append((start_pos, current_string))
                current_string = ""
        
        if len(current_string) >= min_length:
            strings.append((start_pos, current_string))
        
        return strings


class FirmwareComparator:
    """Compare different firmware versions to identify modifications"""
    
    def __init__(self, firmware1_path: str, firmware2_path: str):
        self.firmware1_path = firmware1_path  
        self.firmware2_path = firmware2_path
        self.firmware1 = FirmwareAnalyzer(firmware1_path)
        self.firmware2 = FirmwareAnalyzer(firmware2_path)
        
    def compare_files(self) -> Dict[str, Any]:
        """Compare two firmware files and find differences"""
        if len(self.firmware1.data) != len(self.firmware2.data):
            print(f"Warning: Different file sizes - {len(self.firmware1.data)} vs {len(self.firmware2.data)}")
            min_size = min(len(self.firmware1.data), len(self.firmware2.data))
        else:
            min_size = len(self.firmware1.data)
        
        differences = []
        for i in range(min_size):
            if self.firmware1.data[i] != self.firmware2.data[i]:
                differences.append({
                    'offset': i,
                    'offset_hex': f"0x{i:04x}",
                    'old_value': self.firmware1.data[i],
                    'new_value': self.firmware2.data[i],
                    'old_hex': f"{self.firmware1.data[i]:02x}",
                    'new_hex': f"{self.firmware2.data[i]:02x}"
                })
        
        return {
            'total_differences': len(differences),
            'differences': differences[:100],  # Limit output
            'analysis': self._analyze_differences(differences)
        }
    
    def _analyze_differences(self, differences: List[Dict]) -> Dict[str, Any]:
        """Analyze the differences to identify patterns"""
        if not differences:
            return {'type': 'identical'}
        
        # Group differences by proximity
        groups = []
        current_group = [differences[0]]
        
        for diff in differences[1:]:
            if diff['offset'] - current_group[-1]['offset'] <= 4:  # Within 4 bytes
                current_group.append(diff)
            else:
                groups.append(current_group)
                current_group = [diff]
        groups.append(current_group)
        
        # Analyze groups
        analysis = {
            'difference_groups': len(groups),
            'largest_group_size': max(len(g) for g in groups),
            'groups': []
        }
        
        for i, group in enumerate(groups[:10]):  # Analyze first 10 groups
            group_analysis = {
                'start_offset': f"0x{group[0]['offset']:04x}",
                'end_offset': f"0x{group[-1]['offset']:04x}",
                'size': len(group),
                'changes': []
            }
            
            for diff in group:
                group_analysis['changes'].append({
                    'offset': diff['offset_hex'],
                    'change': f"{diff['old_hex']} -> {diff['new_hex']}"
                })
            
            analysis['groups'].append(group_analysis)
        
        return analysis
    """Patches NIU firmware parameters"""
    
    def __init__(self, firmware_path: str):
        self.firmware_path = firmware_path
        self.analyzer = FirmwareAnalyzer(firmware_path)
        self.modifications = []
    
class FirmwarePatcher:
    """Patches NIU firmware parameters"""
    
    def __init__(self, firmware_path: str):
        self.firmware_path = firmware_path
        self.analyzer = FirmwareAnalyzer(firmware_path)
        self.modifications = []
    
    def analyze_speed_candidates(self) -> List[Dict[str, Any]]:
        """Analyze potential speed modification locations"""
        patterns = self.analyzer.find_speed_patterns()
        
        # Group patterns by speed value and representation
        speed_groups = {}
        for pos, desc, data in patterns:
            speed = desc.split()[0]
            rep = desc.split()[-1].strip('()')
            
            key = f"{speed}_{rep}"
            if key not in speed_groups:
                speed_groups[key] = []
            speed_groups[key].append(pos)
        
        candidates = []
        for key, positions in speed_groups.items():
            speed, rep = key.split('_')
            candidates.append({
                'speed': speed,
                'representation': rep,
                'byte_pattern': bytes.fromhex(rep),
                'occurrences': len(positions),
                'positions': positions[:10]  # Show first 10 positions
            })
        
        return sorted(candidates, key=lambda x: x['occurrences'])
    
    def suggest_patches(self, target_speed: int) -> List[Dict[str, Any]]:
        """Suggest potential patches to change speed limit"""
        candidates = self.analyze_speed_candidates()
        suggestions = []
        
        # Look for current speed candidates with reasonable occurrence counts
        for candidate in candidates:
            try:
                current_speed = int(candidate['speed'])
                if candidate['occurrences'] > 1 and candidate['occurrences'] < 50:
                    # Generate suggestion for this pattern
                    new_pattern = None
                    rep_len = len(candidate['byte_pattern'])
                    
                    if rep_len == 1:
                        if target_speed <= 255:
                            new_pattern = target_speed.to_bytes(1, 'little')
                    elif rep_len == 2:
                        if target_speed <= 65535:
                            # Try both endian formats
                            new_pattern_le = target_speed.to_bytes(2, 'little')
                            new_pattern_be = target_speed.to_bytes(2, 'big')
                            
                            # Use the same endianness as the original
                            if candidate['byte_pattern'] == current_speed.to_bytes(2, 'little'):
                                new_pattern = new_pattern_le
                            elif candidate['byte_pattern'] == current_speed.to_bytes(2, 'big'):
                                new_pattern = new_pattern_be
                            elif candidate['byte_pattern'] == (current_speed * 10).to_bytes(2, 'little'):
                                new_pattern = (target_speed * 10).to_bytes(2, 'little')
                            elif candidate['byte_pattern'] == (current_speed * 100).to_bytes(2, 'little'):
                                new_pattern = (target_speed * 100).to_bytes(2, 'little')
                    
                    if new_pattern:
                        suggestions.append({
                            'current_speed': current_speed,
                            'target_speed': target_speed,
                            'old_pattern': candidate['byte_pattern'],
                            'new_pattern': new_pattern,
                            'old_hex': candidate['byte_pattern'].hex(),
                            'new_hex': new_pattern.hex(),
                            'positions': candidate['positions'],
                            'occurrences': candidate['occurrences'],
                            'confidence': self._calculate_confidence(candidate)
                        })
            except ValueError:
                continue
        
        return sorted(suggestions, key=lambda x: x['confidence'], reverse=True)
    
    def _calculate_confidence(self, candidate: Dict[str, Any]) -> float:
        """Calculate confidence score for a patch candidate"""
        # Base confidence on occurrence count (not too few, not too many)
        count = candidate['occurrences']
        if count < 2:
            return 0.1
        elif count <= 5:
            return 0.9
        elif count <= 10:
            return 0.7
        elif count <= 20:
            return 0.5
        else:
            return 0.2
        """Patch speed limit in firmware"""
    def patch_speed_limit(self, old_speed: int, new_speed: int) -> bool:
        """Patch speed limit in firmware"""
        print(f"Attempting to patch speed from {old_speed} to {new_speed} KPH...")
        
        suggestions = self.suggest_patches(new_speed)
        matching_suggestions = [s for s in suggestions if s['current_speed'] == old_speed]
        
        if not matching_suggestions:
            print(f"No suitable patterns found for changing {old_speed} KPH to {new_speed} KPH")
            print("Available suggestions:")
            for suggestion in suggestions[:5]:
                print(f"  {suggestion['current_speed']} -> {suggestion['target_speed']} KPH "
                      f"(confidence: {suggestion['confidence']:.1f}, "
                      f"pattern: {suggestion['old_hex']} -> {suggestion['new_hex']})")
            return False
        
        best_suggestion = matching_suggestions[0]
        print(f"Found patch suggestion with confidence {best_suggestion['confidence']:.1f}")
        print(f"  Pattern: {best_suggestion['old_hex']} -> {best_suggestion['new_hex']}")
        print(f"  {best_suggestion['occurrences']} occurrences at positions: {best_suggestion['positions']}")
        
        # Store the patch for later application
        self.modifications.append({
            'type': 'speed_patch',
            'old_speed': old_speed,
            'new_speed': new_speed,
            'suggestion': best_suggestion
        })
        
        return True
    
    def create_patched_firmware(self, output_path: str, patches: List[Tuple[int, bytes]]) -> bool:
        """Create patched firmware file"""
        try:
            data = bytearray(self.analyzer.data)
            
            for offset, new_data in patches:
                if offset + len(new_data) > len(data):
                    raise Exception(f"Patch at offset {offset} exceeds firmware size")
                data[offset:offset+len(new_data)] = new_data
            
            with open(output_path, 'wb') as f:
                f.write(data)
            
            print(f"Patched firmware saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Failed to create patched firmware: {e}")
            return False


def main():
    """Main function for command-line interface"""
    parser = argparse.ArgumentParser(description="NIU Firmware Decompiler/Patcher Tool")
    parser.add_argument("firmware", help="Path to firmware file")
    parser.add_argument("--analyze", action="store_true", help="Analyze firmware structure")
    parser.add_argument("--find-speeds", action="store_true", help="Find speed patterns")
    parser.add_argument("--speed-candidates", action="store_true", help="Analyze speed modification candidates")
    parser.add_argument("--suggest-patch", type=int, metavar="TARGET_SPEED", help="Suggest patches for target speed")
    parser.add_argument("--compare", help="Compare with another firmware file")
    parser.add_argument("--extract-strings", action="store_true", help="Extract strings")
    parser.add_argument("--patch-speed", nargs=2, type=int, metavar=("OLD", "NEW"), 
                       help="Patch speed limit (OLD NEW)")
    parser.add_argument("--output", "-o", help="Output file for patched firmware")
    parser.add_argument("--apply-patches", action="store_true", help="Apply stored patches to create output file")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.firmware):
        print(f"Error: Firmware file not found: {args.firmware}")
        return 1
    
    try:
        if args.analyze:
            analyzer = FirmwareAnalyzer(args.firmware)
            header = analyzer.analyze_header()
            print("\nFirmware Analysis:")
            print(f"  Size: {header['size']} bytes")
            print(f"  MD5: {header['md5']}")
            print(f"  First 16 bytes: {header['first_bytes']}")
            print(f"  Entropy estimate: {header['entropy_estimate']:.2f}")
            if header['possible_magic']:
                print("  Possible magic bytes:")
                for pos, magic in header['possible_magic'][:5]:
                    print(f"    Position {pos}: {magic}")
        
        if args.compare:
            if not os.path.exists(args.compare):
                print(f"Error: Comparison file not found: {args.compare}")
                return 1
            
            comparator = FirmwareComparator(args.firmware, args.compare)
            result = comparator.compare_files()
            print(f"\nFirmware Comparison:")
            print(f"  Total differences: {result['total_differences']}")
            
            if result['total_differences'] > 0:
                print(f"  Difference groups: {result['analysis']['difference_groups']}")
                print(f"  Largest group size: {result['analysis']['largest_group_size']}")
                print("\nFirst few difference groups:")
                for i, group in enumerate(result['analysis']['groups'][:3]):
                    print(f"    Group {i+1}: {group['start_offset']}-{group['end_offset']} ({group['size']} bytes)")
                    for change in group['changes'][:5]:
                        print(f"      {change['offset']}: {change['change']}")
        
        if args.find_speeds:
            analyzer = FirmwareAnalyzer(args.firmware)
            patterns = analyzer.find_speed_patterns()
            print(f"\nFound {len(patterns)} potential speed patterns:")
            for pos, desc, data in patterns[:50]:  # Show first 50
                print(f"  0x{pos:04x}: {desc}")
            if len(patterns) > 50:
                print(f"  ... and {len(patterns) - 50} more")
        
        if args.speed_candidates:
            patcher = FirmwarePatcher(args.firmware)
            candidates = patcher.analyze_speed_candidates()
            print(f"\nSpeed Modification Candidates:")
            for candidate in candidates:
                print(f"  {candidate['speed']} KPH ({candidate['representation']}):")
                print(f"    Occurrences: {candidate['occurrences']}")
                print(f"    Sample positions: {[f'0x{p:04x}' for p in candidate['positions'][:5]]}")
        
        if args.suggest_patch:
            patcher = FirmwarePatcher(args.firmware)
            suggestions = patcher.suggest_patches(args.suggest_patch)
            print(f"\nPatch suggestions for {args.suggest_patch} KPH:")
            for i, suggestion in enumerate(suggestions[:5]):
                print(f"  {i+1}. {suggestion['current_speed']} -> {suggestion['target_speed']} KPH")
                print(f"     Confidence: {suggestion['confidence']:.1f}")
                print(f"     Pattern: {suggestion['old_hex']} -> {suggestion['new_hex']}")
                print(f"     Occurrences: {suggestion['occurrences']} at positions {[f'0x{p:04x}' for p in suggestion['positions'][:3]]}")
        
        if args.extract_strings:
            analyzer = FirmwareAnalyzer(args.firmware)
            strings = analyzer.extract_strings()
            print(f"\nFound {len(strings)} strings:")
            for pos, string in strings[:20]:  # Show first 20
                print(f"  0x{pos:04x}: {string}")
            if len(strings) > 20:
                print(f"  ... and {len(strings) - 20} more")
        
        if args.patch_speed:
            patcher = FirmwarePatcher(args.firmware)
            old_speed, new_speed = args.patch_speed
            success = patcher.patch_speed_limit(old_speed, new_speed)
            
            if success and args.apply_patches:
                if not args.output:
                    print("Error: --output required when applying patches")
                    return 1
                
                # Apply the stored modifications
                suggestion = patcher.modifications[0]['suggestion']
                patches = []
                for pos in suggestion['positions']:
                    patches.append((pos, suggestion['new_pattern']))
                
                patcher.create_patched_firmware(args.output, patches)
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())