veracrypt_archive
=================

Creates a VeraCrypt container from a local directory, mounts it, moves all staged items into it, and always dismounts it.

Requirements
------------

- `veracrypt` must be installed on the machine running this role.
- `veracrypt_password` should be provided from an Ansible-vaulted secrets file.

Role Variables
--------------

- `veracrypt_password`: secret used to create and mount the container
- `input_path`: local directory containing items to archive
- `veracrypt_container_path`: full destination path for the `.hc` file
- `veracrypt_mount_point`: mount target directory (default: `/mnt/veracrypt_archive`)
- `veracrypt_filesystem`: container filesystem (default: `ext4`)
- `veracrypt_encryption`: cipher (default: `AES`)
- `veracrypt_hash`: hash algorithm (default: `SHA-512`)

Behavior
--------

1. Calculates total bytes under `input_path`.
2. Computes container size as 125% of that value.
3. Creates the VeraCrypt container at `veracrypt_container_path`.
4. Ensures the mount point exists, then mounts the container.
5. Moves all items from `input_path` into the mounted container.
6. Always dismounts in an `always` block, even when earlier steps fail.

Example Playbook
----------------

```yaml
- name: Archive staged backup files
  hosts: localhost
  gather_facts: false
  vars_files:
    - group_vars/secrets.yml
  vars:
    input_path: "/home/pat/backups/shiori/staging-20260909-123000"
    veracrypt_container_path: "/home/pat/OneDrive/backups/shiori/shiori-backup-20260909-123000.hc"
    veracrypt_mount_point: "/mnt/shiori_vc"
  roles:
    - veracrypt_archive
```
