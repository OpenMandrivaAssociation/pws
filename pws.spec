%define libname      %{mklibname pws 0.1}
%define libnamedevel %{mklibname pws -d}

Name:           pws
Version:        0.3.0
Release:        %mkrel 2
Summary:        Fully compatible passwordsafe implementation
License:        GPL
Group:          Text tools
BuildRequires:  libgcrypt-devel
BuildRequires:  qt4-devel
URL:            http://www.pwsafe.de/
Source0:        http://www.pwsafe.de/releases/unstable/pws-%{version}.tar.gz
Source1:        pws.desktop
Source2:        pws-x-psafe3.desktop
Patch0:         pws-0.3.0-destdir.patch
Requires(post):  desktop-file-utils
Requires(postun):  desktop-file-utils
BuildRequires:  desktop-file-utils
BuildRequires:  imagemagick
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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
%patch0 -p1

%build
export CFLAGS="-fPIC %{optflags}"
%{configure2_5x} --with-qt=%{qt4dir}
%{make}

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}

%{__mkdir_p} %{buildroot}%{_datadir}/pixmaps
%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/16x16/apps
%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/64x64/apps

%{_bindir}/convert -scale 32 pws/images/logo.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
%{__cp} -a pws/images/logo.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_bindir}/convert -scale 32 pws/images/logo.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_bindir}/convert -scale 64 pws/images/logo.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png

%{__mkdir_p} %{buildroot}%{_datadir}/applications
%{_bindir}/desktop-file-install --vendor "" \
        --dir %{buildroot}%{_datadir}/applications \
        %{SOURCE1}

%{__install} -D -m 644 -p %{SOURCE2} %{buildroot}%{_datadir}/mimelnk/application/x-psafe3.desktop

%clean
%{__rm} -rf %{buildroot}

%post
%{update_desktop_database}
%update_icon_cache hicolor
%{update_mime_database}

%postun
%{clean_desktop_database}
%clean_icon_cache hicolor
%{clean_mime_database}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(0644,root,root,0755)
%doc misc/* README.txt CHANGELOG
%attr(0755,root,root) %{_bindir}/pws
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/mimelnk/application/x-psafe3.desktop

%files -n %{libname}
%defattr(0755,root,root,0755)
%{_libdir}/libpws.so.*

%files -n %{libnamedevel}
%defattr(0644,root,root,0755)
%{_includedir}/libpws
