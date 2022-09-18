%define version 1.4.0
%define relnum 1
%define NVdir %{name}-%{version}
%define modname cspnonce

Name:           mod_%{modname}
Version:        %{version}
Release:        %{relnum}%{?dist}
Summary:        Apache module to generate 'nonce' codes

Group:          Applications/System
License:        Apache 2.0
URL:            https://github.com/celane/mod_cspnonce
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  git
BuildRequires:  httpd-devel
Requires:       httpd

%description
mod_cspnonce is an Apache2 module that makes it dead simple to add cryptographically random "nonce" values to the (`Content-Security-Policy`) headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy).

`nonce` values are a great way to enable CSP headers while still having dynamic scripts and styles in your web app. Here's an [example from MDN web docs showing a use of `nonce` with `script-src` (https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src).


%prep
### build from git ###
rm -rf %{NVdir}
git clone %{url}.git %{NVdir}
###
cd %{NVdir}


%build
cd %{NVdir}
%{_httpd_apxs} -c %{name}.c

%install
if [ "$RPM_BUILD_ROOT" != "/" ]; then
    rm -rf $RPM_BUILD_ROOT
fi
cd %{NVdir}
mkdir -p %{buildroot}/%{_httpd_moddir}
%{_httpd_apxs} -i -S LIBEXECDIR=%{buildroot}%{_httpd_moddir} -n %{name} %{name}.la

%clean
if [ "$RPM_BUILD_ROOT" != "/" ]; then
   rm -rf $RPM_BUILD_ROOT
fi



%files
%defattr(655,root,root,755)
%doc %{NVdir}/LICENSE %{NVdir}/README.md
%doc %{NVdir}/cspnonce.conf
%{_httpd_moddir}/%{name}.so

%post
tmp=$(mktemp -d ${TMPDIR:-/tmp}/mod_cspnonce_rpm.XXXXXXX)
#echo "temp is $tmp"
trap "rm -f $tmp" EXIT
mv %{_httpd_moddir}/%{name}.so $tmp/
%{_httpd_apxs} -i -A -n %{name} $tmp/%{name}.so
rm -f $tmp

%changelog
* Sat Sep 17 2022 Cuck Lane <lane@dchooz.org> - 1.4.0
- initial version
