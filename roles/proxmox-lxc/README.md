# Proxmox LXC Role Bundle

This directory contains a collection of Ansible roles and playbook patterns for creating and operating lightweight LXC containers on Proxmox, then installing self-hosted services inside them.

The playbook in this folder is effectively a service catalog: it creates base containers, configures them for SSH and basic runtime support, and then deploys one or more application stacks such as Homer, OpenBooks, Mosquitto, Shiori, Gotenberg, Paperless, and some backup automations.

## High-level flow

The typical lifecycle is:

1. Create a Proxmox LXC container using one of the base provisioning roles.
2. Bootstrap the container with SSH/Python/OS packages.
3. Add it into dynamic inventory.
4. Run a service-specific role to install the app and configure it as a system service.
5. For certain services, enable backup or archive tasks that export data, encrypt it, and sync it to cloud storage.

## Role inventory

### Base/container provisioning roles

- `proxmox_lxc_nodejs`
  - Creates an LXC container on Proxmox using the Proxmox API.
  - Starts the container and waits for it to obtain an IP address.
  - Adds the container to inventory and SSH known_hosts for later playbook stages.

- `proxmox_lxc_nodejs_config`
  - Bootstraps a generic dynamic LXC host after creation.
  - Installs Python, package dependencies, NodeSource repository, and Node.js.
  - Prepares the container so app-specific roles can run cleanly on Alpine/Ubuntu-based LXC targets.

- `proxmox_ubuntu`
  - Creates an Ubuntu-based LXC container with custom CPU, RAM, disk, swap, AppArmor, and feature settings.
  - Installs SSH and Python, then adds it to Ansible inventory.
  - Used for heavier services like Gotenberg and Paperless.

- `alpine_lxc_init`
  - Creates an Alpine-based LXC container for lightweight services.
  - Installs OpenSSH, Python, unzip, and starts the SSH daemon.
  - Common prerequisite role for application-specific Alpine deployments.

### Application deployment roles

- `openbooks_setup`
  - Installs [OpenBooks](https://evan-buss.github.io/openbooks/) on an Alpine LXC.
  - Creates the service user and runtime directory, downloads the binary, and registers an OpenRC init service.
  - Starts the OpenBooks web app as a background service.

- `homer_setup`
  - Deploys [Homer](https://homer-demo.netlify.app/), a dashboard/start page.
  - Installs dependencies, downloads the Homer release zip, copies custom icons/config, and runs a lightweight Python HTTP service.
  - Used to provide a home dashboard for internal links and bookmarks.

- `mosquitto_setup`
  - Installs and configures the [Mosquitto MQTT broker](https://github.com/eclipse-mosquitto/mosquitto).
  - Creates users/passwords, obtains a Let's Encrypt certificate, configures TLS, and runs Moquitto as a service.
  - Intended for self-hosted messaging and broker connectivity.

- `cloudflared`
  - Installs the [Cloudflare tunnel client](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/).
  - Creates the service user and config directory, stores the tunnel token securely, and runs cloudflared as a managed service.
  - Used to expose services through Cloudflare tunnels instead of direct inbound ports.

- `shiori_setup`
  - Installs [Shiori](https://github.com/go-shiori/shiori), a self-hosted bookmark manager.
  - Creates the service user, downloads the app archive, configures an init script, and starts the service.
  - Imports bookmarks from a Pocket export and marks the import as complete.

- `tika_setup`
  - Installs [Apache Tika](https://tika.apache.org/) server for document parsing and text extraction.
  - Creates the Tika user, downloads the Tika server JAR, and starts it as a service.
  - Used by Paperless and other document-processing pipelines.

- `gotenberg_setup`
  - Deploys [Gotenberg](https://gotenberg.dev/), a headless API for converting HTML/PDF documents.
  - Installs Docker tooling, creates the system service, and starts the Gotenberg process.
  - Used for PDF rendering and conversion tasks.

### Backup and archive roles

- `veracrypt_archive`
  - Creates a VeraCrypt-encrypted archive container for backups.
  - Validates the input directory, computes the required container size, creates the encrypted volume, mounts it, moves content in, and unmounts it.
  - Reusable helper for encrypted store-and-forward backup tasks.

- `bitwarden_backup`
  - Exports a Bitwarden vault, stages the result, wraps it in a VeraCrypt archive, and uploads it to OneDrive.
  - Handles secret validation, export, log in/out, and cleanup.
  - Intended for scheduled secure backup of credentials.

- `shiori_backup`
  - Pulls the Shiori SQLite database from the LXC, compresses the data, wraps it in a VeraCrypt archive, and uploads it to OneDrive.
  - Helps maintain a restorable backup of Shiori content and bookmarks.

- `paperless_samba`
  - Configures a Samba share for the Paperless consumption directory.
  - Creates the Samba user and share, applies ACLs, and ensures the share is available for uploads or drop-folder workflows.

### External integration used by the playbook

- `paperless_ngx.paperless_ngx`
  - This is not a folder under `roles/`, but it references this [ansible role](https://github.com/paperless-ngx/ansible) directly in the playbook.
  - Provisioning role for Paperless NGX itself, configured with OCR, Tika, Gotenberg, and SQLite-backed settings.

## Deployment pattern in this repo

The playbook mixes two broad patterns:

- LXC provisioning plays: create the host/container and add it to inventory.
- Service deployment plays: run app-specific role logic against the target host.

This makes the role bundle useful for a self-hosted homelab where each app gets its own purpose-built container, with backup and cloud-sync automation layered on top.

## Secrets & inventory files
There is an example secrets variable file in group_vars/secrets.example.yml with placeholder values so that (should you wnat to use these provisioning roles) you know what should be stored in the ansible-vault. 

There is also an inventory file that references the proxmox host values (for if you are provisioning multiple LXC containers in one proxmox instance) and some other inventory variables I used throughout my time working on this. I'm kind of bad at ansible organization, so ultimately you could probably just go without that file.