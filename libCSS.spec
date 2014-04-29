# TODO:
# - avoid compilation in the install stage
#
# Conditional build:
%bcond_without	static_libs	# don't build static library

Summary:	CSS parser and selection engine
Name:		libCSS
Version:	0.3.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/libcss-%{version}-src.tar.gz
# Source0-md5:	f4bf855bab90ef5225dbeeb7d97c514c
#Patch0:		lib.patch
URL:		http://www.netsurf-browser.org/projects/libcss/
BuildRequires:	libparserutils-devel >= 0.2.0
BuildRequires:	libwapcaplet-devel >= 0.2.1
BuildRequires:	netsurf-buildsystem >= 1.1
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
#%%patch0 -p1

%build
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} Q= \
	CC="%{__cc}" \
	PREFIX=%{_prefix}  \
	COMPONENT_TYPE=lib-shared

%if %{with static_libs}
%{__make} Q= \
	CC="%{__cc}" \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -j1 install Q= \
	lib=%{_lib} \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -j1 install Q= \
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
%attr(755,root,root) %{_libdir}/libcss.so.*.*.*
%ghost %{_libdir}/libcss.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcss.so
%{_includedir}/libcss
%{_pkgconfigdir}/libcss.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcss.a
%endif

