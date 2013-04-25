%define qemu_name	qemu
%define qemu_version	1.2.0
%define qemu_rel	8
#define qemu_snapshot	0
%define qemu_release	%mkrel %{?qemu_snapshot:0.%{qemu_snapshot}.}%{qemu_rel}

Summary:	QEMU CPU Emulator
Name:		qemu
Version:	%{qemu_version}
Release:	%{qemu_release}
Source0:	http://kent.dl.sourceforge.net/sourceforge/kvm/%{qemu_name}-%{version}%{?qemu_snapshot:-%{qemu_snapshot}}.tar.bz2
Source1:	kvm.modules
# KSM control scripts
Source4:	ksm.service
Source5:	ksm.sysconfig
Source6:	ksmtuned.service
Source7:	ksmtuned
Source8:	ksmtuned.conf
Source9:	ksmctl.c
# (cjw) fix qemu crashing on guest X11 login when vmvga + spice is used
#       caused by negative screen coordinates or width/height
#       from ubuntu (for vnc) + stricter check
Patch1:		fix-vmware-vga-negative-vals.patch

# fix CVE-2012-6075 (from upstream via debian)
Patch2:		qemu-e1000-discard-packets-that-are-too-long-if-not-SBP-and-not-LPE.patch
Patch3:		qemu-e1000-discard-oversized-packets-based-on-SBP_LPE.patch

Patch4:		qemu-1.2.0-link-rt.patch

# Patch from fedora, fixes CVE-2013-1922
Patch5:		qemu-1.2.0-CVE-2013-1922.patch

License:	GPLv2+
URL:		http://wiki.qemu.org/Main_Page
Group:		Emulators
Provides:	kvm
# remove once 2010.0 is EOL
Obsoletes:	kvm < 86
Requires:	qemu-img = %{version}-%{release}
# for %%{_sysconfdir}/sasl2
Requires:	cyrus-sasl
BuildRequires:	libtool
BuildRequires:	libSDL-devel
BuildRequires:	texi2html
BuildRequires:	e2fsprogs-devel
BuildRequires:	kernel-headers	
BuildRequires:	pulseaudio-devel
BuildRequires:	zlib-devel
BuildRequires:	brlapi-devel
BuildRequires:	gnutls-devel
BuildRequires:	libsasl2-devel
BuildRequires:	pciutils-devel
BuildRequires:	texinfo
BuildRequires:	vde-devel
BuildRequires:	bluez-devel
BuildRequires:	curl-devel
BuildRequires:	pkgconfig(libusbredirparser) >= 0.3.4
BuildRequires:	libuuid-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	libaio-devel
BuildRequires:	cap-ng-devel
# for virtfs
BuildRequires:	cap-devel
BuildRequires:	attr-devel
# for direct xfs access with raw device
BuildRequires:  libxfs-devel

%ifarch %{ix86} x86_64
BuildRequires: spice-protocol >= 0.8.1
BuildRequires: spice-server-devel >= 0.9.0
BuildRequires: xen-devel >= 4.1.2
%endif

BuildRequires:	dev86
BuildRequires:	iasl
ExclusiveArch:	%{ix86} ppc x86_64 amd64 %{sunsparc}

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
%setup -q -n %{qemu_name}-%{qemu_version}%{?qemu_snapshot:-%{qemu_snapshot}}
%patch1 -p1 -b .vmware-abort
%patch2 -p1 -b .CVE-2012-6075-1
%patch3 -p1 -b .CVE-2012-6075-2
%patch4 -p1 -b .link-rt
%patch5 -p1 -b .CVE-2013-1922

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
	--disable-kvm \
    --enable-mixemu \
	--extra-ldflags=$extraldflags \
	--extra-cflags="$CFLAGS"

%make V=1 $buildldflags
cp -a x86_64-softmmu/qemu-system-x86_64 qemu-xen
make clean

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
	--disable-xen \
    --enable-mixemu \
	--extra-ldflags=$extraldflags \
	--extra-cflags="$CFLAGS"

%make V=1 $buildldflags
cp -a x86_64-softmmu/qemu-system-x86_64 qemu-kvm
make clean

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
rm -rf $RPM_BUILD_ROOT

install -D -p -m 0644 %{SOURCE4} $RPM_BUILD_ROOT%{_unitdir}/ksm.service
install -D -p -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ksm
install -D -p -m 0755 ksmctl $RPM_BUILD_ROOT/lib/systemd/ksmctl

install -D -p -m 0644 %{SOURCE6} $RPM_BUILD_ROOT%{_unitdir}/ksmtuned.service
install -D -p -m 0755 %{SOURCE7} $RPM_BUILD_ROOT%{_sbindir}/ksmtuned
install -D -p -m 0644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/ksmtuned.conf

%ifarch %{ix86} x86_64
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/modules
mkdir -p $RPM_BUILD_ROOT%{_bindir}/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}

install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/modules/kvm.modules
install -m 0755 qemu-kvm $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 qemu-xen $RPM_BUILD_ROOT%{_bindir}/
%endif

%makeinstall_std BUILD_DOCS="yes"

install -D -p -m 0644 qemu.sasl $RPM_BUILD_ROOT%{_sysconfdir}/sasl2/qemu.conf

# remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_docdir}/qemu %{buildroot}%{_bindir}/vscclient

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
%{_datadir}/qemu/*.bin
%{_datadir}/qemu/*.rom
%{_datadir}/qemu/cpus-*.conf
%{_datadir}/qemu/keymaps
%{_datadir}/qemu/openbios-sparc32
%{_datadir}/qemu/openbios-sparc64
%{_datadir}/qemu/openbios-ppc
%{_datadir}/qemu/*.dtb
%{_datadir}/qemu/palcode-clipper
%{_datadir}/qemu/qemu-icon.bmp
/usr/libexec/qemu-bridge-helper

%files img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*


