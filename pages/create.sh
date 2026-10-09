#!bash
cp README.md pages/index.md
cp --parents assessments/**/*.md pages
cp --parents assessments/**/*.xlsx pages
cp --parents components/**/*.md pages
cp --parents specifications/**/*.yaml pages
cp --parents specifications/**/*.toml pages
cp specifications/README.md pages/specifications/index.md
cp guidelines/* pages/guidelines/
cp CONTRIBUTING.md pages/guidelines/contributing.md
cp SECURITY.md pages/guidelines/security.md

echo "# Assessments" > pages/assessments/index.md
echo "" >> pages/assessments/index.md
ls -1 pages/assessments/**/*.md | while read file; do
    sed -i 's/\.md\(#[^)">]*\)\?\([">]\)/\.html\1\2/g' "$file"
    parentdir=$(dirname "$file")
    parentname=$(basename "$parentdir")
    filename=$(basename "$file" .md)
    echo "- [$parentname](/assessments/$parentname/$filename.html)" >> pages/assessments/index.md
done

echo "# Components" > pages/components/index.md
echo "" >> pages/components/index.md
ls -1 pages/components/**/*.md | while read file; do
    sed -i 's/\.md\(#[^)">]*\)\?\([">]\)/\.html\1\2/g' "$file"
    parentdir=$(dirname "$file")
    parentname=$(basename "$parentdir")
    filename=$(basename "$file" .md)
    echo "- [$parentname/$filename](/components/$parentname/$filename.html)" >> pages/components/index.md
done

echo "# Guidelines" > pages/guidelines/index.md
echo "" >> pages/guidelines/index.md
ls -1 pages/guidelines/*.md | grep -v index.md | while read file; do
    sed -i 's/\.md\(#[^)">]*\)\?\([">]\)/\.html\1\2/g' "$file"
    filename=$(basename "$file" .md)
    echo "- [$filename](/guidelines/$filename)" >> pages/guidelines/index.md
done

echo "" >> pages/specifications/index.md
echo "# Specifications" >> pages/specifications/index.md
echo "" >> pages/specifications/index.md
ls -1 pages/specifications/**/* | while read file; do
    sed -i 's/\.md\(#[^)">]*\)\?\([">]\)/\.html\1\2/g' "$file"
    parentname=$(basename $(dirname "$file"))
    filename=$(basename "$file")
    echo "- [$parentname/$filename](/specifications/$parentname/$filename)" >> pages/specifications/index.md
done