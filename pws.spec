%define libname      %{mklibname pws 0.1}
%define libnamedevel %{mklibname pws -d}

Name:           pws
Version:        0.1.4
Release:        %mkrel 1
Summary:        Fully compatible passwordsafe implementation
License:        GPL
Group:          Text tools
BuildRequires:  libgcrypt-devel
BuildRequires:  qt4-devel
URL:            http://www.pwsafe.de/
Source0:        http://www.pwsafe.de/releases/unstable/pws-%{version}.tar.gz
Patch0:         pws-0.1.3_destdir.patch

%description
pws aims to be a fully compatible passwordsafe implementation.
heart of the project is libpws, a general library for reading and
writing passwordsafe compatible files. currently passwordsafe files
format v2 and passwordsafe files format v3.2 are supported.

%package -n %{libname}
Summary:        General library for reading and writing passwordsafe compatible files
Group:          System/Libraries

%description -n %{libname}
A general library for reading and writing passwordsafe compatible files.

%package -n %{libnamedevel}
Summary:        Development files for the PWS library
Group:          Development/C

%description -n %{libnamedevel}
The development files for the PWS library.

%prep
%setup -q
%patch0 -p0

%build
%{configure2_5x} --with-qt=%{qt4dir}
%{make}

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}

%clean
%{__rm} -rf %{buildroot}

%post -n %{libname}
/sbin/ldconfig

%postun -n %{libname}
/sbin/ldconfig

%files
%defattr(0644,root,root,0755)
%doc misc/* README.txt CHANGELOG
%attr(0755,root,root) %{_bindir}/pws

%files -n %{libname}
%defattr(0755,root,root,0755)
%{_libdir}/libpws.so.*

%files -n %{libnamedevel}
%defattr(0644,root,root,0755)
%{_includedir}/libpws

