
sudo ovs-vsctl -- set port S3-eth3 qos=@defaultqos -- --id=@defaultqos create qos type=linux-htb \
other-config:max-rate=1000000000 queues=0=@q0 -- \
--id=@q0 create queue other-config:max-rate=1000000 other-config:min-rate=1000000

