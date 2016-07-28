DATE=`date +%Y-%m-%d`
DIRNAME="../History Generator-$DATE"
mkdir "$DIRNAME"
cp src/*.py "$DIRNAME"
cp changelog.txt "$DIRNAME"
zip -r "$DIRNAME.zip" "$DIRNAME"
rm -rf "$DIRNAME"
