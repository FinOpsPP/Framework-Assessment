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

REPO_NAME="/Framework-Assessment"

pages_link_converter() {
    local file="$1"
    
    # Replace .md with .html
    sed -i 's/\.md\(#[^)">]*\)\?\([">]\)/\.html\1\2/g' "$file"
    
    # Add repo-name prefix to relative links
    sed -i 's|\(/assessments\)|'"${REPO_NAME}"'\1|g' "$file"
    sed -i 's|\(/components\)|'"${REPO_NAME}"'\1|g' "$file"
    sed -i 's|\(/guidelines\)|'"${REPO_NAME}"'\1|g' "$file"
    sed -i 's|\(/specifications\)|'"${REPO_NAME}"'\1|g' "$file"
    sed -i 's|\(/tools\)|'"https://github.com/FinOpsPP/Framework-Assessment/tree/main"'\1|g' "$file"
}

pages_link_converter pages/index.md

echo "# Assessments" > pages/assessments/index.md
echo "" >> pages/assessments/index.md
ls -1 pages/assessments/**/*.md | grep -v index.md | while read file; do
    pages_link_converter "$file"

    parentdir=$(dirname "$file")
    parentname=$(basename "$parentdir")
    filename=$(basename "$file" .md)
    echo "- [$parentname]($REPO_NAME/assessments/$parentname/$filename.html)" >> pages/assessments/index.md
done

echo "# Components" > pages/components/index.md
echo "" >> pages/components/index.md
ls -1 pages/components/**/*.md | grep -v index.md | while read file; do
    pages_link_converter "$file"

    parentdir=$(dirname "$file")
    parentname=$(basename "$parentdir")
    filename=$(basename "$file" .md)
    echo "- [$parentname/$filename]($REPO_NAME/components/$parentname/$filename.html)" >> pages/components/index.md
done

echo "# Guidelines" > pages/guidelines/index.md
echo "" >> pages/guidelines/index.md
ls -1 pages/guidelines/*.md | grep -v index.md | while read file; do
    pages_link_converter "$file"

    filename=$(basename "$file" .md)
    echo "- [$filename]($REPO_NAME/guidelines/$filename)" >> pages/guidelines/index.md
done

echo "" >> pages/specifications/index.md
echo "# Specifications" >> pages/specifications/index.md
echo "" >> pages/specifications/index.md
pages_link_converter pages/specifications/index.md
ls -1 pages/specifications/**/* | grep -v index.md | while read file; do
    parentname=$(basename $(dirname "$file"))
    filename=$(basename "$file")
    echo "- [$parentname/$filename]($REPO_NAME/specifications/$parentname/$filename)" >> pages/specifications/index.md
done