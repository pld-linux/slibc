#
# Conditional build:
%bcond_with	apidocs		# build and package API docs [nothing useful as of 0.9.2]
%bcond_without	static_libs	# don't build static libraries
%bcond_without	tests		# don't perform "make test"
#
Summary:	Implementation of the bounds-checking C functions
Summary(pl.UTF-8):	Implementacja funkcji C z kontrolą ograniczeń
Name:		slibc
Version:	0.9.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: http://code.google.com/p/slibc/downloads/list
Source0:	http://slibc.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	9400e134e714b1fb94234075e628e1b9
Patch0:		%{name}-glibc.patch
Patch1:		%{name}-make.patch
URL:		http://code.google.com/p/slibc/
BuildRequires:	libstdc++-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library provides an implementation of the bounds-checking C
functions (as specified in Annex K of the current C standard, a.k.a.
C11) for use with the GNU C library.

%description -l pl.UTF-8
Ta biblioteka udostępnia implementacje funkcji C z kontrolą ograniczeń
(zgodnych z Annex K obecnego standardu C, tj. C11), przeznaczone do
używania z bibloteką GNU C.

%package devel
Summary:	Header files for slibc library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki slibc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for slibc library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki slibc.

%package static
Summary:	Static slibc library
Summary(pl.UTF-8):	Statyczna biblioteka slibc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static slibc library.

%description static -l pl.UTF-8
Statyczna biblioteka slibc.

%package apidocs
Summary:	%{name} API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki %{name}
Group:		Documentation

%description apidocs
API and internal documentation for %{name} library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS='%{rpmcflags} -Wall -pthread -fPIC $(INCLUDE_DIRS)' \
	CXXFLAGS='%{rpmcxxflags} -Wall -pthread -fPIC $(INCLUDE_DIRS)' \

%if %{with static_libs}
%{__make} -C src libslibc.a libslibc++.a
%endif

%if %{with apidocs}
doxygen mainpage.dox
%endif

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

# make install is broken (as of 0.9.2); do it manually
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/slibc}
cp -p include/slibc/*.h* $RPM_BUILD_ROOT%{_includedir}/slibc
cp -dp src/libslibc*.so* $RPM_BUILD_ROOT%{_libdir}
%if %{with static_libs}
cp -p src/libslibc*.a $RPM_BUILD_ROOT%{_libdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSES README TODO
%attr(755,root,root) %{_libdir}/libslibc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libslibc.so.0
%attr(755,root,root) %{_libdir}/libslibc++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libslibc++.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libslibc.so
%attr(755,root,root) %{_libdir}/libslibc++.so
%{_includedir}/slibc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libslibc.a
%{_libdir}/libslibc++.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc html/*
%endif
