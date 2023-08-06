import socket
import threading
import time

import serial

import Locker_Project.Locker
from Locker_Project import CMD_ScanInput, CMD_Thread, CMD_Process, Func,Locker

host='192.168.100.3'
Port=3003
threamain=[]
lstID=[]
lstLocker={}
lst=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
lstouputtemp = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
lstinputtemp = [7, 6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 15, 14, 13, 12]
lstInput1=[]
lstInput2=[]
lstOutput1=[]
lstOutput2=[]

exit_event=threading.Event()


#uart = serial.Serial("/dev/ttyS0", baudrate=528000, timeout=1)#489600  528000
#finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

Danhsachtu=[] # chứa và quản lý danh sách tủ


def KhaiBaoInput(mcpInput1,mcpInput2):
    for i in lstinputtemp:
        pin = mcpInput1.get_pin(i)
        pin.direction = digitalio.Direction.INPUT
        pin.pull = digitalio.Pull.UP
        lstInput1.append(pin)
        pin1 = mcpInput2.get_pin(i)
        pin1.direction = digitalio.Direction.INPUT
        pin1.pull = digitalio.Pull.UP
        lstInput2.append(pin1)
        pass
    pass
def KhaiBaoOutput(mcpOutput1,mcpOutput2):
    for i in lstouputtemp:
        pin1 = mcpOutput1.get_pin(i)
        pin1.switch_to_output(value=False)
        lstOutput1.append(pin1)
        pin2 = mcpOutput2.get_pin(i)
        pin2.switch_to_output(value=False)
        lstOutput2.append(pin2)
        pass
    pass
def Get_Finger_Image(signak=True):
    """Scan fingerprint then save image to filename."""
    times=time.time()
    check=False
    try:
        while ((time.time()-times<=5) and signak==True):
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                check=True
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="", flush=True)
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False
        if check==False:
            return False

        # let PIL take care of the image headers and file structure
        from PIL import Image  # pylint: disable=import-outside-toplevel
        img= Image.new("L", (256, 288), "white")#256, 288
        pixeldata = img.load()
        mask = 0b00001111
        result = finger.get_fpdata(sensorbuffer="image")
        x = 0
        y = 0
        for i in range(len(result)):
            pixeldata[x, y] = (int(result[i]) >> 4) * 17
            x += 1
            pixeldata[x, y] = (int(result[i]) & mask) * 17
            if x == 255:
                x = 0
                y += 1
            else:
                x += 1
        buffer = BytesIO()
        img.save(buffer,format="PNG") #Enregistre l'image dans le buffer
        myimage = buffer.getvalue()
        return base64.b64encode(myimage).decode('utf-8')
    except Exception as e:
        print('Loi Doc Van Tay',str(e))
        sensor_reset()
        return False
def Run():
    try:
        chuoi = '<id>1212</id><type>getdata</type><data>statusdoor</data>'
        chuoi = chuoi.encode('utf-8')
        size = len(chuoi)
        while 1:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scok112:
                    scok112.connect((host, Port))
                    scok112.sendall(size.to_bytes(4, byteorder='big'))
                    scok112.sendall(chuoi)
                    msg = scok112.recv(1024)
                    dta = msg.decode('utf-8')
                    id = dta.split(';')[0]
                    ref = dta.split(';')[1].split('\n')[0].split('/')
                    print(ref)
                    if id == '1212':
                        lstLocker = Func.Convert1(ref)
                        print(lstLocker)
                    scok112.close()

                    for i in lstLocker.items():
                        tu=Locker.Locker(Id=i[0],Status=i[1],Sign='')
                        Danhsachtu.append(tu)
                    print(Danhsachtu)
                    break
            except Exception as e:
                scok112.close()
                print('Loi Roi')
        time.sleep(2)

        condition=threading.Condition()
        lstLock=threading.Lock()

        producer=CMD_Thread.Producer(Cmd=lstID,condition=condition,host=host,Port=Port,exitEvent=exit_event)
        threamain.append(producer)

        fingerT=CMD_Process.CMD_Process(Cmd=lstID,condition=condition,lst_input=lstLocker,lstLock=lstLock,exitEvent=exit_event)
        threamain.append(fingerT)
        scan = CMD_ScanInput.ScanInput(lstinput=lstLocker, lstlock=lstLock,lstID=lst,exitEvent=exit_event)
        threamain.append(scan)
        for t in threamain:
            t.start()

        #print('Xuong roi ne')
        #exit_event.set()

    except Exception as e:
        print('Connect Mysql Error:',str(e))