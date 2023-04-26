declare -a arr=("3.7" "3.8" "3.9" "3.10" "3.11" "3.12")
set -e 
set -o pipefail
for i in "${arr[@]}"
do
   echo "$i"
   docker run -v ~/src/dirigera:/dirigera python:"$i"-slim /bin/bash -c "
    cd /dirigera
    pip install -r requirements.txt > /dev/null
    pip install -r dev-requirements.txt > /dev/null
    bash run-test.sh"

done