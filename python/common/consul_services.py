import consul
from dns import resolver


def consul_register(service_name, port, address = '127.0.0.1'):
    print('register started of {}, addr={}, port={}'.format(service_name, address, port))
    c = consul.Consul()
    check = consul.Check.tcp(address, port, '30s')
    c.agent.service.register(service_name, service_name + '-' + str(port), address=address, port=port)#, check=check)
    #print('services: ' + str(c.agent.services()))


def consul_unregister(service_name, port):
    print('unregister started of ' + service_name)
    c = consul.Consul()
    c.agent.service.deregister(service_name + '-' + str(port))
    print('unregistered ' + service_name)
    #print("services: " + str(c.agent.services()))


def consul_find_service(service_name, address = '127.0.0.1'):
    consul_resolver = resolver.Resolver()
    consul_resolver.port = 8600
    consul_resolver.nameservers = [address]

    dnsanswer = consul_resolver.query(service_name + '.service.consul', 'A')
    ip = str(dnsanswer[0])
    dnsanswer_srv = consul_resolver.query(service_name + '.service.consul', 'SRV')
    ports = []
    for srv in dnsanswer_srv:
        ports.append(int(str(srv).split()[2]))

    print('Found service "{}" at ip:{} ports:{} using consul'.format(service_name, ip, ', '.join([str(p) for p in ports])))

    return (ip,ports)


