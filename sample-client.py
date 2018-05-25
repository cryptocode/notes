from nanoapi import (Client, SocketConnection, types)

# Domain socket. On multiuser systems, this file can be protected to allow only specific users
nano = Client(SocketConnection('/var/nano/api'))

pending = types.query_account_pending();
pending.threshold.value = "200000000000000000000000";
pending.accounts.append("xrb_16u1uufyoig8777y6r8iqjtrw8sg8maqrm36zzcm95jmbd9i9aj5i8abr8u5");
pending.accounts.append("xrb_3eff1rokrp4ryronxpjdhzijxt9oax117xtn3eaqcaxcemp6y6fkarpqq8wj");

res = nano.query(pending)

print "Pending: %s" % nano.to_json(res)

"""
$python sample-client.py

{
  "block": [
    {
      "account": "xrb_16u1uufyoig8777y6r8iqjtrw8sg8maqrm36zzcm95jmbd9i9aj5i8abr8u5",
      "block": [
        "F66352BF63D0CC49E7CB6D81E1450DB95535DB1D0134FF477A83A796E75E59AB",
        "150AEE04A869AA2901F41CB40070D586F50C72DEBBF91A56691FAE1C266DA295"
      ]
    }
  ]
}
"""
