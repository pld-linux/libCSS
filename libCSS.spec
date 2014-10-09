#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	CSS parser and selection engine
Summary(pl.UTF-8):	Silnik analizujący i wybierający CSS
Name:		libCSS
Version:	0.3.0
Release:	2
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/libcss-%{version}-src.tar.gz
# Source0-md5:	f4bf855bab90ef5225dbeeb7d97c514c
Patch0:		%{name}-build.patch
URL:		http://www.netsurf-browser.org/projects/libcss/
BuildRequires:	libparserutils-devel >= 0.2.0
BuildRequires:	libwapcaplet-devel >= 0.2.1
BuildRequires:	netsurf-buildsystem >= 1.1
Requires:	libparserutils >= 0.2.0
Requires:	libwapcaplet >= 0.2.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibCSS is a CSS (Cascading Style Sheet) parser and selection engine,
written in C. It was developed as part of the NetSurf project and is
available for use by other software under the MIT licence.

Features:
- Parses CSS, good and bad
- Simple C API
- Low memory usage
- Fast selection engine
- Portable
- Shared library

%description -l pl.UTF-8
LibCSS to silnik analizujący i wybierający CSS (Cascading Style
Sheet), napisany w C. Powstał jako część projektu NetSurf i można go
używać w innych programach na licencji MIT. 

Cechy:
- analizuje CSS, dobry i wadliwy
- proste API dla języka C
- małe zużycie pamięci
- szybki silnik wybierający
- przenośność
- biblioteka współdzielona

%package devel
Summary:	libCSS library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libCSS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libparserutils-devel >= 0.2.0
Requires:	libwapcaplet-devel >= 0.2.1

%description devel
This package contains the include files and other resources you can
use to incorporate libCSS into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libCSS w swoich
programach.

%package static
Summary:	libCSS static library
Summary(pl.UTF-8):	Statyczna biblioteka libCSS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libCSS library.

%description static -l pl.UTF-8
Statyczna biblioteka libCSS.

%prep
%setup -q -n libcss-%{version}
%patch0 -p1

# create "gen" target just to execute PRE_TARGETS
printf '\ngen: $(PRE_TARGETS)\n' >> Makefile

%define	comps	lib-shared %{?with_static_libs:lib-static}

%build
export CC="%{__cc}"
export CFLAGS="%{rpmcflags} %{rpmcppflags}"
export LDFLAGS="%{rpmldflags}"

# generate sources first to avoid recompilation on install when sources
# get regenerated during build for second component type
for c in %{comps} ; do
%{__make} gen \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=$c
done

for c in %{comps} ; do
%{__make} \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=$c
done

%install
rm -rf $RPM_BUILD_ROOT

for c in %{comps} ; do
%{__make} -j1 install \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=$c \
	DESTDIR=$RPM_BUILD_ROOT
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %{_libdir}/libcss.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcss.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcss.so
%{_includedir}/libcss
%{_pkgconfigdir}/libcss.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcss.a
%endif
