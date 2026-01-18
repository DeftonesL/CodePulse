"""
Quick Test Script
Run this to verify CodePulse installation
"""

import sys
from pathlib import Path

def check_installation():
    """Verify all dependencies are installed"""
    
    print("🔍 Checking CodePulse installation...\n")
    
    required = {
        'click': 'CLI framework',
        'rich': 'Terminal UI',
        'networkx': 'Graph analysis'
    }
    
    all_good = True
    
    for package, description in required.items():
        try:
            __import__(package)
            print(f"✅ {package:15} - {description}")
        except ImportError:
            print(f"❌ {package:15} - {description} (MISSING)")
            all_good = False
    
    # Check optional
    print("\n🎨 Optional packages:")
    
    optional = {
        'anthropic': 'AI features',
        'pytest': 'Testing'
    }
    
    for package, description in optional.items():
        try:
            __import__(package)
            print(f"✅ {package:15} - {description}")
        except ImportError:
            print(f"⚪ {package:15} - {description} (not installed)")
    
    print("\n" + "="*50)
    
    if all_good:
        print("✅ Installation successful!")
        print("\nRun CodePulse:")
        print("  python codepulse.py")
    else:
        print("❌ Some dependencies missing!")
        print("\nRun setup:")
        print("  Windows: setup.bat")
        print("  Linux/Mac: ./setup.sh")
    
    print("="*50 + "\n")

if __name__ == "__main__":
    check_installation()
