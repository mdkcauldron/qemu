%define qemu_rel	1
%define qemu_snapshot	rc2
%define qemu_snapshot_prefix 0

%define qemu_release	%mkrel %{?qemu_snapshot:%{qemu_snapshot_prefix}.%{qemu_snapshot}.}%{qemu_rel}
%define qemu_pkgver     qemu-%{version}%{?qemu_snapshot:-%{qemu_snapshot}}

%ifarch %{ix86}
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%endif
%ifarch x86_64
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%endif

# Xen is available only on i386 x86_64 (from libvirt spec)
%ifarch %{ix86} x86_64
%global have_xen 1
%endif

Summary:	QEMU CPU Emulator
Name:		qemu
Version:	2.6.0
Release:	%{qemu_release}
Source0:	http://wiki.qemu-project.org/download/qemu-%{version}%{?qemu_snapshot:-%{qemu_snapshot}}.tar.bz2
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
%ifarch %{ix86} x86_64
Provides:	kvm
%endif
Requires:	qemu-img = %{version}-%{release}
# for %%{_sysconfdir}/sasl2
Requires:	cyrus-sasl
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	texi2html
BuildRequires:	e2fsprogs-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	SDL2-devel
BuildRequires:	zlib-devel
BuildRequires:	gnutls-devel
BuildRequires:	libsasl-devel
BuildRequires:	vde-devel
BuildRequires:	libtool
BuildRequires:	libaio-devel
BuildRequires:	pciutils-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	cap-ng-devel
BuildRequires:	libattr-devel
# for direct xfs access with raw device
BuildRequires:  libxfs-devel
# USB features
BuildRequires: usbredir-devel >= 0.5.
BuildRequires:	pkgconfig(libusbredirparser-0.5) >= 0.6
%ifarch %{ix86} x86_64
BuildRequires:	dev86
%endif
BuildRequires: texinfo
# For /usr/bin/pod2man
BuildRequires: perl
BuildRequires: spice-protocol >= 0.12.2
BuildRequires: spice-server-devel >= 0.12.0
# For network block driver
BuildRequires: libcurl-devel
# For VNC PNG support
BuildRequires: libpng-devel
# For uuid generation
BuildRequires: libuuid-devel
# For BlueZ device support
BuildRequires: bluez-devel
# For Braille device support
BuildRequires: brlapi-devel
# For virtfs
BuildRequires: libcap-devel
# Hard requirement for version >= 1.3
BuildRequires: pixman-devel
# Needed for usb passthrough for qemu >= 1.5
BuildRequires: libusbx-devel
# GTK frontend
BuildRequires: gtk3-devel
BuildRequires: vte3-devel
BuildRequires:	kernel-headers	
# For acpi compilation
BuildRequires:	iasl
# Xen support
%if 0%{?have_xen:1}
BuildRequires:	xen-devel
%endif
# Added in qemu 2.3
BuildRequires: bzip2-devel
# Added in qemu 2.4 for opengl bits
BuildRequires: libepoxy-devel
# For 2.5 TLS test suite
BuildRequires: libtasn1-devel
# libcacard is it's own project as of qemu 2.5
BuildRequires: libcacard-devel >= 2.5.0
# virgl 3d support
BuildRequires: virglrenderer-devel
# Needed explicitly for qemu 2.6 GL support
BuildRequires: pkgconfig(gbm)

# Security fixes

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

%description img
This package contains the QEMU disk image utility that is used to
create, commit, convert and get information from a disk image.


%prep
%setup -q -n %{qemu_pkgver}
%autopatch -p1


%build
# --build-id option is used for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

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
	--libdir=%{_libdir} \
	--sysconfdir=%{_sysconfdir} \
	--interp-prefix=%{_prefix}/qemu-%%M \
	--extra-ldflags=$extraldflags \
	--extra-cflags="%{optflags}" \
	--audio-drv-list=pa,sdl,alsa,oss \
	--enable-kvm \
	--with-sdlabi="2.0" \
	--with-gtkabi="3.0" \

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
%endif

%make_install BUILD_DOCS="yes"

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
#{_sysconfdir}/qemu/target-x86_64.conf
%{_bindir}/ivshmem-client
%{_bindir}/ivshmem-server
%{_bindir}/qemu-io
%ifarch %{ix86} x86_64
%{_sysconfdir}/sysconfig/modules/kvm.modules
%endif
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
%{_mandir}/man8/qemu-ga.8*
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
%{_datadir}/qemu/trace-events
%{_datadir}/qemu/*.svg
/usr/libexec/qemu-bridge-helper

%files img
%{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*
