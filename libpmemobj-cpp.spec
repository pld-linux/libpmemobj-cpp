#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	C++ bindings for PMDK libpmemobj library
Summary(pl.UTF-8):	Wiązania C++ do biblioteki PMDK libpmemobj
Name:		libpmemobj-cpp
Version:	1.13.0
Release:	2
License:	BSD
Group:		Applications/System
#Source0Download: https://github.com/pmem/libpmemobj-cpp/releases
Source0:	https://github.com/pmem/libpmemobj-cpp/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2c1829e984de4a369fd2bbdadccc893d
Patch0:		%{name}-get_allocator.patch
URL:		http://pmem.io/pmdk/cpp_obj/
BuildRequires:	cmake >= 3.3
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	pmdk-devel >= 1.9
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	perl-base >= 1:5.16
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
ExclusiveArch:	%{x8664} aarch64
%define		_enable_debug_packages	0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
C++ bindings for PMDK libpmemobj library.

%description -l pl.UTF-8
Wiązania C++ do biblioteki PMDK libpmemobj.

%package devel
Summary:	C++ bindings for PMDK libpmemobj library
Summary(pl.UTF-8):	Wiązania C++ do biblioteki PMDK libpmemobj
Group:		Development/Libraries
Requires:	pmdk-devel >= 1.9
Requires:	libstdc++-devel >= 6:5
Obsoletes:	pmdk-c++-devel < 1.5

%description devel
C++ bindings for PMDK libpmemobj library.

%description devel -l pl.UTF-8
Wiązania C++ do biblioteki PMDK libpmemobj.

%package apidocs
Summary:	API documentation for libpmemobj++ library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libpmemobj++
Group:		Documentation
Obsoletes:	pmdk-c++-apidocs < 1.5
BuildArch:	noarch

%description apidocs
API documentation for libpmemobj++ library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libpmemobj++.

%prep
%setup -q
%patch -P0 -p1

%build
install -d build
cd build
# .pc file creation expects CMAKE_INSTALL_{INCLUDE,LIB}DIR relative to CMAKE_INSTALL_PREFIX
%cmake .. \
	-DBUILD_BENCHMARKS=OFF \
	%{!?with_apidocs:-DBUILD_DOC=OFF} \
	-DBUILD_EXAMPLES=OFF \
	-DBUILD_TESTS=OFF \
	-DCMAKE_INSTALL_DOCDIR=%{_docdir}/libpmemobj-cpp \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libpmemobj-cpp/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
# installed as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libpmemobj-cpp

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc ChangeLog LICENSE README.md
%{_includedir}/libpmemobj++
%dir %{_libdir}/libpmemobj++
%{_libdir}/libpmemobj++/cmake
%{_pkgconfigdir}/libpmemobj++.pc
%{_examplesdir}/%{name}-%{version}

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/cpp_html/*
%endif
