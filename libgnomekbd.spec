Name:           libgnomekbd
Version:        2.28.2
Release:        2%{?dist}
Summary:        A keyboard configuration library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://gswitchit.sourceforge.net
Source0:        http://download.gnome.org/sources/libgnomekbd/2.28/libgnomekbd-%{version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  dbus-devel >= 0.92
BuildRequires:  dbus-glib >= 0.34
BuildRequires:  GConf2-devel >= 2.14.0
BuildRequires:  gtk2-devel >= 2.10.3
BuildRequires:  cairo-devel
BuildRequires:  libglade2-devel >= 2.6.0
BuildRequires:  libgnome-devel >= 2.16.0
BuildRequires:  libgnomeui-devel >= 2.16.0
BuildRequires:  libxklavier-devel >= 3.4
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  intltool

Requires(pre): GConf2
Requires(post): GConf2
Requires(preun): GConf2

# updated translations
# https://bugzilla.redhat.com/show_bug.cgi?id=589219
Patch0: libgnomekbd-translations.patch

%description
The libgnomekbd package contains a GNOME library which manages
keyboard configuration and offers various widgets related to
keyboard configuration.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libxklavier-devel >= 2.91
Requires:       libgnome-devel >= 2.16.0
Requires:       pkgconfig


%description    devel
The libgnomekbd-devel package contains libraries and header files for
developing applications that use libgnomekbd.


%package        capplet
Summary:        A configuration applet to select libgnomekbd plugins
Group:          User Interface/Desktops
Requires:       %{name} = %{version}-%{release}

%description    capplet
The libgnomekbd-capplet package contains a configuration applet to
select libgnomekbd plugins. These plugins can modify the appearance
of the keyboard indicator applet.

%prep
%setup -q
%patch0 -p1 -b .translations

%build
%configure --disable-static --enable-compile-warnings=no
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

desktop-file-install --vendor gnome --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  $RPM_BUILD_ROOT%{_datadir}/applications/gkbd-indicator-plugins-capplet.desktop

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/desktop_gnome_peripherals_keyboard_xkb.schemas >& /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :


%pre
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/desktop_gnome_peripherals_keyboard_xkb.schemas >& /dev/null || :
fi


%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/desktop_gnome_peripherals_keyboard_xkb.schemas >& /dev/null || :
fi


%postun
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LIB
%{_libdir}/*.so.*
%{_sysconfdir}/gconf/schemas/*
%{_datadir}/libgnomekbd

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files capplet
%defattr(-,root,root,-)
%{_bindir}/gkbd-indicator-plugins-capplet
%{_datadir}/applications/gnome-gkbd-indicator-plugins-capplet.desktop


%changelog
* Mon May 24 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.2-2
- Updated translations
Resolves: #589219

* Wed Dec 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.2-1
- Update to 2.28.2
- See http://download.gnome.org/sources/libgnomekbd/2.28/libgnomekbd-2.28.2.news

* Thu Dec 03 2009 Bastien Nocera <bnocera@redhat.com> 2.28.0-4
- Remove debug in patch

* Thu Dec  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-3
- Small spec fixes

* Thu Oct  8 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-2
- Incorporate visual fixes from upstream

* Wed Sep 23 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Tue Aug 25 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91-1
- Update to 2.27.91

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.4-1
- Update to 2.27.4

* Tue Jun 30 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.2-3
- Rebuild against new libxklavier
- Adapt to api changes

* Sun May 31 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.2-1
- Update to 2.27.2

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Thu Sep  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Fri Aug 29 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2-2
- Plug a small memory leak

* Sun May 11 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2-1
- Update to 2.23.2

* Sun Apr  6 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-2
- Split the plugins capplet off into a subpackage, since we don't
  have any plugins and don't want the capplet by default

* Thu Mar 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Thu Jan 31 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.4.1-2
- Rebuild against new libxklavier

* Tue Dec 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.4.1-1
- Update to 2.21.4.1

* Thu Dec 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.4-1
- Update to 2.21.4

* Tue Nov 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.1-1
- Update to 2.21.1

* Tue Oct 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-2
- Rebuild against new dbus-glib

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Mon Sep  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.91-1
- Update to 2.19.91

* Mon Aug 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.90-2
- Fix a bad free

* Sun Aug 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.90-1
- Update to 2.19.90 

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.2-2
- Update the license field

* Sun May 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.2-1
- Update to 2.18.2

* Sun May 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.1-1
- Update to 2.18.1

* Wed Apr  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-2
- Fix a typo in URL

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Wed Jan 24 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.2-2
- Port former control-center patches to improve keyboard drawing

* Tue Nov  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2

* Tue Nov  7 2006 Matthias Clasen <mclasen@redhat.com> - 0.1-4
- Fix up Requires

* Thu Nov  2 2006 Matthias Clasen <mclasen@redhat.com> - 0.1-3
- Don't use --Werror

* Sat Oct 28 2006 Matthias Clasen <mclasen@redhat.com> - 0.1-2
- Fix a memory allocation error

* Sat Oct 28 2006 Matthias Clasen <mclasen@redhat.com> - 0.1-1
- Initial release
