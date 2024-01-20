import ctypes

cpp = ctypes.cdll.LoadLibrary('./selflib/minic.dll')

if __name__ == '__main__':
    print(cpp.add(1, 2))
    print(cpp.sub(5, 4))
