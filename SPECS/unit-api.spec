Name:          unit-api
Version:       1.0
Release:       5%{?dist}
Summary:       JSR 363 - Units of Measurement API
# JSR-363 has been approved as an official JCP standard (https://jcp.org/en/jsr/results?id=5877)
License:       BSD
URL:           http://unitsofmeasurement.github.io/
Source0:       https://github.com/unitsofmeasurement/unit-api/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: maven-local
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.sonatype.oss:oss-parent:pom:)

BuildArch:     noarch

%description
The Unit of Measurement library provides a set of
Java language programming interfaces for handling
units and quantities. The interfaces provide a layer
which separates client code, which would call the
API, from library code, which implements the API.

The specification contains Interfaces and abstract
classes with methods for unit operations:

* Checking of unit compatibility
* Expression of a quantity in various units
* Arithmetic operations on units

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{version}
find . -name "*.class" -print -delete
find . -name "*.jar" -print -delete

# Not available plugins
%pom_remove_plugin :coveralls-maven-plugin
%pom_remove_plugin :findbugs-maven-plugin
%pom_remove_plugin :formatter-maven-plugin
# Useless tasks
%pom_remove_plugin :jacoco-maven-plugin
%pom_remove_plugin :license-maven-plugin
%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-pmd-plugin
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-source-plugin

# Remove duplicate pom entry
%pom_remove_plugin :maven-jar-plugin
%pom_add_plugin org.apache.maven.plugins:maven-jar-plugin:'${maven.jar.version}' . "
<executions>
   <execution>
      <goals>
         <goal>test-jar</goal>
      </goals>
   </execution>
</executions>"
# Fix pom entries
%pom_remove_plugin :maven-bundle-plugin
%pom_add_plugin org.apache.felix:maven-bundle-plugin:'${felix.version}' . "
<extensions>true</extensions>
<configuration>
  <instructions>
    <Specification-Title>\${project.name}</Specification-Title>
    <Specification-Version>\${project.version}</Specification-Version>
    <Specification-Vendor>\${project.organization.name}</Specification-Vendor>
    <Implementation-Vendor>Unit-API contributors</Implementation-Vendor>
    <Implementation-URL>\${project.organization.url}</Implementation-URL>
  </instructions>
</configuration>
<executions>
  <execution>
    <id>bundle-manifest</id>
    <phase>process-classes</phase>
    <goals>
      <goal>manifest</goal>
    </goals>
  </execution>
</executions>"

%mvn_file  : %{name}
%mvn_file :%{name}:tests: %{name}-tests
%mvn_package :%{name}:tests: %{name}

%build

%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 16 2016 gil cattaneo <puntogil@libero.it> 1.0-1
- update to 1.0

* Wed Sep 02 2015 gil cattaneo <puntogil@libero.it> 0.7-1
- update to 0.7

* Sun Oct 20 2013 gil cattaneo <puntogil@libero.it> 0.6.2-0.1.RC1
- initial rpm
