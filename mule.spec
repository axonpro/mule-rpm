%define muleuser mule
%define mulegroup mule

Name:		mule-standalone
Version:	3.4.0
Release:	2%{?dist}
Summary:	Mule ESB Standalone Binary distribution

Group:		Java
License:	CPAL
URL:		http://www.mulesoft.org/
Source0:	http://dist.codehaus.org/mule/distributions/%{name}-%{version}.tar.gz
Source1:	mule-init-script
Source2:	mule-sysconfig
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	java
Requires:	java

%description
Mule is a lightweight integration platform that enables you to connect anything, anywhere. Rather than creating multiple point-to-point integrations between systems, services, APIs, and devices, you can use Mule to intelligently manage message routing, data mapping, orchestration, reliability, security, and scalability between nodes. Plug other systems and applications into Mule and let it handle all the communication between systems, enabling you to track and monitor everything that happens. 

Mule is so named because it “carries the heavy development load” of connecting systems.

With Mule, you can:

    integrate applications or systems on premise or in the cloud
    use out-of-the-box connectors to integrate software-as-a-service (SaaS) applications
    build and expose APIs
    consume APIs
    create Web services which orchestrate calls to other services
    create interfaces to expose applications for mobile consumption
    integrate B2B with solutions that are secure, efficient, and quick to build and deploy
    shift applications onto the cloud
    connect B2B e-commerce activities

%prep
rm -rf %{buildroot}
%setup -q 

%build

%pre
getent group %{mulegroup} >/dev/null || groupadd -r %{mulegroup}
getent passwd %{muleuser} >/dev/null || \
useradd -r -g %{mulegroup} -d /var/lib/%{name} -s /sbin/nologin \
    -c "Mule user" %{muleuser} || :

%post
chkconfig --add %{name}
chkconfig %{name} on


%preun
service %{name} stop
chkconfig %{name} off
chkconfig --del %{name}
#userdel -f %{muleuser} 2> /dev/null
#groupdel %{mulegroup} 2> /dev/null

%install
install -m 755 -d %{buildroot}/usr/share/doc/%{name}-%{version}
cp -a examples/ %{buildroot}/usr/share/doc/%{name}-%{version}/examples/
cp -a docs/ LICENSE.txt README.txt  %{buildroot}/usr/share/doc/%{name}-%{version}/
install -m 755 -d %{buildroot}/%{_javadir}/%{name}/
cp -a lib/ bin/ %{buildroot}/%{_javadir}/%{name}/
rm $(find %{buildroot}/%{_javadir}/%{name}/ | egrep "solaris|macosx|linux-ia-64|linux-ppc-64|hpux-parisc|freebsd")
install -m 755 -d %{buildroot}/var/lib/%{name}
install -m 755 -d %{buildroot}/var/lib/%{name}/work
cp -a apps/ conf/ %{buildroot}/var/lib/%{name}
install -m 755 -d %{buildroot}/%{_initddir}
install -m 755 -d %{buildroot}/etc/sysconfig/
install -m 755 -d %{buildroot}/var/log/%{name}/
install -m 755 -d %{buildroot}/var/run/%{name}/
install -m 755 %{SOURCE1} %{buildroot}/%{_initddir}/%{name}
cp %{SOURCE2} %{buildroot}/etc/sysconfig/%{name}

ln -s /var/lib/%{name}/apps %{buildroot}%{_javadir}/%{name}/apps
ln -s /var/lib/%{name}/conf %{buildroot}%{_javadir}/%{name}/conf
ln -s /var/log/%{name}/     %{buildroot}%{_javadir}/%{name}/logs
ln -s /var/lib/%{name}/work %{buildroot}%{_javadir}/%{name}/.mule

#disable PIDDIR in original stupid initscript
perl -p -i -e 's/^PIDDIR/#PIDDIR/g' %{buildroot}/%{_javadir}/%{name}/bin/mule


#drwxr-xr-x.  3  400  400  4096 Apr 14 22:03 apps/
#drwxr-xr-x.  2 root root  4096 Aug 22 11:38 bin/
#drwxr-xr-x.  2  400  400  4096 Aug 22 11:38 conf/
#drwxr-xr-x.  3  400  400  4096 Apr 14 22:03 docs/
#drwxrwxrwx. 11  400  400  4096 Apr 14 22:08 examples/
#drwxr-xr-x.  8  400  400  4096 Aug 22 11:38 lib/
#-rw-r--r--.  1  400  400 27932 Apr 14 22:03 LICENSE.txt
#drwxr-xr-x.  2  400  400  4096 Aug 22 11:38 logs/
#-rw-r--r--.  1  400  400  4049 Apr 14 22:03 README.txt
#drwxr-xr-x.  2  400  400  4096 Aug 22 11:38 src/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc /usr/share/doc/%{name}-%{version}
%{_javadir}/%{name}/
%attr(775, %{muleuser}, %{mulegroup}) /var/lib/%{name}
%{_initddir}/%{name}
%config /etc/sysconfig/%{name}
%attr(775, %{muleuser}, %{mulegroup}) /var/log/%{name}/
%attr(775, %{muleuser}, %{mulegroup}) /var/run/%{name}/

%changelog
* Thu Aug 22 2013 Ernest Beinrohr <Ernest@Beinrohr.sk> - 3.4.0-2
- Initial RPM release


