shopt -s extglob
shopt -s globstar

mkdir -p dist

cat .srcfiles | while read globs
do
	for file in $globs
	do
		[[ -d "${file}" ]] && mkdir -p "dist/${file}"
		[[ -f "${file}" ]] && python3 scripts/replace.py "${file}" dist  
	done
done

zip -r dist/all.zip dist/
rm -rdf dist/!(all.zip)
