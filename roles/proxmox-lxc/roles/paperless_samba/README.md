paperless_samba
===============

Configures Samba on the Paperless container and exposes a writable share mapped to the Paperless consumption directory.

Required variable
-----------------
- paperless_samba_password

Important defaults
------------------
- paperless_samba_path: /var/lib/paperless-ngx/consume
- paperless_samba_share_name: paperless-drop
- paperless_samba_user: paperlessdrop
- paperless_samba_group: paperlessngx