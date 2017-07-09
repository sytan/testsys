

'''
dut flash start
the chip select is: 10
The device information :
Manufacturer ID: C2
Device Type: 20
Device ID: 17
Manufacturer: MXIC
Device type: SPI Serial Flash
Device name: MX25L6406E
Device size(Mbits): 64
Page: 0x7FFF
dut flash stopped
'''



if __name__ == "__main__":
    script = {"age":18.125,"name":"Lily"}
    string = """age = script.get("age")*10\nprint age+1\nif age >= 180:\n\tisTrue = True\nelse:\n\tisTrue = False"""
    exec(string)
    print isTrue

    s = "ABCDEFG"
    print s.lower()
