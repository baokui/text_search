path_user=$1
savepath0=$2
U=(and ios)
userlist=(0 1 2 3 4 5 6 7 8 9 a b c d e f)
##########################################
i=0
A=${U[$i]}
for((j=0;j<16;j++));
do
user=${userlist[$j]}
userfiles=$path_user/user_$user-$A
if [ $(($j%2)) -eq 1 ];then
python -u userDataPre2.py $userfiles $savepath0  >> ./log/userDataPre-$user-$A.log 2>&1
else
python -u userDataPre2.py $userfiles $savepath0  >> ./log/userDataPre-$user-$A.log 2>&1
fi
done
##########################################
i=1
A=${U[$i]}
for((j=0;j<16;j++));
do
user=${userlist[$j]}
userfiles=$path_user/user_$user-$A
if [ $(($j%3)) -eq 2 ];then
python -u userDataPre2.py $userfiles $savepath0  >> ./log/userDataPre-$user-$A.log 2>&1
else
python -u userDataPre2.py $userfiles $savepath0  >> ./log/userDataPre-$user-$A.log 2>&1
fi
done
