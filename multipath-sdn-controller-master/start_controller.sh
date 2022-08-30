# Deleting first the flows which were already set on our topology

if [[ $1 = "c" ]]; then 
    ovs-ofctl -O OpenFlow13 del-flows h1
    ovs-ofctl -O OpenFlow13 del-flows h2
    ovs-ofctl -O OpenFlow13 del-flows h3
    ovs-ofctl -O OpenFlow13 del-flows h4
fi

# Start controller
ryu-manager --observe-links --enable-debugger controller/mpsdn_controller.py
