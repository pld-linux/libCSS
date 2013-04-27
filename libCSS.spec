# TODO:
# - avoid compilation in the install stage
#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	CSS parser and selection engine
Name:		libCSS
Version:	0.2.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/libcss-%{version}-src.tar.gz
# Source0-md5:	e61700e0dce2a122d65b85dba04c4b40
Patch0:		lib.patch
URL:		http://www.netsurf-browser.org/projects/libcss/
BuildRequires:	libparserutils-devel >= 0.1.2
BuildRequires:	libwapcaplet-devel >= 0.2.0
BuildRequires:	netsurf-buildsystem
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# broken linking
%define	no_install_post_check_so 1

%description
LibCSS is a CSS (Cascading Style Sheet) parser and selection engine,
written in C. It was developed as part of the NetSurf project and is
available for use by other software under the MIT licence. For further
details, see the readme.

Features:
- Parses CSS, good and bad
- Simple C API
- Low memory usage
- Fast selection engine
- Portable
- Shared library

%package devel
Summary:	libCSS library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libCSS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the libraries, include files and other resources you can use
to incorporate libCSS into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libCSS w swoich
programach.

%package static
Summary:	libCSS static libraries
Summary(pl.UTF-8):	Statyczne biblioteki libCSS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libCSS libraries.

%description static -l pl.UTF-8
Statyczna biblioteka libCSS.

%prep
%setup -q -n libcss-%{version}
%patch0 -p1

%build
%{__make} PREFIX=%{_prefix} COMPONENT_TYPE=lib-shared Q='' \
	CFLAGS="%{rpmcflags} -Iinclude -Isrc" LDFLAGS="%{rpmldflags}"
%if %{with static_libs}
%{__make} PREFIX=%{_prefix} COMPONENT_TYPE=lib-static Q='' \
	CFLAGS="%{rpmcflags} -Iinclude -Isrc" LDFLAGS="%{rpmldflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -j1 install Q='' \
	lib=%{_lib} \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -j1 install Q='' \
	lib=%{_lib} \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/libcss
%{_pkgconfigdir}/*pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
