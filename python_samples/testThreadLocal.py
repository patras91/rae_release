__author__ = 'patras'
import threading

def a(var):
    var[0] = 3

def main():
    v = threading.local()
    v.var = [1, 2]
    t = threading.Thread(target=a, args=[v.var])
    t.start()
    t.join()
    print(v.var)

if __name__ == "__main__":
    main()