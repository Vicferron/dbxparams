set -e

CURRENT_VERSION=$(grep -Po '(?<=^version = ")[^"]*' pyproject.toml)
echo "Current version: $CURRENT_VERSION"

IFS='.' read -r major minor patch <<< "$CURRENT_VERSION"
NEW_VERSION="$major.$minor.$((patch+1))"

sed -i "s/version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml

echo "Bumped version to: $NEW_VERSION"
git add .
git commit -m "chore: bump version to $NEW_VERSION"
git tag "v$NEW_VERSION"
git push origin main --tags
