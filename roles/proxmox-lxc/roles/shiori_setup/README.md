shiori_setup
============

Provision an existing Alpine LXC container with the precompiled Shiori binary and run it as an OpenRC service.

Requirements
------------

- Alpine Linux target host (for this repo, this is expected to come from `alpine_lxc_init` into `dynamic_lxc`)

Role Variables
--------------

Main variables are in [defaults/main.yml](defaults/main.yml):

- `shiori_version`
- `shiori_platform`
- `shiori_arch`
- `shiori_archive_url`
- `shiori_archive_path`
- `shiori_user`
- `shiori_group`
- `shiori_home`
- `shiori_install_dir`
- `shiori_binary_path`
- `shiori_symlink_path`
- `shiori_data_dir`
- `shiori_service_name`
- `shiori_listen_address`
- `shiori_port`

Example Playbook
----------------

```yaml
---
- name: Deploy Shiori in Proxmox LXC
  hosts: proxmox
  gather_facts: false
  vars:
    alpine_lxc_hostname: "shiori"
    proxmox_api_password: "{{ ansible_password }}"
  roles:
    - alpine_lxc_init

- name: Configure Shiori in LXC
  hosts: dynamic_lxc
  gather_facts: false
  become: true
  vars:
    shiori_port: 8080
  roles:
    - role: shiori_setup
```

Notes
-----

- Shiori is managed by OpenRC as service `shiori`.
- Shiori data persists in `shiori_data_dir` (default: `/var/lib/shiori`).
- If you change `shiori_port` or `shiori_listen_address`, re-running the role updates the init script and restarts the service.
