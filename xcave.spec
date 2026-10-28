%define name xcave
%define version 2.3.2
%define release 4

Summary: A wine cellar manager
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://xcave.free.fr/download/en/%{name}-%{version}.tar.gz
# (fc) 2.3.2-1mdv fix build with latest glibc/gcc
Patch0: xcave-2.3.2-fixbuild.patch
License: GPLv2+
Group: Databases
Url: https://xcave.free.fr/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool-base
BuildRequires:	slibtool
BuildRequires:	make
BuildRequires: pkgconfig(libxml-2.0)
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
%patch 0 -p1 -b .fixbuild
# libxml2 2.15 made xmlCharEncodingHandler.input a union.
sed -i 's/handler->input(/handler->input.legacyFunc(/g' src/xcave_xmlwriter.c
# msgfmt's iconv has no ISO-8859-15 converter. Recode the catalogs first.
python - << 'PY'
import pathlib
for po in pathlib.Path("po").glob("*.po"):
    raw = po.read_bytes()
    head = raw[:800].decode("latin1", "replace")
    charset = None
    for token in ("ISO-8859-15", "ISO-8859-1"):
        if "charset=" + token in head:
            charset = token
            break
    if charset is None:
        continue
    codec = "iso8859-15" if charset.endswith("15") else "iso8859-1"
    text = raw.decode(codec)
    text = text.replace("charset=" + charset, "charset=UTF-8", 1)
    po.write_bytes(text.encode("utf-8"))
PY

intltoolize --force
libtoolize --copy --force
autoreconf

%build
%configure2_5x
# Generated libtool is a no-op after slibtoolize. Link with slibtool.
%make LIBTOOL=slibtool-shared

%install
rm -rf %{buildroot}
%makeinstall_std LIBTOOL=slibtool-shared

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
