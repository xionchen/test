import yaml
AZ0_NAME='AZ0'
AZ1_NAME='AZ1'
AZ2_NAME='AZ2'

component_list = ['neutron-server','nova-api']

def get_component_ip_mapper():
    return {'neutron-server':['8.10.53.39','8.13.3.39','8.10.3.39'],
            'nova-api':['8.10.53.39','8.13.3.39','8.10.3.39']}

def get_component_service_mapper():
    service_component_mapper = {'neutron':['neutron-server','neutron-dhcp-agent'],'nova':['nova-api']}
    print service_component_mapper
    component_service_mapper = {}
    for service,component_list in service_component_mapper.items():
        for component in component_list:
            component_service_mapper[component] = service
    return component_service_mapper

def get_component_iscascading_mapper():
    return {'neutron-server': True,'nova-api':False}

def get_AZ_by_ip(ip):
    if '8.10.53.' in ip:
        return AZ0_NAME
    elif '8.13.3' in ip:
        return AZ1_NAME
    elif '8.10.3' in ip:
        return AZ2_NAME



if __name__ == '__main__':
    component_iscascading_mapper = get_component_iscascading_mapper()
    component_service_mapper = get_component_service_mapper()
    component_ip_mapper = get_component_ip_mapper()

    fd_info = []
    for component,iscascading in component_iscascading_mapper.items():
        component_info = {}
        component_info['template_name'] = component
        service = component_service_mapper[component]
        component_info['service'] = service
        ip_list = component_ip_mapper[component]
        if iscascading:
            component_info_cascading = component_info.copy()
            component_info_cascaded = component_info.copy()
            AZ_distrubtion = [(get_AZ_by_ip(ip),ip) for ip in ip_list]

            meet_AZ = set()

            for (AZ_name, ip) in AZ_distrubtion:
                if AZ_name not in meet_AZ:
                    meet_AZ.add(AZ_name)
                else:
                    continue

                if AZ_name == AZ0_NAME:
                    component_info_cascading['fd_name'] = 'cascading-%s-%s' % (service, component)
                    component_info_cascading['env_list'] = []
                    env = {'name':AZ_name,'ip':ip}
                    component_info_cascading['env_list'].append(env)
                    continue

                else:
                    component_info_cascaded['fd_name'] = 'cascaded-%s-%s' % (service, component)
                    env = {'name':AZ_name,'ip':ip}
                    component_info_cascaded.setdefault('env_list',[]).append(env)

            if component_info_cascading.get('fd_name'):
                fd_info.append(component_info_cascading)
            if component_info_cascaded.get('fd_name'):
                fd_info.append(component_info_cascaded)
        else:
            component_info['fd_name'] = component
            AZ_distrubtion = [(get_AZ_by_ip(ip),ip) for ip in ip_list]
            meet_AZ = set()

            for (AZ_name, ip) in AZ_distrubtion:
                if AZ_name not in meet_AZ:
                    meet_AZ.add(AZ_name)
                else:
                    continue

                env = {'name':AZ0_NAME,'ip':ip}
                component_info.setdefault('env_list',[]).append(env)
            fd_info.append(component_info)
    print yaml.dump(fd_info, default_flow_style=False)
