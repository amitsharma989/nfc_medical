import nfc

def test_nfc():
    try:
        clf = nfc.ContactlessFrontend('usb')
        print("NFC reader connected successfully.")
        tag = clf.connect(rdwr={'on-connect': lambda tag: tag})
        print("NFC tag detected:", tag)
    except Exception as e:
        print("Error:", e)
    finally:
        clf.close()

if __name__ == "__main__":
    test_nfc()
