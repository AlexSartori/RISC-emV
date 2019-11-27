
class DataMemory:
    def __init__(self, size):
        self.size = size  # In bytes
        self.__memory = {}

    # TODO: add checks on address
    def store(self, address, value):
        address = int(address)
        
        if address >= self.size:
            raise MemoryError("Segmentation Fault: address is out of memory bounds")
        # TODO: elif len(bytes(value)) > 1:
        #     pass
        else:
            self.__memory[address] = value


    def load(self, address):
        address = int(address)

        if address >= self.size:
            raise MemoryError("Segmentation Fault: address is out of memory bounds")
        else:
            address = int(address)
            if address in self.__memory:
                return self.__memory[address]
            else:
                return 0x00


    def __iter__(self):
        for addr in range(self.size):
            yield self.load(addr)
