# Prepare Docker
```
% docker build -t openwrt-sdk .
% docker run --rm -it -v "$(pwd)":/workspace openwrt-sdk
```
# Prepare OpenWrt SDK
```
% cd /root
% git clone https://github.com/kismetwireless/kismet-packages.git
% git clone https://git.openwrt.org/openwrt/openwrt.git
% cd openwrt
% git checkout v22.03.4
% ./scripts/feeds update -a
% ./scripts/feeds install -a
% cp -r ../kismet-packages/openwrt/kismet-openwrt/ package/
% make menuconfig
```

```
Target System (Atheros ATH79)  --->
Subtarget (Generic devices with NAND flash)  --->
Target Profile (GL.iNet GL-E750)  --->
```

```
% export FORCE_UNSAFE_CONFIGURE=1
% make package/symlinks
% make tools/install V=s -j$(nproc)
% make toolchain/install V=s -j$(nproc)
% make target/compile V=s -j$(nproc)
% make V=s -j$(nproc)
```


# Compile Kismet for GL.iNet GL-E750 MUDI
![image](https://github.com/user-attachments/assets/f05879e0-6fe2-47b2-9ae0-07ceee73239c)

`Base firmware: OpenWrt 22.03.4, ARCH=mips_24kc, TARGET=ath79/nand`

```
% make menuconfig
```
```
Network  --->
    kismet  --->
        <M> kismet
        <M> kismet-capture-linux-wifi
        <M> kismet-capture-linux-bluetooth
        <M> kismet-capture-nrf-51822
        <M> kismet-capture-nrf-52840
        <M> kismet-manuf-database
        <M> kismet-tools
```

```
% export LDFLAGS="-L/root/openwrt/staging_dir/target-mips_24kc_musl/usr/lib"
% export CFLAGS="-I/root/openwrt/staging_dir/target-mips_24kc_musl/usr/include"
% make V=s -j$(nproc)
```
**or**
```
% make package/kismet/compile LDFLAGS="-L/root/openwrt/staging_dir/target-mips_24kc_musl/usr/lib" CFLAGS="-I/root/openwrt/staging_dir/target-mips_24kc_musl/usr/include" V=s -j$(nproc)
```
