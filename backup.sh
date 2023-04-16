
# find i such that test[i] does not exist
i=0
while [ -e "test$i" ]; do
    i=$((i+1))
done

mkdir "test$i"
cp -f base.{kra,png,psd} out.png prompt.txt negative.txt "test$i" 2>/dev/null

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
touch "test$i/$TIMESTAMP"
