import uvicorn
import sys
import os

if __name__ == "__main__":
    print("===============================================================")
    print("   [+] VitalMind AI - Antigravity Health Platform (Zero-G)     ")
    print("===============================================================")
    print(" Server launching on http://127.0.0.1:8000")
    print(" Access Web Interface: http://127.0.0.1:8000")
    print(" Access API Specs:     http://127.0.0.1:8000/docs")
    print("===============================================================\n")

    sys.path.insert(0, os.path.dirname(__file__))
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

