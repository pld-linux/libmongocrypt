#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	The companion C library for client side encryption in drivers
Summary(pl.UTF-8):	Biblioteka towarzysząca C do szyfrowania w sterownikach po stronie klienta
Name:		libmongocrypt
Version:	1.0.4
Release:	2
# see kms-message/THIRD_PARTY_NOTICES
# kms-message/src/kms_b64.c is ISC
# everything else is ASL 2.0
License:	ASL 2.0 and ISC
Group:		Libraries
Source0:	https://github.com/mongodb/libmongocrypt/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e8939c3ed5c8b797dd8d4ea1290f7652
Patch0:		no-Werror.patch
URL:		https://github.com/mongodb/libmongocrypt
BuildRequires:	cmake >= 3.5
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libbson-devel >= 1.11
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
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
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files and other development files for
libmongocrypt library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe i inne pliki programistyczne
biblioteki libmongocrypt.

%prep
%setup -q
%patch -P0 -p1
echo "%{version}" > VERSION_CURRENT

%build
%cmake \
	-DCMAKE_C_FLAGS="%{optflags} -fPIC" \
	-DENABLE_SHARED_BSON:BOOL=ON \
	-DENABLE_STATIC:BOOL=OFF \
	.

%{__make}

%if %{with tests}
%{__make} test
%endif

%if %{with apidocs}
doxygen doc/Doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE
%ghost %{_libdir}/libmongocrypt.so.0
%attr(755,root,root) %{_libdir}/libmongocrypt.so.*.*.*
%ghost %{_libdir}/libkms_message.so.0
%attr(755,root,root) %{_libdir}/libkms_message.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc *.md
%if %{with apidocs}
%doc doc/html
%endif
%{_libdir}/libkms_message.so
%{_libdir}/libmongocrypt.so
%{_includedir}/kms_message
%{_includedir}/mongocrypt
%{_libdir}/cmake/kms_message
%{_libdir}/cmake/mongocrypt
%{_pkgconfigdir}/libkms_message.pc
%{_pkgconfigdir}/libmongocrypt.pc
