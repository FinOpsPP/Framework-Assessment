#!bash
cp README.md pages/index.md
cp CONTRIBUTING.md pages/contributing.md
cp SECURITY.md pages/security.md
cp --parents assessments/**/*.md pages
cp --parents components/**/*.md pages
cp guidelines/* pages/guidelines/

ls -1 assessments/**/*.md | while read file; do
    parentname=$(basename $(dirname "$file"))
    filename=$(basename "$file" .md)
    echo "- [$parentname](/assessments/$parentname/$filename.md)" >> pages/assessments/index.md
done

ls -1 components/**/*.md | while read file; do
    parentname=$(basename $(dirname "$file"))
    filename=$(basename "$file" .md)
    echo "- [$parentname/$filename](/components/$parentname/$filename.md)" >> pages/components/index.md
done

ls -1 guidelines/*.md | while read file; do
    filename=$(basename "$file" .md)
    echo "- [$filename](/guidelines/$filename.md)" >> pages/guidelines/index.md
done