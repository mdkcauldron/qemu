%define qemu_name	qemu
%define qemu_version	2.1.3
%define qemu_rel	5
#define qemu_snapshot	rc2
#define qemu_snapshot_prefix 0

%define qemu_release	%mkrel %{?qemu_snapshot:%{qemu_snapshot_prefix}.%{qemu_snapshot}.}%{qemu_rel}
%define qemu_pkgver     %{qemu_name}-%{qemu_version}%{?qemu_snapshot:-%{qemu_snapshot}}

Summary:	QEMU CPU Emulator
Name:		qemu
Version:	%{qemu_version}
Release:	%{qemu_release}
Source0:	http://wiki.qemu-project.org/download/%{qemu_name}-%{version}%{?qemu_snapshot:-%{qemu_snapshot}}.tar.bz2
Source1:	kvm.modules
# KSM control scripts
Source4:	ksm.service
Source5:	ksm.sysconfig
Source6:	ksmtuned.service
Source7:	ksmtuned
Source8:	ksmtuned.conf
Source9:	ksmctl.c

License:	GPLv2+
URL:		http://wiki.qemu.org/Main_Page
Group:		Emulators
Provides:	kvm
Requires:	qemu-img = %{version}-%{release}
# for %%{_sysconfdir}/sasl2
Requires:	cyrus-sasl
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	libtool
BuildRequires:	libSDL-devel
BuildRequires:	texi2html
BuildRequires:	e2fsprogs-devel
BuildRequires:	kernel-headers	
BuildRequires:	pulseaudio-devel
BuildRequires:	zlib-devel
BuildRequires:	brlapi-devel
BuildRequires:	gnutls-devel
BuildRequires:	libsasl-devel
BuildRequires:	pciutils-devel
BuildRequires:	texinfo
BuildRequires:	vde-devel
BuildRequires:	bluez-devel
BuildRequires:	curl-devel
BuildRequires:	pkgconfig(libusbredirparser-0.5) >= 0.6
BuildRequires:	libuuid-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	libaio-devel
BuildRequires:	cap-ng-devel
# for virtfs
BuildRequires:	cap-devel
BuildRequires:	attr-devel
# for direct xfs access with raw device
BuildRequires:  libxfs-devel
BuildRequires:  pkgconfig(libcacard)
# USB features
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  usbredir-devel

%ifarch %{ix86} x86_64
BuildRequires: spice-protocol >= 0.8.1
BuildRequires: spice-server-devel >= 0.9.0
BuildRequires: xen-devel >= 4.1.2
%endif

BuildRequires:	dev86
BuildRequires:	iasl
ExclusiveArch:	%{ix86} ppc x86_64 amd64 %{sunsparc}

#http://lists.gnu.org/archive/html/qemu-devel/2014-01/msg01035.html
Patch0: qemu-2.0.0-mga-compile-fix.patch

# Fedora patches
# Allow aarch64 to boot compressed kernel
Patch0001: 0001-loader-Add-load_image_gzipped-function.patch
Patch0002: 0002-aarch64-Allow-kernel-option-to-take-a-gzip-compresse.patch
# Fix crash in curl driver
Patch0003: 0003-block.curl-adding-timeout-option.patch
Patch0004: 0004-curl-Allow-a-cookie-or-cookies-to-be-sent-with-http-.patch
Patch0005: 0005-curl-Don-t-deref-NULL-pointer-in-call-to-aio_poll.patch
# Fix PPC virtio regression (bz #1144490)
Patch0006: 0006-virtio-pci-fix-migration-for-pci-bus-master.patch
Patch0007: 0007-Revert-virtio-pci-fix-migration-for-pci-bus-master.patch
# Fix qemu-img convert corruption for unflushed files (bz #1167249)
Patch0008: 0008-block-raw-posix-Fix-disk-corruption-in-try_fiemap.patch
Patch0009: 0009-block-raw-posix-use-seek_hole-ahead-of-fiemap.patch
# Fix USB host assignment (bz #1187749)
Patch0010: 0010-usb-host-fix-usb_host_speed_compat-tyops.patch
# Qemu: PRDT overflow from guest to host (bz #1204919, bz #1205322)
Patch0011: 0011-ide-Correct-handling-of-malformed-short-PRDTs.patch
# CVE-2014-8106: cirrus: insufficient blit region checks (bz #1170612,
# bz #1169454)
Patch0012: 0012-cirrus-fix-blit-region-check.patch
Patch0013: 0013-cirrus-don-t-overflow-CirrusVGAState-cirrus_bltbuf.patch
# Fix .vdi disk corruption (bz #1199400)
Patch0014: 0014-block-vdi-Add-locking-for-parallel-requests.patch
# CVE-2015-1779 vnc: insufficient resource limiting in VNC websockets
# decoder (bz #1205051, bz #1199572)
Patch0015: 0015-CVE-2015-1779-incrementally-decode-websocket-frames.patch
Patch0016: 0016-CVE-2015-1779-limit-size-of-HTTP-headers-from-websoc.patch
# Fix qemu-img error (bz #1200043)
Patch0017: 0017-block-Fix-max-nb_sectors-in-bdrv_make_zero.patch
# CVE-2015-3456: (VENOM) fdc: out-of-bounds fifo buffer memory access
# (bz #1221152)
Patch0018: 0018-fdc-force-the-fifo-access-to-be-in-bounds-of-the-all.patch
# User interface freezes when entering space character in Xfig (bz
# #1151253)
Patch0019: 0019-qxl-keep-going-if-reaching-guest-bug-on-empty-area.patch
# CVE-2015-4037: insecure temporary file use in /net/slirp.c (bz
# #1222894)
Patch0020: 0020-slirp-use-less-predictable-directory-name-in-tmp-for.patch
# Backport {Haswell,Broadwell}-noTSX cpu models (bz #1213053)
Patch0021: 0021-target-i386-Haswell-noTSX-and-Broadwell-noTSX.patch
# CVE-2015-3214: i8254: out-of-bounds memory access (bz #1243728)
Patch0022: 0022-CVE-2015-3214-i8254-out-of-bounds-pit.patch
# CVE-2015-5154: ide: atapi: heap overflow during I/O buffer memory
# access (bz #1247141)
Patch0023: 0023-CVE-2015-5154-check-ide-array-bounds-patch.patch
# CVE-2015-3209: pcnet: multi-tmd buffer overflow in the tx path (bz
# #1230536)
Patch0024: 0024-CVE-2015-3209-fix-pcnet-heap-buffer-overflow.patch
Patch0025: 0025-CVE-2015-4103-gate-xen-pci-cfg-contents.patch
Patch0026: 0026-CVE-2015-4104-xen-dont-allow-guest-control-msi-mask.patch
Patch0027: 0027-CVE-2015-4105-xen-limit-msi-error-messages.patch
Patch0028: 0028-CVE-2015-4106-xen-improper-restrict-pci-config-space.patch
# CVE-2015-5745: buffer overflow in virtio-serial (bz #1251160)
# https://github.com/qemu/qemu/commit/7882080388be5088e72c425b02223c02e6cb4295
# virtio-serial: fix ANY_LAYOUT
Patch0029: qemu-2.4.0-rc3-CVE-2015-5745.patch
# CVE-2015-5165: rtl8139 uninitialized heap memory information leakage
# to guest (bz #1249755)
Patch0030: 0030-rtl8139-avoid-nested-ifs-in-IP-header-parsing-CVE-20.patch
Patch0031: 0031-rtl8139-drop-tautologous-if-ip-.-statement-CVE-2015-.patch
Patch0032: 0032-rtl8139-skip-offload-on-short-Ethernet-IP-header-CVE.patch
Patch0033: 0033-rtl8139-check-IP-Header-Length-field-CVE-2015-5165.patch
Patch0034: 0034-rtl8139-check-IP-Total-Length-field-CVE-2015-5165.patch
Patch0035: 0035-rtl8139-skip-offload-on-short-TCP-header-CVE-2015-51.patch
Patch0036: 0036-rtl8139-check-TCP-Data-Offset-field-CVE-2015-5165.patch

# Fix crash in qemu_spice_create_display (bz #1163047)
Patch0100: 0022-spice-display-fix-segfault-in-qemu_spice_create_upda.patch
# CVE-2015-5255: heap memory corruption in vnc_refresh_server_surface
# (bz #1255899)
Patch0101: 0101-vnc-fix-memory-corruption-CVE-2015-5225.patch
Patch0102: 0102-e1000-Avoid-infinite-loop-in-processing-transmit-des.patch
Patch0103: 0103-ide-fix-ATAPI-command-permissions.patch

%description
QEMU is a FAST! processor emulator. By using dynamic translation it
achieves a reasonnable speed while being easy to port on new host
CPUs. QEMU has two operating modes:

* User mode emulation. In this mode, QEMU can launch Linux processes
  compiled for one CPU on another CPU. Linux system calls are
  converted because of endianness and 32/64 bit mismatches. Wine
  (Windows emulation) and DOSEMU (DOS emulation) are the main targets
  for QEMU.

* Full system emulation. In this mode, QEMU emulates a full system,
  including a processor and various peripherials. Currently, it is
  only used to launch an x86 Linux kernel on an x86 Linux system. It
  enables easier testing and debugging of system code. It can also be
  used to provide virtual hosting of several virtual PC on a single
  server.

%package img
Summary:	QEMU disk image utility
Group:		Emulators
Version:	%{qemu_version}
Release:	%{qemu_release}

%description img
This package contains the QEMU disk image utility that is used to
create, commit, convert and get information from a disk image.

%prep
%setup -q -n %{qemu_pkgver}
%apply_patches

%build
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

%ifarch %{ix86} x86_64
./configure \
	--target-list=x86_64-softmmu \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--audio-drv-list=pa,sdl,alsa,oss \
	--enable-spice \
	--enable-xen \
	--enable-xen-pci-passthrough \
        --enable-libusb \
        --enable-linux-aio \
        --enable-usb-redir \
	--disable-kvm \
	--extra-ldflags=$extraldflags \
	--extra-cflags="$CFLAGS"

%make V=1 $buildldflags
cp -a x86_64-softmmu/qemu-system-x86_64 qemu-xen
%make clean

# sdl outputs to alsa or pulseaudio depending on system config, but it's broken (RH bug #495964)
# alsa works, but causes huge CPU load due to bugs
# oss works, but is very problematic because it grabs exclusive control of the device causing other apps to go haywire
./configure \
	--target-list=x86_64-softmmu \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--audio-drv-list=pa,sdl,alsa,oss \
	--enable-spice \
	--enable-kvm \
        --enable-libusb \
        --enable-linux-aio \
        --enable-usb-redir \
	--disable-xen \
	--extra-ldflags=$extraldflags \
	--extra-cflags="$CFLAGS"

%make V=1 $buildldflags
cp -a x86_64-softmmu/qemu-system-x86_64 qemu-kvm
%make clean

%endif

./configure \
	--target-list="i386-softmmu x86_64-softmmu arm-softmmu cris-softmmu m68k-softmmu \
		mips-softmmu mipsel-softmmu mips64-softmmu mips64el-softmmu ppc-softmmu \
		ppcemb-softmmu ppc64-softmmu sh4-softmmu sh4eb-softmmu sparc-softmmu \
		i386-linux-user x86_64-linux-user alpha-linux-user arm-linux-user \
		armeb-linux-user cris-linux-user m68k-linux-user mips-linux-user \
		mipsel-linux-user ppc-linux-user ppc64-linux-user ppc64abi32-linux-user \
		sh4-linux-user sh4eb-linux-user sparc-linux-user sparc64-linux-user \
		sparc32plus-linux-user" \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--interp-prefix=%{_prefix}/qemu-%%M \
	--audio-drv-list=pa,sdl,alsa,oss \
        --enable-linux-aio \
        --enable-libusb \
        --enable-usb-redir \
	--disable-kvm \
	--disable-xen \
%ifarch %{ix86} x86_64
	--enable-spice \
%endif
	--extra-ldflags=$extraldflags \
	--extra-cflags="$CFLAGS"

%make V=1 $buildldflags

gcc %{SOURCE9} -O2 -g -o ksmctl

%install
install -D -p -m 0644 %{SOURCE4} %{buildroot}/%{_unitdir}/ksm.service
install -D -p -m 0644 %{SOURCE5} %{buildroot}/%{_sysconfdir}/sysconfig/ksm
install -D -p -m 0755 ksmctl %{buildroot}/lib/systemd/ksmctl

install -D -p -m 0644 %{SOURCE6} %{buildroot}/%{_unitdir}/ksmtuned.service
install -D -p -m 0755 %{SOURCE7} %{buildroot}/%{_sbindir}/ksmtuned
install -D -p -m 0644 %{SOURCE8} %{buildroot}/%{_sysconfdir}/ksmtuned.conf

%ifarch %{ix86} x86_64
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig/modules
mkdir -p %{buildroot}/%{_bindir}/
mkdir -p %{buildroot}/%{_datadir}/%{name}

install -m 0755 %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/modules/kvm.modules
install -m 0755 qemu-kvm %{buildroot}/%{_bindir}/
install -m 0755 qemu-xen %{buildroot}/%{_bindir}/
%endif

%makeinstall_std BUILD_DOCS="yes"

install -D -p -m 0644 qemu.sasl %{buildroot}/%{_sysconfdir}/sasl2/qemu.conf

# remove unpackaged files
rm -rf %{buildroot}/%{_docdir}/qemu %{buildroot}%{_bindir}/vscclient
rm -f %{buildroot}/%{_libdir}/libcacard*
rm -f %{buildroot}/usr/lib/libcacard*
rm -f %{buildroot}/%{_libdir}/pkgconfig/libcacard.pc
rm -f %{buildroot}/usr/lib/pkgconfig/libcacard.pc
rm -rf %{buildroot}/%{_includedir}/cacard

%post 
%ifarch %{ix86} x86_64
# load kvm modules now, so we can make sure no reboot is needed.
# If there's already a kvm module installed, we don't mess with it
sh /%{_sysconfdir}/sysconfig/modules/kvm.modules
%endif
%_post_service ksmtuned
%_post_service ksm

%preun
%_preun_service ksm
%_preun_service ksmtuned



%files
%doc README qemu-doc.html qemu-tech.html
%config(noreplace)%{_sysconfdir}/sasl2/qemu.conf
%{_unitdir}/ksm.service
/lib/systemd/ksmctl
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
%{_unitdir}/ksmtuned.service
%{_sbindir}/ksmtuned
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%{_sysconfdir}/sysconfig/modules/kvm.modules
%{_sysconfdir}/qemu/target-x86_64.conf
%{_bindir}/qemu-io
%{_bindir}/qemu-kvm
%{_bindir}/qemu-xen
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm*
%{_bindir}/qemu-cris
%{_bindir}/qemu-ga
%{_bindir}/qemu-i386
%{_bindir}/qemu-m68k
%{_bindir}/qemu-mips*
%{_bindir}/qemu-nbd
%{_bindir}/qemu-ppc*
%{_bindir}/qemu-sh4*
%{_bindir}/qemu-sparc*
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-system-arm
%{_bindir}/qemu-system-cris
%{_bindir}/qemu-system-m68k
%{_bindir}/qemu-system-sh4*
%{_bindir}/qemu-system-ppc*
%{_bindir}/qemu-system-mips*
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-x86_64
%{_bindir}/qemu-system-i386
%{_bindir}/virtfs-proxy-helper
%{_mandir}/man1/qemu.1*
%{_mandir}/man8/qemu-nbd.8*
%{_mandir}/man1/virtfs-proxy-helper.*
%dir %{_datadir}/qemu
%{_datadir}/qemu/*.aml
%{_datadir}/qemu/*.bin
%{_datadir}/qemu/*.img
%{_datadir}/qemu/*.rom
%{_datadir}/qemu/u-boot.e500
%{_datadir}/qemu/keymaps
%{_datadir}/qemu/openbios-sparc32
%{_datadir}/qemu/openbios-sparc64
%{_datadir}/qemu/openbios-ppc
%{_datadir}/qemu/*.dtb
%{_datadir}/qemu/palcode-clipper
%{_datadir}/qemu/qemu-icon.bmp
/usr/libexec/qemu-bridge-helper
%{_datadir}/qemu/*.svg

%files img
%{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*


