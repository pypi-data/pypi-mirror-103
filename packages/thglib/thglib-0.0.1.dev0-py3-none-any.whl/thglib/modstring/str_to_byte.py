class STR_TO_BYTE:
    def __init__(self,code):
        self.code = code

    def mostra(self):

        # string with encoding 'utf-8'
        arr = bytes(self.code, 'utf-8')
        arr2 = bytes(self.code, 'ascii')

        print(arr, '\n')

        # actual bytes in the the string
        for byte in arr:
            print(byte, end=' ')
        print("\n")
        for byte in arr2:
            print(byte, end=' ')