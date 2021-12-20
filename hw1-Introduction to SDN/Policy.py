import httplib
import json
import datetime

class flowStat(object):
    def __init__(self, server):
        self.server = server

    def get(self, switch):
        ret = self.rest_call({}, 'GET', switch)
        return json.loads(ret[2])

    def rest_call(self, data, action, switch):
        path = '/wm/core/switch/'+switch+"/flow/json"
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        #print path
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        conn.close()
        return ret

class StaticFlowPusher(object):
    def __init__(self, server):
        self.server = server

    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])

    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200

    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200

    def rest_call(self, data, action):
        path = '/wm/staticflowpusher/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        #print ret
        conn.close()
        return ret

pusher = StaticFlowPusher('127.0.0.1')
flowget = flowStat('127.0.0.1')

switchTable = {
    "1": "00:00:00:00:00:00:00:01",
    "2": "00:00:00:00:00:00:00:02",
    "3": "00:00:00:00:00:00:00:03"
}

hostIPTable = {
    "1": "10.0.0.1",
    "2": "10.0.0.2",
    "3": "10.0.0.3",
    "4": "10.0.0.4",
    "5": "10.0.0.5",
    "6": "10.0.0.6"
}

def createRule(switch: int,
               priority: int,
               in_port: int,
               ipv4_src_host_id: int,
               ipv4_dst_host_id: int,
               actions: str):

    time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    name = "S{switch}-H{src_host_id}toH{dst_host_id}-{time}"\
        .format(switch=switch, src_host_id=ipv4_src_host_id, dst_host_id=ipv4_dst_host_id, time=time)

    rule = {"cookie": "0", "eth_type": "0x800", "active": "true"}
    rule["switch"] = switchTable[str(switch)]
    rule["name"] = name
    rule["priority"] = str(priority)
    rule["in_port"] = str(in_port)
    rule["ipv4_src"] = hostIPTable[str(ipv4_src_host_id)]
    rule["ipv4_dst"] = hostIPTable[str(ipv4_dst_host_id)]
    rule["actions"] = actions

    return rule


# To insert the policies for the traffic applicable to path between S1 and S2
def S1toS2():

    ruleS1H2toH4 = createRule(switch=1, priority=2, in_port=4, 
        ipv4_src_host_id=2, ipv4_dst_host_id=4, actions="")
    ruleS1H2toH4["ip_proto"] = "0x11"

    ruleS1H4toH2 = createRule(switch=1, priority=2, in_port=1,
        ipv4_src_host_id=4, ipv4_dst_host_id=2, actions="")
    ruleS1H4toH2["ip_proto"] = "0x11"

    ruleS2H2toH4 = createRule(switch=2, priority=2, in_port=1,
        ipv4_src_host_id=2, ipv4_dst_host_id=4, actions="")
    ruleS2H2toH4["ip_proto"] = "0x11"

    ruleS2H4toH2 = createRule(switch=2, priority=2, in_port=3,
        ipv4_src_host_id=4, ipv4_dst_host_id=2, actions="")
    ruleS2H4toH2["ip_proto"] = "0x11"

    for port in range(1000,1101):
        ruleS1H2toH4["udp_dst"] = str(port)
        ruleS1H4toH2["udp_dst"] = str(port)
        ruleS2H2toH4["udp_dst"] = str(port)
        ruleS2H4toH2["udp_dst"] = str(port)
        pusher.set(ruleS1H2toH4)
        pusher.set(ruleS1H4toH2)
        pusher.set(ruleS2H2toH4)
        pusher.set(ruleS2H4toH2)

# To insert the policies for the traffic applicable to path between S2 and S3
def S2toS3():        
    pass
# To insert the policies for the traffic applicable to path between S1 and S3
def S1toS3():
    pass


def staticForwarding():
    # The lines below set a static route for the flow between h3 and h6. Note
    # that since traffci travels both ways, you will need to set 2 forwarding 
    # rules on each switch on the path.

    # Ports connected with hosts:
    # h1-3 h2-4 h3-3 h4-3 h5-4 h6-5

    # Available ports of switches:
    # s1: 1 2 3 4
    # s2: 1 2 3 4 5
    # s3: 1 2 3

    # Rules of S1
    S1RuleForh1Toh5 = createRule(switch=1, priority=1, in_port=3, 
        ipv4_src_host_id=1, ipv4_dst_host_id=5, actions="output=2")
    S1RuleForh5Toh1 = createRule(switch=1, priority=1, in_port=2, 
        ipv4_src_host_id=5, ipv4_dst_host_id=1, actions="output=3")


    S1RuleForh2Toh4 = createRule(switch=1, priority=1, in_port=4, 
        ipv4_src_host_id=2, ipv4_dst_host_id=4, actions="output=1")
    S1RuleForh4Toh2 = createRule(switch=1, priority=1, in_port=1, 
        ipv4_src_host_id=4, ipv4_dst_host_id=2, actions="output=4")

    # Rules of S2
    S2RuleForh2Toh4 = createRule(switch=2, priority=1, in_port=1, 
        ipv4_src_host_id=2, ipv4_dst_host_id=4, actions="output=3")
    S2RuleForh4Toh2 = createRule(switch=2, priority=1, in_port=3, 
        ipv4_src_host_id=4, ipv4_dst_host_id=2, actions="output=1")

    S2RuleForh1Toh5 = createRule(switch=2, priority=1, in_port=2, 
        ipv4_src_host_id=1, ipv4_dst_host_id=5, actions="output=4")
    S2RuleForh5Toh1 = createRule(switch=2, priority=1, in_port=4,
        ipv4_src_host_id=5, ipv4_dst_host_id=1, actions="output=2")

    S2RuleForh3Toh6 = createRule(switch=2, priority=1, in_port=2,
        ipv4_src_host_id=3, ipv4_dst_host_id=6, actions="output=5")
    S2RuleForh6Toh3 = createRule(switch=2, priority=1, in_port=5,
        ipv4_src_host_id=6, ipv4_dst_host_id=3, actions="output=2")

    # Rules of S3
    S3RuleForh1Toh5 = createRule(switch=3, priority=1, in_port=2,
        ipv4_src_host_id=1, ipv4_dst_host_id=5, actions="output=1")
    S3RuleForh5Toh1 = createRule(switch=3, priority=1, in_port=1,
        ipv4_src_host_id=5, ipv4_dst_host_id=1, actions="output=2")

    S3RuleForh3Toh6 = createRule(switch=3, priority=1, in_port=3,
        ipv4_src_host_id=3, ipv4_dst_host_id=6, actions="output=1")
    S3RuleForh6Toh3 = createRule(switch=3, priority=1, in_port=1,
        ipv4_src_host_id=6, ipv4_dst_host_id=3, actions="output=3")

    # Now, Insert the flows to the switches
    pusher.set(S1RuleForh1Toh5)
    pusher.set(S1RuleForh5Toh1)
    pusher.set(S1RuleForh2Toh4)
    pusher.set(S1RuleForh4Toh2)

    pusher.set(S2RuleForh2Toh4)
    pusher.set(S2RuleForh4Toh2)
    pusher.set(S2RuleForh1Toh5)
    pusher.set(S2RuleForh5Toh1)
    pusher.set(S2RuleForh3Toh6)
    pusher.set(S2RuleForh6Toh3)

    pusher.set(S3RuleForh1Toh5)
    pusher.set(S3RuleForh5Toh1)
    pusher.set(S3RuleForh3Toh6)
    pusher.set(S3RuleForh6Toh3)


if __name__ =='__main__':
    staticForwarding()
    S1toS2()
    S2toS3()
    S1toS3()
    pass