import socket
import thread
import binascii
import ctypes
import sys
import time
import requests
import json
from parse_rest.connection import register
from parse_rest.datatypes import Object, GeoPoint
import datetime
from threading import current_thread

APPLICATION_ID = "VcaP3ITCoGA7x67VyawTjgIyubOGs5oW3o89JyL2"
REST_API_KEY = "B09xqq3MTk6nZooEEfTruT6iHrYY1h1Z0X0vI7aE"
MASTER_KEY = "WmDY5EpsQNkMdwouEoOkchzBx9UQVKlOkiX328Sh"

register(APPLICATION_ID, REST_API_KEY)


class equipo(Object):
    pass


class georeferencia(Object):
    pass


class alarma(Object):
    pass


class heartbeat(Object):
    pass


class operaciones(Object):
    pass


def GetCrc16(datos, offset, length):
    crctab16 = (
        0x0000, 0x1189, 0x2312, 0x329B, 0x4624, 0x57AD, 0x6536, 0x74BF,
        0x8C48, 0x9DC1, 0xAF5A, 0xBED3, 0xCA6C, 0xDBE5, 0xE97E, 0xF8F7,
        0x1081, 0x0108, 0x3393, 0x221A, 0x56A5, 0x472C, 0x75B7, 0x643E,
        0x9CC9, 0x8D40, 0xBFDB, 0xAE52, 0xDAED, 0xCB64, 0xF9FF, 0xE876,
        0x2102, 0x308B, 0x0210, 0x1399, 0x6726, 0x76AF, 0x4434, 0x55BD,
        0xAD4A, 0xBCC3, 0x8E58, 0x9FD1, 0xEB6E, 0xFAE7, 0xC87C, 0xD9F5,
        0x3183, 0x200A, 0x1291, 0x0318, 0x77A7, 0x662E, 0x54B5, 0x453C,
        0xBDCB, 0xAC42, 0x9ED9, 0x8F50, 0xFBEF, 0xEA66, 0xD8FD, 0xC974,
        0x4204, 0x538D, 0x6116, 0x709F, 0x0420, 0x15A9, 0x2732, 0x36BB,
        0xCE4C, 0xDFC5, 0xED5E, 0xFCD7, 0x8868, 0x99E1, 0xAB7A, 0xBAF3,
        0x5285, 0x430C, 0x7197, 0x601E, 0x14A1, 0x0528, 0x37B3, 0x263A,
        0xDECD, 0xCF44, 0xFDDF, 0xEC56, 0x98E9, 0x8960, 0xBBFB, 0xAA72,
        0x6306, 0x728F, 0x4014, 0x519D, 0x2522, 0x34AB, 0x0630, 0x17B9,
        0xEF4E, 0xFEC7, 0xCC5C, 0xDDD5, 0xA96A, 0xB8E3, 0x8A78, 0x9BF1,
        0x7387, 0x620E, 0x5095, 0x411C, 0x35A3, 0x242A, 0x16B1, 0x0738,
        0xFFCF, 0xEE46, 0xDCDD, 0xCD54, 0xB9EB, 0xA862, 0x9AF9, 0x8B70,
        0x8408, 0x9581, 0xA71A, 0xB693, 0xC22C, 0xD3A5, 0xE13E, 0xF0B7,
        0x0840, 0x19C9, 0x2B52, 0x3ADB, 0x4E64, 0x5FED, 0x6D76, 0x7CFF,
        0x9489, 0x8500, 0xB79B, 0xA612, 0xD2AD, 0xC324, 0xF1BF, 0xE036,
        0x18C1, 0x0948, 0x3BD3, 0x2A5A, 0x5EE5, 0x4F6C, 0x7DF7, 0x6C7E,
        0xA50A, 0xB483, 0x8618, 0x9791, 0xE32E, 0xF2A7, 0xC03C, 0xD1B5,
        0x2942, 0x38CB, 0x0A50, 0x1BD9, 0x6F66, 0x7EEF, 0x4C74, 0x5DFD,
        0xB58B, 0xA402, 0x9699, 0x8710, 0xF3AF, 0xE226, 0xD0BD, 0xC134,
        0x39C3, 0x284A, 0x1AD1, 0x0B58, 0x7FE7, 0x6E6E, 0x5CF5, 0x4D7C,
        0xC60C, 0xD785, 0xE51E, 0xF497, 0x8028, 0x91A1, 0xA33A, 0xB2B3,
        0x4A44, 0x5BCD, 0x6956, 0x78DF, 0x0C60, 0x1DE9, 0x2F72, 0x3EFB,
        0xD68D, 0xC704, 0xF59F, 0xE416, 0x90A9, 0x8120, 0xB3BB, 0xA232,
        0x5AC5, 0x4B4C, 0x79D7, 0x685E, 0x1CE1, 0x0D68, 0x3FF3, 0x2E7A,
        0xE70E, 0xF687, 0xC41C, 0xD595, 0xA12A, 0xB0A3, 0x8238, 0x93B1,
        0x6B46, 0x7ACF, 0x4854, 0x59DD, 0x2D62, 0x3CEB, 0x0E70, 0x1FF9,
        0xF78F, 0xE606, 0xD49D, 0xC514, 0xB1AB, 0xA022, 0x92B9, 0x8330,
        0x7BC7, 0x6A4E, 0x58D5, 0x495C, 0x3DE3, 0x2C6A, 0x1EF1, 0x0F78,
    )
    fcs = 0xFFFF
    i = offset
    while i < length + offset:
        fcs = ((fcs >> 8) ^ crctab16[(fcs ^ datos[i]) & 0xFF])
        i += 1
    return '%004x' % ctypes.c_ushort(~fcs).value


def handler(clientsocket, clientaddr):
    imei = ""
    loginpacket = ""
    equipos = None
    ip, proceso = clientaddr
    clientsocket.settimeout(190)

    print "Accepted connection from: ", clientaddr

    while 1:
        try:
            data = clientsocket.recv(1024)
        except socket.timeout:
            print clientaddr, " - timeout error"
            break
        except socket.error:
            print clientaddr, "socket error occured: "
            break

        if data:
            receivedString = binascii.hexlify(data)
            receivedString = str(receivedString)

            hexStrings = receivedString.split('0d0a')

            for hexstring in hexStrings:
                hexstring = hexstring + "0d0a"

                if hexstring.strip() != '':
                    packetlength = hexstring[6:8]
                    if packetlength == "01":
                        # Identificando, parseando y respondiendo paquete de login.
                        loginpacket = hexstring
                        imei = hexstring[9:24]
                        print "Login packet: " + hexstring + " From IMEI:" + imei + " IP: " + ip
                        strpackage = ' '.join(hexstring[i: i + 2] for i in range(0, len(hexstring), 2))
                        strpackage = strpackage.split()
                        strpackage = [int(p, 16) for p in strpackage]
                        strpackage = (0x05, strpackage[3], strpackage[12], strpackage[13])
                        crc16 = GetCrc16(strpackage, 0, 4)
                        strpackage = '78780501' + '%002x' % strpackage[2] + '%002x' % strpackage[3] + crc16 + '0d0a'
                        packagetosend = binascii.unhexlify(strpackage)
                        clientsocket.send(packagetosend)
                        print "Login response sent : " + strpackage + " To IMEI:" + imei + " IP: " + ip
                        equipos = equipo.Query.get(IMEI=imei)
                        equipos.online = True
                        equipos.save()
                    elif packetlength == "12":
                        #
                        print "GPS Location data : " + hexstring + " From IMEI:" + imei + " IP: " + ip
                        if len(hexstring) > 16:
                            latitud = int(hexstring[22:30], 16) / 1800000.0
                            longitud = int(hexstring[30:38], 16) / 1800000.0
                            year = int(hexstring[8:10], 16)
                            month = int(hexstring[10:12], 16)
                            day = int(hexstring[12:14], 16)
                            hour = int(hexstring[14:16], 16)
                            minute = int(hexstring[16:18], 16)
                            second = int(hexstring[18:20], 16)
                            speed = int(hexstring[38:40], 16)
                            course = bin(int(hexstring[40:44], 16))[2:]
                            course = course.zfill(16)
                            longitud = longitud * -1 if course[4:5] == "1" else longitud
                            latitud = latitud * -1 if course[5:6] == "0" else latitud
                            direction = int(course[6:16], 2)
                            fecha = "20" + str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2) + " " + str(
                                hour).zfill(
                                2) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)

                            fechahora = datetime.datetime((2000 + year), month, day, hour, minute, second)

                            geopoint = georeferencia(id_equipo=equipos, latitud=latitud, longitud=longitud,
                                                     geopoint=GeoPoint(latitude=latitud, longitude=longitud),
                                                     fecha=fechahora,
                                                     curso=direction, velocidad=speed)
                            geopoint.save()

                            print "IMEI : " + imei + ", Latitud: " + str(latitud) + ", Longitud: " + str(
                                longitud) + " Datetime :" + fecha + ", Speed : " + str(speed) + " Km/h" + " IP: " + ip
                        else:
                            print "IMEI : " + imei + ", No location data for"
                    elif packetlength == "13":
                        print "GPS Heartbeat Packet : " + hexstring + " From IMEI: " + imei + " IP: " + ip
                        strpackage = ' '.join(hexstring[i: i + 2] for i in range(0, len(hexstring), 2))
                        strpackage = strpackage.split()
                        strpackage = [int(p, 16) for p in strpackage]
                        strpackage = (0x05, strpackage[3], strpackage[9], strpackage[10])
                        terminalinformation = str(bin(int(hexstring[8:10], 16))[2:])
                        language = hexstring[14:18]
                        crc16 = GetCrc16(strpackage, 0, 4)
                        strpackage = '78780513' + '%002x' % strpackage[2] + '%002x' % strpackage[3] + crc16 + '0d0a'
                        packagetosend = binascii.unhexlify(strpackage)
                        clientsocket.send(packagetosend)
                        heart = heartbeat(id_equipo=equipos, terminalinformation=terminalinformation.zfill(8),
                                          language=language)
                        heart.save()
                        print "Heartbeat response sent : " + strpackage + " to IMEI: " + imei + " IP: " + ip
                    elif packetlength == "16":
                        print "Alarm data packet : " + hexstring + " From IMEI:" + imei + " IP: " + ip
                        if len(hexstring) > 16:
                            strpackage = ' '.join(hexstring[i: i + 2] for i in range(0, len(hexstring), 2))
                            strpackage = strpackage.split()
                            strpackage = [int(p, 16) for p in strpackage]
                            strpackage = (0x05, strpackage[3], strpackage[36], strpackage[37])
                            crc16 = GetCrc16(strpackage, 0, 4)
                            strpackage = '78780516' + '%002x' % strpackage[2] + '%002x' % strpackage[3] + crc16 + '0d0a'
                            packagetosend = binascii.unhexlify(strpackage)
                            clientsocket.send(packagetosend)

                            latitud = int(hexstring[22:30], 16) / 1800000.0
                            longitud = int(hexstring[30:38], 16) / 1800000.0
                            year = int(hexstring[8:10], 16)
                            month = int(hexstring[10:12], 16)
                            day = int(hexstring[12:14], 16)
                            hour = int(hexstring[14:16], 16)
                            minute = int(hexstring[16:18], 16)
                            second = int(hexstring[18:20], 16)
                            speed = int(hexstring[38:40], 16)
                            course = bin(int(hexstring[40:44], 16))[2:]
                            course = course.zfill(16)
                            longitud = longitud * -1 if course[4:5] == "1" else longitud
                            latitud = latitud * -1 if course[5:6] == "0" else latitud
                            direction = int(course[6:16], 2)
                            fecha = "20" + str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2) + " " + str(
                                hour).zfill(
                                2) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)
                            terminalinformation = bin(int(hexstring[62:64], 16))[2:]
                            terminalinformation = terminalinformation.zfill(8)
                            oilelectricity = terminalinformation[0:1]
                            gpstracking = terminalinformation[1:2]
                            alarmtype = terminalinformation[2:5]
                            chargeonof = terminalinformation[5:6]
                            acclowhigh = terminalinformation[6:7]
                            defense = terminalinformation[7:8]
                            alarm = hexstring[68:70]
                            language = hexstring[70:72]

                            fechahora = datetime.datetime((2000 + year), month, day, hour, minute, second)

                            print "IMEI : " + imei + ", Latitud: " + str(latitud) + ", Longitud: " + str(
                                longitud) + " Datetime :" + fecha + ", Speed : " + str(
                                speed) + " Km/h" + "Oil/Electricity: "
                            "" + oilelectricity + ", GPS Tracking: " + gpstracking + ", Alarm Type: " + alarmtype + ""
                            ", Charge: " + chargeonof + ", ACC: " + acclowhigh + ", Defense: " + defense + ", Alarm:" + alarm + ""
                            ", Language: " + language + " IP: " + ip

                            print "Alarm response sent : " + strpackage + " Trom IMEI:" + imei
                            alarmas = alarma(id_equipo=equipos, latitud=latitud, longitud=longitud,
                                             geopoint=GeoPoint(latitude=latitud, longitude=longitud), fecha=fechahora,
                                             curso=direction, velocidad=speed, oilelectricity=oilelectricity,
                                             gpstracking=gpstracking, alarmtype=alarmtype, alarm=alarm, defense=defense,
                                             acclowhigh=acclowhigh, chargeonof=chargeonof)

                            alarmas.save()
                        else:
                            print "IMEI : " + imei + ", No Alarm data for"
                    elif packetlength == "15":
                        print "Recibiendo solicitud imei: " + imei
        time.sleep(0.1)

    clientsocket.close()
    print clientaddr, "- closed connection"
    thread.exit()


def envios(inicio, seguido):
    imei = "123456789012345"
    url = "http://grupotactuk.com/gpsapi/index.php/api/operaciones/"
    while 1:
        if imei != "":
            try :
                r = requests.get(url + "getalloperaciones.json")
                #r = requests.get(url + "operacion/imei/" + imei + ".json")
                rarray = json.loads(r.text)

                if rarray[0]['enviado'] == "0":
                    print rarray[0]['imei']
                    #loginpacket = "78780D01012345678901234500018CDD0D0A"
                    #informationserialnumber = loginpacket[24:28]
                    paqueteenviar = "787815800F0001A9584459442C3030303030302300A0DCF10D0A"

                    strpackage = ' '.join(paqueteenviar[i: i + 2] for i in range(0, len(paqueteenviar), 2))
                    strpackage = strpackage.split()
                    strpackage = [int(p, 16) for p in strpackage]
                    strpackage = (0X15, strpackage[3], strpackage[4], strpackage[5], strpackage[6], strpackage[7],
                                  strpackage[8], strpackage[9], strpackage[10], strpackage[11], strpackage[12],
                                  strpackage[13], strpackage[14], strpackage[15], strpackage[16], strpackage[17],
                                  strpackage[18], strpackage[19], strpackage[20], strpackage[21])
                    crc16 = GetCrc16(strpackage, 0, 20)
                    print crc16
                    payload = {'imei': imei, 'enviado': 1, 'resultado': 'N/A'}
                    #req = requests.post(url + "actualizarOperacion.json", data=payload)
                   # print req.text
            except:
                print "error"
        time.sleep(3)


if __name__ == "__main__":
    global mandatos

    # mandatos = []
    host = '0.0.0.0'
    port = 8000
    buf = 1024

    addr = (host, port)
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(addr)
    serversocket.listen(max(1024, socket.SOMAXCONN))


    envios = thread.start_new(envios, ("ok", "seguido"))

    while 1:
        print "El servidor esta escuchando las conexiones\n"
        time.sleep(3)
''' try:
        while 1:
            clientsocket, clientaddr = serversocket.accept()
            thread.start_new_thread(handler, (clientsocket, clientaddr))
        serversocket.close()
    except (KeyboardInterrupt, SystemExit):
        serversocket.close()
        sys.exit()'''


