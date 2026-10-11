#
# Conditional build:
%bcond_without	apidocs		# Doxygen API documentation
%bcond_without	static_libs	# static library
%bcond_with	tests		# test suite

%if %{without static_libs}
# tests rely on static libs (internal symbols)
%undefine	with_tests
%endif
Summary:	The companion C library for client side encryption in drivers
Summary(pl.UTF-8):	Biblioteka towarzysząca C do szyfrowania w sterownikach po stronie klienta
Name:		libmongocrypt
# 1.16+ require libbson2
Version:	1.15.2
Release:	1
# see kms-message/THIRD_PARTY_NOTICES
# kms-message/src/kms_b64.c is ISC
# everything else is Apache v2.0
License:	Apache v2.0 and ISC
Group:		Libraries
#Source0Download: https://github.com/mongodb/libmongocrypt/releases
Source0:	https://github.com/mongodb/libmongocrypt/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4b5235a225256bebcf8cde2e1f5c0c5b
Patch0:		no-Werror.patch
Patch1:		%{name}-types.patch
Patch2:		%{name}-tests.patch
URL:		https://github.com/mongodb/libmongocrypt
BuildRequires:	cmake >= 3.15
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libbson-devel >= 1.30
%{?with_static_libs:BuildRequires:	libbson-static >= 1.30}
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The companion C library for client side encryption in drivers.

%description -l pl.UTF-8
Biblioteka towarzysząca C do szyfrowania w sterownikach po stronie
klienta.

%package devel
Summary:	Header files for libmongocrypt library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libmongocrypt
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libbson-devel >= 1.30

%description devel
This package contains the header files and other development files for
libmongocrypt library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe i inne pliki programistyczne
biblioteki libmongocrypt.

%package static
Summary:	Static libmongocrypt libraries
Summary(pl.UTF-8):	Statyczne biblioteki libmongocrypt
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Requires:	libbson-static >= 1.30
Requires:	openssl-devel

%description static
Static libmongocrypt libraries.

%description static -l pl.UTF-8
Statyczne biblioteki libmongocrypt.

%package apidocs
Summary:	API documentation for libmongocrypt library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libmongocrypt
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libmongocrypt library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libmongocrypt.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
echo "%{version}" > VERSION_CURRENT

%build
# .pc file generation expects relative CMAKE_INSTALL_{INSTALL,LIB}DIR
%cmake -B build \
	%{!?with_tests:-DBUILD_TESTING:BOOL=OFF} \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DENABLE_ONLINE_TESTS:BOOL=OFF \
	%{!?with_static_libs:-DENABLE_STATIC:BOOL=OFF} \
	-DMONGOCRYPT_MONGOC_DIR:STRING="USE-SYSTEM" \
	-DUSE_SHARED_LIBBSON:BOOL=ON

%{__make} -C build

%if %{with tests}
%{__make} -C build test
%endif

%if %{with apidocs}
doxygen doc/Doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%{_libdir}/libkms_message.so.*.*.*
%ghost %{_libdir}/libkms_message.so.0
%{_libdir}/libmongocrypt.so.*.*.*
%ghost %{_libdir}/libmongocrypt.so.0

%files devel
%defattr(644,root,root,755)
%doc integrating.md
%{_libdir}/libkms_message.so
%{_libdir}/libmongocrypt.so
%{_includedir}/kms_message
%{_includedir}/mongocrypt
%{_libdir}/cmake/kms_message
%{_libdir}/cmake/mongocrypt
%{_pkgconfigdir}/libkms_message.pc
%{_pkgconfigdir}/libmongocrypt.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbson-static-for-libmongocrypt.a
%{_libdir}/libkms_message-static.a
%{_libdir}/libmongocrypt-static.a
%{_pkgconfigdir}/libmongocrypt-static.pc
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
%endif
