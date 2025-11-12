#!/usr/bin/env python3
"""
Simple test script to verify backend setup
Run this after setting up the backend to check if everything works
"""

import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("🔍 Testing Python imports...")
    
    try:
        import grpc
        print("  ✅ grpc")
    except ImportError:
        print("  ❌ grpc - Run: pip install grpcio")
        return False
    
    try:
        import flask
        print("  ✅ flask")
    except ImportError:
        print("  ❌ flask - Run: pip install flask")
        return False
    
    try:
        import flask_cors
        print("  ✅ flask-cors")
    except ImportError:
        print("  ❌ flask-cors - Run: pip install flask-cors")
        return False
    
    return True

def test_proto_files():
    """Test if proto files are generated"""
    print("\n🔍 Testing proto files...")
    
    proto_dir = os.path.join(os.path.dirname(__file__), 'proto')
    
    files_to_check = [
        'jokes_pb2.py',
        'jokes_pb2_grpc.py'
    ]
    
    all_exist = True
    for file in files_to_check:
        path = os.path.join(proto_dir, file)
        if os.path.exists(path):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - Run generate_proto.sh or use the command in README")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 60)
    print("Backend Test Suite")
    print("=" * 60)
    
    results = {
        "Imports": test_imports(),
        "Proto Files": test_proto_files()
    }
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed! Your backend is ready to run.")
        print("\nStart the server with:")
        print("  python server.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
