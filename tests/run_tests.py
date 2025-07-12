#!/usr/bin/env python3
"""
Test runner for all Dustbin tests
Runs all test files and generates a comprehensive report
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def run_test_file(test_file):
    """Run a specific test file and capture results"""
    print(f"\n🧪 Running {test_file}")
    print("=" * 50)
    
    try:
        # Run the test file
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=60)
        
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        success = result.returncode == 0
        return {
            'file': test_file,
            'success': success,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'return_code': result.returncode
        }
        
    except subprocess.TimeoutExpired:
        print(f"❌ Test {test_file} timed out after 60 seconds")
        return {
            'file': test_file,
            'success': False,
            'stdout': '',
            'stderr': 'Test timed out',
            'return_code': -1
        }
    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        return {
            'file': test_file,
            'success': False,
            'stdout': '',
            'stderr': str(e),
            'return_code': -1
        }

def main():
    """Run all tests and generate report"""
    print("🚀 Dustbin Test Suite Runner")
    print("=" * 60)
    print(f"Started at: {datetime.now().isoformat()}")
    
    # Get all test files
    test_files = []
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    
    for file in os.listdir(tests_dir):
        if file.startswith('test_') and file.endswith('.py'):
            test_files.append(os.path.join(tests_dir, file))
    
    if not test_files:
        print("❌ No test files found!")
        return
    
    print(f"📋 Found {len(test_files)} test files:")
    for test_file in test_files:
        print(f"   - {os.path.basename(test_file)}")
    
    # Run all tests
    results = []
    for test_file in test_files:
        result = run_test_file(test_file)
        results.append(result)
        time.sleep(1)  # Brief pause between tests
    
    # Generate summary report
    print("\n" + "=" * 60)
    print("📊 Test Suite Summary Report")
    print("=" * 60)
    
    passed = sum(1 for r in results if r['success'])
    total = len(results)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    print(f"\n🎯 Overall Results:")
    print(f"   Total Test Files: {total}")
    print(f"   Passed: {passed}")
    print(f"   Failed: {total - passed}")
    print(f"   Success Rate: {success_rate:.1f}%")
    
    print(f"\n📋 Individual Test Results:")
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        filename = os.path.basename(result['file'])
        print(f"   {filename}: {status}")
        
        if not result['success']:
            print(f"      Return Code: {result['return_code']}")
            if result['stderr']:
                print(f"      Error: {result['stderr'][:100]}...")
    
    # Performance rating
    if success_rate == 100:
        print("\n🏆 PERFECT! All tests passed!")
    elif success_rate >= 80:
        print("\n🎉 EXCELLENT! Most tests passed!")
    elif success_rate >= 60:
        print("\n👍 GOOD! Majority of tests passed!")
    else:
        print("\n⚠️  NEEDS ATTENTION! Many tests failed!")
    
    print(f"\n⏰ Completed at: {datetime.now().isoformat()}")
    print("✅ Test suite execution completed!")

if __name__ == "__main__":
    main()
