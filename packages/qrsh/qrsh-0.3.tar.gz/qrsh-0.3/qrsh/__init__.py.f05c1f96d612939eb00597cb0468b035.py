from pyzbar.pyzbar import decode
import sys
import webbrowser


def _decode(frame):
    barcodes = decode(frame)
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        if barcode_data is not None:
            print(barcode_data)
            confirm = input('Open link? (yes to confirm): ')
            if confirm == 'y' or confirm == 'yes':
                if barcode_data.startswith('http://') \
                        or barcode_data.startswith('https://'):
                    webbrowser.open(barcode_data)
                else:
                    webbrowser.open('http://' + barcode_data)
            sys.exit()
