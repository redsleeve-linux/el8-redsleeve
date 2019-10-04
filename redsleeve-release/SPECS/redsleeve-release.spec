%define debug_package %{nil}
%define product_family RedSleeve Linux
%define release_name Ootpa
%define base_release_version 8
%define full_release_version 8.0
%define dist_release_version 8
%define upstream_rel_long 8.0-0.44.el8
%define upstream_rel 8.0
#define beta Beta
%define dist .el%{dist_release_version}

Name:           redsleeve-release
Version:        %{full_release_version}
Release:        0.2%{?dist}
Summary:        %{product_family} release file
Group:          System Environment/Base
License:        GPLv2
Provides:       redsleeve-release = %{version}-%{release}
Provides:       redsleeve-release(upstream) = %{upstream_rel}
Provides:       redhat-release = %{upstream_rel_long}
Provides:       system-release = %{upstream_rel_long}
Provides:       system-release(releasever) = %{base_release_version}
#Recommends:       redhat-release-eula

Source0:        redsleeve-release-%{base_release_version}.0.tar.gz
Source1:        85-display-manager.preset
Source2:        90-default.preset
Source3:        99-default-disable.preset
Source4:        arch

Source100:      rootfs-expand


%description
%{product_family} release files

%prep
%setup -q -n redsleeve-release-%{base_release_version}

%build
echo OK

%install
rm -rf %{buildroot}

# create /etc
mkdir -p %{buildroot}/etc

# create /etc/system-release and /etc/redhat-release
echo "%{product_family} release %{full_release_version} (%{release_name}) " > %{buildroot}/etc/redsleeve-release
echo "Derived from Red Hat Enterprise Linux %{upstream_rel} (Source)" > %{buildroot}/etc/redsleeve-release-upstream
ln -s redsleeve-release %{buildroot}/etc/system-release
ln -s redsleeve-release %{buildroot}/etc/redhat-release

# create /etc/os-release
cat << EOF >>%{buildroot}/etc/os-release
NAME="%{product_family}"
VERSION="%{full_release_version} (%{release_name})"
ID="rsel"
ID_LIKE="rhel fedora"
VERSION_ID="%{full_release_version}"
PRETTY_NAME="%{product_family} %{full_release_version} (%{release_name})"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:redsleeve:enterprise_linux:%{full_release_version}"
HOME_URL="https://www.redsleeve.org/"
BUG_REPORT_URL="https://github.com/redsleeve-linux/el8/issues"

REDHAT_SUPPORT_PRODUCT="%{product_family}"
REDHAT_SUPPORT_PRODUCT_VERSION="%{full_release_version}"
EOF
# write cpe to /etc/system/release-cpe
echo "cpe:/o:redsleeve:enterprise_linux:%{full_release_version}" > %{buildroot}/etc/system-release-cpe

# create /etc/issue and /etc/issue.net
echo '\S' > %{buildroot}/etc/issue
echo 'Kernel \r on an \m' >> %{buildroot}/etc/issue
cp %{buildroot}/etc/issue %{buildroot}/etc/issue.net
echo >> %{buildroot}/etc/issue

# copy GPG keys
mkdir -p -m 755 %{buildroot}/etc/pki/rpm-gpg
for file in RPM-GPG-KEY* ; do
    install -m 644 $file %{buildroot}/etc/pki/rpm-gpg
done

# copy yum repos
mkdir -p -m 755 %{buildroot}/etc/yum.repos.d
for file in RedSleeve*.repo; do 
    install -m 644 $file %{buildroot}/etc/yum.repos.d
done

# set up the dist tag macros
install -d -m 755 %{buildroot}/etc/rpm
cat >> %{buildroot}/etc/rpm/macros.dist << EOF
# dist macros.

%%rsel %{base_release_version}
%%rhel %{base_release_version}
%%dist .el8
%%el%{base_release_version} 1
EOF

# use unbranded docdir
mkdir -p -m 755 %{buildroot}/%{_docdir}/redsleeve-release
ln -s redsleeve-release %{buildroot}/%{_docdir}/redhat-release
install -m 644 GPL %{buildroot}/%{_docdir}/redsleeve-release

# copy systemd presets
mkdir -p %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE1} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE2} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE3} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
mkdir -p %{buildroot}/etc/dnf/vars/
install -m 0644 %{SOURCE4} %{buildroot}/etc/dnf/vars

# Install arm32 specific tools
mkdir -p %{buildroot}/%{_bindir}/
install -m 0755 %{SOURCE100} %{buildroot}%{_bindir}/


%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
/etc/redhat-release
/etc/system-release
/etc/redsleeve-release
/etc/redsleeve-release-upstream
%config(noreplace) /etc/os-release
%config /etc/system-release-cpe
%config(noreplace) /etc/issue
%config(noreplace) /etc/issue.net
/etc/pki/rpm-gpg/
%config(noreplace) /etc/yum.repos.d/*
%config(noreplace) /etc/dnf/vars/*
/etc/rpm/macros.dist
%{_docdir}/redhat-release
%{_docdir}/redsleeve-release/*
%{_prefix}/lib/systemd/system-preset/*
%attr(0755,root,root) %{_bindir}/rootfs-expand

%changelog
* Fri Jul 19 2019 Jacco Ligthart <jacco@redsleeve.org> 8.0-0.2.el8
- added arch=armv5tel for dnf

* Sat May 18 2019 Jacco Ligthart <jacco@redsleeve.org> 8.0-0.1.el8
- Initial setup for Redsleeve-8.0
