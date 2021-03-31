#
# Conditional build:
%bcond_with	nftables	# nftables instead of iptables

Summary:	Connection Manager
Summary(pl.UTF-8):	Zarządca połączeń
Name:		connman
Version:	1.39
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	https://www.kernel.org/pub/linux/network/connman/%{name}-%{version}.tar.xz
# Source0-md5:	b740a8859d1f0473fc76f8f590e4b57a
URL:		https://connman.net/
BuildRequires:	dbus-devel >= 1.4
BuildRequires:	glib2-devel >= 1:2.40
BuildRequires:	gnutls-devel
BuildRequires:	libmnl-devel >= 1.0.0
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel
BuildRequires:	ppp-plugin-devel
BuildRequires:	readline-devel
BuildRequires:	systemd-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with nftables}
BuildRequires:	libnftnl-devel >= 1.0.4
%else
BuildRequires:	iptables-devel >= 1.4.11
%endif
Requires:	dbus >= 1.4
Requires:	glib2 >= 1:2.40
Requires:	libmnl >= 1.0.0
%if %{with nftables}
Requires:	libnftnl >= 1.0.4
%else
Requires:	iptables-libs >= 1.4.11
%endif
Obsoletes:	connman-plugin-wimax < 1.11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libppp-plugin.so.*

%description
The ConnMan project provides a daemon for managing Internet
connections within embedded devices running the Linux operating
system. The Connection Manager is designed to be slim and to use as
few resources as possible, so it can be easily integrated. It is a
fully modular system that can be extended, through plug-ins, to
support all kinds of wired or wireless technologies. Also,
configuration methods, like DHCP and domain name resolving, are
implemented using plug-ins. The plug-in approach allows for easy
adaption and modification for various use cases.

%description -l pl.UTF-8
Projekt ConnMan udostępnia demona do zarządzania połączeniami z
Internetem na urządzeniach wbudowanych z działającym Linuksem jako
systemem operacyjnym. Zarządca połączeń został zaprojektowany jako
lekki i używający jak najmniej zasobów, dzięki czemu może być łatwo
integrowany. Ma w pełni modularny system, który można rozszerzać
poprzez wtyczki, aby obsługiwał wszelkie rodzaje przewodowych i
bezprzewodowych połączeń. Metody konfiguracji, takie jak DHCP czy
rozwiązywanie nazw domenowych, także są implementowane poprzez
wtyczki. Takie podejście do wtyczek pozwala na łatwe adaptowanie i
modyfikowanie pod kątem różnych przypadków użycia.

%package devel
Summary:	Header files for ConnMan plugins
Summary(pl.UTF-8):	Pliki nagłówkowe dla wtyczek ConnMana
Group:		Development/Libraries
# doesn't require base

%description devel
Header files for ConnMan plugins.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla wtyczek ConnMana.

%prep
%setup -q

%build
%configure \
	IPTABLES_SAVE=/usr/sbin/iptables-save \
	PPPD=/usr/sbin/pppd \
	WPASUPPLICANT=/usr/sbin/wpa_supplicant \
	--disable-silent-rules \
	--enable-hh2serial-gps \
	--enable-iospm \
	--enable-iwd \
	--enable-l2tp \
	--enable-nmcompat \
	--enable-openconnect \
	--enable-openvpn \
	--enable-polkit \
	--enable-pptp \
	--enable-tist \
	--enable-vpnc \
	%{?with_nftables:--with-firewall=nftables} \
	--with-l2tp=/usr/sbin/xl2tpd \
	--with-openconnect=/usr/sbin/openconnect \
	--with-openvpn=/usr/sbin/openvpn \
	--with-pptp=/usr/sbin/pptp \
	--with-vpnc=/usr/bin/vpnc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/connman/{plugins,plugins-vpn,scripts}/*.la

install -d $RPM_BUILD_ROOT/var/{lib/connman{,-vpn},run/connman}

install -D src/main.conf $RPM_BUILD_ROOT%{_sysconfdir}/connman/main.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%dir %{_sysconfdir}/connman
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/connman/main.conf
%attr(755,root,root) %{_bindir}/connmanctl
%attr(755,root,root) %{_sbindir}/connman-vpnd
%attr(755,root,root) %{_sbindir}/connmand
%attr(755,root,root) %{_sbindir}/connmand-wait-online
%dir %{_libdir}/connman
%dir %{_libdir}/connman/plugins
%attr(755,root,root) %{_libdir}/connman/plugins/hh2serial-gps.so
%attr(755,root,root) %{_libdir}/connman/plugins/iospm.so
%attr(755,root,root) %{_libdir}/connman/plugins/tist.so
%dir %{_libdir}/connman/plugins-vpn
%attr(755,root,root) %{_libdir}/connman/plugins-vpn/l2tp.so
%attr(755,root,root) %{_libdir}/connman/plugins-vpn/openconnect.so
%attr(755,root,root) %{_libdir}/connman/plugins-vpn/openvpn.so
%attr(755,root,root) %{_libdir}/connman/plugins-vpn/pptp.so
%attr(755,root,root) %{_libdir}/connman/plugins-vpn/vpnc.so
%attr(755,root,root) %{_libdir}/connman/plugins-vpn/wireguard.so
%dir %{_libdir}/connman/scripts
%attr(755,root,root) %{_libdir}/connman/scripts/libppp-plugin.so*
%attr(755,root,root) %{_libdir}/connman/scripts/openvpn-script
%attr(755,root,root) %{_libdir}/connman/scripts/vpn-script
/usr/share/dbus-1/system.d/connman.conf
/usr/share/dbus-1/system.d/connman-nmcompat.conf
/usr/share/dbus-1/system.d/connman-vpn-dbus.conf
/usr/share/dbus-1/system-services/net.connman.vpn.service
/usr/share/polkit-1/actions/net.connman.policy
/usr/share/polkit-1/actions/net.connman.vpn.policy
%{systemdunitdir}/connman.service
%{systemdunitdir}/connman-vpn.service
%{systemdunitdir}/connman-wait-online.service
%{systemdtmpfilesdir}/connman_resolvconf.conf
%dir /var/lib/connman
%dir /var/lib/connman-vpn
%dir /var/run/connman
%{_mandir}/man1/connmanctl.1*
%{_mandir}/man5/connman.conf.5*
%{_mandir}/man5/connman-service.config.5*
%{_mandir}/man5/connman-vpn.conf.5*
%{_mandir}/man5/connman-vpn-provider.config.5*
%{_mandir}/man8/connman.8*
%{_mandir}/man8/connman-vpn.8*

%files devel
%defattr(644,root,root,755)
%doc doc/*.txt
%{_includedir}/connman
%{_pkgconfigdir}/connman.pc
