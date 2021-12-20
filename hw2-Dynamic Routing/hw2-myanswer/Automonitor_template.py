#!/usr/bin/python

import httplib
import json
from time import sleep
import time
import Policy1, Policy2, Policy3

debug = False

class flowStat(object):
    def __init__(self, server):
        self.server = server

    def get(self, switch,statType):
        ret,resTime = self.rest_call({}, 'GET', switch,statType)
        return json.loads(ret[2]),resTime

    def rest_call(self, data, action, switch,statType):
        path = '/wm/core/switch/'+switch+"/"+statType+"/json"
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        #print path
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        resTime = time.time()
        ret = (response.status, response.reason, response.read())
        conn.close()
        return ret,resTime

def monitor(policy):
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
        "5": "10.0.0.5"
    }

    bwS1toS3 = 100 * 1000000 / 8.0      # bandwidth S1-S3 in bytes/s
    bwS2toS3 = 100 * 1000000 / 8.0      # bandwidth S2-S3 in bytes/s

    retS1 = flowget.get(switchTable["1"], "flow")
    flowInfoS1, resTimeS1 = retS1[0], retS1[1]

    retS2 = flowget.get(switchTable["2"], "flow")
    flowInfoS2, resTimeS2 = retS2[0], retS2[1]

    retS3 = flowget.get(switchTable["3"], "flow")
    flowInfoS3, resTimeS3 = retS3[0], retS3[1]
        
    flowsS1, flowsS2, flowsS3 = flowInfoS1["flows"], flowInfoS2["flows"], flowInfoS3["flows"]

    # initialize counters
    byteCountS1toS3, packetCountS1toS3 = 0, 0
    for flow in flowsS1:
        if "match" in flow.keys():
            match = flow["match"]
            if "ipv4_dst" in match.keys():
                dst = match["ipv4_dst"]
                if dst == hostIPTable["3"] or dst == hostIPTable["4"] or dst == hostIPTable["5"]:
                    byteCountS1toS3 += int(flow["byteCount"])
                    packetCountS1toS3 += int(flow["packetCount"])
        
    byteCountS2toS3, pakcetCountS2toS3 = 0, 0
    for flow in flowsS2:
        if "match" in flow.keys():
            match = flow["match"]
            if "ipv4_dst" in match.keys():
                dst = match["ipv4_dst"]
                if dst == hostIPTable["3"] or dst == hostIPTable["4"] or dst == hostIPTable["5"]:
                    byteCountS2toS3 += int(flow["byteCount"])
                    pakcetCountS2toS3 += int(flow["packetCount"])

    packetCountS3FromS1, packetCountS3FromS2 = 0, 0
    byteCountS3toH3 = 0
    for flow in flowsS3:
        if "match" in flow.keys():
            match = flow["match"]
            if "ipv4_src" in match.keys() and "ipv4_dst" in match.keys():
                src, dst = match["ipv4_src"], match["ipv4_dst"]
                if src == hostIPTable["1"] \
                and (dst == hostIPTable["3"] or dst == hostIPTable["4"] or dst == hostIPTable["5"]):
                    packetCountS3FromS1 += int(flow["packetCount"])
                if src == hostIPTable["2"] \
                and (dst == hostIPTable["3"] or dst == hostIPTable["4"] or dst == hostIPTable["5"]):
                    packetCountS3FromS2 += int(flow["packetCount"])
                if dst == hostIPTable["3"]:
                    byteCountS3toH3 += int(flow["byteCount"])

    byteCountS1toS3_lastCount = byteCountS1toS3
    byteCountS2toS3_lastCount = byteCountS2toS3
    byteCountS3toH3_lastCount = byteCountS3toH3

    packetCountS1_lastCount = packetCountS1toS3
    packetCountS2_lastCount = pakcetCountS2toS3
    packetCountS3FromS1_lastCount = packetCountS3FromS1
    packetCountS3FromS2_lastCount = packetCountS3FromS2

    while(True):
        timeInterval = 1.0      # count every 1.0 second
        time.sleep(timeInterval)

        retS1 = flowget.get(switchTable["1"], "flow")
        flowInfoS1, resTimeS1 = retS1[0], retS1[1]

        retS2 = flowget.get(switchTable["2"], "flow")
        flowInfoS2, resTimeS2 = retS2[0], retS2[1]

        retS3 = flowget.get(switchTable["3"], "flow")
        flowInfoS3, resTimeS3 = retS3[0], retS3[1]
        
        flowsS1, flowsS2, flowsS3 = flowInfoS1["flows"], flowInfoS2["flows"], flowInfoS3["flows"]
    
    
        byteCountS1toS3, packetCountS1toS3 = 0, 0
        for flow in flowsS1:
            if "match" in flow.keys():
                match = flow["match"]
                if "ipv4_dst" in match.keys():
                    dst = match["ipv4_dst"]
                    if dst == hostIPTable["3"] or dst == hostIPTable["4"] or dst == hostIPTable["5"]:
                        byteCountS1toS3 += int(flow["byteCount"])
                        packetCountS1toS3 += int(flow["packetCount"])
        
        byteCountS2toS3, pakcetCountS2toS3 = 0, 0
        for flow in flowsS2:
            if "match" in flow.keys():
                match = flow["match"]
                if "ipv4_dst" in match.keys():
                    dst = match["ipv4_dst"]
                    if dst == hostIPTable["3"] or dst == hostIPTable["4"] or dst == hostIPTable["5"]:
                        byteCountS2toS3 += int(flow["byteCount"])
                        pakcetCountS2toS3 += int(flow["packetCount"])

        packetCountS3FromS1, packetCountS3FromS2 = 0, 0
        byteCountS3toH3 = 0
        for flow in flowsS3:
            if "match" in flow.keys():
                match = flow["match"]
                if "ipv4_src" in match.keys() and "ipv4_dst" in match.keys():
                    src, dst = match["ipv4_src"], match["ipv4_dst"]
                    if src == hostIPTable["1"] \
                    and (dst == hostIPTable["3"] or dst == hostIPTable["4"] or dst == hostIPTable["5"]):
                        packetCountS3FromS1 += int(flow["packetCount"])
                    if src == hostIPTable["2"] \
                    and (dst == hostIPTable["3"] or dst == hostIPTable["4"] or dst == hostIPTable["5"]):
                        packetCountS3FromS2 += int(flow["packetCount"])
                    if dst == hostIPTable["3"]:
                        byteCountS3toH3 += int(flow["byteCount"])

        # calculate LU in S1-S3
        byteDifferenceS1toS3 = byteCountS1toS3 - byteCountS1toS3_lastCount
        luS1toS3 = min((byteDifferenceS1toS3 / timeInterval) / bwS1toS3, 1.0)

        # calculate LU in S2-S3
        byteDifferenceS2toS3 = byteCountS2toS3 - byteCountS2toS3_lastCount
        luS2toS3 = min((byteDifferenceS2toS3 / timeInterval) /  bwS2toS3, 1.0)

        # calculate drop rate in S1-S3
        dropRateS1toS3 = 0
        packetSentS1toS3 = packetCountS1toS3 - packetCountS1_lastCount
        packetReceivedS3FromS1 = packetCountS3FromS1 - packetCountS3FromS1_lastCount

        packetDropS1toS3 = packetSentS1toS3 - packetReceivedS3FromS1
        if packetSentS1toS3 > 0:
            dropRateS1toS3 = max(float(packetDropS1toS3) / packetSentS1toS3, 0)

        # calculate drop rate in S2-S3
        dropRateS2toS3 = 0
        packetSentS2toS3 = pakcetCountS2toS3 - packetCountS2_lastCount
        packetReceivedS3FromS2 = packetCountS3FromS2 - packetCountS3FromS2_lastCount

        packetDropS2toS3 = packetSentS2toS3 - packetReceivedS3FromS2
        if packetSentS2toS3 > 0:
            dropRateS2toS3 = max(float(packetDropS2toS3) / packetSentS2toS3, 0)

        # calculate throughput received by H3 (in Mbps)
        throughtputH3 = (byteCountS3toH3 - byteCountS3toH3_lastCount) * 8.0 / 1000000 / timeInterval

        if debug:
            print('------Link utilization------')
            print('S1-S3: byteCount:{bc}, byteCountLast:{bcl}, link utilization:{lu}'\
                .format(bc=byteCountS1toS3, bcl=byteCountS1toS3_lastCount, lu=luS1toS3))
            print('S2-S3: byteCount:{bc}, byteCountLast:{bcl}, link utilization:{lu}'\
                .format(bc=byteCountS2toS3, bcl=byteCountS2toS3_lastCount, lu=luS2toS3))
            print('------Drop rate------')
            print('S1-S3: packetSent:{ps}, packetReceived:{pr}, packetDrop:{pd}, dropRate:{dr}'\
                .format(ps=packetSentS1toS3, pr=packetReceivedS3FromS1, pd=packetDropS1toS3, dr=dropRateS1toS3))
            print('S2-S3: packetSent:{ps}, packetReceived:{pr}, packetDrop:{pd}, dropRate:{dr}'\
                .format(ps=packetSentS2toS3, pr=packetReceivedS3FromS2, pd=packetDropS2toS3, dr=dropRateS2toS3))
            print('------Throughput------')
            print('S3-H3: byteCount:{bc}, byteCountLast:{bcl}, throughput:{t}Mbps'\
                .format(bc=byteCountS3toH3, bcl=byteCountS3toH3_lastCount, t=throughtputH3))
        else:
            print('S1-S3: link utilization={lu}, drop rate={dr}'.format(lu=luS1toS3,dr=dropRateS1toS3))
            print('S2-S3: link utilization={lu}, drop rate={dr}'.format(lu=luS2toS3,dr=dropRateS2toS3))
            print('S3-H3: throughput={t}Mbps'.format(t=throughtputH3))

        byteCountS1toS3_lastCount = byteCountS1toS3
        byteCountS2toS3_lastCount = byteCountS2toS3
        byteCountS3toH3_lastCount = byteCountS3toH3

        packetCountS1_lastCount = packetCountS1toS3
        packetCountS2_lastCount = pakcetCountS2toS3
        packetCountS3FromS1_lastCount = packetCountS3FromS1
        packetCountS3FromS2_lastCount = packetCountS3FromS2

        # trigger dynamic routing
        if policy == "policy1":
            Policy1.dynamicRouting(switchTable, hostIPTable, luS1toS3, dropRateS1toS3)
        if policy == "policy2":
            Policy2.dynamicRouting(switchTable, hostIPTable, luS1toS3, dropRateS1toS3)
        if policy == "policy3":
            Policy3.dynamicRouting(switchTable, hostIPTable, luS2toS3, dropRateS2toS3)


