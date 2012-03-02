%define qemu_name	qemu-kvm
%define qemu_version	1.0
%define qemu_rel	2
#define qemu_snapshot	0
%define qemu_release	%mkrel %{?qemu_snapshot:0.%{qemu_snapshot}.}%{qemu_rel}

Summary:	QEMU CPU Emulator
Name:		qemu
Version:	%{qemu_version}
Release:	%{qemu_release}
Source0:	http://kent.dl.sourceforge.net/sourceforge/kvm/%{qemu_name}-%{version}%{?qemu_snapshot:-%{qemu_snapshot}}.tar.gz
Source1:	kvm.modules
# KSM control scripts
Source4: ksm.init
Source5: ksm.sysconfig
Source6: ksmtuned.init
Source7: ksmtuned
Source8: ksmtuned.conf
# come from fedora package + some custom fix
# to send upstream
Patch1: Fix_save-restore_of_in-kernel_i8259.patch

License:	GPLv2+
URL:		http://wiki.qemu.org/Main_Page
Group:		Emulators
Provides:	kvm
# remove once 2010.0 is EOL
Obsoletes:	kvm < 86
Requires:	qemu-img = %{version}-%{release}
# for %%{_sysconfdir}/sasl2
Requires:	cyrus-sasl
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
%ifarch %{ix86} x86_64
BuildRequires: spice-protocol >= 0.8.1
BuildRequires: spice-server-devel >= 0.9.0
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
%patch1 -p1

%build

extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

%ifarch %{ix86} x86_64
# sdl outputs to alsa or pulseaudio depending on system config, but it's broken (RH bug #495964)
# alsa works, but causes huge CPU load due to bugs
# oss works, but is very problematic because it grabs exclusive control of the device causing other apps to go haywire
./configure \
	--target-list=x86_64-softmmu \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--audio-drv-list=pa,sdl,alsa,oss \
	--enable-spice \
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
%ifarch %{ix86} x86_64
	--enable-spice \
%endif
	--extra-ldflags=$extraldflags \
	--extra-cflags="$CFLAGS"

%make V=1 $buildldflags

%install
rm -rf $RPM_BUILD_ROOT

install -D -p -m 0755 %{SOURCE4} $RPM_BUILD_ROOT%{_initddir}/ksm
install -D -p -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ksm

install -D -p -m 0755 %{SOURCE6} $RPM_BUILD_ROOT%{_initddir}/ksmtuned
install -D -p -m 0755 %{SOURCE7} $RPM_BUILD_ROOT%{_sbindir}/ksmtuned
install -D -p -m 0644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/ksmtuned.conf

%ifarch %{ix86} x86_64
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/modules
mkdir -p $RPM_BUILD_ROOT%{_bindir}/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}

install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/modules/kvm.modules
install -m 0755 kvm/kvm_stat $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 qemu-kvm $RPM_BUILD_ROOT%{_bindir}/
%endif

%makeinstall_std BUILD_DOCS="yes"

install -D -p -m 0644 qemu.sasl $RPM_BUILD_ROOT%{_sysconfdir}/sasl2/qemu.conf

# remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_docdir}/qemu

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
%{_initddir}/ksm
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
%{_initddir}/ksmtuned
%{_sbindir}/ksmtuned
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%{_sysconfdir}/sysconfig/modules/kvm.modules
%{_sysconfdir}/qemu/target-x86_64.conf
%{_bindir}/kvm_stat
%{_bindir}/qemu-io
%{_bindir}/qemu-kvm
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
%{_mandir}/man1/qemu.1*
%{_mandir}/man8/qemu-nbd.8*
%dir %{_datadir}/qemu
%{_datadir}/qemu/*.bin
%{_datadir}/qemu/*.rom
%{_datadir}/qemu/keymaps
%{_datadir}/qemu/openbios-sparc32
%{_datadir}/qemu/openbios-sparc64
%{_datadir}/qemu/openbios-ppc
%{_datadir}/qemu/bamboo.dtb
%{_datadir}/qemu/mpc8544ds.dtb
%{_datadir}/qemu/petalogix-ml605.dtb
%{_datadir}/qemu/petalogix-s3adsp1800.dtb

%files img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*


