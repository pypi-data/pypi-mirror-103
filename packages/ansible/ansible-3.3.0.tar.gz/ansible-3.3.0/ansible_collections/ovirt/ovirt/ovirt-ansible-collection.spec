%global namespace ovirt
%global collectionname ovirt
%global ansible_collections_dir ansible/collections/ansible_collections

Name:		ovirt-ansible-collection
Summary:	Ansible collection to manage all ovirt modules and inventory
Version:	1.4.1
Release:	1%{?release_suffix}%{?dist}
Source0:	http://resources.ovirt.org/pub/src/ovirt-ansible-collection/ovirt-ansible-collection-1.4.1.tar.gz
License:	ASL 2.0 and GPLv3+
BuildArch:	noarch
Url:		http://www.ovirt.org

Requires:	ansible >= 2.9.11
Requires:	python3-ovirt-engine-sdk4 >= 4.4.10
Requires:	python3-netaddr
Requires:	python3-jmespath
Requires:	python3-passlib
Requires:	qemu-img

Obsoletes:	ovirt-ansible-cluster-upgrade
Obsoletes:	ovirt-ansible-disaster-recovery
Obsoletes:	ovirt-ansible-engine-setup
Obsoletes:	ovirt-ansible-hosted-engine-setup
Obsoletes:	ovirt-ansible-image-template
Obsoletes:	ovirt-ansible-infra
Obsoletes:	ovirt-ansible-manageiq
Obsoletes:	ovirt-ansible-repositories
Obsoletes:	ovirt-ansible-roles
Obsoletes:	ovirt-ansible-shutdown-env
Obsoletes:	ovirt-ansible-vm-infra

Provides:	ovirt-ansible-cluster-upgrade
Provides:	ovirt-ansible-disaster-recovery
Provides:	ovirt-ansible-engine-setup
Provides:	ovirt-ansible-hosted-engine-setup
Provides:	ovirt-ansible-image-template
Provides:	ovirt-ansible-infra
Provides:	ovirt-ansible-manageiq
Provides:	ovirt-ansible-repositories
Provides:	ovirt-ansible-roles
Provides:	ovirt-ansible-shutdown-env
Provides:	ovirt-ansible-vm-infra

%description
This Ansible collection is to manage all ovirt modules and inventory

%prep
%setup -c -q

%build

%install
export PKG_DATA_DIR_ORIG=%{_datadir}/%{ansible_collections_dir}
export PKG_DATA_DIR=%{buildroot}$PKG_DATA_DIR_ORIG
export PKG_DOC_DIR=%{buildroot}%{_pkgdocdir}
sh build.sh install %{collectionname}

%files
%{_datadir}/%{ansible_collections_dir}/%{namespace}
%if "%{collectionname}" == "rhv"
%{_datadir}/%{ansible_collections_dir}/ovirt
%endif

%doc README.md
%doc examples/

%license licenses

%changelog
* Mon Mar 22 2021 Martin Necas <mnecas@redhat.com> - 1.4.1-1
- hosted_engine_setup - Fix auth revoke

* Tue Mar 16 2021 Martin Necas <mnecas@redhat.com> - 1.4.0-1
- cluster_upgrade - Add correlation-id header
- engine_setup - Add skip renew pki confirm
- examples - Add recipe for removing DM device
- hosted_engine_setup - Filter devices with unsupported bond mode
- infra - Add reboot host parameters
- ovirt_disk - Add SATA support
- ovirt_user - Add ssh_public_key
- Set auth options into argument spec definition

* Wed Feb 10 2021 Martin Necas <mnecas@redhat.com> - 1.3.1-1
- ovirt_host - Add reboot_after_installation option
- hosted_engine_setup - Disable reboot_after_installation

* Thu Jan 28 2021 Martin Necas <mnecas@redhat.com> - 1.3.0-1
- ovirt_system_option_info - Add new module
- ansible-builder - Update bindep
- hosted_engine_setup - Collect all engine /var/log
- hosted_engine_setup - Use ovirt_system_option_info instead of REST API
- ovirt_disk - Add install warning
- ovirt_info - Fragment add auth suboptions to documentation

* Mon Dec 14 2020 Martin Necas <mnecas@redhat.com> - 1.2.4-1
- infra - Allow remove of user without password
- inventory plugin - Correct os_type name
- ovirt_disk - automatically detect virtual size of qcow image

* Mon Nov 30 2020 Martin Necas <mnecas@redhat.com> - 1.2.3-1
- Add hosted_engine_setup after_add_host hook
- Add engine_setup restore files

* Thu Nov 12 2020 Martin Perina <mperina@redhat.com> - 1.2.2-1
- inventory plugin - Fix Python 2 timestamp issue
- hosted_engine_setup - Clean VNC encryption config
- RPM packaging - Add Provides to previous oVirt Ansible roles RPMs to
  minimize upgrade issues

* Mon Nov 2 2020 Martin Necas <mnecas@redhat.com> - 1.2.1-1
- Split README for build and GitHub
- Add ovirt_repositories_disable_gpg_check to repositories

* Tue Oct 27 2020 Martin Necas <mnecas@redhat.com> - 1.2.0-1
- Fix ovirt_disk ignore moving of hosted engine disks
- Obsolete old roles

* Mon Oct 12 2020 Martin Necas <mnecas@redhat.com> - 1.2.0-0.2
- Add role disaster_recovery
- Fix engine_setup yum.conf
- Fix hosted_engine_setup - Allow uppercase characters in mac address

* Mon Oct 12 2020 Martin Necas <mnecas@redhat.com> - 1.2.0-0.2
- Add ovirt_vm_info current_cd
- Add ovirt_nic_info template
- Add ovirt_nic template_version
- Fix ovirt_disk move
- Fix ovirt inventory connection close
- Fix ovirt_vm rename q35_sea to q35_sea_bios
- Fix ovirt_vm template search

* Wed Sep 16 2020 Martin Necas <mnecas@redhat.com> - 1.2.0-0.1
- Add role cluster_upgrade
- Add role engine_setup
- Add role vm_infra
- Add role infra
- Add role manageiq
- Add role hosted_engine_setup
- Add role image_template
- Add role shutdown_env

* Mon Aug 17 2020 Martin Necas <mnecas@redhat.com> - 1.1.2-1
- Add ansible changelogs

* Wed Aug 12 2020 Martin Necas <mnecas@redhat.com> - 1.1.1-1
- Fix ovirt_permission FQCNs

* Wed Aug 12 2020 Martin Necas <mnecas@redhat.com> - 1.1.0-1
- Add ovirt_vm_os_info module
- Add ovirt_disk backup
- Add ovirt_disk autodetect size when uploading
- Add ovirt_host add ssh_port
- Add ovirt_network support of removing vlan_tag
- Fix ovirt_disk upload

* Thu Apr 9 2020 Martin Necas <mnecas@redhat.com> - 1.0.0-1
- Initial release
