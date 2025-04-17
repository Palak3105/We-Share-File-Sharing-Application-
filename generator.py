import pyqrcode

def generateQRCode(IP):
    try:
        qr = pyqrcode.create("http://{addr}:9000".format(addr=IP))
        qr.png("./qr.png", scale=5)
        return qr
    except:
        print("Failed to generate QR Code")