# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname networking-omnipath
%global pyname networking-omnipath

%global with_doc 1

Name:           python-%{sname}
Version:        XXX
Release:        XXX
Summary:        Python library for Intel Omnipath ML2 driver.

License:        ASL 2.0
URL:            https://opendev.org/x/%{sname}.git
Source0:        https://opendev.org/x/networking-omnipath/archive/master.tar.gz
BuildArch:      noarch

%description
OpenStack networking-omnipath is a ML2 mechanism driver that integrates
OpenStack Neutron API with Omnipath backend. It enables Omnipath switching
fabric in OpenStack cloud and each network in Openstack networking realm
corresponds to a virtual fabric on omnipath side.

%package -n     python%{pyver}-%{sname}
Summary:        %{summary}
%{?python_provide:%python_provide python%{pyver}-%{sname}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-jsonschema
BuildRequires:  python%{pyver}-pbr >= 2.0
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-sushy >= 1.8.1
BuildRequires:  python%{pyver}-sushy-tests >= 1.7.0
BuildRequires:  python-oslo-config >= 5.2.0
BuildRequires:  python%{pyver}-oslo.log

Requires:       python%{pyver}-jsonschema
Requires:       python%{pyver}-pbr >= 2.0
Requires:       python%{pyver}-sushy >= 1.8.1

#imported from requirements.txt, with some changes
Requires:       python%{pyver}-SQLAlchemy >= 1.3.11-1
Requires:       python-neutron-lib >= 1.25.0
Requires:       python-oslo-config >= 5.2.0
Requires:       python%{pyver}-paramiko >= 2.4.2
Requires:       python%{pyver}-six >= 1.10.0
Requires:       openstack-neutron >= 13.0.0.0b2
Requires:       python-oslo-log >= 3.36.0

%description -n python%{pyver}-%{sname}
OpenStack networking-omnipath is a ML2 mechanism driver that integrates
OpenStack Neutron API with Omnipath backend. It enables Omnipath switching
fabric in OpenStack cloud and each network in Openstack networking realm
corresponds to a virtual fabric on omnipath side.

%package -n python%{pyver}-%{sname}-tests
Summary: OpenStack networking-omnipath tests

BuildRequires: python%{pyver}-devel
BuildRequires: python-oslo-log >= 3.36.0

#imported from test-requirements.txt
Requires: python%{pyver}-hacking >= 1.1.0
Requires: python%{pyver}-coverage >= 4.5
Requires: python%{pyver}-flake8-import-order = 0.12
Requires: python%{pyver}-subunit >= 1.0.0
Requires: python%{pyver}-sphinx > 1.6.7
Requires: python%{pyver}-openstackdocstheme >= 1.18.1
Requires: python%{pyver}-doc8 >= 0.6.0
Requires: python%{pyver}-oslotest >= 3.2.0
Requires: python%{pyver}-os-testr >= 1.0.0
%if 0%{?fedora} || 0%{?rhel} > 7
Requires: python3-pylint == 2.3.0
%else
Requires: python2-pylint == 1.9.3
%endif
Requires: python%{pyver}-testresources >= 2.0.0
Requires: python%{pyver}-testscenarios >= 0.4
Requires: python%{pyver}-webtest >= 2.0.27
Requires: python%{pyver}-testtools >= 2.2.0
Requires: python%{pyver}-reno >= 2.5.0

Requires: python%{pyver}-%{sname} = %{version}-%{release}
Requires: python%{pyver}-jsonschema
Requires: python%{pyver}-pbr
Requires: python%{pyver}-setuptools
Requires: python%{pyver}-sushy >= 1.8.1
Requires: python%{pyver}-sushy-tests >= 1.7.0

%description -n python%{pyver}-%{sname}-tests
Tests for networking-omnipath

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary: networking-omnipath documentation

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme >= 1.11.0

%description -n python-%{sname}-doc
Documentation for networking-omnipath
%endif

%prep
%autosetup -n %{sname}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
sed -i '/warning-is-error/d' setup.cfg

%{pyver_build}

%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%check
export PYTHON=%{pyver_bin}
%{pyver_bin} setup.py test || true

%files -n python%{pyver}-%{sname}
%license LICENSE
%doc doc/source/readme.rst README.rst
%{pyver_sitelib}/%{pyname}
%{pyver_sitelib}/%{pyname}-*.egg-info
%exclude %{pyver_sitelib}/%{pyname}/tests

%files -n python%{pyver}-%{sname}-tests
%license LICENSE
%{pyver_sitelib}/%{pyname}/tests

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
