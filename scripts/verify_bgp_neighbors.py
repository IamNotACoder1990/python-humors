from netmiko import ConnectHandler

def check_bgp(router):
    conn = ConnectHandler(**router)
    output = conn.send_command("show ip bgp summary")
    print(output)
    conn.disconnect()

# Example device:
# router = {"device_type": "cisco_ios", "host": "10.1.1.1", "username": "admin", "password": "pass"}
