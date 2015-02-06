%define name xcave
%define version 2.3.2
%define release 3

Summary: A wine cellar manager
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://xcave.free.fr/download/en/%{name}-%{version}.tar.gz
# (fc) 2.3.2-1mdv fix build with latest glibc/gcc
Patch0: xcave-2.3.2-fixbuild.patch
License: GPLv2+
Group: Databases
Url: http://xcave.free.fr/
BuildRequires: pkgconfig(gtk+-2.0)
BuildRequires: pkgconfig(libglade-2.0)
BuildRequires: pkgconfig(atk)
BuildRequires: imagemagick
BuildRequires: intltool

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
%patch0 -p1 -b .fixbuild

intltoolize --force
libtoolize --copy --force
autoreconf

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=XCave
Comment=View and manage a wine cellar
Exec=%_bindir/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Office;Database;GTK;
EOF

mkdir -p %{buildroot}%{_liconsdir} %{buildroot}%{_iconsdir} %{buildroot}%{_miconsdir}
convert -geometry 48x48 pixmaps/%{name}-icon.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 pixmaps/%{name}-icon.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 pixmaps/%{name}-icon.png %{buildroot}%{_miconsdir}/%{name}.png

rm -rf %{buildroot}%{_prefix}/doc
%find_lang %{name}


%files -f %{name}.lang
%doc ChangeLog README TODO
%{_bindir}/%{name}
%{_datadir}/pixmaps/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
