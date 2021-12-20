import httplib
import json
import time
import math

debug = True

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

if debug:
    flowgetInfo = flowget.get(switchTable["1"])
    flows = flowgetInfo["flows"]
    print(type(flowgetInfo))
    print(type(flows))
    flow = flows[0]
    print(type(flow))
    print(len(flows))
    print('---------FLOW----------------')
    for key in flow.keys():
        print(key)
    match = flow["match"]
    print('---------MATCH---------------')
    for key in match.keys():
        print(key)

# optional helper function for Rule #3
def Rule3Helper():
    S1BlockH1ToH5 = {'switch':"00:00:00:00:00:00:00:01","name":"S1Blockh1toh5","cookie":"0",
                    "priority":"3","in_port":"3","eth_type":"0x800","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.5","active":"true","actions":""}
    S1BlockH5ToH1 = {'switch':"00:00:00:00:00:00:00:01","name":"S1Blockh5toh1","cookie":"0",
                    "priority":"3","in_port":"2","eth_type":"0x800","ipv4_src":"10.0.0.5",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":""}

    S2BlockH1ToH5 = {'switch':"00:00:00:00:00:00:00:02","name":"S2Blockh1toh5","cookie":"0",
                    "priority":"3","in_port":"2","eth_type":"0x800","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.5","active":"true","actions":""}
    S2BlockH5ToH1 = {'switch':"00:00:00:00:00:00:00:02","name":"S2Blockh5toh1","cookie":"0",
                    "priority":"3","in_port":"4","eth_type":"0x800","ipv4_src":"10.0.0.5",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":""}

    S3BlockH1ToH5 = {'switch':"00:00:00:00:00:00:00:03","name":"S3Blockh1toh5","cookie":"0",
                    "priority":"3","in_port":"2","eth_type":"0x800","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.5","active":"true","actions":""}
    S3BlockH5ToH1 = {'switch':"00:00:00:00:00:00:00:03","name":"S3Blockh5toh1","cookie":"0",
                    "priority":"3","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.5",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":""}
            
    pusher.set(S1BlockH1ToH5)
    pusher.set(S1BlockH5ToH1)
    pusher.set(S2BlockH1ToH5)
    pusher.set(S2BlockH5ToH1)
    pusher.set(S3BlockH1ToH5)
    pusher.set(S3BlockH5ToH1)

# To insert the policies for Rule #1
def Rule1():
    S3Rule1Forh3Toh6 = {'switch':"00:00:00:00:00:00:00:03","name":"S3R1h3toh6","cookie":"0",
                    "priority":"2","in_port":"3","eth_type":"0x800","ipv4_src":"10.0.0.3",
                    "ipv4_dst":"10.0.0.6","active":"true","actions":"output=1,set_queue=1"}
    S3Rule1Forh6Toh3 = {'switch':"00:00:00:00:00:00:00:03","name":"S3R1h6toh3","cookie":"0",
                    "priority":"2","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.6",
                    "ipv4_dst":"10.0.0.3","active":"true","actions":"output=3,set_queue=1"}

    S2Rule1Forh3Toh6 = {'switch':"00:00:00:00:00:00:00:02","name":"S2R1h3toh6","cookie":"0",
                    "priority":"2","in_port":"2","eth_type":"0x800","ipv4_src":"10.0.0.3",
                    "ipv4_dst":"10.0.0.6","active":"true","actions":"output=5,set_queue=1"}
    S2Rule1Forh6Toh3 = {'switch':"00:00:00:00:00:00:00:02","name":"S2R1h6toh3","cookie":"0",
                    "priority":"2","in_port":"5","eth_type":"0x800","ipv4_src":"10.0.0.6",
                    "ipv4_dst":"10.0.0.3","active":"true","actions":"output=2,set_queue=1"}
    pusher.set(S3Rule1Forh3Toh6)
    pusher.set(S3Rule1Forh6Toh3)
    pusher.set(S2Rule1Forh3Toh6)
    pusher.set(S2Rule1Forh6Toh3)

# To insert the policies for Rule #2
def Rule2():
    for port in range(1000, 1101):
        S1Rule2Forh2Toh4 = {'switch':"00:00:00:00:00:00:00:01","cookie":"0",
                    "ip_proto":"0x11","priority":"2","in_port":"4","eth_type":"0x800","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.4","active":"true","actions":""}
        S1Rule2Forh2Toh4["name"] = "S1R2h2toh4-{udp_port}".format(udp_port=port)
        S1Rule2Forh2Toh4["udp_dst"] = str(port)

        S1Rule2Forh4Toh2 = {'switch':"00:00:00:00:00:00:00:01","cookie":"0",
                    "ip_proto":"0x11","priority":"2","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.4",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":""}
        S1Rule2Forh4Toh2["name"] = "S1R2h4toh2-{udp_port}".format(udp_port=port)
        S1Rule2Forh4Toh2["udp_dst"] = str(port)

        S2Rule2Forh2Toh4 = {'switch':"00:00:00:00:00:00:00:02","cookie":"0",
                    "ip_proto":"0x11","priority":"2","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.4","active":"true","actions":""}
        S2Rule2Forh2Toh4["name"] = "S2R2h2toh4-{udp_port}".format(udp_port=port)
        S2Rule2Forh2Toh4["udp_dst"] = str(port)

        S2Rule2Forh4Toh2 = {'switch':"00:00:00:00:00:00:00:02","cookie":"0",
                    "ip_proto":"0x11","priority":"2","in_port":"3","eth_type":"0x800","ipv4_src":"10.0.0.4",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":""}
        S2Rule2Forh4Toh2["name"] = "S2R2h4toh2-{udp_port}".format(udp_port=port)
        S2Rule2Forh4Toh2["udp_dst"] = str(port)

        pusher.set(S1Rule2Forh2Toh4)
        pusher.set(S1Rule2Forh4Toh2)
        pusher.set(S2Rule2Forh2Toh4)
        pusher.set(S2Rule2Forh4Toh2)

# To insert the policies for Rule #3
def Rule3():
    packetLimitH1ToH5 = 100000000.0 / 1500.0  # 100MB data, 1500 bytes each packet
    packetSentBetweenH1andH5 = 0
    # track the total packets between h1 and h5 every second
    while(True):
        flowsInfo = flowget.get(switchTable["1"])
        flows = flowsInfo["flows"]
        # print(type(flows)) # list
        packetCountFromH1ToH5 = 0
        packetCountFromH5ToH1 = 0
        for flow in flows:
            if "match" in flow.keys():
                match = flow["match"]
                # print(match)
                if "ipv4_src" in match.keys() and "ipv4_dst" in match.keys():
                    src = match["ipv4_src"]
                    dst = match["ipv4_dst"]
                    if src == hostIPTable["1"] and dst == hostIPTable["5"]:
                        packetCount = int(flow["packetCount"])
                        if debug:
                            print('packetCount from h1 to h5: ', packetCount)
                        packetCountFromH1ToH5 += packetCount
                    if src == hostIPTable["5"] and dst == hostIPTable["1"]:
                        packetCount = int(flow["packetCount"])
                        if debug:
                            print('packetCount from h5 to h1: ', packetCount)
                        packetCountFromH5ToH1 += packetCount
        packetSentBetweenH1andH5 = packetCountFromH1ToH5 + packetCountFromH5ToH1
        if debug:
            print('------Packets sent between h1 and h5: ', packetSentBetweenH1andH5)

        # If the number of packets sent between h1 and h5 reached the threshold, 
        # block the link between h1 and h5
        if packetSentBetweenH1andH5 >= math.floor(packetLimitH1ToH5):
            Rule3Helper()
            if debug:
                print('-------Packets sent between h1 and h5 reached %d, blocked!' %packetSentBetweenH1andH5)
            break
        time.sleep(1)


def staticForwarding():
    # The lines below set a static route for the flow between h3 and h6. Note
    # that since traffci travels both ways, you will need to set 2 forwarding 
    # rules on each switch on the path.
    
    # Rules of S1
    S1RuleForh1Toh5 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h1toh5","cookie":"0",
                    "priority":"1","in_port":"3","eth_type":"0x800","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.5","active":"true","actions":"output=2"}
    S1RuleForh5Toh1 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h5toh1","cookie":"0",
                    "priority":"1","in_port":"2","eth_type":"0x800","ipv4_src":"10.0.0.5",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=3"}

    S1RuleForh2Toh4 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h2toh4","cookie":"0",
                    "priority":"1","in_port":"4","eth_type":"0x800","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.4","active":"true","actions":"output=1"}
    S1RuleForh4Toh2 = {'switch':"00:00:00:00:00:00:00:01","name":"S1h4toh2","cookie":"0",
                    "priority":"1","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.4",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":"output=4"}

    # Rules of S2
    S2RuleForh2Toh4 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h2toh4","cookie":"0",
                    "priority":"1","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.2",
                    "ipv4_dst":"10.0.0.4","active":"true","actions":"output=3"}
    S2RuleForh4Toh2 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h4toh2","cookie":"0",
                    "priority":"1","in_port":"3","eth_type":"0x800","ipv4_src":"10.0.0.4",
                    "ipv4_dst":"10.0.0.2","active":"true","actions":"output=1"}

    S2RuleForh1Toh5 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h1toh5","cookie":"0",
                    "priority":"1","in_port":"2","eth_type":"0x800","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.5","active":"true","actions":"output=4"}
    S2RuleForh5Toh1 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h5toh1","cookie":"0",
                    "priority":"1","in_port":"4","eth_type":"0x800","ipv4_src":"10.0.0.5",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=2"}

    S2RuleForh3Toh6 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h3toh6","cookie":"0",
                    "priority":"1","in_port":"2","eth_type":"0x800","ipv4_src":"10.0.0.3",
                    "ipv4_dst":"10.0.0.6","active":"true","actions":"output=5"}
    S2RuleForh6Toh3 = {'switch':"00:00:00:00:00:00:00:02","name":"S2h6toh3","cookie":"0",
                    "priority":"1","in_port":"5","eth_type":"0x800","ipv4_src":"10.0.0.6",
                    "ipv4_dst":"10.0.0.3","active":"true","actions":"output=2"}

    # Rules of S3
    S3RuleForh1Toh5 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h1toh5","cookie":"0",
                    "priority":"1","in_port":"2","eth_type":"0x800","ipv4_src":"10.0.0.1",
                    "ipv4_dst":"10.0.0.5","active":"true","actions":"output=1"}
    S3RuleForh5Toh1 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h5toh1","cookie":"0",
                    "priority":"1","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.5",
                    "ipv4_dst":"10.0.0.1","active":"true","actions":"output=2"}

    S3RuleForh3Toh6 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h3toh6","cookie":"0",
                    "priority":"1","in_port":"3","eth_type":"0x800","ipv4_src":"10.0.0.3",
                    "ipv4_dst":"10.0.0.6","active":"true","actions":"output=1"}
    S3RuleForh6Toh3 = {'switch':"00:00:00:00:00:00:00:03","name":"S3h6toh3","cookie":"0",
                    "priority":"1","in_port":"1","eth_type":"0x800","ipv4_src":"10.0.0.6",
                    "ipv4_dst":"10.0.0.3","active":"true","actions":"output=3"}

    #Now, Insert the flows to the switches
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
    Rule1()
    Rule2()
    Rule3()
    pass