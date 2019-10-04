Summary: Browser default start page for RedSleeve
Name: redsleeve-indexhtml
Version: 8.0
Release: 0%{?dist}
Source: %{name}-%{version}.tar.gz
License: Distributable
Group: Documentation
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes: indexhtml <= 2:5-1
Obsoletes: redhat-indexhtml
Provides: redhat-indexhtml

%description
The indexhtml package contains the welcome page shown by your Web browser,
which you'll see after you've successfully installed RedSleeve Linux.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_defaultdocdir}/HTML
cp -a . $RPM_BUILD_ROOT/%{_defaultdocdir}/HTML/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_defaultdocdir}/HTML/*

%changelog
* Fri Oct 04 2019 Jacco Ligthart <jacco@redsleeve.org> 8.0-0
- RedSleeve Branded based on RdeSleeve7
