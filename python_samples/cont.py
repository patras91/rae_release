if __name__=="__main__":
    for i in range(0, 5):
        if i == 3:
            continue
        print(i)

    for i in range(0, 5):
        if i == 2:
            pass
        else:
            if i == -1:
                pass
            else:
                c = 1
                
                try:
                    a = 1
                    print("continuing")
                    continue
                except Search_Done:
                    pass
                except Failed_task:
                    continue

                print("here")