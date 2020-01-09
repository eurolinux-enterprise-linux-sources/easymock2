Name:           easymock2
Version:        2.5.2
Release:        12%{?dist}
Summary:        Easy mock objects
License:        ASL 2.0
Group:          Development/Languages
URL:            http://easymock.org/
# generated by sh fetch-easymock.sh
Source0:        easymock-%{version}.tgz
# extracted from http://download.eclipse.org/tools/orbit/downloads/drops/R20090529135407/bundles/org.easymock_2.4.0.v20090202-0900.jar#META-INF/MANIFEST.MF
Source1:        easymock-MANIFEST.MF
# generated by mvn ant:ant
Source2:        build.xml.tar.gz
Source3:        fetch-easymock.sh
Patch0:		easymock2-nameClash.patch

BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  ant >= 0:1.6
BuildRequires:  junit >= 3.8.1
BuildRequires:  java-javadoc
BuildRequires:  zip
Requires:       java
BuildArch:      noarch
Requires:       jpackage-utils >= 0:1.7.2

%description
EasyMock provides Mock Objects for interfaces in JUnit tests by generating
them on the fly using Java's proxy mechanism. Due to EasyMock's unique style
of recording expectations, most refactorings will not affect the Mock Objects.
So EasyMock is a perfect fit for Test-Driven Development.

%package javadoc
Summary:    Javadoc for %{name}
Group:      Documentation

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n easymock
%patch0 -p2
mkdir -p .m2/repository/JPP/maven2/default_poms
tar xzf %{SOURCE2}

# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%build
ant -Dmaven.mode.offline=true -Dmaven.repo.local=.m2 -Dmaven.test.skip=true package javadoc
mv target/easymock-2.5.jar target/%{name}-%{version}.jar

# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE1} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u target/%{name}-%{version}.jar META-INF/MANIFEST.MF

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}

install -m 644 target/%{name}-%{version}.jar \
    %{buildroot}%{_javadir}/%{name}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap -v 2.4

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/apidocs

%files
%doc LICENSE.txt
%{_javadir}/%{name}-*.jar
%{_mavenpomdir}/JPP-%{name}-*.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc LICENSE.txt
%doc %{_javadocdir}/*

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.5.2-12
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.2-11
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri May 31 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.2-10
- Convert to a compat package
- Resolves: rhbz#969376

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.5.2-8
- Install LICENSE with javadoc package
- Don't own _mavendepmapfragdir
- Install POM in _mavenpomdir instead of _datadir/maven2/poms
- Update to current packaging guidelines

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 23 2012 Jiri Vanek  <jvanek@redhat.com> - 2.5.2-6
- Fixed for JDK7 - https://fedoraproject.org/wiki/Java7_Package_Rebuild_Status
- Added and aplied patch0, easymock2-nameClash.patch.
  This patch is removing (in easymock3 deprecated) methods, and is keeping new 
  easymock3 api in EasyMock.java for capture set of methods.
  Old methods cant be kept as deprecated as JDK7 can not compile them.
  Test was derived from easymock3' one too.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 8 2010 Alexander Kurtakov <akurtako@redhat.com> 2.5.2-3
- BR zip.
- Don't install versioned jar.
- Use standard file permissions.

* Wed Jul 21 2010 Alexander Kurtakov <akurtako@redhat.com> 2.5.2-2
- Fix maven depmap.

* Fri Jan 15 2010 Alexander Kurtakov <akurtako@redhat.com> 2.5.2-1
- Update to upstream 2.5.2.
- Now under ASL 2.0 license.

* Wed Oct 21 2009 Alexander Kurtakov <akurtako@redhat.com> 2.5-4
- Fix empty jar. Bug #530110.

* Mon Aug 17 2009 Alexander Kurtakov <akurtako@redhat.com> 2.5-3
- Renamed to easymock2.

* Mon Aug 17 2009 Alexander Kurtakov <akurtako@redhat.com> 2.5-2
- Use %%{buildroot} instead of $RPM_BUILD_ROOT.
- Add comment for MANIFEST.MF origin.

* Fri Aug 14 2009 Alexander Kurtakov <akurtako@redhat.com> 2.5-1
- Initial package.
