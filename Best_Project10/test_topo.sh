$topology
$start
$stop
$step
$error=0


for $lambda in range($start, $stop, $step)
    $error = sudo python3 $topology $lambda

python3 generate_graph $topology
clear
