# Velveta Frappe Upstream Base Image

This repository builds and maintains the base upstream Frappe framework, ERPNext, and core add-on applications for Velveta production and development environments.

## Included Components
- **OS**: Debian 12 (Bookworm) Slim
- **Python**: 3.14
- **Node.js**: 22.14.0 (with Yarn)
- **PDF Engine**: wkhtmltopdf 0.12.6.1
- **Web Server**: Nginx with templated Frappe reverse-proxy configuration
- **Upstream Apps**:
  - `frappe/frappe` (`version-16`)
  - `frappe/erpnext` (`version-16`)
  - `frappe/payments` (`develop`)
  - `frappe/blog` (`version-16`)
  - `frappe/drive` (`develop`)
  - `frappe/writer` (`develop`)

## Output Artifacts
- `ghcr.io/antonio-etemadi/velveta-frappe-upstream:latest`
- `ghcr.io/antonio-etemadi/velveta-frappe-upstream:<commit-sha>`
