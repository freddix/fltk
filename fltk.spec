Summary:	Fast Light Tool Kit
Name:		fltk
Version:	1.3.2
Release:	1
License:	LGPL with amendments (see COPYING)
Group:		X11/Libraries
Source0:	http://fltk.org/pub/fltk/%{version}/%{name}-%{version}-source.tar.gz
# Source0-md5:	9f7e707d4fb7a5a76f0f9b73ff70623d
Patch0:		%{name}-link.patch
Patch1:		%{name}-as-needed.patch
URL:		http://www.fltk.org/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	autoconf
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.315
BuildRequires:	xorg-libX11-devel
BuildRequires:	xorg-libXext-devel
BuildRequires:	xorg-libXft-devel
BuildRequires:	xorg-util-makedepend
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1

# don't propagate strip-flags to fltk-config.
%define		filterout_ld	(-Wl,)?-[sS] (-Wl,)?--strip.*

%description
The Fast Light Tool Kit ("FLTK", pronounced "fulltick") is a LGPL'd
C++ graphical user interface toolkit for X (UNIX(r)), OpenGL(r), and
Microsoft(r) Windows(r) NT 4.0, 95, or 98. It was originally developed
by Mr. Bill Spitzak and is currently maintained by a small group of
developers across the world with a central repository in the US.

%package devel
Summary:	FLTK development files
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
FLTK development files.

%package gl
Summary:	FLTK GL library
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	OpenGL

%description gl
FLTK GL library.

%package gl-devel
Summary:	Header files for FLTK GL library
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-gl = %{version}-%{release}

%description gl-devel
Header files for FLTK GL library.

%package games
Summary:	FLTK Games
Group:		X11/Applications/Games
Requires:	%{name} = %{version}-%{release}

%description games
FLTK games: Block Attack!, Checkers, or Sudoku on your computer.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__autoconf}
%configure \
	--enable-largefile		\
	--enable-shared			\
	--enable-threads		\
	--enable-xft			\
	--enable-xinerama		\
	--with-optim="%{rpmcxxflags}"	\
	--with-x
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	install-desktop \
	DESTDIR=$RPM_BUILD_ROOT

# less generic games' names
for f in blocks checkers sudoku ; do
mv -f $RPM_BUILD_ROOT%{_bindir}/{,fltk-}${f}
mv -f $RPM_BUILD_ROOT%{_mandir}/man6/{,fltk-}${f}.6
done

# add link to documentation for fluid help;
# remove /usr/share/doc/fltk contents - it is installed during make install
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}
ln -sf %{name}-devel-%{version} $RPM_BUILD_ROOT%{_datadir}/doc/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
# note: COPYING contains amendments to LGPL, so don't remove!
%doc CHANGES COPYING CREDITS README
%attr(755,root,root) %{_libdir}/libfltk.so.*.*
%attr(755,root,root) %{_libdir}/libfltk_forms.so.*.*
%attr(755,root,root) %{_libdir}/libfltk_images.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/fltk-config
%attr(755,root,root) %{_bindir}/fluid
%attr(755,root,root) %{_libdir}/libfltk.so
%attr(755,root,root) %{_libdir}/libfltk_forms.so
%attr(755,root,root) %{_libdir}/libfltk_images.so
%{_includedir}/FL
%exclude %{_includedir}/FL/Fl_Gl_Window.*
%exclude %{_includedir}/FL/gl*
%{_mandir}/man1/fltk-config.1*
%{_mandir}/man1/fluid.1*
%{_mandir}/man3/fltk.3*

%files gl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfltk_gl.so.*.*

%files gl-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfltk_gl.so
%{_includedir}/FL/Fl_Gl_Window.*
%{_includedir}/FL/gl*

%files games
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}-blocks
%attr(755,root,root) %{_bindir}/%{name}-checkers
%attr(755,root,root) %{_bindir}/%{name}-sudoku
%{_iconsdir}/*/*/*/blocks.png
%{_iconsdir}/*/*/*/checkers.png
%{_iconsdir}/*/*/*/sudoku.png
%{_desktopdir}/blocks.desktop
%{_desktopdir}/checkers.desktop
%{_desktopdir}/sudoku.desktop
%{_mandir}/man6/%{name}-blocks.6*
%{_mandir}/man6/%{name}-checkers.6*
%{_mandir}/man6/%{name}-sudoku.6*

