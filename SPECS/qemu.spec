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

%define qemu_rel	1
# Release candidate version tracking
%global rcver	rc3
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
# guest agent service
Source10: qemu-guest-agent.service
# guest agent udev rules
Source11: 99-qemu-guest-agent.rules
# qemu-kvm back compat wrapper installed as /usr/bin/qemu-kvm
Source13: qemu-kvm.sh

# Adjust spice gl version check to expect F24 backported version
# Not for upstream, f24 only
Patch0001: 0001-spice-F24-spice-has-backported-gl-support.patch


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
# We need both because the 'stap' binary is probed for by configure
BuildRequires: systemtap
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
# memdev hostmem backend added in 2.1
%ifarch %{ix86} x86_64 aarch64
BuildRequires: numactl-devel
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

Requires: seavgabios-bin
# virtio-blk booting is broken for Windows guests
# if you mix seabios 1.7.4 and qemu 2.1.x
Requires: seabios-bin >= 1.7.5
Requires: sgabios-bin
Requires: ipxe-roms-qemu
Recommends: openbios
Recommends: slof
%ifarch %{ix86} x86_64
Recommends: edk2-ovmf-arm edk2-ovmf-aarch64
%endif
%ifarch %{arm}
Recommends: edk2-ovmf-ia32 edk2-ovmf-x64
%endif

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
Group: System Environment/Daemons
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

%global _udevdir /lib/udev/rules.d

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
%endif

%make_install BUILD_DOCS="yes"

# Install qemu-guest-agent service and udev rules
install -m 0644 %{_sourcedir}/qemu-guest-agent.service %{buildroot}%{_unitdir}
install -m 0644 %{_sourcedir}/99-qemu-guest-agent.rules %{buildroot}%{_udevdir}

%find_lang %{name}

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


%post guest-agent
%systemd_post qemu-guest-agent.service
%preun guest-agent
%systemd_preun qemu-guest-agent.service
%postun guest-agent
%systemd_postun_with_restart qemu-guest-agent.service


%files -f %{name}.lang
%doc README qemu-doc.html qemu-tech.html
%config(noreplace)%{_sysconfdir}/sasl2/qemu.conf
%{_bindir}/qemu-aarch64
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm*
%{_bindir}/qemu-cris
%{_bindir}/qemu-i386
%if 0%{?need_qemu_kvm}
%{_bindir}/qemu-kvm
%{_mandir}/man1/qemu-kvm.1*
%endif
%{_bindir}/qemu-m68k
%{_bindir}/qemu-mips*
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
%{_mandir}/man1/virtfs-proxy-helper.*
%dir %{_datadir}/qemu
%{_datadir}/qemu/*.aml
%{_datadir}/qemu/*.bin
%{_datadir}/qemu/*.img
%{_datadir}/qemu/*.rom
%{_datadir}/qemu/u-boot.e500
%{_datadir}/qemu/keymaps
%{_datadir}/qemu/*.dtb
%{_datadir}/qemu/palcode-clipper
%{_datadir}/qemu/qemu-icon.bmp
%{_datadir}/qemu/trace-events
%{_datadir}/qemu/*.svg
/usr/libexec/qemu-bridge-helper

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
