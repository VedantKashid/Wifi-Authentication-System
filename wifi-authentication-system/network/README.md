# WiFi / Captive Portal Integration

The upgraded Flask application is the authentication layer of the project. A real WiFi deployment should use an authorized Linux gateway/access point and enforce network policy at that gateway.

Recommended lab architecture:

`WiFi client -> access point/gateway -> captive portal -> Flask -> SQLite`

Typical components:

- hostapd: access point
- dnsmasq: DHCP/DNS
- firewall/gateway: traffic policy
- Flask: authentication portal
- SQLite: authentication records

The UI's WiFi status and signal indicators are currently presentation/demo elements. They do not claim to measure radio signal strength from the host machine.

Do not copy firewall or captive-portal rules from the Internet without adapting and reviewing them for your own lab. Test only on networks you own or are authorized to administer.
