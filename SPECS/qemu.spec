%global have_working_systemtap 0

%ifarch %{ix86}
%global kvm_package   system-x86
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%endif
%ifarch x86_64
%global kvm_package   system-x86
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%endif
%ifarch armv7hl
%global kvm_package   system-arm
%endif
%ifarch aarch64
%global kvm_package   system-aarch64
%endif

%global have_kvm 0
%if 0%{?kvm_package:1}
%global have_kvm 1
%endif

%ifarch %{ix86} x86_64 %{arm} aarch64 %{power64} s390 s390x
%global have_seccomp 1
%endif

%ifarch %{ix86} x86_64
%global have_spice   1
%endif

# Xen is available only on i386 x86_64 (from libvirt spec)
%ifarch %{ix86} x86_64
%global have_xen 1
%endif

# Release candidate version tracking
#global rcver	rc5
%if 0%{?rcver:1}
%global rcstr -%{rcver}
%endif

Summary:	QEMU is a FAST! processor emulator
Name:		qemu
Version:	2.6.0
Release:	%mkrel %{?rcver:0.%{rcver}.}3
Epoch: 0
License:	GPLv2+ and LGPLv2+ and BSD
Group:		Emulators
URL:		http://www.qemu.org/

Source0:	http://wiki.qemu-project.org/download/%{name}-%{version}%{?rcstr}.tar.bz2

Source1: qemu.binfmt

# Creates /dev/kvm
Source3: 80-kvm.rules
# KSM control scripts
Source4:	ksm.service
Source5:	ksm.sysconfig
Source6:	ksmctl.c
Source7:	ksmtuned.service
Source8:	ksmtuned
Source9:	ksmtuned.conf
# guest agent service
Source10: qemu-guest-agent.service
# guest agent udev rules
Source11: 99-qemu-guest-agent.rules
# /etc/qemu/bridge.conf
Source12: bridge.conf
# qemu-kvm back compat wrapper installed as /usr/bin/qemu-kvm
Source13: qemu-kvm.sh
# /etc/modprobe.d/kvm.conf
Source20: kvm.conf

# Adjust spice gl version check to expect F24 backported version
# Not for upstream, f24 only
Patch0001: 0001-spice-F24-spice-has-backported-gl-support.patch
# Fix gtk UI crash when switching to monitor (bz #1333424)
# Not upstream yet
Patch0002: 0002-ui-gtk-fix-crash-when-terminal-inner-border-is-NULL.patch
# Fix sdl2 UI lockup lockup when switching to monitor
# Not upstream yet
Patch0003: 0003-ui-sdl2-Release-grab-before-opening-console-window.patch


# for %%{_sysconfdir}/sasl2
Requires:	cyrus-sasl
# documentation deps
BuildRequires:	texi2html
BuildRequires:	texinfo
# For /usr/bin/pod2man
BuildRequires:	perl
BuildRequires:	kernel-headers	
# For acpi compilation
BuildRequires:	iasl
# For chrpath calls in specfile
BuildRequires:	chrpath

BuildRequires:	e2fsprogs-devel
BuildRequires:	pulseaudio-devel
# -display sdl support
BuildRequires:	SDL2-devel
# used in various places for compression
BuildRequires:	zlib-devel
# used in various places for crypto
BuildRequires:	gnutls-devel
# VNC sasl auth support
BuildRequires:	libsasl-devel
BuildRequires:	vde-devel
BuildRequires:	libtool
# aio implementation for block drivers
BuildRequires:	libaio-devel
# pulseaudio audio output
BuildRequires:	pulseaudio-devel
# iscsi drive support
BuildRequires:	pkgconfig(libiscsi)
# NFS drive support
BuildRequires: libnfs-devel
# snappy compression for memory dump
BuildRequires: snappy-devel
# lzo compression for memory dump
BuildRequires:	lzo-devel
# needed for -display curses
BuildRequires:	ncurses-devel
# used by 9pfs
BuildRequires:	libattr-devel
BuildRequires: libcap-devel
# used by qemu-bridge-helper
BuildRequires: libcap-ng-devel
# spice usb redirection support
BuildRequires: usbredir-devel >= 0.5.2
# tcmalloc support
BuildRequires: gperftools-devel
%if 0%{?have_spice:1}
# spice graphics support
BuildRequires: spice-protocol >= 0.12.2
BuildRequires: spice-server-devel >= 0.12.0
%endif
%if 0%{?have_seccomp:1}
# seccomp containment support
BuildRequires: libseccomp-devel >= 2.3.0
%endif
# For network block driver
BuildRequires: libcurl-devel
# We need both because the 'stap' binary is probed for by configure
BuildRequires: systemtap
# For VNC JPEG support
BuildRequires: libjpeg-devel
# For VNC PNG support
BuildRequires: libpng-devel
# For uuid generation
BuildRequires: libuuid-devel
# For BlueZ device support
BuildRequires: bluez-devel
# For Braille device support
BuildRequires: brlapi-devel
# For FDT device tree support
BuildRequires: libfdt-devel
# Hard requirement for version >= 1.3
BuildRequires: pixman-devel
# For gluster support
BuildRequires: glusterfs-devel >= 3.4.0
# Needed for usb passthrough for qemu >= 1.5
BuildRequires: libusbx-devel
# SSH block driver
BuildRequires: libssh2-devel
# GTK frontend
BuildRequires: gtk3-devel
BuildRequires: vte2.90-devel
# GTK translations
BuildRequires: gettext
# RDMA migration
BuildRequires: librdmacm-devel
%if 0%{?have_xen:1}
# Xen support
BuildRequires:	xen-devel
%endif
%ifarch %{ix86} x86_64 aarch64
# qemu 2.1: needed for memdev hostmem backend
BuildRequires: numactl-devel
%endif
# qemu 2.3: reading bzip2 compressed dmg images
BuildRequires: bzip2-devel
# qemu 2.4: needed for opengl bits
BuildRequires: libepoxy-devel
# qemu 2.5: needed for TLS test suite
BuildRequires: libtasn1-devel
# qemu 2.5: libcacard is it's own project now
BuildRequires: libcacard-devel >= 2.5.0
# qemu 2.5: virgl 3d support
BuildRequires: virglrenderer-devel
# qemu 2.6: Needed for gtk GL support
BuildRequires: pkgconfig(gbm)
BuildRequires: libegl-devel

Requires: %{name}-user = %{epoch}:%{version}-%{release}
Requires: %{name}-system-alpha = %{epoch}:%{version}-%{release}
Requires: %{name}-system-arm = %{epoch}:%{version}-%{release}
Requires: %{name}-system-cris = %{epoch}:%{version}-%{release}
Requires: %{name}-system-lm32 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-m68k = %{epoch}:%{version}-%{release}
Requires: %{name}-system-microblaze = %{epoch}:%{version}-%{release}
Requires: %{name}-system-mips = %{epoch}:%{version}-%{release}
Requires: %{name}-system-or32 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-ppc = %{epoch}:%{version}-%{release}
Requires: %{name}-system-s390x = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sh4 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sparc = %{epoch}:%{version}-%{release}
Requires: %{name}-system-unicore32 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-x86 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-xtensa = %{epoch}:%{version}-%{release}
Requires: %{name}-system-moxie = %{epoch}:%{version}-%{release}
Requires: %{name}-system-aarch64 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-tricore = %{epoch}:%{version}-%{release}
Requires: %{name}-img = %{epoch}:%{version}-%{release}


%description
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation. QEMU has two operating modes:

 * Full system emulation. In this mode, QEMU emulates a full system (for
   example a PC), including a processor and various peripherials. It can be
   used to launch different Operating Systems without rebooting the PC or
   to debug system code.
 * User mode emulation. In this mode, QEMU can launch Linux processes compiled
   for one CPU on another CPU.

As QEMU requires no host kernel patches to run, it is safe and easy to use.

%package  common
Summary: QEMU common files needed by all QEMU targets
Group: Development/Tools
# For: /usr/bin/getent
Requires: glibc
#For: /usr/sbin/useradd
Requires: shadow-utils
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6

%description common
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the common files needed by all QEMU targets


%package -n ksm
Summary: Kernel Samepage Merging services
Group: Development/Tools
Requires(post): systemd-units
Requires(postun): systemd-units
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description -n ksm
Kernel Samepage Merging (KSM) is a memory-saving de-duplication feature,
that merges anonymous (private) pages (not pagecache ones).

This package provides service files for disabling and tuning KSM.


%package guest-agent
Summary: QEMU guest agent
Group: Emulators
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6

%description guest-agent
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.


%package img
Summary:	QEMU command line tool for manipulating disk images
Group:		Emulators
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6

%description img
This package provides a command line tool for manipulating disk images

%package -n ivshmem-tools
Summary: Client and server for QEMU ivshmem device
Group: Development/Tools
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6

%description -n ivshmem-tools
This package provides client and server tools for QEMU's ivshmem device.



%if %{have_kvm}
%package kvm
Summary: QEMU metapackage for KVM support
Group: Development/Tools
Requires: qemu-%{kvm_package} = %{epoch}:%{version}-%{release}

%description kvm
This is a meta-package that provides a qemu-system-<arch> package for native
architectures where kvm can be enabled. For example, in an x86 system, this
will install qemu-system-x86


%package kvm-tools
Summary: KVM debugging and diagnostics tools
Group: Development/Tools

%description kvm-tools
This package contains some diagnostics and debugging tools for KVM,
such as kvm_stat.
%endif


%package user
Summary: QEMU user mode emulation of qemu targets
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description user
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the user mode emulation of qemu targets


%package system-x86
Summary: QEMU system emulator for x86
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Provides: kvm = 85
Obsoletes: kvm < 85
Requires: seavgabios-bin
# virtio-blk booting is broken for Windows guests
# if you mix seabios 1.7.4 and qemu 2.1.x
Requires: seabios-bin >= 1.7.5
Requires: sgabios-bin
Requires: ipxe-roms-qemu
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%ifarch %{ix86} x86_64
Recommends: edk2-ovmf-arm edk2-ovmf-aarch64
%endif
%ifarch %{arm}
Recommends: edk2-ovmf-ia32 edk2-ovmf-x64
%endif


%description system-x86
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.


%package system-alpha
Summary: QEMU system emulator for Alpha
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description system-alpha
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Alpha systems.


%package system-arm
Summary: QEMU system emulator for ARM
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description system-arm
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ARM boards.


%package system-mips
Summary: QEMU system emulator for MIPS
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description system-mips
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for MIPS boards.


%package system-cris
Summary: QEMU system emulator for CRIS
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description system-cris
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for CRIS boards.


%package system-lm32
Summary: QEMU system emulator for LatticeMico32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description system-lm32
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for LatticeMico32 boards.


%package system-m68k
Summary: QEMU system emulator for ColdFire (m68k)
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description system-m68k
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ColdFire boards.


%package system-microblaze
Summary: QEMU system emulator for Microblaze
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description system-microblaze
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Microblaze boards.


%package system-or32
Summary: QEMU system emulator for OpenRisc32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description system-or32
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for OpenRisc32 boards.


%package system-s390x
Summary: QEMU system emulator for S390
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description system-s390x
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for S390 systems.


%package system-sh4
Summary: QEMU system emulator for SH4
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description system-sh4
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SH4 boards.


%package system-sparc
Summary: QEMU system emulator for SPARC
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
Requires: openbios
%description system-sparc
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SPARC and SPARC64 systems.


%package system-ppc
Summary: QEMU system emulator for PPC
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: openbios
Requires: SLOF
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description system-ppc
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for PPC and PPC64 systems.


%package system-xtensa
Summary: QEMU system emulator for Xtensa
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description system-xtensa
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Xtensa boards.


%package system-unicore32
Summary: QEMU system emulator for Unicore32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description system-unicore32
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Unicore32 boards.


%package system-moxie
Summary: QEMU system emulator for Moxie
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description system-moxie
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Moxie boards.


%package system-aarch64
Summary: QEMU system emulator for AArch64
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description system-aarch64
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for AArch64.


%package system-tricore
Summary: QEMU system emulator for tricore
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Conflicts: qemu <= 2.6.0-0.rc3.1.mga6
%description system-tricore
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Tricore.


%prep
%setup -q -n qemu-%{version}%{?rcstr}
%autopatch -p1


%build
# --build-id option is used for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

# As of qemu 2.1, --enable-trace-backends supports multiple backends,
# but there's a performance impact for non-dtrace so we don't use them
tracebackends="dtrace"

    buildarch="i386-softmmu x86_64-softmmu alpha-softmmu arm-softmmu \
cris-softmmu lm32-softmmu m68k-softmmu microblaze-softmmu \
microblazeel-softmmu mips-softmmu mipsel-softmmu mips64-softmmu \
mips64el-softmmu or32-softmmu ppc-softmmu ppcemb-softmmu ppc64-softmmu \
s390x-softmmu sh4-softmmu sh4eb-softmmu sparc-softmmu sparc64-softmmu \
xtensa-softmmu xtensaeb-softmmu unicore32-softmmu moxie-softmmu \
tricore-softmmu \
i386-linux-user x86_64-linux-user aarch64-linux-user alpha-linux-user \
arm-linux-user armeb-linux-user cris-linux-user m68k-linux-user \
microblaze-linux-user microblazeel-linux-user mips-linux-user \
mipsel-linux-user mips64-linux-user mips64el-linux-user \
mipsn32-linux-user mipsn32el-linux-user \
or32-linux-user ppc-linux-user ppc64-linux-user ppc64le-linux-user \
ppc64abi32-linux-user s390x-linux-user sh4-linux-user sh4eb-linux-user \
sparc-linux-user sparc64-linux-user sparc32plus-linux-user \
unicore32-linux-user aarch64-softmmu"

    %global tcmallocflag --enable-tcmalloc

%if 0%{?have_spice:1}
    %global spiceflag --enable-spice
%else
    %global spiceflag --disable-spice
%endif

./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--sysconfdir=%{_sysconfdir} \
	--interp-prefix=%{_prefix}/qemu-%%M \
	--localstatedir=%{_localstatedir} \
	--libexecdir=%{_libexecdir} \
	--with-pkgversion=%{name}-%{version}-%{release} \
	--disable-strip \
	--extra-ldflags=$extraldflags \
	--extra-cflags="%{optflags}" \
	--disable-xfsctl \
	--target-list="$buildarch" \
	--audio-drv-list=pa,sdl,alsa,oss \
	--enable-kvm \
	%{tcmallocflag} \
	%{spiceflag} \
	--with-sdlabi="2.0" \
	--with-gtkabi="3.0" \

echo "config-host.mak contents:"
echo "==="
cat config-host.mak
echo "==="

%make V=1 $buildldflags

gcc %{_sourcedir}/ksmctl.c -O2 -g -o ksmctl


%install

%global _udevdir /lib/udev/rules.d
%global qemudocdir %{_docdir}/%{name}

mkdir -p %{buildroot}%{_udevdir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/qemu

install -D -p -m 0644 %{_sourcedir}/ksm.service %{buildroot}%{_unitdir}
install -D -p -m 0644 %{_sourcedir}/ksm.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/ksm
install -D -p -m 0755 ksmctl %{buildroot}%{_libexecdir}/ksmctl
install -D -p -m 0644 %{_sourcedir}/ksmtuned.service %{buildroot}%{_unitdir}
install -D -p -m 0755 %{_sourcedir}/ksmtuned %{buildroot}%{_sbindir}/ksmtuned
install -D -p -m 0644 %{_sourcedir}/ksmtuned.conf %{buildroot}%{_sysconfdir}/ksmtuned.conf

install -D -p -m 0644 %{_sourcedir}/kvm.conf %{buildroot}%{_sysconfdir}/modprobe.d/kvm.conf

# Install qemu-guest-agent service and udev rules
install -m 0644 %{_sourcedir}/qemu-guest-agent.service %{buildroot}%{_unitdir}
install -m 0644 %{_sourcedir}/99-qemu-guest-agent.rules %{buildroot}%{_udevdir}

# Install kvm specific bits
%if %{have_kvm}
mkdir -p %{buildroot}%{_bindir}/
install -m 0755 scripts/kvm/kvm_stat %{buildroot}%{_bindir}/
install -m 0644 %{_sourcedir}/80-kvm.rules %{buildroot}%{_udevdir}
%endif


%make_install BUILD_DOCS="yes"

%find_lang %{name}

chmod -x %{buildroot}%{_mandir}/man1/*
install -D -p -m 0644 -t %{buildroot}%{qemudocdir} Changelog README COPYING COPYING.LIB LICENSE
for emu in %{buildroot}%{_bindir}/qemu-system-*; do
    ln -sf qemu.1.xz %{buildroot}%{_mandir}/man1/$(basename $emu).1.xz
done

%if 0%{?need_qemu_kvm}
install -m 0755 %{_sourcedir}/qemu-kvm.sh %{buildroot}%{_bindir}/qemu-kvm
ln -sf qemu.1.xz %{buildroot}%{_mandir}/man1/qemu-kvm.1.xz
%endif

install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/qemu.conf

# Provided by package openbios
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-ppc
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc32
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc64
# Provided by package SLOF
rm -rf %{buildroot}%{_datadir}/%{name}/slof.bin
# Provided by package ipxe
rm -rf %{buildroot}%{_datadir}/%{name}/pxe*rom
rm -rf %{buildroot}%{_datadir}/%{name}/efi*rom
# Provided by package seavgabios
rm -rf %{buildroot}%{_datadir}/%{name}/vgabios*bin
# Provided by package seabios
rm -rf %{buildroot}%{_datadir}/%{name}/bios.bin
rm -rf %{buildroot}%{_datadir}/%{name}/bios-256k.bin
rm -rf %{buildroot}%{_datadir}/%{name}/acpi-dsdt.aml
rm -rf %{buildroot}%{_datadir}/%{name}/q35-acpi-dsdt.aml
# Provided by package sgabios
rm -rf %{buildroot}%{_datadir}/%{name}/sgabios.bin
 
# the pxe gpxe images will be symlinks to the images on
# /usr/share/ipxe, as QEMU doesn't know how to look
# for other paths, yet.
pxe_link() {
  ln -s ../ipxe/$2.rom %{buildroot}%{_datadir}/%{name}/pxe-$1.rom
  ln -s ../ipxe.efi/$2.rom %{buildroot}%{_datadir}/%{name}/efi-$1.rom
}
 
pxe_link e1000 8086100e
pxe_link ne2k_pci 10ec8029
pxe_link pcnet 10222000
pxe_link rtl8139 10ec8139
pxe_link virtio 1af41000
 
rom_link() {
    ln -s $1 %{buildroot}%{_datadir}/%{name}/$2
}
 
rom_link ../seavgabios/vgabios-isavga.bin vgabios.bin
rom_link ../seavgabios/vgabios-cirrus.bin vgabios-cirrus.bin
rom_link ../seavgabios/vgabios-qxl.bin vgabios-qxl.bin
rom_link ../seavgabios/vgabios-stdvga.bin vgabios-stdvga.bin
rom_link ../seavgabios/vgabios-vmware.bin vgabios-vmware.bin
rom_link ../seavgabios/vgabios-virtio.bin vgabios-virtio.bin
rom_link ../seabios/bios.bin bios.bin
rom_link ../seabios/bios-256k.bin bios-256k.bin
rom_link ../seabios/acpi-dsdt.aml acpi-dsdt.aml
rom_link ../seabios/q35-acpi-dsdt.aml q35-acpi-dsdt.aml
rom_link ../sgabios/sgabios.bin sgabios.bin

# Install binfmt
mkdir -p %{buildroot}%{_exec_prefix}/lib/binfmt.d
for i in dummy \
%ifnarch %{ix86} x86_64
    qemu-i386 \
%endif
%ifnarch alpha
    qemu-alpha \
%endif
%ifnarch %{arm}
    qemu-arm \
%endif
    qemu-armeb \
    qemu-cris \
    qemu-microblaze qemu-microblazeel \
%ifnarch mips
    qemu-mips qemu-mips64 \
%endif
%ifnarch mipsel
    qemu-mipsel qemu-mips64el \
%endif
%ifnarch m68k
    qemu-m68k \
%endif
%ifnarch ppc ppc64 ppc64le
    qemu-ppc qemu-ppc64abi32 qemu-ppc64 \
%endif
%ifnarch sparc sparc64
    qemu-sparc qemu-sparc32plus qemu-sparc64 \
%endif
%ifnarch s390 s390x
    qemu-s390x \
%endif
%ifnarch sh4
    qemu-sh4 \
%endif
    qemu-sh4eb \
; do
  test $i = dummy && continue
  grep /$i:\$ %{_sourcedir}/qemu.binfmt > %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i.conf
  chmod 644 %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i.conf
done < %{_sourcedir}/qemu.binfmt


# Install rules to use the bridge helper with libvirt's virbr0
install -m 0644 %{_sourcedir}/bridge.conf %{buildroot}%{_sysconfdir}/qemu

# When building using 'rpmbuild' or 'fedpkg local', RPATHs can be left in
# the binaries and libraries (although this doesn't occur when
# building in Koji, for some unknown reason). Some discussion here:
#
# https://lists.fedoraproject.org/pipermail/devel/2013-November/192553.html
#
# In any case it should always be safe to remove RPATHs from
# the final binaries:
for f in %{buildroot}%{_bindir}/* %{buildroot}%{_libdir}/* \
         %{buildroot}%{_libexecdir}/*; do
  if file $f | grep -q ELF; then chrpath --delete $f; fi
done

%check

# Tests are hanging on s390 as of 2.3.0
#   https://bugzilla.redhat.com/show_bug.cgi?id=1206057
# Tests seem to be a recurring problem on s390, so I'd suggest just leaving
# it disabled.
%global archs_skip_tests s390
%global archs_ignore_test_failures 0

%ifnarch %{archs_skip_tests}

# Check the binary runs (see eg RHBZ#998722).
b="./x86_64-softmmu/qemu-system-x86_64"
if [ -x "$b" ]; then "$b" -help; fi

%ifarch %{archs_ignore_test_failures}
make check V=1
%else
make check V=1 || :
%endif

# Sanity-check current kernel can boot on this qemu.
# The results are advisory only.
%ifarch %{arm}
hostqemu=arm-softmmu/qemu-system-arm
%endif
%ifarch aarch64
hostqemu=arm-softmmu/qemu-system-aarch64
%endif
%ifarch %{ix86}
hostqemu=i386-softmmu/qemu-system-i386
%endif
%ifarch x86_64
hostqemu=x86_64-softmmu/qemu-system-x86_64
%endif
if test -f "$hostqemu"; then qemu-sanity-check --qemu=$hostqemu ||: ; fi

%endif  # archs_skip_tests


%if %{have_kvm}
%post %{kvm_package}
# Default /dev/kvm permissions are 660, we install a udev rule changing that
# to 666. However trying to trigger the re-permissioning via udev has been
# a neverending source of trouble, so we just force it with chmod. For
# more info see: https://bugzilla.redhat.com/show_bug.cgi?id=950436
chmod --quiet 666 /dev/kvm || :
%endif

%post common
getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
  useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
    -c "qemu user" qemu

%post -n ksm
%systemd_post ksm.service
%systemd_post ksmtuned.service
%preun -n ksm
%systemd_preun ksm.service
%systemd_preun ksmtuned.service
%postun -n ksm
%systemd_postun_with_restart ksm.service
%systemd_postun_with_restart ksmtuned.service

%post user
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :


%post guest-agent
%systemd_post qemu-guest-agent.service
%preun guest-agent
%systemd_preun qemu-guest-agent.service
%postun guest-agent
%systemd_postun_with_restart qemu-guest-agent.service


%global kvm_files \
%{_udevdir}/80-kvm.rules

%files
# Deliberately empty


%files common -f %{name}.lang
%dir %{qemudocdir}
%doc %{qemudocdir}/Changelog
%doc %{qemudocdir}/README
%doc %{qemudocdir}/qemu-doc.html
%doc %{qemudocdir}/qemu-tech.html
%doc %{qemudocdir}/qmp-commands.txt
%doc %{qemudocdir}/COPYING
%doc %{qemudocdir}/COPYING.LIB
%doc %{qemudocdir}/LICENSE
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/qemu-icon.bmp
%{_datadir}/%{name}/qemu_logo_no_text.svg
%{_datadir}/%{name}/keymaps/
%{_datadir}/%{name}/trace-events
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/virtfs-proxy-helper.1*
%{_bindir}/virtfs-proxy-helper
%attr(4755, root, root) %{_libexecdir}/qemu-bridge-helper
%config(noreplace) %{_sysconfdir}/sasl2/qemu.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/kvm.conf
%dir %{_sysconfdir}/qemu
%config(noreplace) %{_sysconfdir}/qemu/bridge.conf


%files -n ksm
%{_libexecdir}/ksmctl
%{_sbindir}/ksmtuned
%{_unitdir}/ksmtuned.service
%{_unitdir}/ksm.service
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%config(noreplace) %{_sysconfdir}/sysconfig/ksm

%files guest-agent
%doc COPYING README
%{_bindir}/qemu-ga
%{_mandir}/man8/qemu-ga.8*
%{_unitdir}/qemu-guest-agent.service
%{_udevdir}/99-qemu-guest-agent.rules


%files img
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*

%files -n ivshmem-tools
%{_bindir}/ivshmem-client
%{_bindir}/ivshmem-server

%if %{have_kvm}
%files kvm
# Deliberately empty

%files kvm-tools
%{_bindir}/kvm_stat
%endif

%files user
%{_exec_prefix}/lib/binfmt.d/qemu-*.conf
%{_bindir}/qemu-i386
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-aarch64
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
%{_bindir}/qemu-m68k
%{_bindir}/qemu-microblaze
%{_bindir}/qemu-microblazeel
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-mips64
%{_bindir}/qemu-mips64el
%{_bindir}/qemu-mipsn32
%{_bindir}/qemu-mipsn32el
%{_bindir}/qemu-or32
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64abi32
%{_bindir}/qemu-ppc64le
%{_bindir}/qemu-s390x
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc
%{_bindir}/qemu-sparc32plus
%{_bindir}/qemu-sparc64
%{_bindir}/qemu-unicore32
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-i386*.stp
%{_datadir}/systemtap/tapset/qemu-x86_64*.stp
%{_datadir}/systemtap/tapset/qemu-aarch64*.stp
%{_datadir}/systemtap/tapset/qemu-alpha*.stp
%{_datadir}/systemtap/tapset/qemu-arm*.stp
%{_datadir}/systemtap/tapset/qemu-cris*.stp
%{_datadir}/systemtap/tapset/qemu-m68k*.stp
%{_datadir}/systemtap/tapset/qemu-microblaze*.stp
%{_datadir}/systemtap/tapset/qemu-mips*.stp
%{_datadir}/systemtap/tapset/qemu-or32*.stp
%{_datadir}/systemtap/tapset/qemu-ppc*.stp
%{_datadir}/systemtap/tapset/qemu-s390x*.stp
%{_datadir}/systemtap/tapset/qemu-sh4*.stp
%{_datadir}/systemtap/tapset/qemu-sparc*.stp
%{_datadir}/systemtap/tapset/qemu-unicore32*.stp
%endif


%files system-x86
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-x86_64
%if 0
%{_datadir}/systemtap/tapset/qemu-system-i386*.stp
%{_datadir}/systemtap/tapset/qemu-system-x86_64*.stp
%endif
%{_mandir}/man1/qemu-system-i386.1*
%{_mandir}/man1/qemu-system-x86_64.1*

%if 0%{?need_qemu_kvm}
%{_bindir}/qemu-kvm
%{_mandir}/man1/qemu-kvm.1*
%endif

%{_datadir}/%{name}/acpi-dsdt.aml
%{_datadir}/%{name}/q35-acpi-dsdt.aml
%{_datadir}/%{name}/bios.bin
%{_datadir}/%{name}/bios-256k.bin
%{_datadir}/%{name}/sgabios.bin
%{_datadir}/%{name}/linuxboot.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/%{name}/kvmvapic.bin
%{_datadir}/%{name}/vgabios.bin
%{_datadir}/%{name}/vgabios-cirrus.bin
%{_datadir}/%{name}/vgabios-qxl.bin
%{_datadir}/%{name}/vgabios-stdvga.bin
%{_datadir}/%{name}/vgabios-vmware.bin
%{_datadir}/%{name}/vgabios-virtio.bin
%{_datadir}/%{name}/pxe-e1000.rom
%{_datadir}/%{name}/efi-e1000.rom
%{_datadir}/%{name}/pxe-virtio.rom
%{_datadir}/%{name}/efi-virtio.rom
%{_datadir}/%{name}/pxe-pcnet.rom
%{_datadir}/%{name}/efi-pcnet.rom
%{_datadir}/%{name}/pxe-rtl8139.rom
%{_datadir}/%{name}/efi-rtl8139.rom
%{_datadir}/%{name}/pxe-ne2k_pci.rom
%{_datadir}/%{name}/efi-ne2k_pci.rom
%ifarch %{ix86} x86_64
%{?kvm_files:}
%endif


%files system-alpha
%{_bindir}/qemu-system-alpha
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-system-alpha*.stp
%endif
%{_mandir}/man1/qemu-system-alpha.1*
%{_datadir}/%{name}/palcode-clipper


%files system-arm
%{_bindir}/qemu-system-arm
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-system-arm*.stp
%endif
%{_mandir}/man1/qemu-system-arm.1*
%ifarch armv7hl
%{?kvm_files:}
%endif


%files system-mips
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-mipsel
%{_bindir}/qemu-system-mips64
%{_bindir}/qemu-system-mips64el
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-system-mips*.stp
%endif
%{_mandir}/man1/qemu-system-mips.1*
%{_mandir}/man1/qemu-system-mipsel.1*
%{_mandir}/man1/qemu-system-mips64el.1*
%{_mandir}/man1/qemu-system-mips64.1*


%files system-cris
%{_bindir}/qemu-system-cris
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-system-cris*.stp
%endif
%{_mandir}/man1/qemu-system-cris.1*


%files system-lm32
%{_bindir}/qemu-system-lm32
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-system-lm32*.stp
%endif
%{_mandir}/man1/qemu-system-lm32.1*


%files system-m68k
%{_bindir}/qemu-system-m68k
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-system-m68k*.stp
%endif
%{_mandir}/man1/qemu-system-m68k.1*


%files system-microblaze
%{_bindir}/qemu-system-microblaze
%{_bindir}/qemu-system-microblazeel
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-system-microblaze*.stp
%endif
%{_mandir}/man1/qemu-system-microblaze.1*
%{_mandir}/man1/qemu-system-microblazeel.1*
%{_datadir}/%{name}/petalogix*.dtb


%files system-or32
%{_bindir}/qemu-system-or32
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-system-or32*.stp
%endif
%{_mandir}/man1/qemu-system-or32.1*


%files system-s390x
%{_bindir}/qemu-system-s390x
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-system-s390x*.stp
%endif
%{_mandir}/man1/qemu-system-s390x.1*
%{_datadir}/%{name}/s390-ccw.img
%ifarch s390x
%{?kvm_files:}
%{_sysconfdir}/sysctl.d/50-kvm-s390x.conf
%endif


%files system-sh4
%{_bindir}/qemu-system-sh4
%{_bindir}/qemu-system-sh4eb
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-system-sh4*.stp
%endif
%{_mandir}/man1/qemu-system-sh4.1*
%{_mandir}/man1/qemu-system-sh4eb.1*


%files system-sparc
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-sparc64
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-system-sparc*.stp
%endif
%{_mandir}/man1/qemu-system-sparc.1*
%{_mandir}/man1/qemu-system-sparc64.1*
%{_datadir}/%{name}/QEMU,tcx.bin
%{_datadir}/%{name}/QEMU,cgthree.bin


%files system-ppc
%{_bindir}/qemu-system-ppc
%{_bindir}/qemu-system-ppc64
%{_bindir}/qemu-system-ppcemb
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-system-ppc*.stp
%endif
%{_mandir}/man1/qemu-system-ppc.1*
%{_mandir}/man1/qemu-system-ppc64.1*
%{_mandir}/man1/qemu-system-ppcemb.1*
%{_datadir}/%{name}/bamboo.dtb
%{_datadir}/%{name}/ppc_rom.bin
%{_datadir}/%{name}/spapr-rtas.bin
%{_datadir}/%{name}/u-boot.e500
%ifarch ppc64 ppc64le
%{?kvm_files:}
%endif


%files system-unicore32
%{_bindir}/qemu-system-unicore32
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-system-unicore32*.stp
%endif
%{_mandir}/man1/qemu-system-unicore32.1*


%files system-xtensa
%{_bindir}/qemu-system-xtensa
%{_bindir}/qemu-system-xtensaeb
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-system-xtensa*.stp
%endif
%{_mandir}/man1/qemu-system-xtensa.1*
%{_mandir}/man1/qemu-system-xtensaeb.1*


%files system-moxie
%{_bindir}/qemu-system-moxie
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-system-moxie*.stp
%endif
%{_mandir}/man1/qemu-system-moxie.1*


%files system-aarch64
%{_bindir}/qemu-system-aarch64
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-system-aarch64*.stp
%endif
%{_mandir}/man1/qemu-system-aarch64.1*
%ifarch aarch64
%{?kvm_files:}
%endif


%files system-tricore
%{_bindir}/qemu-system-tricore
%if %have_working_systemtap
%{_datadir}/systemtap/tapset/qemu-system-tricore*.stp
%endif
%{_mandir}/man1/qemu-system-tricore.1*
