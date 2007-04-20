%define name xcave
%define version 2.2.4
%define release %mkrel 3

Summary: A wine cellar manager
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://xcave.free.fr/download/en/%{name}-%{version}.tar.bz2
License: GPL
Group: Databases
Url: http://xcave.free.fr/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gtk+2-devel
BuildRequires: ImageMagick

%description
xcave is a cellar manager, to allow to view and manage the contents of
a wine cellar.
The 'wine' referred to here, is for drinking, nothing to do with
Windows emulator.
It provides:
- a wine cellar manager
- a graphical representation of the cellar
  (the rack number and rack dimensions can be changed)
- many fields are predetermined depending on the appellation
- a stock data or information about a specific wine can be printed
- a tasting notes and comments
- a xml structure for the stock file
- a colour differences calculated by vintage and time stored in cellar
- a different sorting and presentation options
  (by maturity, name, vintage (year), producer and quantity)

%prep
%setup -q

%build
%configure
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

install -d $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): \
 command="%{_bindir}/%{name}" \
 needs="x11" \
 section="More Applications/Databases" \
 title="XCave" \
 icon="%{name}.png" \
 longtitle="View and manage a wine cellar"
EOF

mkdir -p $RPM_BUILD_ROOT%{_liconsdir} $RPM_BUILD_ROOT%{_iconsdir} $RPM_BUILD_ROOT%{_miconsdir}
convert -geometry 48x48 pixmaps/%{name}-icon.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
convert -geometry 32x32 pixmaps/%{name}-icon.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert -geometry 16x16 pixmaps/%{name}-icon.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

rm -rf $RPM_BUILD_ROOT%{_docdir}
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus

%postun
%clean_menus

%files -f %{name}.lang
%defattr(-,root,root)
%doc ChangeLog README TODO
%{_bindir}/%{name}
%{_datadir}/pixmaps/%{name}
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png