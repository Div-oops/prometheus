%define		app_name		prometheus-2.12.0.linux-amd64
%define		app_version		2.12.0
%define		app_release		2%{?dist}
%define		app_arch                x86_64
%define		app_owner		prometheus

Name:		prometheus
Version:	%{app_version}
Release:        %{app_release}
Summary:        prometheus-server

License:       	Apache Software License 2.0
URL:		http://www.apache.org/licenses/LICENSE-2.0
Source0:	prometheus.service

%description
prometheus-server


%install
pwd
mkdir -p %{buildroot}
cd %{buildroot}
pwd
wget https://github.com/prometheus/prometheus/releases/download/v2.12.0/%{app_name}.tar.gz
tar -xf %{app_name}.tar.gz
rm %{app_name}.tar.gz
%{__mkdir_p} %{buildroot}/{etc,var/lib,usr/share{,/doc}}/prometheus/
%{__mkdir_p} %{buildroot}/usr/local/bin/
mv %{buildroot}/%{app_name}/{LICENSE,NOTICE} %{buildroot}%{_docdir}/prometheus/
mv %{buildroot}/%{app_name}/{prometheus.yml,consoles,console_libraries} %{buildroot}/etc/prometheus/
mv %{buildroot}/%{app_name}/{prometheus,promtool} %{buildroot}/usr/local/bin/
rm -Rf %{buildroot}/%{app_name}
pwd
%{__install} -p -D -m 0755 %{SOURCE0} %{buildroot}%{_sysconfdir}/systemd/system/prometheus.service


%pre
getent passwd %{app_owner} >/dev/null || \
    useradd -r --no-create-home -s /bin/false \
    -c "user for progect" %{app_owner}

%post
systemctl daemon-reload

%postun
systemctl daemon-reload


%files
%defattr(755,%{app_owner},%{app_owner},755)
/usr/local/bin/{prometheus,promtool}
%defattr(644,%{app_owner},%{app_owner},755)
%dir %{_sysconfdir}/prometheus
%config %{_sysconfdir}/prometheus/prometheus.yml
%{_sysconfdir}/prometheus/consoles
%{_sysconfdir}/prometheus/console_libraries
%{_sharedstatedir}/prometheus
%defattr(-,root,root,-)
%{_sysconfdir}/systemd/system/prometheus.service
%license %{_docdir}/prometheus/LICENSE
%doc %{_docdir}/prometheus/



%changelog
