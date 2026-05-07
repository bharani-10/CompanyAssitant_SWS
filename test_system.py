"""
System test script - Verify everything is working correctly
"""
import sys
import os
from pathlib import Path

print("\n" + "="*50)
print("🧪 SWS AI Chatbot - System Test")
print("="*50 + "\n")

test_results = []

# Test 1: Python version
print("Test 1: Checking Python version...")
python_version = sys.version_info
if python_version.major >= 3 and python_version.minor >= 8:
    print(f"✅ Python {python_version.major}.{python_version.minor} OK")
    test_results.append(True)
else:
    print(f"❌ Python 3.8+ required (found {python_version.major}.{python_version.minor})")
    test_results.append(False)

# Test 2: Check PDF files
print("\nTest 2: Checking PDF files...")
pdf_files = list(Path(".").glob("*.pdf"))
if len(pdf_files) == 10:
    print(f"✅ All 10 PDF files found")
    test_results.append(True)
else:
    print(f"❌ Expected 10 PDFs, found {len(pdf_files)}")
    for pdf in pdf_files:
        print(f"   - {pdf.name}")
    test_results.append(False)

# Test 3: Check required files
print("\nTest 3: Checking project files...")
required_files = [
    "main.py",
    "app.py",
    "document_ingestion.py",
    "rag_system.py",
    "requirements.txt",
    ".env.example"
]
all_present = all(os.path.exists(f) for f in required_files)
if all_present:
    print("✅ All required project files present")
    test_results.append(True)
else:
    print("❌ Missing files:")
    for f in required_files:
        status = "✓" if os.path.exists(f) else "✗"
        print(f"   {status} {f}")
    test_results.append(False)

# Test 4: Check .env file
print("\nTest 4: Checking environment setup...")
if os.path.exists(".env"):
    with open(".env", "r") as f:
        content = f.read()
        if "OPENAI_API_KEY" in content and "sk-" in content:
            print("✅ .env file configured with API key")
            test_results.append(True)
        else:
            print("❌ .env file missing OPENAI_API_KEY")
            test_results.append(False)
else:
    print("❌ .env file not found")
    print("   Creating from template...")
    os.system("cp .env.example .env" if os.name != "nt" else "copy .env.example .env")
    test_results.append(False)

# Test 5: Try importing required packages
print("\nTest 5: Checking dependencies...")
dependencies = [
    ("langchain", "LangChain"),
    ("chromadb", "ChromaDB"),
    ("fastapi", "FastAPI"),
    ("streamlit", "Streamlit"),
    ("pydantic", "Pydantic"),
]

all_deps_ok = True
for module, name in dependencies:
    try:
        __import__(module)
        print(f"   ✅ {name}")
    except ImportError:
        print(f"   ❌ {name} not installed")
        all_deps_ok = False

test_results.append(all_deps_ok)

# Test 6: Check vector store
print("\nTest 6: Checking vector store...")
if os.path.exists("chroma_db"):
    print("✅ Vector store exists (chroma_db/)")
    test_results.append(True)
else:
    print("⚠️  Vector store not found")
    print("   Run: python -c \"from document_ingestion import initialize_pipeline; initialize_pipeline('.', rebuild=True)\"")
    test_results.append(False)

# Summary
print("\n" + "="*50)
passed = sum(test_results)
total = len(test_results)
print(f"Results: {passed}/{total} tests passed")

if passed == total:
    print("\n✅ All systems ready!")
    print("\nNext steps:")
    print("1. python main.py          (Backend)")
    print("2. streamlit run app.py    (Frontend)")
    print("3. Open http://localhost:8501")
else:
    print("\n⚠️  Some tests failed. Please check above.")
    if not all_deps_ok:
        print("\nInstall dependencies:")
        print("pip install -r requirements.txt")

print("="*50 + "\n")
