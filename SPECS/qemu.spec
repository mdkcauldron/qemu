%ifarch %{ix86}
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%endif
%ifarch x86_64
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
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

%define qemu_rel	3
%global rcver	rc2
%if 0%{?rcver:1}
%global rcstr -%{rcver}
%endif

Summary:	QEMU is a FAST! processor emulator
Name:		qemu
Version:	2.6.0
Release:	%mkrel %{?rcver:0.%{rcver}.}%{qemu_rel}
License:	GPLv2+ and LGPLv2+ and BSD
Group:		Emulators
URL:		http://www.qemu.org/

Source0:	http://wiki.qemu-project.org/download/%{name}-%{version}%{?rcstr}.tar.bz2
# KSM control scripts
Source4:	ksm.service
Source5:	ksm.sysconfig
Source6:	ksmctl.c
Source7:	ksmtuned.service
Source8:	ksmtuned
Source9:	ksmtuned.conf
# qemu-kvm back compat wrapper installed as /usr/bin/qemu-kvm
Source13: qemu-kvm.sh
# Mageia stuff:
Source100:	kvm.modules

%ifarch %{ix86} x86_64
Provides:	kvm
%endif
Requires:	qemu-img = %{version}-%{release}
# for %%{_sysconfdir}/sasl2
Requires:	cyrus-sasl
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
BuildRequires: libiscsi-devel
BuildRequires: libnfs-devel
BuildRequires: snappy-devel
BuildRequires:	lzo-devel
BuildRequires:	ncurses-devel
BuildRequires:	libattr-devel
# for direct xfs access with raw device
BuildRequires:  libxfs-devel
# USB features
BuildRequires: usbredir-devel >= 0.5.
BuildRequires:	pkgconfig(libusbredirparser-0.5) >= 0.6
BuildRequires: gperftools-devel
BuildRequires: texinfo
# For /usr/bin/pod2man
BuildRequires: perl
%if 0%{?have_spice:1}
BuildRequires: spice-protocol >= 0.12.2
BuildRequires: spice-server-devel >= 0.12.0
%endif
%if 0%{?have_seccomp:1}
BuildRequires: libseccomp-devel >= 2.3.0
%endif
# For network block driver
BuildRequires: libcurl-devel
# For smartcard NSS support
BuildRequires: nss-devel
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
# For virtfs
BuildRequires: libcap-devel
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
BuildRequires: vte3-devel
# GTK translations
BuildRequires: gettext
# RDMA migration
BuildRequires: librdmacm-devel
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
BuildRequires: libegl-devel

# Security fixes

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

%package img
Summary:	QEMU command line tool for manipulating disk images
Group:		Emulators

%description img
This package provides a command line tool for manipulating disk images


%prep
%setup -q -n qemu-%{version}%{?rcstr}
%autopatch -p1


%build
# --build-id option is used for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

    buildarch="i386-softmmu x86_64-softmmu aarch64-linux-user arm-softmmu \
cris-softmmu m68k-softmmu mips-softmmu mipsel-softmmu mips64-softmmu \
mips64el-softmmu ppc-softmmu ppcemb-softmmu ppc64-softmmu \
sh4-softmmu sh4eb-softmmu sparc-softmmu \
i386-linux-user x86_64-linux-user aarch64-linux-user alpha-linux-user \
arm-linux-user armeb-linux-user cris-linux-user m68k-linux-user \
mips-linux-user \
mipsel-linux-user ppc-linux-user ppc64-linux-user \
ppc64abi32-linux-user sh4-linux-user sh4eb-linux-user \
sparc-linux-user sparc64-linux-user sparc32plus-linux-user \
aarch64-softmmu"

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
	--extra-ldflags=$extraldflags \
	--extra-cflags="%{optflags}" \
	--target-list="$buildarch" \
	--audio-drv-list=pa,sdl,alsa,oss \
	--enable-kvm \
	%{tcmallocflag} \
	%{spiceflag} \
	--with-sdlabi="2.0" \
	--with-gtkabi="3.0" \

%make V=1 $buildldflags

gcc %{_sourcedir}/ksmctl.c -O2 -g -o ksmctl


%install

mkdir -p %{buildroot}%{_udevdir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/qemu

install -D -p -m 0644 %{_sourcedir}/ksm.service %{buildroot}%{_unitdir}
install -D -p -m 0644 %{_sourcedir}/ksm.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/ksm
install -D -p -m 0755 ksmctl %{buildroot}%{_libexecdir}/ksmctl
install -D -p -m 0644 %{_sourcedir}/ksmtuned.service %{buildroot}%{_unitdir}
install -D -p -m 0755 %{_sourcedir}/ksmtuned %{buildroot}%{_sbindir}/ksmtuned
install -D -p -m 0644 %{_sourcedir}/ksmtuned.conf %{buildroot}%{_sysconfdir}/ksmtuned.conf

%ifarch %{ix86} x86_64
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig/modules
mkdir -p %{buildroot}/%{_bindir}/
mkdir -p %{buildroot}/%{_datadir}/%{name}

install -m 0755 %{SOURCE100} %{buildroot}/%{_sysconfdir}/sysconfig/modules/kvm.modules
%endif

%make_install BUILD_DOCS="yes"

%find_lang %{name}

%if 0%{?need_qemu_kvm}
install -m 0755 %{_sourcedir}/qemu-kvm.sh %{buildroot}%{_bindir}/qemu-kvm
ln -sf qemu.1.xz %{buildroot}%{_mandir}/man1/qemu-kvm.1.xz
%endif

install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/qemu.conf

# remove unpackaged files
rm -rf %{buildroot}/%{_docdir}/qemu %{buildroot}%{_bindir}/vscclient
rm -f %{buildroot}/%{_libdir}/libcacard*
rm -f %{buildroot}/usr/lib/libcacard*
rm -f %{buildroot}/%{_libdir}/pkgconfig/libcacard.pc
rm -f %{buildroot}/usr/lib/pkgconfig/libcacard.pc
rm -rf %{buildroot}/%{_includedir}/cacard

%post 
%_post_service ksmtuned
%_post_service ksm

%preun
%_preun_service ksm
%_preun_service ksmtuned



%files -f %{name}.lang
%doc README qemu-doc.html qemu-tech.html
%config(noreplace)%{_sysconfdir}/sasl2/qemu.conf
%{_libexecdir}/ksmctl
%{_sbindir}/ksmtuned
%{_unitdir}/ksmtuned.service
%{_unitdir}/ksm.service
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
%{_bindir}/ivshmem-client
%{_bindir}/ivshmem-server
%{_bindir}/qemu-io
%ifarch %{ix86} x86_64
%{_sysconfdir}/sysconfig/modules/kvm.modules
%endif
%{_bindir}/qemu-aarch64
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm*
%{_bindir}/qemu-cris
%{_bindir}/qemu-ga
%{_bindir}/qemu-i386
%if 0%{?need_qemu_kvm}
%{_bindir}/qemu-kvm
%{_mandir}/man1/qemu-kvm.1*
%endif
%{_bindir}/qemu-m68k
%{_bindir}/qemu-mips*
%{_bindir}/qemu-nbd
%{_bindir}/qemu-ppc*
%{_bindir}/qemu-sh4*
%{_bindir}/qemu-sparc*
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-system-aarch64
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
