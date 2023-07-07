%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order pylint

# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global sname networking-omnipath
%global pyname omnipath

%global with_doc 1

Name:           python-%{sname}
Version:        XXX
Release:        XXX
Summary:        Python library for Intel Omnipath ML2 driver.

License:        Apache-2.0
URL:            https://opendev.org/x/%{sname}.git
Source0:        https://opendev.org/x/%{sname}/archive/master.tar.gz
BuildArch:      noarch

%description
OpenStack networking-omnipath is a ML2 mechanism driver that integrates
OpenStack Neutron API with Omnipath backend. It enables Omnipath switching
fabric in OpenStack cloud and each network in Openstack networking realm
corresponds to a virtual fabric on omnipath side.

%package -n     python3-%{sname}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  git-core
BuildRequires:  openstack-neutron >= 13.0.0.0b2


Requires:       openstack-neutron >= 13.0.0.0b2
%description -n python3-%{sname}
OpenStack networking-omnipath is a ML2 mechanism driver that integrates
OpenStack Neutron API with Omnipath backend. It enables Omnipath switching
fabric in OpenStack cloud and each network in Openstack networking realm
corresponds to a virtual fabric on omnipath side.

%package -n python3-%{sname}-tests
Summary: OpenStack networking-omnipath tests

#imported from test-requirements.txt
BuildRequires: python3-coverage
BuildRequires: python3-subunit >= 1.0.0
BuildRequires: python3-sphinx > 1.6.7
BuildRequires: python3-openstackdocstheme >= 1.18.1
BuildRequires: python3-oslotest >= 3.2.0
BuildRequires: python3-os-testr >= 1.0.0
BuildRequires: python3-testresources
BuildRequires: python3-testscenarios >= 0.4
BuildRequires: python3-neutron-tests
BuildRequires: python3-webtest
BuildRequires: python3-testtools >= 2.2.0

Requires: python3-%{sname} = %{version}-%{release}
Requires: openstack-neutron >= 13.0.0.0b2

%description -n python3-%{sname}-tests
Tests for networking-omnipath

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary: networking-omnipath documentation

%description -n python-%{sname}-doc
Documentation for networking-omnipath
%endif

%prep
%autosetup -n %{sname}-%{upstream_version} -S git


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
sed -i '/warning-is-error/d' setup.cfg

%pyproject_wheel

%if 0%{?with_doc}
%tox -e docs
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

%check
export PYTHON=%{__python3}
#NOTE(xbzhang99): test has issues related to alembic, will fix them in the next release.
%tox -e %{default_toxenv}

%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pyname}
%{python3_sitelib}/networking_%{pyname}-*.dist-info
%exclude %{python3_sitelib}/%{pyname}/tests

%files -n python3-%{sname}-tests
%license LICENSE
%{python3_sitelib}/%{pyname}/tests

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%license LICENSE
%doc README.rst
%doc doc/build/html
%endif

%changelog
