import glob

import os, random, struct

from Crypto.Cipher import AES

def decrypt_file(key, in_filename, out_filename=None, chunksize=24 * 1024):

    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]  # 파일명이 지정되지 않을 경우, 기존파일의 확장자를 추출 / 현재 test.txt.enc 상태

    with open(in_filename, 'rb') as infile:  # 현재 파일을 바이너리로 읽어들임

        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]  # 현재 파일의 int형으로 된 부분을 읽어들여 다시 원래상태로 언패킹함

        iv = infile.read(16)  # 현재파일의 16자리를 읽어들임

        decryptor = AES.new(key, AES.MODE_CBC, iv)  # AES로 암호화된 키값을 생성

        with open(out_filename, 'wb') as outfile:  # 새 파일을 바이너리 모드로 생성

            while True:

                chunk = infile.read(chunksize)  # 쓰레기값을 읽어들임 65536

                if len(chunk) == 0:  # 쓰레기값이 0일 경우 루프 탈출

                    break

                outfile.write(decryptor.decrypt(chunk))  # 쓰레기를 복호화해서 새파일에 작성

            outfile.truncate(origsize)  # 새 파일에 언패킹한 크기 만큼 잘라냄


key = b'asdfghjkl1234567'  # AES 암호화에사용될 키값을 바이너리로 생성

startPath = 'C:/Users/user/Desktop/진형준/**'  # 암 / 복호화할 대상 경로

# Decrypts the files
#
for filename in glob.iglob(startPath, recursive=True):  # 대상 경로를 재귀적 호출

    if (os.path.isfile(filename)):  # 현재파일이 파일일 때

        fname, ext = os.path.splitext(filename)  # 파일명과 확장자를 추출

        if (ext == '.진형준보지지름15cm'):  # 확장자가 .enc (암호화된 파일일 때)

            print('Decrypting> ' + filename)  # 파일명 출력

            decrypt_file(key, filename)  # 복호화 함수 실행

            os.remove(filename)  # 암호화됐던 파일을 제거 (마찬가지로 새파일을 작성하였기에 기존 파일을 제거해야함.)