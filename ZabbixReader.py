#!/usr/bin/env python

""" ZabbixReader.py: Delivery class that read data from zabbix monitoring system. """

__author__      = "Karol Kaczan"
__version__		= "v0.2"

# #########################
# Store version change here
# #########################
# 10/03/2017 - Parse item name to TAGS[metric_name, interface, location]
#
#

from zabbix.api import ZabbixAPI
import json
import re



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

        self.metric_names_regex = [
				'^(ICMP loss).*'
				,'^(ICMP ping).*'
				,'^(ICMP response time).*'
				,'^(Incoming traffic) on interface (\S+) \(CORP-(\S+)[-_]{1}LINKID.*'
				,'^(Outgoing traffic) on interface (\S+) \(CORP-(\S+)[-_]{1}LINKID.*'
				,'^(In utilization) on (\S+) \(CORP-(\S+)[-_]{1}LINKID.*'
				,'^(Out utilization) on (\S+) \(CORP-(\S+)[-_]{1}LINKID.*'
				,'^(Inbound errors) on interface (\S+) \(CORP-(\S+)[-_]{1}LINKID.*'
				,'^(Outbound errors) on interface (\S+) \(CORP-(\S+)[-_]{1}LINKID.*'
				,'^(Percentage inbound errors) on interface (\S+) \(CORP-(\S+)[-_]{1}LINKID.*'
				,'^(Percentage outbound errors) on interface (\S+) \(CORP-(\S+)[-_]{1}LINKID.*'
				,'^(Incoming unicast packets) on interface (\S+) \(CORP-(\S+)[-_]{1}LINKID.*'
				,'^(Outcoming unicast packets) on interface (\S+) \(CORP-(\S+)[-_]{1}LINKID.*'
				,'^(Admin status) of interface (\S+) \(CORP-(\S+)[-_]{1}LINKID.*'
                ,'^(Jitter) for CORP-.* (?:IBM-0-|1-0-).*'
                ,'^(Packet Delay) for CORP-.* (?:IBM-0-|1-0-).*'
                ,'^(Packet loss) for CORP.* (?:IBM-0-|1-0-).*'
			]


    def get_stats_from_hname_json(self, _hname):
        """ Gets all items stats from defined hname """
        host_groups = self.get_gnames_from_hname(_hname)
        print "Start get stats for hname: %s" % (_hname)
        results = []
        iobjects = self.get_iobj_from_hname(_hname)
        print "Start stats for hname [%s]" % (_hname)
        for item in iobjects:
	    tags = self.parseNameToTags(item['key_'], item['name'])
	    if tags is None:
	        continue
            metric_name = tags['metric_name']
	    interface = tags['interface']
	    location = tags['location']
	    if len(location) == 0:
                location = self.getLocationFromHostName(_hname)
	    for history in self.get_stats_for_iid(item['itemid'], item['value_type']):
                # parse history based on data type
                # 0 - numeric float, 3 - numeric unsigned
                if item['value_type'] in ['0','3']:
                    value = float(history['value'])
                else:
		    value = history['value']
		json_body = {
                                "measurement": "zabbix_data",
                                "tags": {
                                    "client": str(host_groups),
                                    "device": _hname,
				    "interface": interface,
				    "location": location,
                                    "itemid": history['itemid']
                                        },
                                "time": int(history['clock']),
                                "fields": {
                                    metric_name: value
                                }
                                        }
		print json_body
		results.append(json_body)
        to_return = json.dumps(results)
        return to_return
    

    def get_stats_from_gname_json(self, _gname):
        """ Gets all items stats from defined gname
            return json with statistics
        """
        
        client_devices = self.get_hnames_from_gname(_gname)
        print "Start get stats for gname [%s], hosts: %s" % (_gname, client_devices)
        results = []
        for device in client_devices:
            iobjects = self.get_iobj_from_hname(device)
            print "Start stats for hname [%s]" % (device)
            for item in iobjects:
		tags = self.parseNameToTags(item['key_'], item['name'])
	        if tags is None:
	            continue
		metric_name = tags['metric_name']
		interface = tags['interface']
		location = tags['location']
		if len(location) == 0:
                    location = self.getLocationFromHostName(device)
		for history in self.get_stats_for_iid(item['itemid'], item['value_type']):

                    # parse history based on data type
                    # 0 - numeric float, 3 - numeric unsigned
		    if item['value_type'] in ['0','3']:
		    	value = float(history['value'])
		    else:
		        value = history['value']
                    json_body = {
                                "measurement": "zabbix_data",
                                "tags": {
                                    "client": _gname,
                                    "device": device,
				    "interface": interface,
				    "location": location,
                                    "itemid": history['itemid']
                                        },
                                "time": int(history['clock']),
                                "fields": {
                                    metric_name: value
                                }
		    				}
                    print json_body
                    results.append(json_body)
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

		
    def get_stats_for_iid(self, _iid, _value_type, _limit=10):
        """ Gets history data for specific item defined by id"""
        result_hist_item= self.zapi.do_request('history.get',
            {
            "output": "extend",
            "history": _value_type,
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
        gid = self.get_gid_from_gname(_group_name)                  
        result_hosts_in_group = self.zapi.do_request('host.get',
            {
            "groupids":gid
            })
        return [hosts['hostid'] for hosts in result_hosts_in_group['result']]
  

    def get_hnames_from_gname(self, _group_name): 
        """ Get hosts names [] from group defined by name """
        gid = self.get_gid_from_gname(_group_name)                  
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

		
    def parseVariableInItemName(self, _ikey, _iname):
	    """ Change item name based on algorithm and variable value
	    	Sample item name: Out Traffic $1 Warsaw 
	    	Action: $1 should be replace with param nr 1 from key_ (key_=keyname[param1, param2,...])
	    """
	
	    var_num = ''
	    param = ''
	    new_name = '?'
	
	    # looking for variable in item name (ex. $1, $2...)
	    var_match = re.search('.*\$([1-9]){1}.*',_iname)
	
	    # if variable not exist do nothing with name
	    if var_match is None:
	    	return _iname
	
	    # read variable value
	    try:
	    	var_num = int(var_match.group(1))
	    except:
	    	# do nothing if there is no group 1 matched - value not readable
	    	return _iname
	
	    # get param from key[var_num]
	    key_match = re.search('.*\[(.*)]',_ikey)
	    if key_match is None:
	    	param = '???'
	    try:
	    	param = key_match.group(1).split(',')[var_num - 1] # list starts from 0
	    except Exception as e:
	        print e
	    	param = '????'
	
	    # replace $var_num with key param number var_num
	    to_replace = '$'+str(var_num)
	    new_name = _iname.replace(to_replace,param)
	    return new_name

		
    def parseNameToTags(self, _ikey, _iname):
		
		tag_dic = {'metric_name':'', 'interface':'', 'location':''}
		metric_name = self.parseVariableInItemName(_ikey, _iname)
		# print 'metric name: ', metric_name
		for metric_regex in self.metric_names_regex:
		        match = re.search(metric_regex,metric_name)

			if match is not None:
				print 'Metric name in regex: ', metric_regex
				try:
					print 'group 1: %s' % match.group(1) # metric_name
					tag_dic['metric_name'] = match.group(1)
				except IndexError as ie:
					print 'Error in metric name: group number invalid'
					print ie
				try:
					print 'group 2: %s' % match.group(2) # interface
					print 'group 3: %s' % match.group(3) # location
					tag_dic['interface'] = match.group(2)
					tag_dic['location'] = match.group(3)
				except IndexError as ie:
					print 'No interface or location: group number invalid'
					print ie
				break
                if match is None:
		        print 'METRIC: %s do not match any pattern' % metric_name
                        return None
		
		#print tag_dic
		return tag_dic

    def getLocationFromHostName(self, _hname):
        """ gets name for metric which don't have name """

        # get all items names from hname
        metric_names = self.get_inames_from_hname(_hname)

        # looking for location name
        location = ''
        for metric_name in metric_names:
            for metric_regex in self.metric_names_regex:
                match = re.search(metric_regex, metric_name)
                if match is not None:
                    try:
                        location = match.group(3)
                    except IndexError as ie:
                        pass
                    else:
                        return location
		else:
			print 'TAG::location not set for %s' % _hname
            return location

    			
##############################################################################

def main():
    print "You have run ZabbixReader package. Please use ZabbixReader class"
    print "from ZabbixReader import ZabbixReader"
    print "zr = ZabbixReader(zab_url, zab_user, zab_password)"
    pass

if __name__ == '__main__':
    main()


