#Module-Specific definitions
%define mod_name mod_extract_forwarded
%define mod_conf A86_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Extract real source IP for forwarded HTTP requests
Name:		apache-%{mod_name}
Version:	2.0.2
Release:	%mkrel 5
Group:		System/Servers
License:	Apache License
URL:		http://www.openinfo.co.uk/apache/
Source0:	http://www.openinfo.co.uk/apache/extract_forwarded-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires(pre):	apache-mod_proxy >= 2.2.0 
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
Requires:	apache-mod_proxy >= 2.2.0 
BuildRequires:	apache-devel >= 2.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_extract_forwarded hooks itself into Apache's header parsing phase and looks
for the X-Forwarded-For header which some (most?) proxies add to the proxied
HTTP requests. It extracts the IP from the X-Forwarded-For and modifies the
connection data so to the rest of Apache the request looks like it came from
that IP rather than the proxy IP.

%prep

%setup -q -n extract_forwarded

chmod 644 INSTALL README

%build

%{_sbindir}/apxs -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
 %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
 if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
 fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc INSTALL README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
