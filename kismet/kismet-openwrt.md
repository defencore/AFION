# Build Kismet for OpenWrt
```
$ git clone https://github.com/kismetwireless/kismet
$ cd kismet
$ ./configure --build=x86_64-unknown-linux-gnu --host=mips-openwrt-linux --with-protoc=/home/ubuntu/build/bin/protoc
$ make HAS_PKG_CONFIG=false CC=mipsel-linux-gnu-gcc CXX=mipsel-linux-gnu-g++ PROTOBUF_CONFIG_OPTS="--host=mipsel-linux CC=mipsel-linux-gnu-gcc CXX=mipsel-linux-gnu-g++ --with-protoc=protoc"
$ ./configure --host=mips-linux CC=mips-linux-gnu-gcc CXX=mips-linux-gnu-g++ --with-protoc=protoc

```
