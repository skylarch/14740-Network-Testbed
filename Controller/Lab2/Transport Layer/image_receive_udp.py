import socket
import numpy as np
import cv2 as cv


addr = ("127.0.0.1", 65535)
buf = 4100
code = b'start'

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    start = False
    chunks = []
    while True:
        chunk, _ = s.recvfrom(buf)
        if chunk.startswith(code):
            start = True
        elif start:
            chunks.insert(int(chunk[:4]), chunk[4:])
            if len(chunk) < buf:
                break

    byte_frame = b''.join(chunks)
    try:
        byte_arr = np.frombuffer(byte_frame, np.uint8)
        image = cv.imdecode(byte_arr, cv.IMREAD_COLOR)
        image = cv.resize(image, (960, 540))
        cv.imshow('Image over UDP', image)
    except:
        print("Error")

    s.close()
    
    while True:
        if cv.waitKey(1) & 0xFF == ord('q'):
                break
    cv.destroyAllWindows()
