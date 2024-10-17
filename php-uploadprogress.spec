%define modname uploadprogress
%define soname %{modname}.so
%define inifile A78_%{modname}.ini

Summary:	Uploadprogress extension
Name:		php-%{modname}
Version:	1.0.3.1
Release:	5
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/uploadprogress/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
An extension to track progress of a file upload.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# lib64 fix
perl -p -i -e "s|/lib\b|/%{_lib}|g" *.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_libdir}/php/extensions

install -m0755 modules/%{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}

[%{modname}]
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml examples
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.3.1-4mdv2012.0
+ Revision: 795525
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.3.1-3
+ Revision: 761340
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3.1-2
+ Revision: 696485
- rebuilt for php-5.3.8

* Sun Aug 21 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3.1-1
+ Revision: 695944
- 1.0.3.1

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-2
+ Revision: 695486
- rebuilt for php-5.3.7

* Thu Aug 11 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-1
+ Revision: 694018
- 1.0.3

* Wed Jul 27 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1
+ Revision: 691890
- 1.0.2

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-11
+ Revision: 646699
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-10mdv2011.0
+ Revision: 629896
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-9mdv2011.0
+ Revision: 628205
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-8mdv2011.0
+ Revision: 600545
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-7mdv2011.0
+ Revision: 588882
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-6mdv2010.1
+ Revision: 514710
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-5mdv2010.1
+ Revision: 485497
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-4mdv2010.1
+ Revision: 468268
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-3mdv2010.0
+ Revision: 451371
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1.0.1-2mdv2010.0
+ Revision: 397303
- Rebuild

* Sun Jun 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-1mdv2010.0
+ Revision: 387639
- 1.0.1

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2mdv2010.0
+ Revision: 377039
- rebuilt for php-5.3.0RC2

* Wed Mar 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1mdv2009.1
+ Revision: 357371
- 1.0.0

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-3mdv2009.1
+ Revision: 346682
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-2mdv2009.1
+ Revision: 341845
- rebuilt against php-5.2.9RC2

* Thu Jan 22 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-1mdv2009.1
+ Revision: 332498
- 0.9.2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-3mdv2009.1
+ Revision: 323122
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-2mdv2009.1
+ Revision: 310689
- rebuilt against php-5.2.7

* Sun Aug 31 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-1mdv2009.0
+ Revision: 277817
- 0.9.1

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.0-2mdv2009.0
+ Revision: 238460
- rebuild

* Thu Jul 10 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.0-1mdv2009.0
+ Revision: 233366
- import php-uploadprogress


* Thu Jul 10 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.0-1mdv2009.0
- initial Mandriva package
