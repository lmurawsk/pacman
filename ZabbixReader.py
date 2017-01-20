#!/usr/bin/env python

""" ZabbixReader.py: Delivery class that read data from zabbix monitoring system."""

__author__      = "Karol Kaczan"


from zabbix.api import ZabbixAPI
import json
import pprint



class ZabbixReader():
    """ Read data from Zabbix monitoring system"""

    def __init__(self,_url, _user, _password):
        url = _url
        user = _user
        password = _password
        try:       
            self.zapi =  ZabbixAPI(url=url, user=user, password=password)
        except Exception as e:
            print 'Error in creating connection to Zabbix Api (%s)' % (url)
            raise Exception(e)


    def get_stats_from_hname_json(self, _hname):
        """ Gets all items stats from defined hname """
        host_groups = self.get_gnames_from_hname(_hname)
        print "Start get stats for hname: %s" % (_hname)
        results = []

        iobjects = self.get_iobj_from_hname(_hname)
        print "Start stats for hname [%s]" % (_hname)
        for item in iobjects:
            metric_name = item['name']
            for value in self.get_stats_for_iid(item['itemid']):
                json_body = {
                            "measurement": "zabbix_data",
                            "tags": {
                                "client": str(host_groups),
                                "device": _hname,
                                "itemid": value['itemid']
                                },
                            "time": int(value['clock']),
                            "fields": {
                                metric_name: float(value['value'])
                                }
                        }
                results.append(json_body)
            print metric_name, " done."
        to_return = json.dumps(results)
        return to_return
    

    def get_stats_from_gname_json(self, _gname):
        """ Gets all items stats from defined gname"""
        client_devices = self.get_hnames_from_gname(_gname)
        print "Start get stats for gname [%s], hosts: %s" % (_gname, client_devices)
        results = []
        for device in client_devices:
            iobjects = self.get_iobj_from_hname(device)
            print "Start stats for hname [%s]" % (device)
            for item in iobjects:
                metric_name = item['name']
                for value in self.get_stats_for_iid(item['itemid']):
                    json_body = {
                            "measurement": "zabbix_data",
                            "tags": {
                                "client": _gname,
                                "device": device,
                                "itemid": value['itemid']
                                },
                            "time": int(value['clock']),
                            "fields": {
                                metric_name: float(value['value'])
                                }
                            }
                    results.append(json_body)
                print metric_name, " done."
        to_return = json.dumps(results)
        return to_return


    def get_gnames_from_hname(self, _hname):
        """ Get gnames [] from host name """
        hid = self.get_hid_from_hname(_hname)
        result_groups = self.zapi.do_request('hostgroup.get',
            {
                "hostids": hid
            })
        group_names = [group['name'] for group in result_groups['result']]
        return group_names


    def get_iobj_from_hname(self, _host_name):
        """ Gets items ids [] from host defined by name """
        hostid = self.get_hid_from_hname(_host_name)
        result_items= self.zapi.do_request('item.get',
            {
            "hostids":hostid,
            "output": "extend",
            "sortfield": "name"
            }
        )
        return result_items['result']


    def get_stats_for_iid(self, _iid, _limit=1):
        """ Gets history data for specific item defined by id"""
        result_hist_item= self.zapi.do_request('history.get',
            {
            "output": "extend",
            "history": 0,
            "itemids": _iid,
            "sortfield": "clock",
            "sortorder": "DESC",
            "limit": _limit
            }
        )
        return result_hist_item['result']


    def get_iids_from_hname(self, _host_name):
        """ Gets items ids [] from host defined by name """
        hostid = self.get_hid_from_hname(_host_name)
        result_items= self.zapi.do_request('item.get',
            {
            "hostids":hostid,
            "output": "extend",
            "sortfield": "name"
            }
        )
        return [items['itemid'] for items in result_items['result']]


    def get_inames_from_hname(self, _host_name):
        """ Gets items names [] from host defined by name """
        hostid = self.get_hid_from_hname(_host_name)
        result_items= self.zapi.do_request('item.get',
            {
            "hostids":hostid,
            "output": "extend",
            "sortfield": "name"
            }
        )
        return [items['name'] for items in result_items['result']]


    def get_hid_from_hname(self, _host_name):
        """ Get host id (unicode) from host name """
        result_hosts = self.zapi.do_request('host.get',
            {
                "filter": {
                    "name":_host_name
                }
            })
        host_id = [host['hostid'] for host in result_hosts['result']]
        return host_id[0]


    def get_hids_from_gname(self, _group_name): 
        """ Get hosts ids [] from group defined by name """
        gid = self.get_gid_from_gname(_group_name)                  # search id for group name
        result_hosts_in_group = self.zapi.do_request('host.get',
            {
            "groupids":gid
            })
        return [hosts['hostid'] for hosts in result_hosts_in_group['result']]
  

    def get_hnames_from_gname(self, _group_name): 
        """ Get hosts names [] from group defined by name """
        gid = self.get_gid_from_gname(_group_name)                  # search id for group name
        result_hosts_in_group = self.zapi.do_request('host.get',
            {
            "groupids":gid
            })
        return [hosts['name'] for hosts in result_hosts_in_group['result']]


    def get_gid_from_gname(self, _group_name):
        """ Get group id (unicode) from group name """
        result_groups = self.zapi.do_request('hostgroup.get',
            {
                "filter": {
                    "name":_group_name
                }
            })
        group_id = [group['groupid'] for group in result_groups['result']]
        return group_id[0]

##############################################################################

def main():
    print "You have run ZabbixReader package. Please use ZabbixReader class"
    print "from ZabbixReader import ZabbixReader"
    print "zr = ZabbixReader(zab_url, zab_user, zab_password)"
    pass

if __name__ == '__main__':
    main()


