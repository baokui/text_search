path_user=$1
savepath0=$2
useridSize=$3
for((user=0;user<3;user++));
do
userfiles=$path_user/user_$user
nohup python -u userDataPre.py $userfiles $savepath0  $useridSize >> ./log/userDataPre-$user.log 2>&1
done
user=3
userfiles=$path_user/user_$user
nohup python -u userDataPre.py $userfiles $savepath0  $useridSize >> ./log/userDataPre-$user.log 2>&1

for((user=4;user<7;user++));
do
userfiles=$path_user/user_$user
nohup python -u userDataPre.py $userfiles $savepath0  $useridSize >> ./log/userDataPre-$user.log 2>&1
done
user=7
userfiles=$path_user/user_$user
nohup python -u userDataPre.py $userfiles $savepath0  $useridSize >> ./log/userDataPre-$user.log 2>&1

user=8
userfiles=$path_user/user_$user
nohup python -u userDataPre.py $userfiles $savepath0  $useridSize >> ./log/userDataPre-$user.log 2>&1
user=9
userfiles=$path_user/user_$user
nohup python -u userDataPre.py $userfiles $savepath0  $useridSize >> ./log/userDataPre-$user.log 2>&1
user=a
userfiles=$path_user/user_$user
nohup python -u userDataPre.py $userfiles $savepath0  $useridSize >> ./log/userDataPre-$user.log 2>&1
user=b
userfiles=$path_user/user_$user
nohup python -u userDataPre.py $userfiles $savepath0  $useridSize >> ./log/userDataPre-$user.log 2>&1

user=c
userfiles=$path_user/user_$user
nohup python -u userDataPre.py $userfiles $savepath0  $useridSize >> ./log/userDataPre-$user.log 2>&1
user=d
userfiles=$path_user/user_$user
nohup python -u userDataPre.py $userfiles $savepath0  $useridSize >> ./log/userDataPre-$user.log 2>&1
user=e
userfiles=$path_user/user_$user
nohup python -u userDataPre.py $userfiles $savepath0  $useridSize >> ./log/userDataPre-$user.log 2>&1
user=f
userfiles=$path_user/user_$user
nohup python -u userDataPre.py $userfiles $savepath0  $useridSize >> ./log/userDataPre-$user.log 2>&1