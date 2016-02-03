Name:          airline
Version:       0.7
Release:       4%{?dist}
Summary:       Java annotation-based framework
License:       ASL 2.0
URL:           https://github.com/airlift/airline
Source0:       https://github.com/airlift/airline/archive/%{version}.tar.gz

BuildRequires: maven-local
BuildRequires: mvn(com.google.code.findbugs:annotations)
BuildRequires: mvn(com.google.code.findbugs:jsr305)
BuildRequires: mvn(com.google.guava:guava)
BuildRequires: mvn(javax.inject:javax.inject)
BuildRequires: mvn(org.testng:testng)
BuildArch:     noarch

%description
Airline is a Java annotation-based framework
for parsing Git like command line structures.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
find -name '*.class' -delete
find -name '*.jar' -delete

# io.airlift:airbase:pom:28
%pom_remove_parent
%pom_xpath_inject "pom:project" "<groupId>io.airlift</groupId>"
# cannot find symbol javax.annotation.Nullable
%pom_add_dep com.google.code.findbugs:jsr305:2.0.3

%pom_xpath_inject "pom:dependency[pom:artifactId='annotations']" '<version>2.0.3</version>'
%pom_xpath_inject "pom:dependency[pom:artifactId='guava']" '<version>18.0</version>'
%pom_xpath_inject "pom:dependency[pom:artifactId='testng']" '<version>6.8.7</version>'

%mvn_file :%{name} %{name}

%build

%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license license.txt notice.md

%files javadoc -f .mfiles-javadoc
%license license.txt notice.md

%changelog
* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 28 2015 gil cattaneo <puntogil@libero.it> - 0.7-3
- rebuilt

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 18 2015 gil cattaneo <puntogil@libero.it> 0.7-1
- initial rpm
