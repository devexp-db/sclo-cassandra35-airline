%{?scl:%scl_package airline}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}airline
Version:	0.7
Release:	7%{?dist}
Summary:	Java annotation-based framework
License:	ASL 2.0
URL:		https://github.com/airlift/%{pkg_name}
Source0:	https://github.com/airlift/%{pkg_name}/archive/%{version}.tar.gz

BuildArch:	noarch

# build parent
BuildRequires:	%{?scl_prefix_maven}mvn(com.google.code.findbugs:jsr305)
# build
BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix}guava >= 18.0
BuildRequires:	%{?scl_prefix}snakeyaml
BuildRequires:	mvn(javax.inject:javax.inject)
# it is not needed by cassandra so it is removed for scl package
%{!?scl:BuildRequires: mvn(com.google.code.findbugs:annotations)}
# test
BuildRequires:	%{?scl_prefix_maven}testng
%{?scl:Requires: %scl_runtime}

%description
Airline is a Java annotation-based framework
for parsing Git like command line structures.

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -qn %{pkg_name}-%{version}

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
# remove parent io.airlift:airbase:pom:45
%pom_remove_parent

# fix pom because of missing parent
%pom_xpath_inject "pom:project" "<groupId>io.airlift</groupId>"
%pom_xpath_inject "pom:dependency[pom:artifactId='annotations']" '<version>2.0.3</version>'
%pom_xpath_inject "pom:dependency[pom:artifactId='guava']" '<version>18.0</version>'
%pom_xpath_inject "pom:dependency[pom:artifactId='testng']" '<version>6.8.7</version>'

# add missing dependency (from removed parent)
# cannot find symbol javax.annotation.Nullable
%pom_add_dep com.google.code.findbugs:jsr305:2.0.3

# remove missing dependency for scl package
%{?scl:%pom_remove_dep com.google.code.findbugs:annotations}

%mvn_file :%{pkg_name} %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc README.md
%license license.txt notice.md

%files javadoc -f .mfiles-javadoc
%license license.txt notice.md

%changelog
* Wed Dec 14 2016 Tomas Repik <trepik@redhat.com> - 0.7-7
- depend on new guava 18.0, no need to remove any tests

* Wed Oct 12 2016 Tomas Repik <trepik@redhat.com> - 0.7-6
- use standard SCL macros

* Tue Aug 23 2016 Tomas Repik <trepik@redhat.com> - 0.7-5
- scl conversion

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 28 2015 gil cattaneo <puntogil@libero.it> - 0.7-3
- rebuilt

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 18 2015 gil cattaneo <puntogil@libero.it> 0.7-1
- initial rpm
